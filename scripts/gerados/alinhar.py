"""Mede onde o video original (1:1) cai dentro do video vertical gerado (reframe):
escala, posicao e correspondencia de tempo. Uso: python alinhar.py <original> <gerado>"""
import sys
import cv2
import numpy as np

orig, ger = sys.argv[1], sys.argv[2]


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
print(f"original {len(O)} quadros a {fo:.2f} | gerado {len(G)} quadros a {fg:.2f}")

# 1) escala e posicao: quadro do meio, casa o original reduzido dentro do gerado
g = cv2.cvtColor(G[len(G) // 2], cv2.COLOR_BGR2GRAY)
t = len(G) // 2 / fg
o = cv2.cvtColor(O[min(len(O) - 1, round(t * fo))], cv2.COLOR_BGR2GRAY)
melhor = None
for lado in range(640, 761, 4):
    p = cv2.resize(o, (lado, lado), interpolation=cv2.INTER_AREA)
    miolo = p[lado // 6: -lado // 6, lado // 6: -lado // 6]
    r = cv2.matchTemplate(g, miolo, cv2.TM_CCOEFF_NORMED)
    _, v, _, loc = cv2.minMaxLoc(r)
    if melhor is None or v > melhor[0]:
        melhor = (v, lado, loc[0] - lado // 6, loc[1] - lado // 6)
v, lado, x, y = melhor
print(f"encaixe: lado {lado} px em x={x} y={y} (nota {v:.3f})")

# 2) tempo: pra cada quadro gerado, qual quadro original casa melhor (regiao da boca/rosto)
cx0, cy0 = int(lado * 0.3), int(lado * 0.2)
cx1, cy1 = int(lado * 0.7), int(lado * 0.65)
Op = [cv2.resize(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY), (lado, lado), interpolation=cv2.INTER_AREA)[cy0:cy1, cx0:cx1].astype(np.float32) for f in O]
for k in range(0, len(G), 12):
    gg = cv2.cvtColor(G[k], cv2.COLOR_BGR2GRAY)[y + cy0:y + cy1, x + cx0:x + cx1].astype(np.float32)
    if gg.shape != Op[0].shape:
        print("fora do quadro")
        break
    erros = [float(np.mean((gg - a) ** 2)) for a in Op]
    i = int(np.argmin(erros))
    print(f"gerado {k:3d} ({k / fg:5.2f}s) ~ original {i:3d} ({i / fo:5.2f}s)  erro {erros[i]:.0f}  (no mesmo tempo: {erros[min(len(O) - 1, round(k / fg * fo))]:.0f})")
