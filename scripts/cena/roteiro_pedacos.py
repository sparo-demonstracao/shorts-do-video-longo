# -*- coding: utf-8 -*-
"""Transforma o roteiro de frases inteiras no roteiro sem pausas, a partir do pedacos.json.

Entra: o roteiro-base (falas = frases inteiras, com `nomes_falas` e `palavras_falas` já conferidas pelo palavras_falas.py)
       e o pedacos.json do pedacos.py.
Sai:   o roteiro novo (uma fala por pedaço, nomes G1, G2, C11...), as palavras de cada pedaço e os fades dos pedaços
       que cortam rente (frase que emenda na seguinte).

Uso: python roteiro_pedacos.py <roteiro-base.json> <pedacos.json> <roteiro.json>

Uma palavra cujo começo (pela transcrição) caiu dentro de uma pausa cortada vai pro começo do pedaço seguinte da mesma
frase; o programa avisa quais foram. Confira a contagem no fim: toda palavra tem que ter achado um pedaço."""
import json, os, sys
base_p, ped_p, sai_p = sys.argv[1:4]
base = json.load(open(base_p, encoding='utf-8')); ped = json.load(open(ped_p, encoding='utf-8'))
pal_base = json.load(open(os.path.join(os.path.dirname(os.path.abspath(base_p)), base['palavras_falas']), encoding='utf-8'))['falas']
nomes_b = base.get('nomes_falas') or [str(k + 1) for k in range(len(base['falas']))]
ini_b = {n: f[0] for n, f in zip(nomes_b, base['falas'])}
conta, nomes, pal = {}, [], []
for p in ped:
    conta[p['fala']] = conta.get(p['fala'], 0) + 1; nomes.append(p['fala'] + str(conta[p['fala']]))
    ws = []
    for w in pal_base[nomes_b.index(p['fala'])]:
        a = ini_b[p['fala']] + w['i']
        if p['in'] - 0.03 <= a < p['out'] - 0.02:
            ws.append({'p': w['p'], 'i': round(max(0.0, a - p['in']), 3), 'f': round(min(ini_b[p['fala']] + w['f'], p['out']) - p['in'], 3)})
    pal.append(ws)
for fi, f in enumerate(nomes_b):
    for w in pal_base[fi]:
        a = ini_b[f] + w['i']
        if not any(p['fala'] == f and p['in'] - 0.03 <= a < p['out'] - 0.02 for p in ped):
            cand = [(k, p) for k, p in enumerate(ped) if p['fala'] == f and p['in'] >= a - 0.05] or [(k, p) for k, p in enumerate(ped) if p['fala'] == f][-1:]
            if not cand: print('  SEM PEDAÇO:', w['p'], 'da fala', f); continue
            k, p = cand[0]; fim = max(0.12, min(ini_b[f] + w['f'], p['out']) - p['in'])
            pal[k].append({'p': w['p'], 'i': 0.04, 'f': round(fim, 3)}); pal[k].sort(key=lambda x: x['i']); print('  realocada:', w['p'], '->', nomes[k])
print('palavras', sum(len(x) for x in pal), 'de', sum(len(x) for x in pal_base))
pasta = os.path.dirname(os.path.abspath(sai_p)); nome_pal = 'palavras-pedacos.json'
json.dump({'falas': pal}, open(os.path.join(pasta, nome_pal), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
rot = dict(base); rot['falas'] = [[p['in'], p['out']] for p in ped]; rot['nomes_falas'] = nomes
rot['palavras_falas'] = nome_pal
rot['fades'] = {str(k): {'out': p['fade_out']} for k, p in enumerate(ped) if p.get('fade_out')}
json.dump(rot, open(sai_p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f'{len(ped)} falas, {sum(p["n"] for p in ped) / 30:.2f} s ->', sai_p)
