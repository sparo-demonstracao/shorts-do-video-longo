"""Junta o video original (1:1, nitido, rosto real) com o video vertical gerado (reframe):
o original fica por cima, no meio, com borda macia; o gerado so aparece em cima e embaixo.
Uso: python compor_vertical.py <original> <gerado> <saida.mp4> [audio.wav inicio_s]"""
import subprocess
import sys

import cv2
import numpy as np

orig, ger, saida = sys.argv[1], sys.argv[2], sys.argv[3]
audio = sys.argv[4] if len(sys.argv) > 4 else None
a_ini = float(sys.argv[5]) if len(sys.argv) > 5 else 0.0
W, H = 1080, 1920
PENA = 70  # largura da borda macia embaixo e dos lados, em pixels da saida
PENA_TOPO = 22  # em cima a borda e curta: a cabeca gerada fica um pouco mais alta que a real e fazia sombra acima do cabelo


def quadros(caminho):
    cap = cv2.VideoCapture(caminho)
    fps = cap.get(cv2.CAP_PROP_FPS)
    fs = []
    while True:
        ok, f = cap.read()
        if not ok:
            break
        fs.append(f)
    return fps, fs


fo, O = quadros(orig)
fg, G = quadros(ger)
gh, gw = G[0].shape[:2]
esc = W / gw


def par(n):
    return O[n], G[min(len(G) - 1, round(n / fo * fg))]


# 1) transformacao original -> gerado (escala + translacao), mediana de varios quadros
sift = cv2.SIFT_create(3000)
bf = cv2.BFMatcher()
Ms = []
for n in range(5, len(O), 12):
    o, g = par(n)
    k1, d1 = sift.detectAndCompute(cv2.cvtColor(o, cv2.COLOR_BGR2GRAY), None)
    k2, d2 = sift.detectAndCompute(cv2.cvtColor(g, cv2.COLOR_BGR2GRAY), None)
    bons = [m for m, n2 in bf.knnMatch(d1, d2, k=2) if m.distance < 0.7 * n2.distance]
    if len(bons) < 30:
        continue
    p1 = np.float32([k1[m.queryIdx].pt for m in bons])
    p2 = np.float32([k2[m.trainIdx].pt for m in bons])
    M, _ = cv2.estimateAffinePartial2D(p1, p2, method=cv2.RANSAC, ransacReprojThreshold=2.0)
    if M is not None:
        Ms.append(M)
M = np.median(np.array(Ms), axis=0)
s = float(np.hypot(M[0, 0], M[1, 0]))
print(f"original -> gerado: escala {s:.4f}, x {M[0, 2]:.1f}, y {M[1, 2]:.1f} ({len(Ms)} medidas)")
M2 = np.array([[s * esc, 0, M[0, 2] * esc], [0, s * esc, M[1, 2] * esc]], np.float32)
oh, ow = O[0].shape[:2]
x0, y0 = M2[0, 2], M2[1, 2]
x1, y1 = x0 + ow * s * esc, y0 + oh * s * esc
print(f"na saida o original ocupa x {x0:.0f}..{x1:.0f}, y {y0:.0f}..{y1:.0f}")

# 2) mascara: 1 no miolo do original, cai pra 0 na borda (so onde existe imagem gerada alem dela)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
ay = np.minimum(np.clip((yy - y0) / PENA_TOPO, 0, 1), np.clip((y1 - yy) / PENA, 0, 1))
ax = np.ones_like(ay)
if x0 > 2:
    ax = np.minimum(ax, np.clip((xx - x0) / PENA, 0, 1))
if x1 < W - 2:
    ax = np.minimum(ax, np.clip((x1 - xx) / PENA, 0, 1))
alfa = (ay * ax)
alfa = (alfa * alfa * (3 - 2 * alfa))[..., None]

# 3) cor: ajusta o gerado pra bater com o original na area comum (ganho e deslocamento por canal)
gs, os_ = [], []
for n in range(5, len(O), 12):
    o, g = par(n)
    go = cv2.resize(g, (W, H), interpolation=cv2.INTER_CUBIC)
    wo = cv2.warpAffine(o, M2, (W, H), flags=cv2.INTER_AREA)
    m = alfa[..., 0] > 0.99
    gs.append(go[m].reshape(-1, 3).astype(np.float32)[::50])
    os_.append(wo[m].reshape(-1, 3).astype(np.float32)[::50])
gs, os_ = np.concatenate(gs), np.concatenate(os_)
ganho = os_.std(0) / gs.std(0)
desl = os_.mean(0) - gs.mean(0) * ganho
print("cor: ganho", np.round(ganho, 3), "deslocamento", np.round(desl, 1))

cmd = ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(fo), "-i", "-"]
if audio:
    cmd += ["-ss", f"{a_ini:.3f}", "-t", f"{len(O) / fo:.3f}", "-i", audio, "-c:a", "aac", "-b:a", "192k"]
cmd += ["-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", "-shortest", saida]
p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
for n in range(len(O)):
    o, g = par(n)
    go = cv2.resize(g, (W, H), interpolation=cv2.INTER_CUBIC).astype(np.float32) * ganho + desl
    wo = cv2.warpAffine(o, M2, (W, H), flags=cv2.INTER_CUBIC).astype(np.float32)
    f = np.clip(wo * alfa + go * (1 - alfa), 0, 255).astype(np.uint8)
    p.stdin.write(f.tobytes())
p.stdin.close()
p.wait()
print("feito", saida, len(O), "quadros")
