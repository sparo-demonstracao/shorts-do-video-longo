# -*- coding: utf-8 -*-
"""Miniaturas numeradas de uma gravação longa, pra achar rápido os momentos que interessam (ele de perfil, virado
pra tela, rindo, sem o microfone na frente...).

Serve pra montar as REFERÊNCIAS DE ROSTO de uma foto gerada. Com um quadro só, de frente, o modelo inventa o perfil dele
e "não fica parecido" (palavras do criador). Com 8 ou 9 quadros reais, de frente, de três quartos e de perfil, fica.

Lê só os quadros-chave do arquivo (rápido: 1h37 de gravação em ~1 min). Não tente detectar perfil por programa em
gravação longa: decodificar tudo levou mais de 10 min e foi abandonado. Olhe as folhas.

Uso: python miniaturas.py <gravação> <pasta_saida> [--cada 12] [--crop l:a:x:y]
Sai <pasta>/chaves/0001.jpg... e <pasta>/folha-0.jpg, folha-1.jpg... (160 por folha, com o número em cada uma).
A miniatura N está no instante (N-1) x cada. Pra tirar o quadro em tamanho cheio:
  ffmpeg -ss <segundos> -i <gravação> -frames:v 1 -vf "crop=900:900:600:0" -q:v 2 rosto/rNNNN.jpg"""
import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont
args = sys.argv[1:]; cada = 12; crop = ''
if '--cada' in args:
    k = args.index('--cada'); cada = float(args[k + 1]); del args[k:k + 2]
if '--crop' in args:
    k = args.index('--crop'); crop = 'crop=' + args[k + 1] + ','; del args[k:k + 2]
video, pasta = args[0], args[1]; ch = os.path.join(pasta, 'chaves'); os.makedirs(ch, exist_ok=True)
for f in os.listdir(ch): os.remove(os.path.join(ch, f))
subprocess.run(['ffmpeg', '-v', 'error', '-skip_frame', 'nokey', '-i', video, '-vf', f'fps=1/{cada},{crop}scale=280:-2',
                '-fps_mode', 'vfr', '-q:v', '3', os.path.join(ch, '%04d.jpg')], stderr=subprocess.DEVNULL)
fs = sorted(os.listdir(ch))
if not fs: sys.exit('nenhuma miniatura saiu: confira o arquivo e o --crop')
fonte = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 16); C = 16
w0, h0 = Image.open(os.path.join(ch, fs[0])).size; W = 168; H = round(h0 * W / w0)
for s in range(0, len(fs), 160):
    g = fs[s:s + 160]; linhas = (len(g) + C - 1) // C
    o = Image.new('RGB', (C * W, linhas * H), (10, 10, 10)); d = ImageDraw.Draw(o)
    for i, n in enumerate(g):
        x, y = (i % C) * W, (i // C) * H
        o.paste(Image.open(os.path.join(ch, n)).resize((W - 2, H - 2)), (x, y)); d.text((x + 3, y + 2), n[:4], fill=(255, 120, 30), font=fonte)
    nome = os.path.join(pasta, f'folha-{s // 160}.jpg'); o.save(nome, quality=85); print(nome, o.size)
print(f'{len(fs)} miniaturas, uma a cada {cada:g} s')
