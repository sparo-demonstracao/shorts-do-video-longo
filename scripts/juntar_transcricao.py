# -*- coding: utf-8 -*-
"""Junta transcrições feitas em partes com sobreposição (transcrever.py --inicio/--fim) numa só.
Uso: python juntar.py <saida.json> <arquivo-original> <parte1.json> <parte2.json> ...
Cada parte cobre [inicio_k, fim_k]; a fronteira entre duas partes é o meio da sobreposição,
deslocada pro silêncio mais próximo (pra não partir palavra)."""
import json, os, re, sys

saida, original, partes = sys.argv[1], sys.argv[2], sys.argv[3:]
ds = [json.load(open(p, encoding='utf-8')) for p in partes]
# limites de cada parte = primeira/última palavra ou silêncio
lim = []
for d in ds:
    ts = [w['i'] for w in d['palavras']] + [s[0] for s in d['silencios']]
    te = [w['f'] for w in d['palavras']] + [s[1] for s in d['silencios']]
    lim.append((min(ts), max(te)))
pal, sil, corte_ant = [], [], -1.0
for k, d in enumerate(ds):
    if k + 1 < len(ds):
        a, b = lim[k + 1][0], lim[k][1]          # sobreposição [a, b]
        meio = (a + b) / 2
        # procura uma pausa entre palavras perto do meio (na parte k)
        ws = [w for w in d['palavras'] if a <= w['i'] <= b]
        melhor, corte = -1, meio
        for x, y in zip(ws, ws[1:]):
            vao = y['i'] - x['f']
            if vao > melhor and abs((x['f'] + y['i']) / 2 - meio) < (b - a) / 2 - 1:
                melhor, corte = vao, (x['f'] + y['i']) / 2
    else:
        corte = 1e12
    pal += [w for w in d['palavras'] if corte_ant <= (w['i'] + w['f']) / 2 < corte]
    sil += [s for s in d['silencios'] if corte_ant <= (s[0] + s[1]) / 2 < corte]
    print(f'parte {k + 1}: de {max(corte_ant, 0):.2f} até {min(corte, lim[k][1]):.2f}')
    corte_ant = corte
dur = max(lim[-1][1], pal[-1]['f'])
json.dump({'arquivo': os.path.abspath(original), 'duracao': round(dur, 2), 'palavras': pal, 'silencios': sil},
          open(saida, 'w', encoding='utf-8'), ensure_ascii=False)
linhas, atual, t0 = [], [], None
for w in pal:
    if t0 is None:
        t0 = w['i']
    atual.append(w['p'])
    if w['f'] - t0 > 12 and re.search(r'[.!?]$', w['p']) or w['f'] - t0 > 20:
        linhas.append(f'[{int(t0 // 60):02d}:{int(t0 % 60):02d}] ' + ' '.join(atual)); atual, t0 = [], None
if atual:
    linhas.append(f'[{int(t0 // 60):02d}:{int(t0 % 60):02d}] ' + ' '.join(atual))
open(os.path.splitext(saida)[0] + '.txt', 'w', encoding='utf-8').write('\n'.join(linhas))
print(f'{len(pal)} palavras, {len(linhas)} linhas -> {saida}')
