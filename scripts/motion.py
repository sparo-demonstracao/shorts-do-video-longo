# -*- coding: utf-8 -*-
"""Cria e renderiza um motion (animação feita em HTML, quadro a quadro) pra um Short. Não gasta crédito.

Uso:
  python motion.py novo   <plano.json> <id> --in 95.2 --out 101.6 [--regiao x,y,l,a] [--foco 0.5] [--sem-cam]
        cria motions/<id>/ ao lado do plano: motion.html (ponto de partida em branco), kit.js, dados.js e os
        quadros das gravações reais daquele trecho (quadros/tela, quadros/cam)
  python motion.py quadros <pasta-do-motion>            refaz os quadros (mudou in/out/regiao no motion.json)
  python motion.py olhar  <pasta-do-motion> 0.4 1.2 2.5 ...   fotografa esses instantes e junta numa folha
  python motion.py render <pasta-do-motion>             renderiza <id>.mp4 (1080x1920, 30 fps) e <id>-sfx.wav
  python motion.py som    <pasta-do-motion>             refaz só o <id>-sfx.wav (mudou um Motion.sfx, a imagem continua a mesma)

O motion.html é escrito à mão pra cada momento (veja references/motions.md). A página expõe Motion.ir(t);
este programa chama pra cada quadro e fotografa com o Edge sem janela, então o resultado é sempre o mesmo.
"""
import argparse, json, os, shutil, subprocess, sys, wave

import numpy as np

W, H, FPS = 1080, 1920, 30
AQUI = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(os.path.dirname(AQUI), 'assets', 'motion')

def run(cmd, **k):
    r = subprocess.run(cmd, capture_output=True, text=True, errors='replace', **k)
    if r.returncode:
        sys.stderr.write((r.stderr or '')[-2500:] + '\n'); raise SystemExit('ffmpeg falhou')
    return r

def dims(arq):
    r = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height',
                        '-of', 'csv=p=0', arq], capture_output=True, text=True)
    w, h = r.stdout.strip().split(',')[:2]
    return int(w), int(h)

def par(x):
    return int(round(x / 2) * 2)

def atraso_em(f, t):
    """atraso da fonte no instante t da fala: número fixo, ou tabela [[t, atraso], ...] interpolada.
    "imagem_atras" {"base", "por_segundo", "desde"} soma o quanto a IMAGEM da câmera vem atrás do próprio som (ver boca.py)."""
    ia = f.get('imagem_atras')
    return _atraso_som(f, t) + (ia['base'] + ia['por_segundo'] * (t - ia['desde']) if ia else 0.0)

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

def caixa(f):
    c = f.get('caixa')
    return f'crop={c[2]}:{c[3]}:{c[0]}:{c[1]},' if c else ''

# ---------- quadros das gravações reais ----------
def extrair(pasta):
    cfg = json.load(open(os.path.join(pasta, 'motion.json'), encoding='utf-8'))
    plano_p = os.path.normpath(os.path.join(pasta, cfg['plano']))
    plano = json.load(open(plano_p, encoding='utf-8-sig')); base = os.path.dirname(plano_p)
    p = lambda rel: rel if os.path.isabs(rel) else os.path.normpath(os.path.join(base, rel))
    dur = cfg['out'] - cfg['in']; n = round(dur * FPS)
    tela = plano['fontes'][cfg.get('fonte_tela', 'tela')]
    reg = cfg.get('regiao')
    if reg:
        tw, th = reg[2], reg[3]
    elif tela.get('caixa'):
        tw, th = tela['caixa'][2], tela['caixa'][3]
    else:
        tw, th = dims(p(tela['arquivo']))
    hs = min(par(W * th / tw), 1100)
    qd = os.path.join(pasta, 'quadros')
    shutil.rmtree(qd, ignore_errors=True)
    os.makedirs(os.path.join(qd, 'tela'))
    rg = f'crop={reg[2]}:{reg[3]}:{reg[0]}:{reg[1]},' if reg else ''
    # tela_in / tela_vel no motion.json: a tela vem de outro instante da gravação e pode tocar acelerada
    t_tela = cfg.get('tela_in', cfg['in']); vel = cfg.get('tela_vel', 1.0)
    acel = f'setpts=PTS/{vel},' if vel != 1.0 else ''
    run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t_tela + atraso_em(tela, t_tela):.3f}', '-t', f'{(dur + 0.2) * vel:.3f}',
         '-i', p(tela['arquivo']), '-vf', f'{acel}{caixa(tela)}{rg}scale={W}:{par(W * th / tw)},fps={FPS}',
         '-frames:v', str(n), '-q:v', '2', os.path.join(qd, 'tela', '%05d.jpg')])
    dados = {'id': cfg['id'], 'dur': round(n / FPS, 4), 'fps': FPS, 'hs': hs, 'quadros': {'tela': n},
             'tela': {'w': W, 'h': par(W * th / tw)}}
    if not cfg.get('sem_cam'):
        cam = plano['fontes']['cam']; ch = cfg.get('cam_altura', H - hs); fx = cfg.get('foco', 0.5)
        os.makedirs(os.path.join(qd, 'cam'))
        run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{cfg["in"] + atraso_em(cam, cfg["in"]):.3f}', '-t', f'{dur + 0.2:.3f}',
             '-i', p(cam['arquivo']), '-vf',
             f"{caixa(cam)}scale={W}:{ch}:force_original_aspect_ratio=increase,crop={W}:{ch}:(iw-{W})*{fx}:(ih-{ch})*0.5,fps={FPS}",
             '-frames:v', str(n), '-q:v', '2', os.path.join(qd, 'cam', '%05d.jpg')])
        dados['quadros']['cam'] = n; dados['cam'] = {'w': W, 'h': ch}
    for nome in list(dados['quadros']):
        tem = len(os.listdir(os.path.join(qd, nome)))
        if tem < n:   # a gravação acabou antes do fim pedido: o último quadro fica congelado
            print(f'AVISO: a gravação "{nome}" só tem {tem} dos {n} quadros desse trecho (in/out passa do fim do arquivo?)')
            dados['quadros'][nome] = max(tem, 1)
    open(os.path.join(pasta, 'dados.js'), 'w', encoding='utf-8').write(
        '// gerado pelo motion.py: não edite à mão\nwindow.MOTION_DADOS = ' + json.dumps(dados, ensure_ascii=False) + ';\n')
    print(f'{cfg["id"]}: {dados["dur"]:.2f} s, {n} quadros por gravação, tela em {W}x{dados["tela"]["h"]}, altura da tela no topo = {hs}')
    return dados

def cmd_novo(a):
    base = os.path.dirname(os.path.abspath(a.plano))
    pasta = os.path.join(base, 'motions', a.id)
    if os.path.exists(os.path.join(pasta, 'motion.html')):
        raise SystemExit(f'já existe um motion em {pasta}: use "quadros" pra refazer os quadros, ou escolha outro id')
    os.makedirs(pasta, exist_ok=True)
    cfg = {'id': a.id, 'plano': os.path.relpath(os.path.abspath(a.plano), pasta).replace('\\', '/'),
           'in': a.inicio, 'out': a.fim}
    if a.regiao:
        cfg['regiao'] = [int(x) for x in a.regiao.split(',')]
    if a.foco != 0.5:
        cfg['foco'] = a.foco
    if a.sem_cam:
        cfg['sem_cam'] = True
    json.dump(cfg, open(os.path.join(pasta, 'motion.json'), 'w', encoding='utf-8'), indent=1)
    shutil.copy(os.path.join(ASSETS, 'esqueleto.html'), os.path.join(pasta, 'motion.html'))
    shutil.copy(os.path.join(ASSETS, 'kit.js'), os.path.join(pasta, 'kit.js'))
    extrair(pasta)
    print(f'pronto: escreva o motion em {os.path.join(pasta, "motion.html")}')

# ---------- navegador ----------
def abrir(pw, pasta):
    try:
        nav = pw.chromium.launch(channel='msedge', headless=True)
    except Exception:
        nav = pw.chromium.launch(headless=True)
    pag = nav.new_page(viewport={'width': W, 'height': H}, device_scale_factor=1)
    erros = []
    pag.on('pageerror', lambda e: erros.append(str(e)))
    pag.on('console', lambda m: erros.append(m.text) if m.type == 'error' else None)
    pag.goto('file:///' + os.path.join(pasta, 'motion.html').replace('\\', '/'), wait_until='load')
    info = pag.evaluate('Motion.pronto()')
    return nav, pag, info, erros

def cmd_olhar(a):
    from playwright.sync_api import sync_playwright
    from PIL import Image, ImageDraw, ImageFont
    pasta = os.path.abspath(a.pasta); sai = os.path.join(pasta, 'olhar'); os.makedirs(sai, exist_ok=True)
    with sync_playwright() as pw:
        nav, pag, info, erros = abrir(pw, pasta)
        tempos = [float(x) for x in a.tempos] or [info['dur'] * (k + 0.5) / 8 for k in range(8)]
        ims = []
        for t in tempos:
            pag.evaluate('(t) => Motion.ir(t)', t)
            arq = os.path.join(sai, f'{t:06.2f}.jpg'); pag.screenshot(path=arq, type='jpeg', quality=90)
            ims.append((t, Image.open(arq).convert('RGB').resize((270, 480), Image.LANCZOS)))
        nav.close()
    try:
        fonte = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 16)
    except OSError:
        fonte = ImageFont.load_default()
    cols = min(8, len(ims)); lin = (len(ims) + cols - 1) // cols
    folha = Image.new('RGB', (cols * 276 + 6, lin * 508 + 6), (18, 16, 16)); des = ImageDraw.Draw(folha)
    for k, (t, im) in enumerate(ims):
        x = 6 + (k % cols) * 276; y = 6 + (k // cols) * 508
        folha.paste(im, (x, y)); des.text((x + 4, y + 484), f'{t:.2f} s', fill=(255, 107, 24), font=fonte)
    arq = os.path.join(pasta, 'olhar.jpg'); folha.save(arq, quality=88)
    print(f'duração {info["dur"]} s · {len(ims)} instantes -> {arq}')
    for e in erros[:8]:
        print('ERRO NA PÁGINA:', e)

# ---------- som sintetizado ----------
SR = 48000
def _env(n, ataque, queda):
    t = np.arange(n) / SR
    return np.minimum(1, t / max(ataque, 1e-4)) * np.exp(-t / queda)

def som(tipo):
    rng = np.random.default_rng(7)
    if tipo == 'pop':
        n = int(SR * 0.12); t = np.arange(n) / SR
        return np.sin(2 * np.pi * (520 * np.exp(-t * 9)) * t) * _env(n, 0.002, 0.03) * 0.8
    if tipo == 'tique':
        n = int(SR * 0.04); t = np.arange(n) / SR
        return (np.sin(2 * np.pi * 2100 * t) * 0.6 + rng.standard_normal(n) * 0.3) * _env(n, 0.0005, 0.006) * 0.6
    if tipo == 'plim':
        n = int(SR * 0.7); t = np.arange(n) / SR
        return (np.sin(2 * np.pi * 1320 * t) + 0.5 * np.sin(2 * np.pi * 1980 * t) + 0.25 * np.sin(2 * np.pi * 2640 * t)) * _env(n, 0.002, 0.16) * 0.45
    if tipo == 'baque':
        n = int(SR * 0.3); t = np.arange(n) / SR
        return np.sin(2 * np.pi * (95 * np.exp(-t * 6) + 40) * t) * _env(n, 0.002, 0.08) * 0.95
    if tipo in ('vuush', 'subida'):
        d = 0.5 if tipo == 'vuush' else 0.8
        n = int(SR * d); t = np.arange(n) / SR
        r = rng.standard_normal(n)
        # ruído com filtro que abre e fecha: média móvel de tamanho variável feita por soma acumulada em 3 faixas
        def passa(x, k):
            c = np.cumsum(np.insert(x, 0, 0)); return (c[k:] - c[:-k])[:len(x) - k + 1] / k
        grave = np.pad(passa(r, 48), (0, 47)); medio = np.pad(passa(r, 12), (0, 11)); agudo = r - np.pad(passa(r, 4), (0, 3))
        p = t / d
        mist = grave * (1 - p) + medio * np.sin(np.pi * p) + agudo * (p ** 2) * 0.35
        env = np.sin(np.pi * p) ** 2 if tipo == 'vuush' else (p ** 2.2) * np.minimum(1, (1 - p) / 0.05)
        tom = np.sin(2 * np.pi * (220 + 700 * p ** 2) * t) * 0.12 if tipo == 'subida' else 0
        return (mist * 0.9 + tom) * env * 0.55
    raise SystemExit(f'som desconhecido: {tipo} (use vuush, pop, tique, plim, subida, baque)')

def som_de_arquivo(arq, corte=0.0, dur=None, entra=0.0, sai=0.03):
    """efeito gravado (mp3/wav), em mono 48 kHz. `corte` pula o silêncio do começo; `dur` limita o tamanho;
    `entra` e `sai` são os segundos de subida e de descida do volume (dão forma a um ruído de passagem)."""
    cmd = ['ffmpeg', '-v', 'error', '-ss', f'{corte:.3f}'] + (['-t', f'{dur:.3f}'] if dur else []) + ['-i', arq, '-ac', '1', '-ar', str(SR), '-f', 'f64le', '-']
    x = np.frombuffer(subprocess.run(cmd, capture_output=True).stdout, np.float64).copy()
    if not len(x):
        raise SystemExit(f'não consegui ler o som {arq}')
    f = min(len(x), max(1, int(SR * sai))); x[-f:] *= np.linspace(1, 0, f) ** 2      # fim sem estalo
    if entra > 0:
        f = min(len(x), int(SR * entra)); x[:f] *= np.linspace(0, 1, f) ** 2
    return x

def pista_sfx(lista, dur, saida, pasta='.'):
    pista = np.zeros(int(SR * (dur + 0.5)))
    for s in lista:
        # tipo pode ser um dos sons sintetizados ou o caminho de um arquivo de som (relativo à pasta do motion)
        if str(s['tipo']).lower().endswith(('.mp3', '.wav', '.m4a', '.ogg')):
            x = som_de_arquivo(os.path.normpath(os.path.join(pasta, s['tipo'])), float(s.get('corte', 0)), s.get('dur'),
                                float(s.get('entra', 0)), float(s.get('sai', 0.03)))
        else:
            x = som(s['tipo'])
        x = x * float(s.get('volume', 1)); i = int(max(0, s['t']) * SR)
        x = x[:max(0, len(pista) - i)]; pista[i:i + len(x)] += x
    pista = np.clip(pista[:int(SR * dur)], -0.98, 0.98)
    pcm = (np.stack([pista, pista], axis=1) * 32767).astype('<i2')
    with wave.open(saida, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())

# ---------- render ----------
def cmd_render(a):
    from playwright.sync_api import sync_playwright
    pasta = os.path.abspath(a.pasta)
    cfg = json.load(open(os.path.join(pasta, 'motion.json'), encoding='utf-8')); mid = cfg['id']
    saida = os.path.join(pasta, f'{mid}.mp4')
    with sync_playwright() as pw:
        nav, pag, info, erros = abrir(pw, pasta)
        n = round(info['dur'] * FPS)
        ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'image2pipe', '-c:v', 'mjpeg', '-framerate', str(FPS),
                               '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '14', '-pix_fmt', 'yuv420p',
                               '-vf', f'scale={W}:{H}:flags=lanczos', '-r', str(FPS), saida], stdin=subprocess.PIPE)
        for k in range(n):
            pag.evaluate('(t) => Motion.ir(t)', k / FPS)
            ff.stdin.write(pag.screenshot(type='jpeg', quality=96))
            if k % 30 == 0:
                print(f'  {k / FPS:5.1f} / {info["dur"]:.1f} s', flush=True)
        ff.stdin.close(); ff.wait(); nav.close()
    if ff.returncode:
        raise SystemExit('o ffmpeg não conseguiu fechar o vídeo do motion')
    extra = ''
    if info['sfx']:
        wav = os.path.join(pasta, f'{mid}-sfx.wav'); pista_sfx(info['sfx'], info['dur'], wav, pasta)
        extra = f' · som: {wav} ({len(info["sfx"])} efeitos)'
    print(f'pronto: {saida} ({info["dur"]:.2f} s, {n} quadros){extra}')
    for e in erros[:8]:
        print('ERRO NA PÁGINA:', e)
    if erros:
        raise SystemExit(1)

def cmd_som(a):
    """refaz só a pista de efeitos (<id>-sfx.wav), sem renderizar a imagem de novo"""
    from playwright.sync_api import sync_playwright
    pasta = os.path.abspath(a.pasta)
    mid = json.load(open(os.path.join(pasta, 'motion.json'), encoding='utf-8'))['id']
    with sync_playwright() as pw:
        nav, pag, info, erros = abrir(pw, pasta); nav.close()
    wav = os.path.join(pasta, f'{mid}-sfx.wav'); pista_sfx(info['sfx'], info['dur'], wav, pasta)
    print(f'som: {wav} ({len(info["sfx"])} efeitos, {info["dur"]:.2f} s)')

if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    s = sub.add_parser('novo'); s.add_argument('plano'); s.add_argument('id')
    s.add_argument('--in', dest='inicio', type=float, required=True); s.add_argument('--out', dest='fim', type=float, required=True)
    s.add_argument('--regiao'); s.add_argument('--foco', type=float, default=0.5); s.add_argument('--sem-cam', action='store_true')
    s = sub.add_parser('quadros'); s.add_argument('pasta')
    s = sub.add_parser('olhar'); s.add_argument('pasta'); s.add_argument('tempos', nargs='*')
    s = sub.add_parser('render'); s.add_argument('pasta')
    s = sub.add_parser('som'); s.add_argument('pasta')
    a = ap.parse_args()
    {'novo': cmd_novo, 'quadros': lambda a: extrair(os.path.abspath(a.pasta)), 'olhar': cmd_olhar, 'render': cmd_render, 'som': cmd_som}[a.cmd](a)
