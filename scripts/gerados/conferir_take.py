# -*- coding: utf-8 -*-
"""Confere um take gerado em que ele fala (câmera 2): a boca foi gerada em cima da fala real?

Compara a curva de volume do som que veio no take com a do áudio real que você mandou de referência, e faz uma folha
de quadros pra olhar o rosto. Você não ouve: é assim que se sabe se o modelo usou a fala de verdade.
  correlação >= 0,7 e atraso de até ~40 ms: o take está no tempo da fala (0,70 e 0,82 nos dois takes aprovados);
  correlação baixa: o modelo inventou outra fala ou esticou o tempo. Não use.

Uso: python conferir_take.py <take.mp4> <audio_real.mp3|wav> <folha.jpg>"""
import subprocess, sys, numpy as np
take, audio, folha = sys.argv[1:4]

def som(f):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-f', 'f32le', '-ac', '1', '-ar', '16000', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.float32)

def env(x):
    k = 320; m = len(x) // k
    return np.sqrt((x[:m * k].reshape(m, k) ** 2).mean(1))

a, b = env(som(audio)), env(som(take))
if len(b) < 10: sys.exit('o take veio sem som: gere com generate_audio ligado e o áudio real em audio_references')
m = min(len(a), len(b)); a, b = a[:m] - a[:m].mean(), b[:m] - b[:m].mean()
best = max(((float(np.dot(a[max(0, l):m + min(0, l)], b[max(0, -l):m - max(0, l)]) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9)), l)
            for l in range(-25, 26)), key=lambda t: t[0])
print(f'som: correlação {best[0]:.3f}, atraso {best[1] * 20} ms')
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', take, '-vf', 'fps=3,scale=270:-1,tile=8x2', '-frames:v', '1', folha])
print('folha', folha)
