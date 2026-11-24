"""No fim da entrada no monitor, troca a pagina gerada pela pagina REAL, acompanhando o movimento da camera.
Pra cada quadro do clipe a partir de t0, acha (SIFT) onde a captura real cai no quadro, deforma a captura real
pra esse lugar e mistura: 0% em t0, 100% em t1. Dai em diante a pagina e so pixel real.
  python fundir_real.py <clipe> <captura_real_inteira> <saida> <t0> <t1> <crop_x> <crop_w>
crop_x/crop_w: faixa da captura que virou o quadro final (ex.: 650 810)."""
import subprocess
import sys

import cv2
import numpy as np

clipe, captura, saida = sys.argv[1:4]
t0, t1 = float(sys.argv[4]), float(sys.argv[5])
cx, cw = float(sys.argv[6]), float(sys.argv[7])
W, H = 1080, 1920

real = cv2.imread(captura)
rh, rw = real.shape[:2]
# captura inteira -> quadro final (o recorte cx..cx+cw ocupa a largura toda)
esc = W / cw
A_fim = np.array([[esc, 0, -cx * esc], [0, H / rh, 0]], np.float64)
final = cv2.warpAffine(real, A_fim.astype(np.float32), (W, H), flags=cv2.INTER_LANCZOS4)

cap = cv2.VideoCapture(clipe)
fps = cap.get(cv2.CAP_PROP_FPS)
quadros = []
while True:
    ok, f = cap.read()
    if not ok:
        break
    quadros.append(cv2.resize(f, (W, H), interpolation=cv2.INTER_LANCZOS4))

sift = cv2.SIFT_create(4000)
kf, df = sift.detectAndCompute(cv2.cvtColor(final, cv2.COLOR_BGR2GRAY), None)
bf = cv2.BFMatcher()


def acha(q):
    """transformacao (escala + translacao + giro pequeno) do quadro final pro quadro q"""
    k, d = sift.detectAndCompute(cv2.cvtColor(q, cv2.COLOR_BGR2GRAY), None)
    if d is None or len(k) < 20:
        return None, 0
    bons = [m for m, n in bf.knnMatch(df, d, k=2) if m.distance < 0.72 * n.distance]
    if len(bons) < 25:
        return None, len(bons)
    p1 = np.float32([kf[m.queryIdx].pt for m in bons])
    p2 = np.float32([k[m.trainIdx].pt for m in bons])
    M, dentro = cv2.estimateAffinePartial2D(p1, p2, method=cv2.RANSAC, ransacReprojThreshold=3.0)
    return M, int(dentro.sum()) if dentro is not None else 0


p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", f"{fps}",
                      "-i", "-", "-c:v", "libx264", "-crf", "14", "-preset", "medium", "-pix_fmt", "yuv420p", saida],
                     stdin=subprocess.PIPE)
ult = None
for i, q in enumerate(quadros):
    t = i / fps
    if t < t0:
        p.stdin.write(q.tobytes())
        continue
    a = min(1.0, (t - t0) / max(1e-6, t1 - t0))
    a = a * a * (3 - 2 * a)
    M, n = acha(q)
    if M is None or n < 20:
        M = ult
    if M is None:
        p.stdin.write(q.tobytes())
        print(f"{t:.2f}s sem encaixe")
        continue
    ult = M
    s = float(np.hypot(M[0, 0], M[1, 0]))
    # captura inteira -> quadro q  =  M o A_fim
    A3 = np.vstack([A_fim, [0, 0, 1]])
    T = (np.vstack([M, [0, 0, 1]]) @ A3)[:2]
    wr = cv2.warpAffine(real, T.astype(np.float32), (W, H), flags=cv2.INTER_LANCZOS4 if s > 0.8 else cv2.INTER_AREA)
    msk = cv2.warpAffine(np.full((rh, rw), 255, np.uint8), T.astype(np.float32), (W, H), flags=cv2.INTER_LINEAR)
    msk = cv2.erode(msk, np.ones((9, 9), np.uint8))
    msk = cv2.GaussianBlur(msk, (0, 0), 6).astype(np.float32)[..., None] / 255.0 * a
    f = np.clip(wr.astype(np.float32) * msk + q.astype(np.float32) * (1 - msk), 0, 255).astype(np.uint8)
    p.stdin.write(f.tobytes())
    if i % 6 == 0:
        print(f"{t:.2f}s escala {s:.3f} pontos {n} mistura {a:.2f}")
p.stdin.close()
p.wait()
print("feito", saida, len(quadros), "quadros a", fps)
