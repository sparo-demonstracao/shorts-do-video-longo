# -*- coding: utf-8 -*-
"""Sincronia boca x voz com detector de rosto (OpenCV): acha o rosto em cada quadro dele (quadros/cam da cena), mede a
abertura da boca (pixels escuros na região da boca, relativos ao tom da pele) e compara com o volume da voz no VO.
Uso: python boca_cv.py short-XX/roteiro.json     -> defasagem em quadros por fala e no conjunto (positivo: imagem atrasada)"""
import json, os, subprocess, sys
import numpy as np, cv2

FPS = 30
rot_p = os.path.abspath(sys.argv[1]); base = os.path.dirname(rot_p); rot = json.load(open(rot_p, encoding='utf-8'))
vo = rot['fontes']['audio']['arquivo']; qd = os.path.join(base, 'cena', 'quadros', 'cam')
cas = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def volume(t0, n):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t0:.3f}', '-t', f'{n / FPS + 0.1:.3f}', '-i', vo, '-ac', '1', '-ar', '48000', '-f', 'f32le', '-'], capture_output=True).stdout
    x = np.frombuffer(raw, np.float32).astype(np.float64)[:n * 1600].reshape(-1, 1600)
    return np.log10(np.sqrt((x ** 2).mean(axis=1)) + 1e-4)

k0 = 1; soma = np.zeros(17); peso = 0
for vin, vout in rot['falas']:
    n = round((vout - vin) * FPS); caixas = []; cinzas = []
    if n < 75: k0 += n; continue        # pedaço curto demais pra medir
    for k in range(k0, k0 + n):
        g = cv2.imread(os.path.join(qd, f'{k:05d}.jpg'), cv2.IMREAD_GRAYSCALE); cinzas.append(g)
        p = cv2.resize(g, (640, 360)); fs = cas.detectMultiScale(p, 1.1, 5, minSize=(110, 110))
        caixas.append(max(fs, key=lambda f: f[2] * f[3]) * 3 if len(fs) else None)
    # preenche falhas e suaviza a caixa
    ok = [c for c in caixas if c is not None]
    if len(ok) < n * 0.5: print(f'fala {vin:.2f}: rosto achado em poucos quadros ({len(ok)}/{n})'); k0 += n; continue
    ult = ok[0]; cs = []
    for c in caixas:
        if c is not None: ult = c
        cs.append(ult)
    cs = np.array(cs, dtype=np.float64); ker = 7
    cs = np.array([np.median(cs[max(0, i - ker):i + ker + 1], axis=0) for i in range(n)])
    ab = []
    for g, (x, y, w, h) in zip(cinzas, cs):
        bx0, bx1 = int(x + 0.30 * w), int(x + 0.70 * w); by0, by1 = int(y + 0.66 * h), int(y + 0.92 * h)
        boca = g[by0:by1, bx0:bx1].astype(np.float64); pele = np.median(g[int(y + 0.45 * h):int(y + 0.6 * h), int(x + 0.2 * w):int(x + 0.8 * w)])
        ab.append((boca < 0.42 * pele).mean())
    a = np.array(ab); v = volume(vin, n)
    a = a - np.convolve(a, np.ones(31) / 31, mode='same'); v = v - np.convolve(v, np.ones(31) / 31, mode='same')
    a /= a.std() + 1e-9; v /= v.std() + 1e-9; res = []
    for d in range(-8, 9):       # d > 0: a boca abre d quadros DEPOIS do som (imagem atrasada)
        res.append((a[d:] * v[:len(v) - d]).mean() if d >= 0 else (a[:d] * v[-d:]).mean())
    res = np.array(res); soma += res * n; peso += n
    print(f"   mais negativo em {int(np.argmin(res)) - 8:+d} ({res.min():.2f})", end=" | ")
    print(f'fala {vin:8.2f} ({n / FPS:4.1f} s, rosto em {len(ok)}/{n}): melhor {int(np.argmax(res)) - 8:+d} (semelhança {res.max():.2f}); em 0: {res[8]:.2f}')
    k0 += n
m = soma / peso
print('conjunto: ' + ' '.join(f'{d:+d}:{c:.2f}' for d, c in zip(range(-8, 9), m)))
print(f'melhor no conjunto: {int(np.argmax(m)) - 8:+d} quadro(s)')
