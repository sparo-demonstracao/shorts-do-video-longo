# -*- coding: utf-8 -*-
"""Folha de conferência: quadros de um ou mais vídeos lado a lado, com o tempo escrito em cada um.

Uso:
  python folha.py <saida.jpg> <video> [<video> ...] [--n 12] [--cols 4] [--inicio 0] [--fim 0] [--largura 360]

Com um vídeo, tira --n quadros espalhados entre --inicio e --fim. Com vários, tira 3 de cada (começo, meio, fim),
uma linha por vídeo: é o jeito de conferir de uma vez todas as cenas geradas.
Olhe a folha com a ferramenta Read antes de seguir: é assim que você "assiste" ao que montou.
"""
import argparse, io, os, subprocess

from PIL import Image, ImageDraw, ImageFont

ap = argparse.ArgumentParser()
ap.add_argument('saida'); ap.add_argument('videos', nargs='+')
ap.add_argument('--n', type=int, default=12); ap.add_argument('--cols', type=int, default=4)
ap.add_argument('--inicio', type=float, default=0.0); ap.add_argument('--fim', type=float, default=0.0)
ap.add_argument('--largura', type=int, default=360)
a = ap.parse_args()

def duracao(v):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', v],
                       capture_output=True, text=True)
    return float(r.stdout.strip() or 0)

def quadro(v, t):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t:.3f}', '-i', v, '-frames:v', '1', '-vf', f'scale={a.largura}:-2',
                        '-f', 'image2pipe', '-vcodec', 'png', '-'], capture_output=True)
    return Image.open(io.BytesIO(r.stdout)).convert('RGB') if r.stdout else None

try:
    fonte = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 16)
except OSError:
    fonte = ImageFont.load_default()

itens = []   # (rótulo, imagem)
if len(a.videos) == 1:
    v = a.videos[0]; d = duracao(v); t0 = a.inicio; t1 = a.fim or d
    for k in range(a.n):
        t = t0 + (t1 - t0) * (k + 0.5) / a.n
        itens.append((f'{int(t // 60)}:{t % 60:05.2f}', quadro(v, t)))
    cols = a.cols
else:
    cols = 3
    for v in a.videos:
        d = duracao(v)
        for nome, t in (('começo', 0.05), ('meio', d / 2), ('fim', max(0, d - 0.12))):
            itens.append((f'{os.path.basename(v)[:22]} · {nome}', quadro(v, t)))

itens = [(r, im) for r, im in itens if im is not None]
if not itens:
    raise SystemExit('nenhum quadro saiu: confira o caminho do vídeo')
w = a.largura; h = max(im.height for _, im in itens)
linhas = (len(itens) + cols - 1) // cols
folha = Image.new('RGB', (cols * w + (cols + 1) * 6, linhas * (h + 28) + 6), (18, 16, 16))
des = ImageDraw.Draw(folha)
for k, (rot, im) in enumerate(itens):
    x = 6 + (k % cols) * (w + 6); y = 6 + (k // cols) * (h + 28)
    folha.paste(im, (x, y))
    des.text((x + 4, y + h + 4), rot, fill=(255, 107, 24), font=fonte)
folha.save(a.saida, quality=88)
print(f'{len(itens)} quadros -> {a.saida} ({folha.width}x{folha.height})')
