# -*- coding: utf-8 -*-
"""Transforma o recorte do Higgsfield (ele sobre fundo preto) em quadros transparentes pra cena.

O Higgsfield devolve um vídeo com ele sobre preto puro e sem o microfone. Pra tirar a transparência sem confundir a
camiseta preta com o fundo, o vídeo que sobe já vai com os pretos levantados (nada abaixo de 51); a transparência de
cada ponto é a razão entre o resultado e o que subiu. A cor vem do quadro original da câmera (não do resultado), e o
microfone volta: dentro da área dele, cada linha é preenchida entre a ponta esquerda e a ponta direita do corpo.

Uso: python recorte_alfa.py <short-XX> [--teste <quadro-da-cena>] [--inverso]
     Leva ~1,3 s por quadro (20 min pra 900). Pra acabar na metade do tempo, rode duas vezes ao mesmo tempo, uma delas
     com --inverso: cada uma pula o quadro que a outra já gravou. Pra refazer um quadro, apague o .webp dele.
Lê  <short>/trechos/recorte-entrada.mp4, <short>/gerados/recorte-resultado.mp4, <short>/tmp/rec-mapa.json
     (pra cada quadro do vídeo que subiu, o número do quadro da câmera na extração ANTIGA, ou 0 se era quadro de espera)
     e <short>/tmp/rec-novo.json: {quadro novo: quadro antigo} (quando a cena foi reextraída com outra numeração).
Grava <short>/cena/quadros/rec/NNNNN.webp (1920x1080, com transparência), com o mesmo número do quadro da câmera."""
import json, os, subprocess, sys
import numpy as np, cv2
from PIL import Image

base = os.path.abspath(sys.argv[1]); teste = int(sys.argv[sys.argv.index('--teste') + 1]) if '--teste' in sys.argv else None
W, H = 1280, 720
MIC = (740, 640, 1110, 1080)          # área onde o microfone pode estar, em pontos do quadro 1920x1080

def quadros(arq):
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', arq, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    while True:
        b = p.stdout.read(W * H * 3)
        if len(b) < W * H * 3:
            break
        yield np.frombuffer(b, np.uint8).reshape(H, W, 3)

mapa = json.load(open(os.path.join(base, 'tmp', 'rec-mapa.json')))
novo = {int(k): v for k, v in json.load(open(os.path.join(base, 'tmp', 'rec-novo.json'))).items()}
j_de = {q: j for j, q in enumerate(mapa) if q}             # quadro antigo -> posição no vídeo que subiu
alfa_dir = os.path.join(base, 'tmp', 'rec-alfa'); os.makedirs(alfa_dir, exist_ok=True)

# 1. transparência crua de cada quadro do vídeo (razão resultado / entrada)
if len(os.listdir(alfa_dir)) < len(mapa):
    for j, (e, r) in enumerate(zip(quadros(os.path.join(base, 'trechos', 'recorte-entrada.mp4')),
                                   quadros(os.path.join(base, 'gerados', 'recorte-resultado.mp4')))):
        raz = r.astype(np.float32).sum(2) / np.maximum(1, e.astype(np.float32).sum(2))
        a = np.clip((raz - 0.12) / 0.76, 0, 1)
        cv2.imwrite(os.path.join(alfa_dir, f'{j + 1:05d}.png'), (a * 255).astype(np.uint8))
    print('transparência crua pronta:', len(os.listdir(alfa_dir)), 'quadros', flush=True)

def pequeno(arq):
    return cv2.resize(cv2.imread(arq, cv2.IMREAD_GRAYSCALE), (320, 180), interpolation=cv2.INTER_AREA).astype(np.float32)

def faz(q, mostra=False):
    cam_arq = os.path.join(base, 'cena', 'quadros', 'cam', f'{q:05d}.jpg')
    # acha o quadro do vídeo que é exatamente este (o esperado ou um vizinho), comparando a imagem
    alvo = pequeno(cam_arq) * 0.8 + 51; melhor = None      # o vídeo que subiu tem os pretos levantados: compara na mesma escala
    for o in (novo[q] - 1, novo[q], novo[q] + 1):
        if o in j_de:
            d = float(np.abs(pequeno(os.path.join(base, 'tmp', 'rec-entrada', f'{j_de[o] + 1:05d}.jpg')) - alvo).mean())
            if melhor is None or d < melhor[0]:
                melhor = (d, o)
    d, o = melhor
    a = cv2.imread(os.path.join(alfa_dir, f'{j_de[o] + 1:05d}.png'), cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255
    # o microfone volta: em cada linha da área dele, preenche entre a ponta esquerda e a direita do corpo
    x0, y0, x1, y1 = [int(round(v * W / 1920)) for v in MIC]
    cx = a[y0:y1, x0:x1]; fg = cx > 0.5
    for y in range(fg.shape[0]):
        xs = np.flatnonzero(fg[y])
        if len(xs) > 1:
            cx[y, xs[0]:xs[-1] + 1] = 1.0
    A = cv2.resize(a, (1920, 1080), interpolation=cv2.INTER_CUBIC)
    A = cv2.GaussianBlur(A, (0, 0), 0.9)
    A = np.clip((A - 0.30) / 0.55, 0, 1)                    # aperta a borda um ponto pra dentro (some a franja da parede)
    A = np.clip((cv2.GaussianBlur(A, (0, 0), 2.4) - 0.16) / 0.84, 0, 1)   # borda macia: o recorte vai por cima da própria imagem dele no cenário real
    C = cv2.imread(cam_arq).astype(np.float32)             # BGR
    O = (A > 0.97).astype(np.float32); O = cv2.erode(O, np.ones((5, 5), np.uint8))
    num = cv2.GaussianBlur(C * O[..., None], (0, 0), 5); den = cv2.GaussianBlur(O, (0, 0), 5)
    dentro = num / np.maximum(den, 1e-3)[..., None]         # a cor de dentro dele, espalhada até a borda
    w = (np.clip((A - 0.55) / 0.42, 0, 1) * (den < 0.999) + (den >= 0.999))[..., None]
    w = np.where(den[..., None] < 0.02, 1.0, w)             # longe dele não há cor de dentro: fica a original (alfa ~0 de todo jeito)
    Cf = C * w + dentro * (1 - w)
    rgba = np.dstack([Cf[..., ::-1], A[..., None] * 255]).clip(0, 255).astype(np.uint8)
    return rgba, d, o

if teste:
    rgba, d, o = faz(teste)
    print(f'quadro {teste}: casou com o antigo {o} (esperado {novo[teste]}), diferença média {d:.2f}')
    A = rgba[..., 3:4].astype(np.float32) / 255
    for nome, cor in (('laranja', (255, 107, 24)), ('creme', (243, 237, 230)), ('preto', (12, 10, 10))):
        comp = (rgba[..., :3] * A + np.array(cor, np.float32) * (1 - A)).astype(np.uint8)
        Image.fromarray(comp).save(os.path.join(base, 'tmp', f'rec-teste-{nome}.jpg'), quality=92)
    sys.exit()

sai = os.path.join(base, 'cena', 'quadros', 'rec'); os.makedirs(sai, exist_ok=True)
trocas = 0; pior = 0.0
for k, q in enumerate(sorted(novo, reverse='--inverso' in sys.argv)):
    if os.path.exists(os.path.join(sai, f'{q:05d}.webp')): continue      # já feito (por outra instância ou numa rodada anterior)
    rgba, d, o = faz(q); trocas += o != novo[q]; pior = max(pior, d)
    Image.fromarray(rgba, 'RGBA').save(os.path.join(sai, f'{q:05d}.webp'), 'WEBP', quality=90, method=2, alpha_quality=92)
    if k % 60 == 0:
        print(f'  {k}/{len(novo)}', flush=True)
print(f'{len(novo)} quadros transparentes em {sai}; {trocas} casaram com o vizinho em vez do esperado; maior diferença {pior:.2f}')
