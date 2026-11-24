# -*- coding: utf-8 -*-
"""Escreve o plano.json de um Short em cena única, a partir do roteiro.json.

O vídeo é a cena renderizada (cena/cena.mp4); cada fala do roteiro vira um bloco que corta o pedaço certo da cena e
põe por baixo o trecho certo da gravação da voz. Assim o compor.py junta imagem e voz, mistura a trilha e a pista de
efeitos da cena, nivela o volume e confere a sincronia ("sincronia conferida ... maior desvio 0 ms").

Uso: python plano_da_cena.py <short-XX/roteiro.json> [--saida saida/short-01-v1.mp4] [--trilha ../material/audio/trilha-ia.mp3] [--volume 0.1] [--nota "..."]

Se o plano.json já existe, só os blocos são refeitos: `saida`, `trilha` e `nota` ficam como estavam, a não ser que
você passe os de cima. Rode de novo sempre que o roteiro mudar (por exemplo, ao encurtar o fim)."""
import json, os, sys
FPS = 30
args = sys.argv[1:]; op = {}
for nome in ('--saida', '--trilha', '--volume', '--nota'):
    if nome in args:
        k = args.index(nome); op[nome[2:]] = args[k + 1]; del args[k:k + 2]
rot_p = os.path.abspath(args[0]); pasta = os.path.dirname(rot_p); rot = json.load(open(rot_p, encoding='utf-8'))
plano_p = os.path.join(pasta, 'plano.json')
plano = json.load(open(plano_p, encoding='utf-8')) if os.path.exists(plano_p) else {}
nomes = rot.get('nomes_falas') or [f'f{k + 1}' for k in range(len(rot['falas']))]; fades = rot.get('fades', {})
blocos, n0 = [], 0
for k, (vin, vout) in enumerate(rot['falas']):
    n = round((vout - vin) * FPS)
    b = {'id': nomes[k].lower(), 'tipo': 'motion', 'arquivo': 'cena/cena.mp4', 'audio': {'in': vin, 'out': vout}, 'legenda': False}
    if n0: b['in'] = round(n0 / FPS - 0.012, 4)               # um tiquinho antes do quadro, pra busca cair exatamente nele
    if k == 0: b['som'] = 'cena/cena-sfx.wav'; b['som_volume'] = 1.0   # a pista de efeitos da cena inteira entra no começo
    f = fades.get(str(k), {})
    if 'in' in f: b['fade_in'] = f['in']
    if 'out' in f: b['fade_out'] = f['out']
    g = rot.get('ganho_db', {}).get(str(k))
    if g: b['ganho_db'] = g                                   # tomada mais alta que as outras (ver plano.md)
    if k == len(rot['falas']) - 1 and 'fade_out' not in b: b['fade_out'] = 0.06     # o Short acaba na última palavra, sem estalo
    blocos.append(b); n0 += n
plano.setdefault('saida', 'saida/' + os.path.basename(pasta) + '-v1.mp4')
plano['fontes'] = rot['fontes']; plano['legendas'] = {'ligado': False}; plano.setdefault('fade_fala', 0.012)
if 'saida' in op: plano['saida'] = op['saida']
if 'trilha' in op or 'volume' in op:
    tr = plano.get('trilha', {}); tr['arquivo'] = op.get('trilha', tr.get('arquivo')); tr['volume'] = float(op.get('volume', tr.get('volume', 0.1))); plano['trilha'] = tr
if 'nota' in op: plano['nota'] = op['nota']
plano['blocos'] = blocos
ordem = ['saida', 'nota', 'fontes', 'legendas', 'fade_fala', 'trilha', 'blocos']
plano = {k: plano[k] for k in ordem if k in plano} | {k: v for k, v in plano.items() if k not in ordem}
json.dump(plano, open(plano_p, 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
print(f'{plano_p}: {len(blocos)} blocos, {n0 / FPS:.2f} s -> {plano["saida"]}' + ('' if plano.get('trilha') else '  (sem trilha: passe --trilha)'))
