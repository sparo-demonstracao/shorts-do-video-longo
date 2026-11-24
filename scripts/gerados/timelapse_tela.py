"""Motion do time-lapse no formato da tela do PC (1920x1080, 30 q/s): o pedido real no Claude Code e, em seguida,
o clone real se montando painel por painel, com um relogio correndo. Tudo sai de capturas reais da gravacao de tela:
nada de texto ou codigo inventado.
  python timelapse_tela.py <pedido.jpg> <clone.jpg> <pasta_saida> [quadros=50]"""
import os
import sys

import cv2
import numpy as np

pedido, clone, saida = sys.argv[1:4]
N = int(sys.argv[4]) if len(sys.argv) > 4 else 50
W, H, FPS = 1920, 1080, 30
K = W / 2560
LAR = np.array([24, 107, 255], np.float32)   # laranja em BGR

P = cv2.imread(pedido).astype(np.float32)
C = cv2.resize(cv2.imread(clone), (W, H), interpolation=cv2.INTER_AREA).astype(np.float32)
fundo_cor = C[int(700 * K):int(760 * K), int(120 * K):int(380 * K)].reshape(-1, 3).mean(0)   # cor da coluna de canais, vazia

# paineis do clone, em pixels da captura 2560x1440: (x, y, w, h, instante em que entra)
PAINEIS = [
    (0, 0, 90, 1440, 0.26), (90, 0, 320, 58, 0.33), (90, 58, 320, 262, 0.40), (90, 320, 320, 902, 0.45),
    (90, 1222, 320, 128, 0.54), (90, 1350, 320, 90, 0.61), (410, 0, 2150, 70, 0.69),
    (433, 394, 1045, 589, 0.80), (1494, 394, 1043, 589, 0.95), (1244, 1329, 481, 89, 1.08),
]
T_PED, T_FIM = 0.22, 1.28   # ate T_PED: o pedido; ate T_FIM: montagem; depois: o clone inteiro

sm = lambda x: float(np.clip(x, 0, 1)) ** 2 * (3 - 2 * float(np.clip(x, 0, 1)))
fora = lambda x: 1 - (1 - float(np.clip(x, 0, 1))) ** 3


def quadro_pedido(t):
    """a captura real do pedido, com a camera chegando perto da mensagem"""
    z = (W / 2560) * (1.0 + 0.55 * fora(t / T_PED))
    cx, cy = 1720, 285 + 240 * (1 - fora(t / T_PED))
    M = np.float32([[z, 0, W / 2 - cx * z], [0, z, H * 0.42 - cy * z]])
    return cv2.warpAffine(P, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)


def quadro_montagem(t):
    q = np.empty((H, W, 3), np.float32); q[:] = fundo_cor * 0.55
    # grade leve no fundo (tela "em obras")
    q[::54, :] += 6; q[:, ::54] += 6
    for (x, y, w, h, t0) in PAINEIS:
        dt = t - t0
        if dt < 0:
            continue
        x0, y0, x1, y1 = [int(round(v * K)) for v in (x, y, x + w, y + h)]
        e = fora(dt / 0.16); s = 0.86 + 0.14 * e
        pw, ph = max(2, int((x1 - x0) * s)), max(2, int((y1 - y0) * s))
        rec = cv2.resize(C[y0:y1, x0:x1], (pw, ph), interpolation=cv2.INTER_AREA)
        ox, oy = x0 + ((x1 - x0) - pw) // 2, y0 + ((y1 - y0) - ph) // 2
        a = sm(dt / 0.07)
        q[oy:oy + ph, ox:ox + pw] = q[oy:oy + ph, ox:ox + pw] * (1 - a) + rec * a
        brilho = 1 - sm(dt / 0.30)                                   # contorno laranja que acende e apaga
        if brilho > 0.01:
            cam = np.zeros((H, W, 3), np.float32)
            cv2.rectangle(cam, (ox, oy), (ox + pw - 1, oy + ph - 1), (1, 1, 1), 7, cv2.LINE_AA)
            cam = cv2.GaussianBlur(cam, (0, 0), 2.2)
            q = q * (1 - cam * brilho) + LAR * cam * brilho
    return q


def relogio(q, t):
    """anel que enche e ponteiro girando: o tempo correndo"""
    p = sm((t - T_PED) / (T_FIM - T_PED)); fim = sm((t - T_FIM) / 0.12)
    some = 1 - sm((t - T_FIM - 0.14) / 0.18)
    if t < T_PED or some <= 0.01:
        return q
    cx, cy, R = 1010, 172, int(80 * (1 + 0.18 * fim * (1 - fim) * 4))   # no alto, ao centro: a cabeca dele cobre o lado direito da tela
    cam = np.zeros((H, W, 3), np.float32); base = np.zeros((H, W), np.float32)
    cv2.circle(base, (cx, cy), R + 26, 1.0, -1, cv2.LINE_AA)
    cv2.circle(cam, (cx, cy), R, (0.35, 0.35, 0.35), 14, cv2.LINE_AA)
    cv2.ellipse(cam, (cx, cy), (R, R), -90, 0, 360 * p, (1, 1, 1), 14, cv2.LINE_AA)
    ang = np.deg2rad(-90 + 360 * 3 * p)
    cv2.line(cam, (cx, cy), (int(cx + np.cos(ang) * R * 0.62), int(cy + np.sin(ang) * R * 0.62)), (1, 1, 1), 10, cv2.LINE_AA)
    cv2.circle(cam, (cx, cy), 9, (1, 1, 1), -1, cv2.LINE_AA)
    q = q * (1 - base[..., None] * 0.72 * some)                        # disco escuro atras, pra ler em qualquer fundo
    cinza = (cam[..., 0] < 0.5) & (cam[..., 0] > 0.02)
    cor = np.where(cinza[..., None], np.float32([150, 150, 150]), LAR)
    return q * (1 - cam * some) + cor * cam * some


os.makedirs(saida, exist_ok=True)
for f in os.listdir(saida):
    if f.endswith(".jpg"):
        os.remove(os.path.join(saida, f))
dur = N / FPS
for n in range(N):
    t = n / FPS
    if t < T_PED:
        q = quadro_pedido(t)
    else:
        q = quadro_montagem(t)
        corte = 1 - sm((t - T_PED) / 0.10)                             # o pedido some rapido por baixo do primeiro painel
        if corte > 0.01:
            q = q * (1 - corte) + quadro_pedido(T_PED) * corte * 0.9
        fim = sm((t - T_FIM) / 0.10)
        if fim > 0:
            z = 1 + 0.018 * (t - T_FIM) / max(1e-6, dur - T_FIM)
            M = np.float32([[z, 0, W / 2 * (1 - z)], [0, z, H / 2 * (1 - z)]])
            inteiro = cv2.warpAffine(C, M, (W, H), flags=cv2.INTER_LINEAR)
            q = q * (1 - fim) + inteiro * fim
            clarao = (1 - sm((t - T_FIM) / 0.22)) * 0.35
            q = q + 255 * clarao
    q = relogio(q, t)
    # barra de progresso no pe da tela
    p = sm((t - T_PED) / (T_FIM - T_PED)); some = 1 - sm((t - T_FIM - 0.05) / 0.15)
    if t >= T_PED and some > 0.01:
        q[H - 16:H, :int(W * p)] = q[H - 16:H, :int(W * p)] * (1 - some) + LAR * some
    cv2.imwrite(os.path.join(saida, f"{n + 1:05d}.jpg"), np.clip(q, 0, 255).astype(np.uint8), [cv2.IMWRITE_JPEG_QUALITY, 95])
print(f"feito: {N} quadros ({dur:.2f} s) em {saida}")
