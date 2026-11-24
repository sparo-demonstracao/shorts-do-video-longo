# -*- coding: utf-8 -*-
"""Transcreve cada fala do roteiro separadamente e acerta, pelo volume, o começo das palavras que vêm depois de pausa.

Por que existe: a transcrição do arquivo inteiro já perdeu palavras no meio de frase ("todas as funcionalidades de") e
adianta em até 0,4 s a palavra que vem depois de uma pausa. A legenda e os motions são amarrados a essas palavras.

Uso: python palavras_falas.py <short-XX/roteiro.json> [saida.json] [--prompt "nomes próprios do vídeo, separados por vírgula"]
Sai {"falas": [[{p, i, f}, ...], ...]} com tempos contados do começo de cada fala (padrão: palavras-falas.json ao lado
do roteiro). Ponha o nome do arquivo em `palavras_falas` no roteiro. Leia o que ele imprime: nome de produto errado se
corrige à mão no arquivo ("Cloud Code" -> "Claude Code")."""
import json, os, subprocess, sys
import numpy as np
from faster_whisper import WhisperModel
args = sys.argv[1:]; prompt = 'Claude Code, GitHub, repositório, prompt, aplicativo.'
if '--prompt' in args:
    k = args.index('--prompt'); prompt = args[k + 1]; del args[k:k + 2]
rot_p = args[0]; rot = json.load(open(rot_p, encoding='utf-8'))
vo = (rot['fontes'].get('audio') or rot['fontes']['cam'])['arquivo']
sai = args[1] if len(args) > 1 else os.path.join(os.path.dirname(os.path.abspath(rot_p)), 'palavras-falas.json')
m = WhisperModel('large-v3', device='cpu', compute_type='int8')      # na CPU e com numpy: GPU e PyAV quebram neste PC
saida = []
for a, b in rot['falas']:
    pcm = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{a:.4f}', '-to', f'{b:.4f}', '-i', vo, '-ac', '1', '-ar', '16000', '-f', 'f32le', '-'], capture_output=True).stdout
    x = np.frombuffer(pcm, np.float32)
    segs, _ = m.transcribe(x, language='pt', word_timestamps=True, condition_on_previous_text=False, beam_size=5, initial_prompt=prompt, vad_filter=False)
    ws = [{'p': w.word.strip(), 'i': round(float(w.start), 3), 'f': round(float(w.end), 3)} for s in segs for w in (s.words or [])]
    # volume de 10 em 10 ms; começo real de cada palavra que vem depois de uma pausa (ou a primeira)
    n = 160; v = np.array([20 * np.log10(max(1e-6, np.sqrt(np.mean(x[k:k + n].astype(np.float64) ** 2)))) for k in range(0, len(x) - n + 1, n)])
    som = v > -42
    for k, w in enumerate(ws):
        ant = ws[k - 1]['f'] if k else 0.0
        if k == 0 or w['i'] - ant > 0.18:
            i0 = int(max(0, (ant if k else 0) * 100)); i1 = int(min(len(v) - 3, w['f'] * 100))
            for j in range(i0, i1):
                if som[j] and som[j + 1] and som[j + 2] and (j == 0 or not som[max(0, j - 8):j].all()):
                    if not som[max(0, j - 6):j].any() or j == i0:
                        w['i'] = round(j / 100, 3); break
    saida.append(ws); print(f'{a:.2f}: ' + ' '.join(f"{w['p']}[{w['i']:.2f}]" for w in ws), flush=True)
json.dump({'falas': saida}, open(sai, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('gravado em', sai)
