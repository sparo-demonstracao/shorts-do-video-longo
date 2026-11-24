# -*- coding: utf-8 -*-
"""Confere, sem ouvir, se alguma fala do roteiro começa ou termina em cima de som (palavra cortada).
Pra cada fala mostra o volume logo dentro (30 ms no começo, 80 ms no fim) e nos 120 ms de fora de cada ponta. Ponta boa: silêncio (abaixo
de -45 dB) dos dois lados. Ponta em cima de som só passa se o roteiro tiver um fade ali (corte no meio da frase).
Uso: python conferir_pontas.py <short-XX/roteiro.json>"""
import json, sys
import pontas
from pontas import volume
rot = json.load(open(sys.argv[1], encoding='utf-8')); pontas.usar((rot['fontes'].get('audio') or rot['fontes']['cam'])['arquivo']); fades = rot.get('fades', {}); ruim = 0
for k, (a, b) in enumerate(rot['falas']):
    nome = rot.get('nomes_falas', [str(i) for i in range(99)])[k]
    ini_dentro = volume(a, 0.03).max(); ini_fora = volume(a - 0.12, 0.12).max()
    fim_dentro = volume(b - 0.08, 0.08).max(); fim_fora = volume(b, 0.12).max()
    f = fades.get(str(k), {})
    obs = []
    if ini_dentro > -45 and 'in' not in f: obs.append('COMEÇA EM CIMA DE SOM'); ruim += 1
    if fim_dentro > -45 and 'out' not in f: obs.append('TERMINA EM CIMA DE SOM'); ruim += 1
    if 'in' in f: obs.append(f'começo com fade de {f["in"]} s (corte no meio da frase)')
    if 'out' in f: obs.append(f'fim com fade de {f["out"]} s')
    print(f'{nome:3s} {a:.2f}-{b:.2f}  começo: fora {ini_fora:5.0f} dB, dentro {ini_dentro:5.0f} dB | fim: dentro {fim_dentro:5.0f} dB, fora {fim_fora:5.0f} dB  {"; ".join(obs)}')
print('pontas conferidas: nenhuma palavra cortada' if not ruim else f'{ruim} ponta(s) em cima de som: ajuste o roteiro')
