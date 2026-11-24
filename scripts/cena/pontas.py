# -*- coding: utf-8 -*-
"""Acha as pontas certas de um trecho de fala na gravação da voz, pra nenhuma palavra sair cortada.
Pra cada trecho aproximado (t0 t1) mostra: onde a fala começa de verdade, onde o último som termina (a sílaba final
fraca costuma continuar 0,2 s depois do que a transcrição diz), o corte sugerido (0,07 s antes e 0,15 s depois, em
quadros inteiros) e as pausas de dentro do trecho.

Uso: python pontas.py [--vo <gravação da voz>] t0 t1 [t0 t1 ...]      (também importável: pontas(t0, t1), volume(t0, d))

De onde vem a gravação da voz, nesta ordem: `--vo`, a variável de ambiente SHORTS_VO, ou o `fontes.json` da pasta em
que você está (`audio.arquivo`; sem áudio separado, `cam.arquivo`). Quem importa pode chamar `usar(arquivo)`."""
import json, os, subprocess, sys, numpy as np
VO = None
FPS = 30

def usar(arquivo):
    global VO
    VO = arquivo

def _vo():
    if VO: return VO
    if os.environ.get('SHORTS_VO'): return os.environ['SHORTS_VO']
    if os.path.exists('fontes.json'):
        f = json.load(open('fontes.json', encoding='utf-8'))
        for chave in ('audio', 'cam'):
            if isinstance(f.get(chave), dict) and f[chave].get('arquivo'): return f[chave]['arquivo']
    raise SystemExit('pontas.py: não sei qual é a gravação da voz. Passe --vo <arquivo>, defina SHORTS_VO ou rode da pasta do vídeo (fontes.json).')

def volume(t0, d, passo=0.01):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t0:.3f}', '-t', f'{d:.3f}', '-i', _vo(), '-ac', '1', '-ar', '16000', '-f', 'f32le', '-'],
                         capture_output=True).stdout
    x = np.frombuffer(raw, np.float32).astype(np.float64); n = int(16000 * passo)
    return np.array([20 * np.log10(max(1e-6, np.sqrt(np.mean(x[k:k + n] ** 2)))) for k in range(0, len(x) - n + 1, n)])

def pontas(t0, t1, antes=0.07, depois=0.15, piso=-50.0, fixo_ini=False):
    a = t0 - 0.5; v = volume(a, t1 - t0 + 1.3); t = a + np.arange(len(v)) * 0.01
    fala = v > piso
    # começo: primeiro instante com som a partir de t0-0.25; fim: último instante com som até t1+0.5 seguido de 0,12 s de silêncio
    i0 = next(k for k in range(len(v)) if t[k] >= t0 - 0.25 and fala[k] and fala[k:k + 3].all())
    i1 = max(k for k in range(len(v)) if t[k] <= t1 + 0.1 and fala[k])
    while True:   # estende enquanto o som volta em menos de 0,12 s (cauda fraca da última sílaba)
        prox = [k for k in range(i1 + 1, min(len(v), i1 + 13)) if fala[k]]
        if not prox or t[prox[-1]] > t1 + 0.6: break
        i1 = prox[-1]
    ini = t0 if fixo_ini else t[i0] - antes
    fim = t[i1] + 0.01 + depois
    n = int(np.ceil((fim - ini) * FPS - 1e-6)); fim = ini + n / FPS
    pausas, k = [], i0
    while k < i1:
        if not fala[k]:
            j = k
            while j < i1 and not fala[j]: j += 1
            if (j - k) * 0.01 >= 0.25: pausas.append((round(float(t[k]), 2), round((j - k) * 0.01, 2)))
            k = j
        else: k += 1
    return {'in': round(float(ini), 4), 'out': round(float(fim), 4), 'n': n, 'fala_de': round(float(t[i0]), 2), 'fala_ate': round(float(t[i1]) + 0.01, 2), 'pausas': pausas}

if __name__ == '__main__':
    args = sys.argv[1:]
    if '--vo' in args:
        k = args.index('--vo'); usar(args[k + 1]); del args[k:k + 2]
    a = [float(x) for x in args]
    for t0, t1 in zip(a[::2], a[1::2]):
        p = pontas(t0, t1)
        print(f"{t0:.2f}-{t1:.2f}: fala de {p['fala_de']:.2f} a {p['fala_ate']:.2f} -> corte {p['in']:.4f} a {p['out']:.4f} ({p['n']} quadros, {p['n']/FPS:.2f} s); pausas (início, tamanho): {p['pausas']}")
