# -*- coding: utf-8 -*-
"""Confere os pontos de corte de cada trecho: transcreve de novo só o trecho (com folga) e mede o volume
em volta do começo e do fim, pra achar o ponto mais silencioso perto do corte.
Uso: python conferir_cortes.py <audio> nome:in:out [nome:in:out ...]
"""
import subprocess, sys
import numpy as np
from faster_whisper import WhisperModel

SR = 16000
audio = sys.argv[1]
trechos = [(a.split(':')[0], float(a.split(':')[1]), float(a.split(':')[2])) for a in sys.argv[2:]]

def som(t0, t1):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t0:.3f}', '-to', f'{t1:.3f}', '-i', audio, '-vn', '-ac', '1',
                        '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(r, np.float32)

def db(x):
    return 20 * np.log10(np.sqrt(np.mean(x.astype(np.float64) ** 2)) + 1e-7)

def vale(t, raio=0.16):
    """ponto mais silencioso (janela de 30 ms) num raio em volta de t; devolve (tempo, dB lá, dB no ponto pedido)"""
    x = som(t - raio - 0.05, t + raio + 0.05); w = int(0.03 * SR); passo = int(0.005 * SR)
    niveis = [(db(x[k:k + w]), (t - raio - 0.05) + (k + w / 2) / SR) for k in range(0, len(x) - w, passo)]
    aqui = min(niveis, key=lambda n: abs(n[1] - t))[0]
    melhor = min(niveis, key=lambda n: n[0])
    return melhor[1], melhor[0], aqui

m = WhisperModel('large-v3', device='cpu', compute_type='int8')
prompt = 'Claude Code, GitHub, Humanizer, Grill Me, Laya, Jev, ScrollCraft, VoiceStudio, ElevenLabs, skill, repositório, ar-condicionado.'
for nome, t0, t1 in trechos:
    f0 = max(0, t0 - 1.2)
    x = som(f0, t1 + 1.2)
    segs, _ = m.transcribe(x, language='pt', word_timestamps=True, condition_on_previous_text=False, beam_size=5,
                           initial_prompt=prompt, vad_filter=False)
    pal = [(w.word.strip(), w.start + f0, w.end + f0) for s in segs for w in (s.words or [])]
    dentro = ' '.join(p for p, i, f in pal if i >= t0 - 0.12 and f <= t1 + 0.12)
    antes = ' '.join(p for p, i, f in pal if i < t0 - 0.12)
    depois = ' '.join(p for p, i, f in pal if f > t1 + 0.12)
    a, b = vale(t0), vale(t1)
    print(f'== {nome}  {t0:.2f}-{t1:.2f} ({t1 - t0:.2f} s)')
    print(f'   antes:  [{antes}]')
    print(f'   DENTRO: {dentro}')
    print(f'   depois: [{depois}]')
    print(f'   começo: no corte {a[2]:.0f} dB · ponto mais silencioso {a[0]:.3f} ({a[1]:.0f} dB)')
    print(f'   fim:    no corte {b[2]:.0f} dB · ponto mais silencioso {b[0]:.3f} ({b[1]:.0f} dB)')
    print('   palavras: ' + ' '.join(f'{p}[{i:.2f}]' for p, i, f in pal if t0 - 0.6 <= i <= t0 + 1.0) + '  ...  ' +
          ' '.join(f'{p}[{i:.2f}-{f:.2f}]' for p, i, f in pal if t1 - 1.0 <= f <= t1 + 0.6))
    sys.stdout.flush()
