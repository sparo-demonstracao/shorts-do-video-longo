# -*- coding: utf-8 -*-
"""Tira as pausas de dentro das falas sem cortar palavra.

O criador reprovou "silêncios desnecessários" e também "áudio cortado no final": as duas coisas se resolvem cortando pelo
VOLUME, não pela transcrição. Cada fala é partida nos silêncios de 0,25 s ou mais; cada pedaço começa 0,04 s antes do
primeiro som e termina 0,08 s depois do último (a cauda fraca da sílaba final entra). Emendados, os pedaços deixam
~0,12 s entre um e outro. Os começos caem na grade de quadros da fala original, pra os quadros da câmera (e um recorte
já feito) continuarem valendo.

O último pedaço do Short termina `--fim` segundos depois do último som (padrão 0,12): ele pediu pra tirar a pausa do
fim ("remova essa pausa pra ficar perfeito"). Só segure mais que isso se algo na tela precisar do tempo.

Uso: python pedacos.py <falas.json> <pedacos.json> [--vo <gravação da voz>] [--fim 0.12]

falas.json: [{"nome": "G", "in": 1028.19, "out": 1033.09}, ...] na ordem do Short, em tempos da gravação da voz.
  Opcionais por fala: "piso" (dB que separa som de silêncio; padrão -44, use -46 em fala baixa),
  "teto" (instante máximo do último som, quando a frase emenda na seguinte sem silêncio).
Depois: python roteiro_pedacos.py pra virar roteiro."""
import json, sys, numpy as np
import pontas
FPS = 30
args = sys.argv[1:]; fim_short = 0.12
if '--vo' in args:
    k = args.index('--vo'); pontas.usar(args[k + 1]); del args[k:k + 2]
if '--fim' in args:
    k = args.index('--fim'); fim_short = float(args[k + 1]); del args[k:k + 2]
falas = json.load(open(args[0], encoding='utf-8')); saida = []; total = 0
for fi, f in enumerate(falas):
    nome, a, b = f['nome'], f['in'], f['out']
    v = pontas.volume(a, b - a + 0.3); t = a + np.arange(len(v)) * 0.01; som = v > f.get('piso', -44)
    # fecha buracos curtos (< 0,25 s) e descarta estalos isolados (< 0,05 s)
    segs = []; k = 0
    while k < len(som):
        if som[k]:
            j = k
            while j < len(som) and (som[j] or som[j:j + 25].any()): j += 1
            if (j - k) * 0.01 >= 0.05: segs.append([float(t[k]), float(t[j - 1]) + 0.01])
            k = j
        else: k += 1
    segs = [s for s in segs if s[0] < b - 0.05]
    if not segs: raise SystemExit(f'{nome}: não achei som entre {a} e {b} (piso {f.get("piso", -44)} dB)')
    colado = 'teto' in f                                       # a frase emenda na próxima: corta rente, com fade no roteiro
    if colado: segs[-1][1] = min(segs[-1][1], f['teto'])
    for i, (s0, s1) in enumerate(segs):
        ini = s0 - 0.04; m = round((ini - a) * FPS); ini = a + m / FPS            # na grade da fala original
        ultimo = i == len(segs) - 1
        cauda = 0.015 if (colado and ultimo) else (fim_short if (ultimo and fi == len(falas) - 1) else 0.08)
        n = int(np.ceil((s1 + cauda - ini) * FPS - 1e-6))
        saida.append({'fala': nome, 'in': round(ini, 4), 'out': round(ini + n / FPS, 4), 'n': n, 'm': m, 'som': [round(s0, 2), round(s1, 2)],
                      **({'fade_out': 0.03} if (colado and ultimo) else {})})
        total += n
        print(f'{nome:4s} pedaço {i + 1}: som {s0:.2f}-{s1:.2f} -> corte {ini:.4f}-{ini + n / FPS:.4f} ({n} quadros)')
print(f'total {total / FPS:.2f} s em {len(saida)} pedaços')
json.dump(saida, open(args[1], 'w', encoding='utf-8'), indent=1)
