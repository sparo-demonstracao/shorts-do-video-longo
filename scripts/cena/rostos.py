# -*- coding: utf-8 -*-
"""Folha do rosto dele em cada fala (um quadro a cada 0,33 s), pra ver onde ele olha pra câmera.

O criador reprovou aparecer "como o foco da cena" em trechos em que está olhando pra tela. Antes de pôr ele grande numa
fala, abra esta folha: ele só entra em destaque onde olha pra lente. No resto, a voz vai por cima do material.

Uso: python rostos.py <short-XX/roteiro.json> <saida.jpg> [nome:in:out ...] [--crop l:a:x:y]
Sem trechos, faz todas as falas do roteiro. Tempos da gravação da voz. `--crop` aproxima no rosto (pixels da câmera)."""
import json, subprocess, sys
from PIL import Image, ImageDraw, ImageFont
args = sys.argv[1:]; crop = ''
if '--crop' in args:
    k = args.index('--crop'); crop = 'crop=' + args[k + 1] + ','; del args[k:k + 2]
rot = json.load(open(args[0], encoding='utf-8')); F = rot['fontes']['cam']

def atraso(t):
    ia = F.get('imagem_atras'); extra = ia['base'] + ia['por_segundo'] * (t - ia['desde']) if ia else 0.0
    a = F.get('atraso', 0)
    if not isinstance(a, list): return a + extra
    pts = sorted(a)
    if t <= pts[0][0]: return pts[0][1] + extra
    for (t0, a0), (t1, a1) in zip(pts, pts[1:]):
        if t <= t1: return a0 + (a1 - a0) * (t - t0) / max(1e-9, t1 - t0) + extra
    return pts[-1][1] + extra

trechos = [a.split(':') for a in args[2:]]
if not trechos:
    nomes = rot.get('nomes_falas') or [str(k + 1) for k in range(len(rot['falas']))]
    trechos = [(n, a, b) for n, (a, b) in zip(nomes, rot['falas'])]
fonte = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 15)
W, H = 256, 144 if not crop else 205; linhas = []
for nome, t0, t1 in trechos:
    t0, t1 = float(t0), float(t1)
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t0 + atraso(t0):.3f}', '-t', f'{max(0.34, t1 - t0):.3f}', '-i', F['arquivo'],
                          '-vf', f'fps=3,{crop}scale={W}:{H}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
    n = len(raw) // (W * H * 3)
    linhas.append((nome, [Image.frombytes('RGB', (W, H), raw[k * W * H * 3:(k + 1) * W * H * 3]) for k in range(n)]))
cols = 12; total = sum((len(q) + cols - 1) // cols for _, q in linhas)
fol = Image.new('RGB', (cols * (W + 2), max(1, total) * (H + 20)), (16, 14, 14)); d = ImageDraw.Draw(fol); y = 0
for nome, qs in linhas:
    for k, im in enumerate(qs):
        x = (k % cols) * (W + 2); yy = y + (k // cols) * (H + 20)
        fol.paste(im, (x, yy)); d.text((x + 3, yy + H + 1), f'{nome} +{k / 3:.2f}s', fill=(255, 107, 24), font=fonte)
    y += ((len(qs) + cols - 1) // cols) * (H + 20)
fol.save(args[1], quality=86); print(args[1], fol.size)
