# -*- coding: utf-8 -*-
"""Faz o `material/sala-fundo.jpg`: o cenário real dele, desfocado e escurecido, pra preencher o alto do quadro
vertical acima da câmera (a câmera de verdade entra por baixo e o alto dela se desfaz nesta imagem).

É o que substituiu o "recorte sobre fundo falso", que o criador chamou de "bem amador": ele fica no cenário dele.

Uso: python fundo_sala.py <quadro da câmera.jpg> <material/sala-fundo.jpg> [--x 0] [--larg 640]
Escolha uma faixa vertical do quadro em que ele NÃO aparece (em geral o lado da estante): --x é onde ela começa e
--larg a largura (a altura é a do quadro inteiro). Um quadro da câmera está em <short>/cena/quadros/cam/00060.jpg."""
import sys
from PIL import Image, ImageEnhance, ImageFilter
args = sys.argv[1:]; x = 0; larg = 640
for nome in ('--x', '--larg'):
    if nome in args:
        k = args.index(nome); v = int(args[k + 1]); del args[k:k + 2]
        if nome == '--x': x = v
        else: larg = v
im = Image.open(args[0]).convert('RGB')
im = im.crop((x, 0, x + larg, im.height)).resize((1080, 1920)).filter(ImageFilter.GaussianBlur(46))
ImageEnhance.Brightness(im).enhance(0.55).save(args[1], quality=90)
print('feito', args[1])
