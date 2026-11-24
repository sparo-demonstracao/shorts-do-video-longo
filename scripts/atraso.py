# -*- coding: utf-8 -*-
"""Mede o atraso entre a gravação de referência (voz) e outra gravação, por correlação do áudio.
Uso: python atraso.py <referencia> <outra> <t1> [<t2> ...]
Devolve, pra cada t da referência, o 'atraso' tal que  t_outra = t_ref + atraso.
"""
import subprocess, sys
import numpy as np

SR = 8000
JAN = 40      # segundos da referência
MARGEM = 200  # procura atraso de -MARGEM a +MARGEM

def som(arq, t0, dur):
    t0 = max(0.0, t0)
    r = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t0:.3f}', '-t', f'{dur:.3f}', '-i', arq, '-vn', '-ac', '1',
                        '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(r, np.float32).astype(np.float64)

ref, outra = sys.argv[1], sys.argv[2]
for t in map(float, sys.argv[3:]):
    a = som(ref, t, JAN)
    ini = max(0.0, t - MARGEM)
    b = som(outra, ini, JAN + 2 * MARGEM)
    a = a - a.mean(); b = b - b.mean()
    n = 1 << int(np.ceil(np.log2(len(a) + len(b))))
    c = np.fft.irfft(np.fft.rfft(b, n) * np.conj(np.fft.rfft(a, n)), n)[:len(b)]
    # normaliza pela energia local de b
    cs = np.concatenate([[0.0], np.cumsum(b * b)])
    idx = np.arange(len(b)); fim = np.minimum(idx + len(a), len(b))
    e = np.sqrt((cs[fim] - cs[idx]) * (a * a).sum()) + 1e-9
    c = c / e
    k = int(np.argmax(c[:max(1, len(b) - len(a))]))
    atraso = ini + k / SR - t
    print(f't_ref={t:8.1f}s  atraso={atraso:+9.3f}s  correlação={c[k]:.3f}')
