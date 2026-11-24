# -*- coding: utf-8 -*-
"""Duas, três ou quatro versões do Short lado a lado, com rótulo em cima de cada uma e o som de UMA delas.

O criador decide comparando: toda vez que existirem duas versões de um trecho ou do Short inteiro, entregue este vídeo
junto. Misturar os sons daria eco, então só uma coluna toca (o rótulo dela fica laranja).

Uso: python lado_a_lado.py <saida.mp4> <indice_do_som 0..> <v1> "<rótulo 1>" <v2> "<rótulo 2>" [...] [--de 0 --ate 4.6] [--leve]
  --de/--ate  compara só um trecho (segundos), por exemplo a abertura;
  --leve      grava também <saida>-leve.mp4 com menos de ~10 MB pra mandar pelo app (arquivo grande falha no envio)."""
import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont
args = sys.argv[1:]; de = ate = None; leve = False
if '--leve' in args: args.remove('--leve'); leve = True
for nome in ('--de', '--ate'):
    if nome in args:
        k = args.index(nome); val = float(args[k + 1]); del args[k:k + 2]
        if nome == '--de': de = val
        else: ate = val
saida, i_som = args[0], int(args[1]); vids, rots = args[2::2], args[3::2]
assert 2 <= len(vids) <= 4 and len(vids) == len(rots), 'passe de 2 a 4 pares <vídeo> "<rótulo>"'
N = len(vids); L = {2: 720, 3: 640, 4: 480}[N]; A = round(L * 16 / 9 / 2) * 2; F = 72
tmp = os.path.join(os.path.dirname(os.path.abspath(saida)), '_lado_tmp'); os.makedirs(tmp, exist_ok=True)
imgs = []
for k, r in enumerate(rots):
    im = Image.new('RGB', (L, F), (12, 12, 14)); d = ImageDraw.Draw(im); tam = 34
    f = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', tam)
    while d.textlength(r, font=f) > L - 30 and tam > 16:
        tam -= 2; f = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', tam)
    d.text(((L - d.textlength(r, font=f)) / 2, (F - tam) / 2 - tam * 0.12), r, font=f, fill=(255, 170, 60) if k == i_som else (225, 225, 230))
    p = os.path.join(tmp, f'rot{k}.png'); im.save(p); imgs.append(p)
corte = (['-ss', f'{de}'] if de is not None else []) + (['-t', f'{ate - (de or 0)}'] if ate is not None else [])
cmd = ['ffmpeg', '-y', '-v', 'error']
for v in vids: cmd += corte + ['-i', v]
for p in imgs: cmd += ['-loop', '1', '-i', p]
fc = ''.join(f'[{k}:v]fps=30,scale={L}:{A}:flags=lanczos,setsar=1[v{k}];[{N + k}:v]fps=30,setsar=1[r{k}];[r{k}][v{k}]vstack=shortest=1[c{k}];' for k in range(N))
fc += ''.join(f'[c{k}]' for k in range(N)) + f'hstack=inputs={N}:shortest=1,pad=iw+4:ih:2:0:color=0x0c0c0e[v]'
cmd += ['-filter_complex', fc, '-map', '[v]', '-map', f'{i_som}:a', '-c:v', 'libx264', '-crf', '21', '-preset', 'medium', '-pix_fmt', 'yuv420p',
        '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', saida]
r = subprocess.run(cmd, capture_output=True, text=True)
if r.returncode: sys.exit(r.stderr[-2000:])
print('feito', saida, f'{os.path.getsize(saida) / 1e6:.1f} MB')
if leve:
    sl = os.path.splitext(saida)[0] + '-leve.mp4'
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', saida, '-c:v', 'libx264', '-crf', '27', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-c:a', 'copy',
                    '-movflags', '+faststart', sl], check=True)
    print('feito', sl, f'{os.path.getsize(sl) / 1e6:.1f} MB')
for p in imgs: os.remove(p)
os.rmdir(tmp)
