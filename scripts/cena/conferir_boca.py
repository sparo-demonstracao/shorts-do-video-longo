# -*- coding: utf-8 -*-
"""Confere a sincronia da boca sem ouvir: compara, quadro a quadro, o quanto a boca dele está aberta (região da boca
mais escura = boca aberta) com o volume da voz no VO.wav, e acha o deslocamento em que os dois casam melhor.
Perto de 0 quadro = boca e voz juntas. Uso: python conferir_boca.py short-XX/roteiro.json"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image

FPS = 30
rot_p = os.path.abspath(sys.argv[1]); base = os.path.dirname(rot_p); rot = json.load(open(rot_p, encoding='utf-8'))
vo = rot['fontes']['audio']['arquivo']
BOCA = (930, 470, 1190, 640)      # região da boca no quadro 1920x1080 dele (com folga pra ele se mexer)

def volume(t0, n):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t0:.3f}', '-t', f'{n / FPS + 0.1:.3f}', '-i', vo, '-ac', '1', '-ar', '48000',
                          '-f', 'f32le', '-'], capture_output=True).stdout
    x = np.frombuffer(raw, np.float32).astype(np.float64)[:n * 1600].reshape(-1, 1600)
    return np.log10(np.sqrt((x ** 2).mean(axis=1)) + 1e-4)

k0 = 1; todos = []
for vin, vout in rot['falas']:
    n = round((vout - vin) * FPS)
    if n >= 120:
        abertura = []
        for k in range(k0, k0 + n):
            im = np.asarray(Image.open(os.path.join(base, 'cena', 'quadros', 'cam', f'{k:05d}.jpg')).convert('L').crop(BOCA), dtype=np.float64)
            abertura.append((im < 60).mean())          # fração de pixels bem escuros na região: o interior da boca
        a = np.array(abertura); v = volume(vin, n)
        a = (a - a.mean()) / (a.std() + 1e-9); v = (v - v.mean()) / (v.std() + 1e-9)
        res = []
        for d in range(-8, 9):                          # d > 0: a boca abre d quadros DEPOIS do som
            if d >= 0: c = (a[d:] * v[:len(v) - d]).mean()
            else: c = (a[:d] * v[-d:]).mean()
            res.append((c, d))
        melhor = max(res); todos.append(melhor[1])
        print(f'fala {vin:8.2f} ({n / FPS:4.1f} s): boca e voz casam melhor com {melhor[1]:+d} quadro(s) (semelhança {melhor[0]:.2f}); em 0: {dict((d, c) for c, d in res)[0]:.2f}')
    k0 += n
print('mediana:', int(np.median(todos)), 'quadro(s)')
