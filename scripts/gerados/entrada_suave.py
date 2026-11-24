"""Refaz a chegada da entrada no monitor com movimento continuo (sem tranco, sem parada).
Medido na versao 4: o clipe do Kling (24 q/s) acelerado 2,19x e amostrado a 30 q/s andava "76, 76, 36 %/s" (um quadro em
cada quatro pela metade), parava de vez na pagina e a cena dava um segundo solavanco.

Como fica:
  parte 1 (camera ainda longe): quadros do clipe de 2 em 2 (2,5x exato, sem quadro repetido nem pulado);
  parte 2 (pagina ja nitida): a posicao da camera vira uma curva suave (Hermite em log da escala) que desacelera da
           velocidade da parte 1 ate a velocidade do empurrao lento da cena; cada quadro e o quadro do Kling mais proximo,
           deformado pra cair exatamente nessa curva, com a pagina REAL por cima (mistura por escala, 0,72 -> 0,82).
Saida: pasta de quadros jpg (30 q/s) e um json com n, n1, v_fim (velocidade no ultimo quadro, em log-escala por segundo).

  python entrada_suave.py <clipe> <captura_real> <pasta_saida> [--ini 0.5] [--sj 0.70] [--dur2 0.87] [--vfim 0.045]"""
import argparse
import json
import os

import cv2
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("clipe"); ap.add_argument("captura"); ap.add_argument("saida")
ap.add_argument("--ini", type=float, default=0.5)      # onde o clipe comeca a ser usado (s)
ap.add_argument("--sj", type=float, default=0.70)      # escala em que a parte 2 assume
ap.add_argument("--dur2", type=float, default=0.87)    # duracao da parte 2 (s)
ap.add_argument("--vfim", type=float, default=0.045)   # velocidade na chegada (log-escala/s): a do empurrao lento da cena
ap.add_argument("--cx", type=float, default=650); ap.add_argument("--cw", type=float, default=810)
a = ap.parse_args()
W, H, FPS = 1080, 1920, 30

real = cv2.imread(a.captura); rh, rw = real.shape[:2]
esc = W / a.cw
A_fim = np.array([[esc, 0, -a.cx * esc], [0, H / rh, 0]], np.float64)
final = cv2.warpAffine(real, A_fim.astype(np.float32), (W, H), flags=cv2.INTER_LANCZOS4)

cap = cv2.VideoCapture(a.clipe); fc = cap.get(cv2.CAP_PROP_FPS)
Q = []
while True:
    ok, f = cap.read()
    if not ok:
        break
    Q.append(cv2.resize(f, (W, H), interpolation=cv2.INTER_LANCZOS4))
print(f"clipe: {len(Q)} quadros a {fc:.0f} q/s")

sift = cv2.SIFT_create(4000); bf = cv2.BFMatcher()
kf, df = sift.detectAndCompute(cv2.cvtColor(final, cv2.COLOR_BGR2GRAY), None)


def acha(q):
    k, d = sift.detectAndCompute(cv2.cvtColor(q, cv2.COLOR_BGR2GRAY), None)
    if d is None or len(k) < 20:
        return None
    bons = [m for m, n in bf.knnMatch(df, d, k=2) if m.distance < 0.72 * n.distance]
    if len(bons) < 30:
        return None
    M, dentro = cv2.estimateAffinePartial2D(np.float32([kf[m.queryIdx].pt for m in bons]), np.float32([k[m.trainIdx].pt for m in bons]),
                                            method=cv2.RANSAC, ransacReprojThreshold=3.0)
    return M if M is not None and dentro.sum() >= 25 else None


# transformacao (quadro final -> quadro k) de cada quadro em que a pagina ja e reconhecivel
Ms = {}
for k in range(int(1.6 * fc), len(Q)):
    M = acha(Q[k])
    if M is not None:
        Ms[k] = M
ks = sorted(Ms)
S = np.array([np.hypot(Ms[k][0, 0], Ms[k][1, 0]) for k in ks])
TX = np.array([Ms[k][0, 2] for k in ks]); TY = np.array([Ms[k][1, 2] for k in ks])
print(f"pagina reconhecida de {ks[0] / fc:.2f}s a {ks[-1] / fc:.2f}s; escala {S[0]:.3f} -> {S[-1]:.3f}")

# quadro em que a parte 2 assume (o primeiro com escala >= sj) e a paridade pra chegar nele de 2 em 2
kj = next(k for k, s in zip(ks, S) if s >= a.sj)
k0 = int(round(a.ini * fc)); k0 += (kj - k0) % 2
parte1 = list(range(k0, kj + 1, 2))   # inclui o proprio kj: a parte 2 comeca um passo depois dele (sem isso a troca pulava dois passos num quadro)
ij = ks.index(kj)
# velocidade do Kling em volta de kj (log-escala por segundo de clipe), media de 8 quadros, vezes 2,5
v_clipe = (np.log(S[min(len(S) - 1, ij + 4)]) - np.log(S[max(0, ij - 4)])) / ((ks[min(len(S) - 1, ij + 4)] - ks[max(0, ij - 4)]) / fc)
vj = v_clipe * 2 * FPS / fc
uj = float(np.log(S[ij]))
print(f"parte 1: {len(parte1)} quadros (do {k0} ao {kj}, de 2 em 2); na troca: escala {S[ij]:.4f}, velocidade {vj * 100:.0f} %/s")

# translacao: num zoom em direcao a um ponto fixo ela e linear na escala; ajusta reta e corrige o residuo de kj, sumindo ate o fim
bx = np.polyfit(S[ij:], TX[ij:], 1); by = np.polyfit(S[ij:], TY[ij:], 1)
rx, ry = TX[ij] - np.polyval(bx, S[ij]), TY[ij] - np.polyval(by, S[ij])
# no fim (escala 1) a pagina tem que cair exatamente no quadro final: tira tambem o que sobrar la
fx_, fy_ = np.polyval(bx, 1.0), np.polyval(by, 1.0)

n2 = int(round(a.dur2 * FPS)); D = n2 / FPS


def hermite(p, u0, v0, u1, v1, d):
    h00, h10, h01, h11 = 2 * p**3 - 3 * p**2 + 1, p**3 - 2 * p**2 + p, -2 * p**3 + 3 * p**2, p**3 - p**2
    return h00 * u0 + h10 * d * v0 + h01 * u1 + h11 * d * v1


os.makedirs(a.saida, exist_ok=True)
for f in os.listdir(a.saida):
    if f.endswith(".jpg"):
        os.remove(os.path.join(a.saida, f))
n = 0


def grava(img):
    global n
    n += 1
    cv2.imwrite(os.path.join(a.saida, f"{n:05d}.jpg"), img, [cv2.IMWRITE_JPEG_QUALITY, 95])


for k in parte1:
    grava(Q[k])

A3 = np.vstack([A_fim, [0, 0, 1]])
mask_real = np.full((rh, rw), 255, np.uint8)
ant = None
for i in range(1, n2 + 1):
    p = i / n2
    u = hermite(p, uj, vj, 0.0, a.vfim, D); s = float(np.exp(u))
    w = 1 - p * p * (3 - 2 * p)                                   # peso do residuo de kj (some ate o fim)
    w1 = p * p * (3 - 2 * p)                                      # peso da correcao do fim
    tx = np.polyval(bx, s) + rx * w - fx_ * w1 * s
    ty = np.polyval(by, s) + ry * w - fy_ * w1 * s
    T = np.array([[s, 0, tx], [0, s, ty]], np.float64)            # quadro final -> quadro de saida
    # quadro do Kling: o de escala mais proxima sem passar muito (pra ampliar, nunca reduzir)
    cand = [(abs(np.log(S[j]) - u) + (0.02 if S[j] > s * 1.004 else 0), j) for j in range(ij, len(ks))]
    j = min(cand)[1]; Mk = np.vstack([Ms[ks[j]], [0, 0, 1]])
    R = (np.vstack([T, [0, 0, 1]]) @ np.linalg.inv(Mk))[:2]
    base = cv2.warpAffine(Q[ks[j]], R.astype(np.float32), (W, H), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REPLICATE)
    Tr = (np.vstack([T, [0, 0, 1]]) @ A3)[:2]
    wr = cv2.warpAffine(real, Tr.astype(np.float32), (W, H), flags=cv2.INTER_LANCZOS4 if s > 0.8 else cv2.INTER_AREA)
    m = cv2.warpAffine(mask_real, Tr.astype(np.float32), (W, H), flags=cv2.INTER_LINEAR)
    m = cv2.GaussianBlur(cv2.erode(m, np.ones((9, 9), np.uint8)), (0, 0), 6).astype(np.float32)[..., None] / 255.0
    al = float(np.clip((s - 0.72) / 0.10, 0, 1)); al = al * al * (3 - 2 * al)
    grava(np.clip(wr.astype(np.float32) * m * al + base.astype(np.float32) * (1 - m * al), 0, 255).astype(np.uint8))
    if i % 4 == 0 or i == n2:
        vel = '' if ant is None else f" vel {(u - ant) * FPS / 4 * 100 if i % 4 == 0 else 0:5.1f} %/s"
        print(f"  parte 2 q{i:02d}: escala {s:.4f} (Kling q{ks[j]}, {S[j]:.3f}) mistura {al:.2f}{vel}")
        ant = u
json.dump({"n": n, "n1": len(parte1), "n2": n2, "v_fim": a.vfim, "escala_troca": float(S[ij])}, open(os.path.join(a.saida, "entrada.json"), "w"))
print(f"feito: {n} quadros ({n / FPS:.2f} s) em {a.saida}")
