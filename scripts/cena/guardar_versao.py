# -*- coding: utf-8 -*-
"""Guarda uma versão do Short antes de mexer nele: <short>/_versao-N/ com a cena, o roteiro, o plano e o vídeo.

O criador compara versões e às vezes volta pra uma anterior ("preferi a versão antiga, vou continuar com ela"). Nenhuma
versão mostrada a ele pode ser sobrescrita: rode isto antes de cada rodada de ajuste.

Uso: python guardar_versao.py <short-XX> <N>"""
import glob, json, os, shutil, sys
short, n = sys.argv[1], sys.argv[2]; dest = os.path.join(short, f'_versao-{n}')
if os.path.exists(dest): sys.exit(f'{dest} já existe: escolha outro número (nunca sobrescreva uma versão guardada)')
os.makedirs(dest)
itens = [os.path.join(short, 'plano.json'), os.path.join(short, 'roteiro.json')] + glob.glob(os.path.join(short, 'palavras*.json'))
itens += [os.path.join(short, 'cena', x) for x in ('motion.html', 'variante.js', 'dados.js')]
try:
    itens.append(os.path.join(short, json.load(open(os.path.join(short, 'plano.json'), encoding='utf-8'))['saida']))
except Exception:
    pass
for p in itens:
    if os.path.exists(p): shutil.copy2(p, dest); print('  guardado', os.path.basename(p))
print('versão', n, 'em', dest)
