# -*- coding: utf-8 -*-
"""Confere a sincronia da boca SEM OUVIR: uma folha com a boca dele em volta do estalo de consoantes como p e b.

Por que existe: o atraso.py casa o SOM da câmera com o áudio de referência, mas celular grava som e imagem com
relógios diferentes. Na 1ª rodada real (12/11/2026) a imagem estava junta com o som no começo da gravação e 70 ms
atrasada depois de 1h25. Quem monta não ouve, então é assim que se confere.

Uso:
  python boca.py <plano.json ou roteiro.json> <saida.jpg> t0-t1 [t0-t1 ...] [--regiao x,y,l,a] [--max 8]

Os trechos t0-t1 são tempos do áudio de referência com fala contínua (pegue um do começo e um do fim da gravação).
O programa acha os estalos (15 ms de silêncio e um salto de volume, no meio de uma fala), e pra cada um mostra 9
quadros da câmera, de 2 antes a 6 depois, usando o atraso que está no plano ("atraso" + "imagem_atras", se houver).

Como ler: em p e b os lábios ficam FECHADOS antes do estalo e se abrem NELE. O quadro "ESTALO" (ou o seguinte) tem
que ser o primeiro com os lábios abrindo. Se eles só abrem 2 quadros depois, a imagem está 2 quadros atrasada:
some 2/30 s ao atraso da câmera (ou ponha em "imagem_atras": {"base", "por_segundo", "desde"} se a diferença
crescer ao longo da gravação). t, d, k e g não fecham os lábios: ignore essas linhas.
"""
import argparse, json, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont

FPS = 30
ap = argparse.ArgumentParser()
ap.add_argument('plano'); ap.add_argument('saida'); ap.add_argument('trechos', nargs='+')
ap.add_argument('--regiao', default=''); ap.add_argument('--max', type=int, default=8)
a = ap.parse_args()
d = json.load(open(a.plano, encoding='utf-8-sig')); f = d['fontes']
ref = f['audio']['arquivo'] if 'audio' in f else f['cam']['arquivo']; cam = f['cam']

def atraso_em(fo, t):
    ia = fo.get('imagem_atras'); extra = ia['base'] + ia['por_segundo'] * (t - ia['desde']) if ia else 0.0
    v = fo.get('atraso', 0)
    if isinstance(v, list):
        pts = sorted(v); v = pts[-1][1]
        if t <= pts[0][0]: v = pts[0][1]
        else:
            for (t0, a0), (t1, a1) in zip(pts, pts[1:]):
                if t <= t1: v = a0 + (a1 - a0) * (t - t0) / max(1e-9, t1 - t0); break
    return v + extra

w_, h_ = [int(x) for x in subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height', '-of', 'csv=p=0',
                                         cam['arquivo']], capture_output=True, text=True).stdout.strip().split(',')[:2]]
reg = [int(x) for x in a.regiao.split(',')] if a.regiao else [int(w_ * 0.47), int(h_ * 0.43), int(w_ * 0.15), int(h_ * 0.17)]

estalos = []
for tr in a.trechos:
    t0, t1 = map(float, tr.split('-'))
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t0:.3f}', '-t', f'{t1 - t0:.3f}', '-i', ref, '-vn', '-ac', '1', '-ar', '48000', '-f', 'f32le', '-'],
                         capture_output=True).stdout
    x = np.frombuffer(raw, np.float32).astype(np.float64); w = 240                        # janelas de 5 ms
    db = 20 * np.log10(np.sqrt((x[:len(x) // w * w].reshape(-1, w) ** 2).mean(axis=1)) + 1e-7); alto = np.percentile(db, 92)
    k = 50
    while k < len(db) - 10:
        quieto = db[k - 3:k].max() < alto - 30 and db[k] > alto - 20                       # 15 ms quietos e então som
        if quieto:
            s = k - 1
            while s > 0 and db[s] < alto - 28: s -= 1
            if 25 <= (k - 1 - s) * 5 <= 160 and db[max(0, s - 24):s + 1].max() > alto - 10:   # silêncio curto, com fala logo antes
                estalos.append(t0 + k * 0.005); k += 60; continue
        k += 1
if len(estalos) > a.max:
    estalos = [estalos[round(i * (len(estalos) - 1) / (a.max - 1))] for i in range(a.max)]
if not estalos:
    raise SystemExit('nenhum estalo claro nesses trechos: escolha trechos com fala contínua')

try: fonte = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 17)
except OSError: fonte = ImageFont.load_default()
QW, QH = 232, round(232 * reg[3] / reg[2])
folha = Image.new('RGB', (9 * (QW + 4) + 8, len(estalos) * (QH + 30) + 8), (18, 16, 16)); des = ImageDraw.Draw(folha)
for li, te in enumerate(estalos):
    tc = te + atraso_em(cam, te)
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{tc - 2 / FPS:.4f}', '-i', cam['arquivo'], '-frames:v', '9', '-vf',
                          f'fps={FPS},crop={reg[2]}:{reg[3]}:{reg[0]}:{reg[1]},scale={QW}:{QH}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                         capture_output=True).stdout
    q = np.frombuffer(raw[:len(raw) // (QW * QH * 3) * QW * QH * 3], np.uint8).reshape(-1, QH, QW, 3)
    for c in range(len(q)):
        x0 = 4 + c * (QW + 4); y0 = 4 + li * (QH + 30); folha.paste(Image.fromarray(q[c]), (x0, y0)); dk = c - 2
        des.text((x0 + 4, y0 + QH + 2), f'{te:.2f}s {dk:+d}' + (' ESTALO' if dk == 0 else ''), fill=(255, 107, 24) if dk == 0 else (200, 200, 200), font=fonte)
folha.save(a.saida, quality=90)
print(f'{len(estalos)} estalos -> {a.saida}. Abra com Read: nos sons de p e b, os lábios têm que abrir no quadro ESTALO (ou no seguinte).')
print(f'região da boca usada: {reg} (mude com --regiao se o rosto não estiver nela)')
