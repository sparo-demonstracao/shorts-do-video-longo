# -*- coding: utf-8 -*-
"""Mede o atraso entre a voz (VO.wav) e a IMAGEM da câmera, sem ouvir.

O atraso.py casa o SOM da câmera com o VO.wav, mas o celular pode gravar a imagem um pouco atrasada em relação ao
próprio som. Aqui a medida é pela boca: nas consoantes de estalo (p, b, t, k...) há um silêncio curto e um salto de
volume; nesse instante a boca se mexe de repente. O programa acha dezenas desses estalos no VO.wav, pega os quadros
da câmera em volta de cada um (pelo atraso atual) e mede em que quadro, em média, o movimento da boca dá o pico.
Pico em 0 = imagem e voz juntas. Pico em +2 = a imagem está 2 quadros atrasada: some 2/30 s ao atraso da câmera.

Uso: python medir_boca.py <roteiro.json> t0-t1 [t0-t1 ...]      (trechos do VO.wav com bastante fala)
"""
import json, subprocess, sys
import numpy as np

FPS = 30
rot = json.load(open(sys.argv[1], encoding='utf-8')); vo = rot['fontes']['audio']['arquivo']; cam = rot['fontes']['cam']
ROI = 'crop=420:300:850:420,scale=140:100,format=gray'      # metade de baixo do rosto no quadro 1920x1080

def atraso_em(f, t):
    a = f.get('atraso', 0)
    if not isinstance(a, list): return a
    pts = sorted(a)
    if t <= pts[0][0]: return pts[0][1]
    for (t0, a0), (t1, a1) in zip(pts, pts[1:]):
        if t <= t1: return a0 + (a1 - a0) * (t - t0) / max(1e-9, t1 - t0)
    return pts[-1][1]

estalos = []
for trecho in sys.argv[2:]:
    a, b = map(float, trecho.split('-'))
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{a:.3f}', '-t', f'{b - a:.3f}', '-i', vo, '-ac', '1', '-ar', '48000', '-f', 'f32le', '-'],
                         capture_output=True).stdout
    x = np.frombuffer(raw, np.float32).astype(np.float64); w = 240                     # janelas de 5 ms
    db = 20 * np.log10(np.sqrt((x[:len(x) // w * w].reshape(-1, w) ** 2).mean(axis=1)) + 1e-7)
    alto = np.percentile(db, 90)
    k = 60
    while k < len(db) - 30:
        # silêncio curto (30 a 150 ms bem abaixo da fala), com fala antes, e um salto forte em 10 ms
        if db[k] > alto - 16 and db[k - 2] < alto - 34:
            s = k - 2
            while s > 0 and db[s] < alto - 30: s -= 1
            silencio = (k - 2 - s) * 5
            if 30 <= silencio <= 150 and db[max(0, s - 30):s].max() > alto - 12:
                estalos.append(a + (k - 1) * 0.005)
                k += 40; continue
        k += 1
print(f'{len(estalos)} estalos achados no VO.wav')

perfis = []
for te in estalos:
    tc = te + atraso_em(cam, te)                      # instante desse estalo na câmera, pelo atraso atual
    f0 = round(tc * FPS) / FPS                        # alinha na grade de quadros
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{tc - 10 / FPS:.4f}', '-i', cam['arquivo'], '-frames:v', '21', '-vf', f'fps={FPS},{ROI}',
                          '-f', 'rawvideo', '-'], capture_output=True).stdout
    if len(raw) < 21 * 14000: continue
    q = np.frombuffer(raw[:21 * 14000], np.uint8).reshape(21, 100, 140).astype(np.float64)
    mov = np.abs(np.diff(q, axis=0)).mean(axis=(1, 2))        # movimento entre quadros vizinhos: 20 valores, o de índice j fica entre os quadros j e j+1
    perfis.append(mov / (mov.mean() + 1e-9))
P = np.array(perfis); media = P.mean(axis=0)
# o quadro 10 começa exatamente no estalo; a diferença entre os quadros j e j+1 acontece em (j + 1 - 10) quadros depois do estalo
print(f'{len(P)} estalos medidos. Movimento médio da boca em volta do estalo (0 = no instante do estalo):')
for j, m in enumerate(media):
    print(f'  {j + 1 - 10:+3d} quadro(s): {m:5.2f} ' + '#' * int(m * 20))
pico = int(np.argmax(media)); viz = media[max(0, pico - 1):pico + 2]; cent = (np.arange(max(0, pico - 1), max(0, pico - 1) + len(viz)) * viz).sum() / viz.sum()
print(f'pico em {cent + 1 - 10:+.1f} quadro(s) = {(cent + 1 - 10) / FPS * 1000:+.0f} ms (positivo: a imagem está atrasada em relação à voz)')
