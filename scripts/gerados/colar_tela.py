"""Cola um motion real (16:9) na tela verde de um plano gerado, quadro a quadro.
O plano vem com o monitor em verde de recorte; a cabeca dele passa na frente e o recorte pelo verde resolve isso em
cada quadro. A tela fica com os pixels exatos do motion (a IA nao redesenha nada).
  python colar_tela.py <clipe_verde> <pasta_motion_1920x1080> <pasta_saida> [primeiro_quadro=10] [passo=2]
Passo 2 = o plano anda 2,5x mais rapido (cara de time-lapse). Sai um quadro por quadro do motion."""
import os
import sys

import cv2
import numpy as np

clipe, pmotion, saida = sys.argv[1:4]
k0 = int(sys.argv[4]) if len(sys.argv) > 4 else 10
passo = int(sys.argv[5]) if len(sys.argv) > 5 else 2
W, H = 1080, 1920

cap = cv2.VideoCapture(clipe); Q = []
while True:
    ok, f = cap.read()
    if not ok:
        break
    Q.append(cv2.resize(f, (W, H), interpolation=cv2.INTER_LANCZOS4))
motion = sorted(f for f in os.listdir(pmotion) if f.endswith(".jpg"))
N = len(motion)
assert k0 + passo * (N - 1) < len(Q), f"clipe curto: {len(Q)} quadros pra {N} do motion"
usados = [Q[k0 + passo * i] for i in range(N)]


def verde(f):
    """quanto cada ponto e verde de recorte (0 a 1)"""
    b, g, r = [f[..., c].astype(np.float32) for c in range(3)]
    return np.clip((g - np.maximum(r, b) - 28) / 60.0, 0, 1)


# ---------- o quadrilatero da tela: uniao do verde em todos os quadros, reta ajustada em cada lado ----------
uni = np.zeros((H, W), np.float32)
for f in usados:
    uni = np.maximum(uni, verde(f))
m = (uni > 0.5).astype(np.uint8)
m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((7, 7), np.uint8))
n, rot, st, _ = cv2.connectedComponentsWithStats(m)
m = (rot == 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))).astype(np.uint8)
ys, xs = np.nonzero(m)
x_min, x_max, y_min, y_max = xs.min(), xs.max(), ys.min(), ys.max()
larg, alt = x_max - x_min, y_max - y_min


def reta(pts_a, pts_b):
    """ajuste robusto b = k*a + c (tira os 20% mais distantes e ajusta de novo)"""
    a, b = np.float64(pts_a), np.float64(pts_b)
    for _ in range(3):
        k, c = np.polyfit(a, b, 1)
        e = np.abs(b - (k * a + c)); ok = e <= np.percentile(e, 80) + 0.5
        a, b = a[ok], b[ok]
    return np.polyfit(a, b, 1)


linhas = [(y, np.nonzero(m[y])[0]) for y in range(y_min + int(alt * 0.08), y_max - int(alt * 0.08), 3)]
cols = [(x, np.nonzero(m[:, x])[0]) for x in range(x_min + int(larg * 0.06), x_min + int(larg * 0.62), 3)]   # so a parte que a cabeca nao cobre
esq = reta([y for y, v in linhas], [v.min() for y, v in linhas])                 # x = k*y + c
topo = reta([x for x, v in cols], [v.min() for x, v in cols])                    # y = k*x + c
base = reta([x for x, v in cols], [v.max() for x, v in cols])
dir_pts = [(y, v.max()) for y, v in linhas if v.max() >= x_max - larg * 0.03]    # linhas em que a borda direita aparece
if len(dir_pts) >= 8:
    dire = reta([y for y, _ in dir_pts], [x for _, x in dir_pts])
else:                                                                             # borda direita sempre coberta: paralela a esquerda
    dire = np.array([esq[0], x_max - esq[0] * (y_min + alt / 2)])


def cruza(vert, horiz):          # x = kv*y + cv ; y = kh*x + ch
    kv, cv_ = vert; kh, ch = horiz
    y = (kh * cv_ + ch) / (1 - kh * kv)
    return [kv * y + cv_, y]


quad = np.float32([cruza(esq, topo), cruza(dire, topo), cruza(dire, base), cruza(esq, base)])
print("tela (cantos):", np.round(quad).astype(int).tolist(), f"| borda direita por {len(dir_pts)} linhas")
Hm = cv2.getPerspectiveTransform(np.float32([[0, 0], [1920, 0], [1920, 1080], [0, 1080]]), quad)
dentro = np.zeros((H, W), np.uint8); cv2.fillConvexPoly(dentro, np.int32(np.round(quad)), 255, cv2.LINE_AA)
dentro_f = cv2.GaussianBlur(cv2.dilate(dentro, np.ones((5, 5), np.uint8)), (0, 0), 1.0).astype(np.float32) / 255.0
perto = cv2.GaussianBlur(cv2.dilate(dentro, np.ones((61, 61), np.uint8)), (0, 0), 45).astype(np.float32) / 255.0   # onde tirar o reflexo verde

os.makedirs(saida, exist_ok=True)
for f in os.listdir(saida):
    if f.endswith(".jpg"):
        os.remove(os.path.join(saida, f))
for i, f in enumerate(usados):
    mo = cv2.imread(os.path.join(pmotion, motion[i]))
    tela = cv2.warpPerspective(mo, Hm, (W, H), flags=cv2.INTER_AREA).astype(np.float32)
    tela = cv2.GaussianBlur(tela, (0, 0), 0.6)
    v = verde(f)
    ff = f.astype(np.float32)
    b_, g, r_ = ff[..., 0], ff[..., 1], ff[..., 2]
    cheio = (v > 0.95) & (dentro > 200)
    Gc = np.median(ff[cheio], axis=0) if cheio.sum() > 500 else np.float32([40, 240, 40])   # o verde puro deste quadro
    d0 = float(Gc[1] - max(Gc[0], Gc[2]))
    # quanto de cada ponto e TELA (0 a 1), linear: num ponto misturado (borda desfocada da cabeca) p = a*verde + (1-a)*frente
    a = np.clip((g - np.maximum(r_, b_)) / (d0 * 0.93) * 1.3, 0, 1) * dentro_f   # 1.3: a faixa de mistura puxa pra tela (borda mais fina)
    a = cv2.GaussianBlur(a, (0, 0), 0.7)[..., None]
    # sombreado da tela real (vinheta e reflexos do verde), bem de leve
    med = float(Gc[1])
    sombra = cv2.GaussianBlur(np.clip(g / max(1.0, med), 0.8, 1.12), (0, 0), 14)
    sombra = np.where(v > 0.3, sombra, 1.0)[..., None]
    tela_s = tela * 1.06 * sombra
    # desmistura: tira do ponto a parte verde (a*verde) e poe no lugar a mesma parte do motion; a frente fica com a cor dela
    out = ff + a * (tela_s - Gc)
    out = np.where(a >= 0.97, tela_s, out)
    # fora da tela (moldura, mesa, cabelo perto): tira o reflexo verde que sobrar
    # (o contorno da cabeca vem com uma luz verde da tela por cima da pele: G alto com R alto, que virava um filete amarelo.
    #  O teto do verde e a MEDIA entre vermelho e azul, nao o maior dos dois, e a luz a mais e abaixada um pouco.)
    o_g = out[..., 1]; lim = 0.56 * out[..., 2] + 0.44 * out[..., 0] + 3
    fora_tela = perto * (a[..., 0] < 0.97)                           # tudo o que nao e tela pura, inclusive a faixa de mistura
    excesso = np.clip((o_g - lim) / 70.0, 0, 1) * fora_tela          # quanto de luz verde sobrou neste ponto
    out[..., 1] = o_g * (1 - fora_tela) + np.minimum(o_g, lim) * fora_tela
    out *= (1 - 0.30 * excesso)[..., None]
    cv2.imwrite(os.path.join(saida, f"{i + 1:05d}.jpg"), np.clip(out, 0, 255).astype(np.uint8), [cv2.IMWRITE_JPEG_QUALITY, 95])
print(f"feito: {N} quadros em {saida} (clipe do quadro {k0} ao {k0 + passo * (N - 1)}, de {passo} em {passo})")
