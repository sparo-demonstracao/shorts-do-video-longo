# -*- coding: utf-8 -*-
"""Prepara a pasta de uma CENA: o Short inteiro como uma única animação (motion.html), com ele e as telas
reais tocando dentro dela.

Uso:  python preparar_cena.py <short-XX/roteiro.json> [--so-dados]

Lê o roteiro (as falas, na ordem, em tempos do VO.wav, e os trechos de tela que a cena usa) e escreve em
<short-XX>/cena/:
  quadros/cam/00001.jpg ...      ele, quadro a quadro, já na ordem do Short (uma fala emendada na outra)
  quadros/<tela>/00001.jpg ...   cada trecho de tela, já recortado e na velocidade pedida
  dados.js                       duração, contagem de quadros, onde cada fala entra e as palavras da legenda
  motion.json, kit.js            o que o motion.py precisa pra fotografar (olhar) e renderizar (render)
"""
import json, os, shutil, subprocess, sys

FPS = 30
AQUI = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(os.path.dirname(AQUI))                       # .../shorts-do-video-longo
KIT = os.path.join(SKILL, 'assets', 'motion', 'kit.js')
PALCO = os.path.join(SKILL, 'assets', 'cena')

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, errors='replace')
    if r.returncode:
        sys.stderr.write((r.stderr or '')[-2000:] + '\n'); raise SystemExit('ffmpeg falhou')

def atraso_em(f, t):
    # "imagem_atras": o celular grava a imagem um pouco atrasada em relação ao próprio som, e a diferença cresce ao longo
    # da gravação (relógios diferentes pro som e pra imagem). Medido pela boca (medir a abertura dos lábios nos estalos).
    ia = f.get('imagem_atras'); extra = ia['base'] + ia['por_segundo'] * (t - ia['desde']) if ia else 0.0
    return _atraso_som(f, t) + extra

def _atraso_som(f, t):
    a = f.get('atraso', 0)
    if not isinstance(a, list):
        return a
    pts = sorted(a)
    if t <= pts[0][0]:
        return pts[0][1]
    for (t0, a0), (t1, a1) in zip(pts, pts[1:]):
        if t <= t1:
            return a0 + (a1 - a0) * (t - t0) / max(1e-9, t1 - t0)
    return pts[-1][1]

rot_p = os.path.abspath(sys.argv[1]); so_dados = '--so-dados' in sys.argv
base = os.path.dirname(rot_p); rot = json.load(open(rot_p, encoding='utf-8'))
fontes = rot['fontes']; cena = os.path.join(base, rot.get('pasta', 'cena')); qd = os.path.join(cena, 'quadros')
os.makedirs(qd, exist_ok=True)

# ---------- as falas: onde cada uma entra no Short ----------
# "abertura": trecho inicial sem fala do VO (por exemplo uma fala gerada por cima da tela). Dura um número inteiro de
# quadros, não tem câmera, e as palavras dela (já no tempo do Short) vêm no próprio roteiro.
ab = rot.get('abertura') or {}; n_ab = int(ab.get('quadros', 0))
falas, t0, k0 = [], n_ab / FPS, 1
for vin, vout in rot['falas']:
    n = round((vout - vin) * FPS)
    falas.append({'in': vin, 'out': vout, 't0': round(t0, 4), 'n': n, 'k0': k0}); t0 += n / FPS; k0 += n
total_n = k0 - 1; dur = (total_n + n_ab) / FPS

# ---------- ele ----------
cam = fontes['cam']; lw = rot.get('cam', {}).get('largura', 1920)
if not so_dados:
    shutil.rmtree(os.path.join(qd, 'cam'), ignore_errors=True); os.makedirs(os.path.join(qd, 'cam'))
    for f in falas:
        run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{f["in"] + atraso_em(cam, f["in"]):.3f}', '-t', f'{f["n"] / FPS + 0.3:.3f}',
             '-i', cam['arquivo'], '-vf', f'fps={FPS},scale={lw}:-2', '-frames:v', str(f['n']), '-q:v', '3',
             '-start_number', str(f['k0']), os.path.join(qd, 'cam', '%05d.jpg')])
        print(f'  cam: fala {f["in"]:.2f}-{f["out"]:.2f} -> quadros {f["k0"]} a {f["k0"] + f["n"] - 1}', flush=True)
quadros = {'cam': total_n}

# ---------- as telas ----------
tela = fontes['tela']
for nome, c in rot.get('telas', {}).items():
    n = round(c['dur'] * FPS); vel = c.get('vel', 1.0); larg = c.get('largura', 1280)
    reg = c.get('regiao'); rg = f'crop={reg[2]}:{reg[3]}:{reg[0]}:{reg[1]},' if reg else ''
    acel = f'setpts=PTS/{vel},' if vel != 1.0 else ''
    if not so_dados:
        shutil.rmtree(os.path.join(qd, nome), ignore_errors=True); os.makedirs(os.path.join(qd, nome))
        run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{c["in"] + atraso_em(tela, c["in"]):.3f}', '-t', f'{(c["dur"] + 0.3) * vel:.3f}',
             '-i', tela['arquivo'], '-vf', f'{acel}{rg}fps={FPS},scale={larg}:-2', '-frames:v', str(n), '-q:v', '3',
             os.path.join(qd, nome, '%05d.jpg')])
        print(f'  tela "{nome}": {n} quadros', flush=True)
    quadros[nome] = len(os.listdir(os.path.join(qd, nome))) if os.path.isdir(os.path.join(qd, nome)) else n

# ---------- as palavras da legenda, já no tempo do Short ----------
pal_src = json.load(open(os.path.normpath(os.path.join(base, rot['palavras'])), encoding='utf-8'))['palavras']
palavras = [dict(w) for w in ab.get('palavras', [])]
# "palavras_falas": arquivo com as palavras de cada fala já conferidas (tempos contados do começo da fala), na ordem das
# falas. Serve quando os cortes são apertados e a transcrição do vídeo inteiro erra a borda das palavras.
pf = rot.get('palavras_falas')
pf = json.load(open(os.path.normpath(os.path.join(base, pf)), encoding='utf-8'))['falas'] if pf else None
for k, f in enumerate(falas):
    if pf:
        for w in pf[k]:
            palavras.append({'p': w['p'], 'i': round(f['t0'] + w['i'], 3), 'f': round(f['t0'] + min(w['f'], f['n'] / FPS), 3)})
        continue
    for w in pal_src:
        if f['in'] - 0.03 <= w['i'] < f['out'] - 0.02:
            palavras.append({'p': w['p'], 'i': round(f['t0'] + w['i'] - f['in'], 3), 'f': round(f['t0'] + min(w['f'], f['out']) - f['in'], 3)})

# sequências que outros programas puseram em quadros/ (recorte dele, segunda câmera...): conta pelo maior número
for nome in sorted(os.listdir(qd)):
    if nome not in quadros and os.path.isdir(os.path.join(qd, nome)):
        nums = [int(os.path.splitext(x)[0]) for x in os.listdir(os.path.join(qd, nome)) if os.path.splitext(x)[0].isdigit()]
        if nums:
            quadros[nome] = max(nums)

dados = {'id': rot.get('id', 'cena'), 'dur': round(dur, 4), 'fps': FPS, 'quadros': quadros, 'abertura': round(n_ab / FPS, 4),
         'falas': [{'t0': f['t0'], 'in': f['in'], 'out': f['out'], 'n': f['n'], 'k0': f['k0']} for f in falas], 'palavras': palavras}
open(os.path.join(cena, 'dados.js'), 'w', encoding='utf-8').write(
    '// gerado pelo preparar_cena.py: não edite à mão\nwindow.MOTION_DADOS = ' + json.dumps(dados, ensure_ascii=False) + ';\n')
json.dump({'id': rot.get('id', 'cena'), 'cena': True}, open(os.path.join(cena, 'motion.json'), 'w', encoding='utf-8'))
shutil.copy(KIT, os.path.join(cena, 'kit.js'))
# palco.js e palco.css (peças comuns de toda cena) moram em <vídeo>/comum; o motion.html os chama por ../../comum/
comum = os.path.normpath(os.path.join(base, '..', 'comum')); os.makedirs(comum, exist_ok=True)
for nome in ('palco.js', 'palco.css'):
    if not os.path.exists(os.path.join(comum, nome)):
        shutil.copy(os.path.join(PALCO, nome), os.path.join(comum, nome))
print(f'cena pronta em {cena}: {dur:.2f} s, {total_n} quadros dele, telas: ' + ', '.join(f'{k} ({v})' for k, v in quadros.items() if k != 'cam'))
print('falas entram em: ' + ' | '.join(f'{f["t0"]:.2f}' for f in falas))
