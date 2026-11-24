# -*- coding: utf-8 -*-
"""Transcreve uma gravação e marca o tempo de cada palavra.

Uso:  python transcrever.py <video-ou-audio> <saida.json> [--modelo large-v3] [--inicio 0] [--fim 0]
Sai:  <saida.json> = {"arquivo", "duracao", "palavras": [{"p", "i", "f"}], "silencios": [[i, f]]}
      e <saida>.txt com o texto em linhas de ~12 s, cada uma começando com [mm:ss], pra ler rápido.

O áudio é decodificado pelo ffmpeg e entregue ao Whisper como array numpy: o PyAV deste PC não abre arquivo
do jeito que o faster-whisper pede. Tenta a placa de vídeo e cai pro processador se faltar DLL da NVIDIA.
No processador, conte ~0,6 min de espera por minuto de áudio: rode em segundo plano em gravação longa.
"""
import argparse, glob, json, os, re, site, subprocess, sys

import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument('entrada'); ap.add_argument('saida')
ap.add_argument('--modelo', default='large-v3')
ap.add_argument('--inicio', type=float, default=0.0)
ap.add_argument('--fim', type=float, default=0.0, help='0 = até o fim')
a = ap.parse_args()

sites = site.getsitepackages() + [site.getusersitepackages()]
dirs = [os.path.abspath(d) for s in sites for d in glob.glob(os.path.join(s, 'nvidia', '*', 'bin'))]
os.environ['PATH'] = ';'.join(dirs) + ';' + os.environ.get('PATH', '')
for d in dirs:
    os.add_dll_directory(d)
from faster_whisper import WhisperModel  # noqa: E402

corte = (['-ss', str(a.inicio)] if a.inicio else []) + (['-to', str(a.fim)] if a.fim else [])
pcm = subprocess.run(['ffmpeg', '-v', 'error', *corte, '-i', a.entrada, '-vn', '-f', 'f32le', '-ac', '1', '-ar', '16000', '-'],
                     capture_output=True, check=True).stdout
som = np.frombuffer(pcm, np.float32)
dur = len(som) / 16000
print(f'{os.path.basename(a.entrada)}: {dur / 60:.1f} min de áudio', flush=True)

# Silêncios longos: o Whisper inventa palavra neles ("Amém", "Tchau, tchau"), então o que cair dentro é descartado.
sd = subprocess.run(['ffmpeg', '-v', 'info', *corte, '-i', a.entrada, '-vn', '-af', 'silencedetect=noise=-38dB:d=1.2', '-f', 'null', '-'],
                    capture_output=True, text=True, errors='replace').stderr
ini = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', sd)]
fim = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', sd)]
silencios = [[round(i, 2), round(f, 2)] for i, f in zip(ini, fim + [dur])]

# O prompt cheio de hesitação faz o Whisper manter "é", "tipo", "né": eles marcam onde NÃO cortar bonito.
prompt = 'É... então, tipo, né, a gente vai, ãh, olhar isso aqui. Tá? Beleza. Claude Code, Antigravity, Higgsfield, n8n, MCP, skill.'
for dev, ct in (('cuda', 'float16'), ('cpu', 'int8')):
    try:
        m = WhisperModel(a.modelo, device=dev, compute_type=ct)
        segs, _ = m.transcribe(som, language='pt', word_timestamps=True, condition_on_previous_text=False,
                               beam_size=5, initial_prompt=prompt, vad_filter=False)
        pal = []
        for s in segs:
            for w in s.words or []:
                pal.append({'p': w.word.strip(), 'i': round(w.start + a.inicio, 3), 'f': round(w.end + a.inicio, 3)})
            print(f'  {s.end / 60:5.1f} min', end='\r', flush=True)
        print(f'\nwhisper rodou em {dev}')
        break
    except RuntimeError as e:
        if dev == 'cpu':
            raise
        print('placa de vídeo indisponível, indo pro processador:', str(e)[:100], flush=True)

def no_silencio(w):
    meio = (w['i'] + w['f']) / 2 - a.inicio
    return any(i + 0.15 < meio < f - 0.15 for i, f in silencios)

antes = len(pal)
pal = [w for w in pal if w['p'] and not no_silencio(w)]
if antes - len(pal):
    print(f'descartadas {antes - len(pal)} palavras que caíram em silêncio (invenção do Whisper)')

json.dump({'arquivo': os.path.abspath(a.entrada), 'duracao': round(dur, 2), 'palavras': pal,
           'silencios': [[round(i + a.inicio, 2), round(f + a.inicio, 2)] for i, f in silencios]},
          open(a.saida, 'w', encoding='utf-8'), ensure_ascii=False)

linhas, atual, t0 = [], [], None
for w in pal:
    if t0 is None:
        t0 = w['i']
    atual.append(w['p'])
    if w['f'] - t0 > 12 and re.search(r'[.!?]$', w['p']) or w['f'] - t0 > 20:
        linhas.append(f'[{int(t0 // 60):02d}:{int(t0 % 60):02d}] ' + ' '.join(atual)); atual, t0 = [], None
if atual:
    linhas.append(f'[{int(t0 // 60):02d}:{int(t0 % 60):02d}] ' + ' '.join(atual))
txt = os.path.splitext(a.saida)[0] + '.txt'
open(txt, 'w', encoding='utf-8').write('\n'.join(linhas))
print(f'{len(pal)} palavras -> {a.saida}\ntexto com tempos -> {txt}')
