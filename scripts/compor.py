# -*- coding: utf-8 -*-
"""Monta um Short vertical (1080x1920, 30 fps, -14 LUFS) a partir de um plano.json.

Uso:  python compor.py <plano.json> <comando> [...]
  conferir                      confere o plano e mostra a linha do tempo (não renderiza nada)
  trechos                       exporta trechos/<id>-cam.mp4 dos blocos que pedem recorte (é o arquivo que vai pro recorte)
  bloco <id>                    renderiza só um bloco em tmp/<id>.mkv, pra olhar antes de montar tudo
                                (blocos "motion" são renderizados antes, pelo motion.py)
  quadro <id> inicio|fim <png>  salva o primeiro ou o último quadro de um bloco (ponta de uma transição gerada)
  montar                        renderiza todos os blocos, junta, põe legenda, trilha e efeitos, e nivela o volume

Os caminhos dentro do plano são relativos à pasta do plano. O formato do plano está em references/plano.md.
Este programa só corta, encaixa e mixa material que já existe: ele não gera imagem nem som.
"""
import json, math, os, re, shutil, subprocess, sys, unicodedata

from PIL import Image, ImageDraw, ImageFilter

W, H, FPS = 1080, 1920, 30
SR = 48000   # amostras de áudio por segundo: 1600 por quadro
COR_FUNDO_JANELA = (21, 19, 19)

# ---------- utilidades ----------
def run(cmd, cwd=None, quieto=True):
    r = subprocess.run(cmd, cwd=cwd, capture_output=quieto, text=True, errors='replace')
    if r.returncode:
        sys.stderr.write((r.stderr or '')[-3000:] + '\n')
        raise SystemExit(f'ffmpeg falhou (comando acima). Primeiro argumento: {cmd[0]} ... {cmd[-1]}')
    return r

def sonda(arq, campo):
    r = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', campo, '-of', 'csv=p=0', arq],
                       capture_output=True, text=True)
    return r.stdout.strip()

def dims(arq):
    w, h = sonda(arq, 'stream=width,height').split(',')[:2]
    return int(w), int(h)

def duracao(arq):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', arq],
                       capture_output=True, text=True)
    return float(r.stdout.strip() or 0)

def tem_audio(arq):
    r = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'a:0', '-show_entries', 'stream=index', '-of', 'csv=p=0', arq],
                       capture_output=True, text=True)
    return bool(r.stdout.strip())

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

class Plano:
    def __init__(self, caminho):
        self.caminho = os.path.abspath(caminho)
        self.pasta = os.path.dirname(self.caminho)
        self.d = json.load(open(self.caminho, encoding='utf-8-sig'))
        self.tmp = os.path.join(self.pasta, 'tmp'); os.makedirs(self.tmp, exist_ok=True)
        self.trechos = os.path.join(self.pasta, 'trechos')
        self.blocos = self.d['blocos']
        ids = [b['id'] for b in self.blocos]
        if len(set(ids)) != len(ids):
            raise SystemExit('há dois blocos com o mesmo id no plano')

    def p(self, rel):
        return rel if os.path.isabs(rel) else os.path.normpath(os.path.join(self.pasta, rel))

    def fonte(self, nome):
        f = self.d['fontes'].get(nome)
        if not f:
            raise SystemExit(f'o plano não tem a fonte "{nome}" em "fontes"')
        return f

    def bloco(self, bid):
        for b in self.blocos:
            if b['id'] == bid:
                return b
        raise SystemExit(f'bloco "{bid}" não existe no plano')

    def dur(self, b):
        a = b.get('audio') if isinstance(b.get('audio'), dict) else None
        if b['tipo'] in ('gerado', 'motion'):
            if a and 'in' in a:                       # fala real continua por baixo da cena gerada
                return a['out'] - a['in']
            if a and 'arquivo' in a:                  # fala gerada por baixo da cena gerada
                return duracao(self.p(a['arquivo']))
            d = (b.get('out') or duracao(self.p(b['arquivo']))) - b.get('in', 0)
            return d / b.get('velocidade', 1.0)
        if a and 'arquivo' in a and 'out' not in b:   # bloco que dura o que a fala gerada durar
            return duracao(self.p(a['arquivo']))
        return b['out'] - b['in']

    def trecho_cam(self, b):
        return os.path.join(self.trechos, f'{b["id"]}-cam.mp4')

# ---------- pedaços de filtro ----------
def caixa(f):
    c = f.get('caixa')
    return f'crop={c[2]}:{c[3]}:{c[0]}:{c[1]},' if c else ''

def cobrir(w, h, fx=0.5, fy=0.5):
    return (f"scale={w}:{h}:force_original_aspect_ratio=increase,"
            f"crop={w}:{h}:(iw-{w})*{fx}:(ih-{h})*{fy},setsar=1")

def empurra(b, n):
    e = b.get('empurra', 0)
    if not e:
        return ''
    # zoom lento: dobra a resolução antes pra câmera não tremer no arredondamento de pixel
    return (f",scale={W * 2}:{H * 2},zoompan=z='1+{e}*on/{max(n, 1)}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
            f":d=1:s={W}x{H}:fps={FPS}")

def regiao(b, f):
    r = b.get('regiao')
    return f'crop={r[2]}:{r[3]}:{r[0]}:{r[1]},' if r else ''

def dims_tela(pl, b):
    f = pl.fonte(b.get('fonte_tela', 'tela'))
    if b.get('regiao'):
        return b['regiao'][2], b['regiao'][3]
    if f.get('caixa'):
        return f['caixa'][2], f['caixa'][3]
    return dims(pl.p(f['arquivo']))

# ---------- imagens de apoio (PIL) ----------
def png_estudio_furado(pl):
    e = pl.d['estudio']
    sai = os.path.join(pl.tmp, 'estudio-furo.png')
    im = Image.open(pl.p(e['imagem'])).convert('RGBA')
    esc = max(W / im.width, H / im.height)
    im = im.resize((math.ceil(im.width * esc), math.ceil(im.height * esc)), Image.LANCZOS)
    x0, y0 = (im.width - W) // 2, (im.height - H) // 2
    im = im.crop((x0, y0, x0 + W, y0 + H))
    furo = Image.new('L', (W * 2, H * 2), 255)   # desenha no dobro e reduz: borda do furo sem serrilhado
    ImageDraw.Draw(furo).polygon([(x * 2, y * 2) for x, y in e['tela_quad']], fill=0)
    im.putalpha(furo.resize((W, H), Image.LANCZOS))
    im.save(sai)
    return sai

def pngs_janela(pl, b, lw, lh, barra):
    base = os.path.join(pl.tmp, b['id'])
    raio = b.get('raio', 28); th = lh + barra
    m = Image.new('L', (lw * 2, th * 2), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, lw * 2 - 1, th * 2 - 1], raio * 2, fill=255)
    m.resize((lw, th), Image.LANCZOS).save(base + '-mascara.png')
    bar = Image.new('RGBA', (lw, barra), COR_FUNDO_JANELA + (255,))
    des = ImageDraw.Draw(bar)
    for k, cor in enumerate(((255, 107, 24), (243, 237, 230), (110, 104, 100))):
        cx = 26 + k * 26; des.ellipse([cx - 7, barra // 2 - 7, cx + 7, barra // 2 + 7], fill=cor)
    des.line([0, barra - 1, lw, barra - 1], fill=(50, 46, 46), width=1)
    bar.save(base + '-barra.png')
    mg = 70
    s = Image.new('RGBA', (lw + mg * 2, th + mg * 2), (0, 0, 0, 0))
    ImageDraw.Draw(s).rounded_rectangle([mg, mg + 14, mg + lw, mg + th + 14], raio, fill=(0, 0, 0, 150))
    s.filter(ImageFilter.GaussianBlur(26)).save(base + '-sombra.png')
    return base + '-mascara.png', base + '-barra.png', base + '-sombra.png', mg

# ---------- render de um bloco ----------
def entradas_audio(pl, b, dur):
    """devolve (args de entrada, é_silêncio)"""
    a = b.get('audio')
    if a is False:
        return ['-f', 'lavfi', '-t', f'{dur:.3f}', '-i', 'anullsrc=r=48000:cl=stereo'], True
    if a and 'arquivo' in a:
        return ['-i', pl.p(a['arquivo'])], False
    nome = 'audio' if 'audio' in pl.d['fontes'] else 'cam'
    f = pl.fonte(nome)
    ini = (a['in'] if a else b['in']); ini += _atraso_som(f, ini)   # o SOM não leva o "imagem_atras"
    return ['-ss', f'{ini:.3f}', '-t', f'{dur:.3f}', '-i', pl.p(f['arquivo'])], False

def render_bloco(pl, b, saida=None, so_video=False):
    dur = pl.dur(b); n = round(dur * FPS); t = b['tipo']
    saida = saida or os.path.join(pl.tmp, b['id'] + '.mkv')
    ent, fc = [], ''
    def vid(nome, ini, vel=1.0):
        f = pl.fonte(nome)
        return ['-ss', f'{ini + atraso_em(f, ini):.3f}', '-t', f'{(dur + 0.2) * vel:.3f}', '-i', pl.p(f['arquivo'])]
    # a tela pode vir de outro instante da gravação (tela_in) e tocar mais rápido (tela_vel); a fala segue a do bloco
    t_tela = b.get('tela_in', b.get('in', 0)); v_tela = b.get('tela_vel', 1.0)
    acel = f'setpts=PTS/{v_tela},' if v_tela != 1.0 else ''
    def png(arq):
        return ['-loop', '1', '-framerate', str(FPS), '-t', f'{dur + 0.2:.3f}', '-i', arq]
    fx, fy = b.get('foco_x', 0.5), b.get('foco_y', 0.5)

    if t == 'camera':
        cam = pl.fonte('cam')
        ent += vid('cam', b['in'])
        z = b.get('zoom', 1.0)   # zoom > 1 aproxima (corte seco "pra dentro" entre dois blocos de câmera)
        zf = f",scale={par(W * z)}:{par(H * z)},crop={W}:{H}:(iw-{W})*{b.get('zoom_x', 0.5)}:(ih-{H})*{b.get('zoom_y', 0.4)}" if z != 1.0 else ''
        fc = f"[0:v]{caixa(cam)}{cobrir(W, H, fx, fy)}{zf},fps={FPS}{empurra(b, n)}[v]"

    elif t == 'tela':
        cam, tela = pl.fonte('cam'), pl.fonte(b.get('fonte_tela', 'tela'))
        tw, th = dims_tela(pl, b)
        hs = min(par(W * th / tw), b.get('altura_max', 1100))
        ent += vid(b.get('fonte_tela', 'tela'), t_tela, v_tela) + vid('cam', b['in'])
        q = pl.d.get('quadro_tela')
        if q:
            # quadro fixo: caixa da tela com altura fixa (o conteúdo encosta embaixo), faixa escura da legenda e ele
            # embaixo, sempre do mesmo tamanho. Serve pra câmera em close, onde a legenda no peito cairia no rosto.
            alt, faixa, cor = q.get('altura', 810), q.get('faixa', 130), q.get('cor', '0x0c0a0a')
            hc = min(par(W * th / tw), alt)
            cima = (f"[0:v]{acel}{caixa(tela)}{regiao(b, tela)}{cobrir(W, hc, 0.5, 0)},fps={FPS},"
                    f"pad={W}:{alt + faixa}:0:{alt - hc}:color={cor}[a]")
            baixo = f"[1:v]{caixa(cam)}{cobrir(W, H - alt - faixa, fx, fy)},fps={FPS}[b]"
            fc = f"{cima};{baixo};[a][b]vstack{empurra(b, n)}[v]"
        else:
            cima = f"[0:v]{acel}{caixa(tela)}{regiao(b, tela)}{cobrir(W, hs, 0.5, 0)},fps={FPS}[a]"
            baixo = f"[1:v]{caixa(cam)}{cobrir(W, H - hs, fx, fy)},fps={FPS}[b]"
            ordem = '[b][a]' if b.get('camera_em_cima') else '[a][b]'
            fc = f"{cima};{baixo};{ordem}vstack{empurra(b, n)}[v]"

    elif t == 'telao':
        tela = pl.fonte(b.get('fonte_tela', 'tela'))
        q = pl.d['estudio']['tela_quad']   # ordem: cima-esq, cima-dir, baixo-dir, baixo-esq
        pts = f"{q[0][0]}:{q[0][1]}:{q[1][0]}:{q[1][1]}:{q[3][0]}:{q[3][1]}:{q[2][0]}:{q[2][1]}"
        ent += vid(b.get('fonte_tela', 'tela'), t_tela, v_tela) + png(png_estudio_furado(pl))
        fc = (f"[0:v]{acel}{caixa(tela)}{regiao(b, tela)}scale={W}:{H},setsar=1,fps={FPS},"
              f"perspective={pts}:sense=destination:interpolation=cubic[s];[s][1:v]overlay=0:0[bg]")
        rec = b.get('recorte')
        if rec:
            pe = b.get('pessoa', {})
            esc, px, sobe = pe.get('escala', 0.82), pe.get('x', 0.5), pe.get('sobe', 0)
            ent += ['-i', pl.trecho_cam(b), '-i', pl.p(rec)]
            fc += (f";[3:v]format=gray,scale={W}:{H}[m];[2:v]format=rgba[p0];[p0][m]alphamerge,scale={par(W * esc)}:{par(H * esc)}[pp]"
                   f";[bg][pp]overlay=x=({W}-w)*{px}:y={H}-h-{sobe}:shortest=0[c]")
            fc += f";[c]null{empurra(b, n)}[v]"
        else:
            fc += f";[bg]null{empurra(b, n)}[v]"

    elif t == 'janela':
        tela = pl.fonte(b.get('fonte_tela', 'tela'))
        tw, th = dims_tela(pl, b)
        lw = par(b.get('largura', 940)); lh = par(lw * th / tw); barra = 46
        masc, bar, sombra, mg = pngs_janela(pl, b, lw, lh, barra)
        wx = b.get('x', (W - lw) // 2); wy = b.get('y', 210)
        entra = b.get('entra', True)
        mov = (f"+56*pow(1-min(t/0.45\\,1)\\,3)" if entra else '') + "+5*sin(2*PI*t/5)"
        fade = ",fade=in:st=0:d=0.3:alpha=1" if entra else ''
        rec = b.get('recorte')
        base_in = ['-i', pl.trecho_cam(b)] if rec else vid('cam', b['in'])
        base_f = '' if rec else f"{caixa(pl.fonte('cam'))}{cobrir(W, H, fx, fy)},"
        ent += base_in + vid(b.get('fonte_tela', 'tela'), t_tela, v_tela) + png(bar) + png(masc) + png(sombra)
        fc = (f"[0:v]{base_f}fps={FPS},split[b0][b1]"
              f";[1:v]{acel}{caixa(tela)}{regiao(b, tela)}scale={lw}:{lh},setsar=1,fps={FPS},"
              f"pad={lw}:{lh + barra}:0:{barra}:color=0x{'%02x%02x%02x' % COR_FUNDO_JANELA}[c0]"
              f";[c0][2:v]overlay=0:0,format=rgba[c1];[3:v]format=gray[mk];[c1][mk]alphamerge{fade}[win]"
              f";[4:v]format=rgba{fade}[sh]"
              f";[b0]eq=brightness={b.get('escurece', -0.06)}[bb]"
              f";[bb][sh]overlay=x={wx - mg}:y={wy - mg}{mov}[bs]"
              f";[bs][win]overlay=x={wx}:y={wy}{mov}[bw]")
        if rec:
            ent += ['-i', pl.p(rec)]
            fc += (f";[5:v]format=gray,scale={W}:{H}[m];[b1]format=rgba[p0];[p0][m]alphamerge[pp]"
                   f";[bw][pp]overlay=0:0{empurra(b, n)}[v]")
        else:
            fc += f";[b1]nullsink;[bw]null{empurra(b, n)}[v]"

    elif t in ('gerado', 'motion'):
        vel = b.get('velocidade', 1.0)
        corte = (['-ss', str(b['in'])] if b.get('in') else []) + (['-to', str(b['out'])] if b.get('out') else [])
        ent += corte + ['-i', pl.p(b['arquivo'])]
        fc = (f"[0:v]setpts=PTS/{vel},{cobrir(W, H, fx, fy)},fps={FPS},"
              f"tpad=stop_mode=clone:stop_duration=3{empurra(b, n)}[v]")
        if 'audio' not in b:
            b = dict(b, audio=False)   # cena sem fala por baixo: silêncio (o som do modelo não entra)
    else:
        raise SystemExit(f'tipo de bloco desconhecido: {t}')

    cmd = ['ffmpeg', '-v', 'error', '-y', *ent]
    n_v = sum(1 for x in ent if x == '-i')
    if so_video:
        cmd += ['-filter_complex', fc, '-map', '[v]', '-an']
    else:
        aent, _ = entradas_audio(pl, b, dur)
        # o áudio sai com o número exato de amostras do bloco (1600 por quadro), nem um quadro a mais nem a menos
        # "fade_in"/"fade_out" (segundos) no bloco, ou "fade_fala" no plano: suaviza um corte feito no meio de uma frase
        fi = b.get('fade_in', pl.d.get('fade_fala', 0)); fo = b.get('fade_out', pl.d.get('fade_fala', 0))
        fades = (f",afade=t=in:st=0:d={fi}" if fi else '') + (f",afade=t=out:st={max(0, n / FPS - fo):.4f}:d={fo}" if fo else '')
        # "ganho_db" no bloco: iguala o volume de tomadas gravadas em momentos diferentes (só reduza: ganho positivo pode estourar)
        if b.get('ganho_db'): fades = f",volume={float(b['ganho_db']):.2f}dB" + fades
        cmd += aent + ['-filter_complex', fc + f";[{n_v}:a]aresample=48000,aformat=channel_layouts=stereo,apad,"
                       f"atrim=end_sample={n * SR // FPS},asetpts=N/SR/TB{fades}[a]",
                       '-map', '[v]', '-map', '[a]', '-c:a', 'pcm_s16le']
    cmd += ['-frames:v', str(n), '-r', str(FPS), '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '14',
            '-pix_fmt', 'yuv420p', saida]
    run(cmd)
    return saida

# ---------- trechos pro recorte ----------
def cmd_trechos(pl):
    os.makedirs(pl.trechos, exist_ok=True)
    cam = pl.fonte('cam'); feitos = []
    for b in pl.blocos:
        if b['tipo'] not in ('telao', 'janela') or not b.get('recorte'):
            continue
        dur = pl.dur(b); sai = pl.trecho_cam(b)
        run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{b["in"] + atraso_em(cam, b["in"]):.3f}', '-t', f'{dur + 0.2:.3f}',
             '-i', pl.p(cam['arquivo']), '-vf',
             f"{caixa(cam)}{cobrir(W, H, b.get('foco_x', 0.5), b.get('foco_y', 0.5))},fps={FPS}",
             '-frames:v', str(round(dur * FPS)), '-an', '-c:v', 'libx264', '-preset', 'medium', '-crf', '14',
             '-pix_fmt', 'yuv420p', sai])
        feitos.append((b['id'], dur, sai, b['recorte']))
    if not feitos:
        print('nenhum bloco do plano pede recorte'); return
    total = sum(d for _, d, _, _ in feitos)
    print(f'{len(feitos)} trechos, {total:.1f} s no total. Mande cada um pro recorte e salve o resultado no caminho da direita:')
    for bid, d, sai, rec in feitos:
        print(f'  {bid:10s} {d:5.1f} s  {sai}  ->  {rec}')

# ---------- legendas ----------
def tempo_ass(t):
    t = max(0, t); return f'{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}'

def gerar_legendas(pl, inicios):
    cfg = pl.d.get('legendas') or {}
    if not cfg.get('ligado', True) or not cfg.get('transcricao'):
        return None
    pal = json.load(open(pl.p(cfg['transcricao']), encoding='utf-8'))['palavras']
    destaques = {norm(x) for x in cfg.get('destaques', [])}
    tam = cfg.get('tamanho', 84); y = cfg.get('y', 1400); q = pl.d.get('quadro_tela')
    def y_do(b):   # altura da legenda neste bloco: a do bloco, a faixa do quadro fixo, ou a padrão
        if 'legenda_y' in b:
            return int(b['legenda_y'])
        if q and b['tipo'] == 'tela':
            return int(q.get('altura', 810) + max(0, (q.get('faixa', 130) - tam * 1.2) / 2))
        return int(y)
    falas = []   # (início, fim, palavra, altura) já na linha do tempo do Short
    for b, t0 in zip(pl.blocos, inicios):
        if b.get('legenda') is False:
            continue
        yb = y_do(b)
        a = b.get('audio')
        if a is False or (a and 'arquivo' in a) or (b['tipo'] in ('gerado', 'motion') and not a):
            for k, (p, i, f) in enumerate(b.get('palavras', [])):   # fala gerada: tempos escritos no plano
                falas.append((t0 + i, t0 + f, p, yb))
            continue
        ini, fim = (a['in'], a['out']) if a else (b['in'], b['out'])
        for w in pal:
            if ini - 0.02 <= w['i'] and w['f'] <= fim + 0.25:
                falas.append((t0 + w['i'] - ini, t0 + min(w['f'], fim) - ini, w['p'], yb))
    grupos, atual = [], []
    for it in falas:
        texto = ' '.join(x[2] for x in atual + [it])
        quebra = atual and (len(atual) >= cfg.get('max_palavras', 3) or len(texto) > 18
                            or it[0] - atual[-1][1] > 0.45 or re.search(r'[.!?…:]$', atual[-1][2]))
        if quebra:
            grupos.append(atual); atual = []
        atual.append(it)
    if atual:
        grupos.append(atual)
    fonte = cfg.get('fonte', 'Segoe UI Black')
    cab = (f"[Script Info]\nScriptType: v4.00+\nPlayResX: {W}\nPlayResY: {H}\nWrapStyle: 2\n\n[V4+ Styles]\n"
           "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, "
           "Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, "
           "MarginV, Encoding\n"
           f"Style: L,{fonte},{tam},&H00E6EDF3,&H00E6EDF3,&H00100C0C,&H78000000,-1,0,0,0,100,100,0,0,1,7,3,8,60,60,{y},1\n\n"
           "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
    linhas = []
    for k, g in enumerate(grupos):
        ini = g[0][0]; fim = g[-1][1]
        if k + 1 < len(grupos) and grupos[k + 1][0][0] - fim < 0.3:
            fim = grupos[k + 1][0][0]
        partes = []
        for _, _, p, _ in g:
            limpa = re.sub(r'[.,;:!…]+$', '', p).upper()
            partes.append('{\\c&H186BFF&}' + limpa + '{\\c&HE6EDF3&}' if norm(p) in destaques else limpa)
        mv = g[0][3] if g[0][3] != int(y) else 0   # margem própria do bloco (0 = a do estilo)
        linhas.append(f"Dialogue: 0,{tempo_ass(ini)},{tempo_ass(fim)},L,,0,0,{mv},,{{\\fad(60,0)}}{' '.join(partes)}")
    sai = os.path.join(pl.tmp, 'legendas.ass')
    open(sai, 'w', encoding='utf-8').write(cab + '\n'.join(linhas) + '\n')
    return sai

def norm(x):
    x = unicodedata.normalize('NFD', x.lower())
    return re.sub(r'[^a-z0-9]', '', ''.join(c for c in x if unicodedata.category(c) != 'Mn'))

# ---------- comandos ----------
def linha_do_tempo(pl):
    t, ini = 0.0, []
    for b in pl.blocos:
        ini.append(t); t += round(pl.dur(b) * FPS) / FPS
    return ini, t

def cmd_conferir(pl):
    erros, avisos = [], []
    for nome, f in pl.d['fontes'].items():
        if not os.path.exists(pl.p(f['arquivo'])):
            erros.append(f'fonte "{nome}": arquivo não existe: {pl.p(f["arquivo"])}')
    if erros:
        print('\n'.join('ERRO  ' + e for e in erros)); raise SystemExit(1)
    nome_a = 'audio' if 'audio' in pl.d['fontes'] else 'cam'
    if not tem_audio(pl.p(pl.fonte(nome_a)['arquivo'])):
        erros.append(f'a fonte "{nome_a}" não tem áudio: aponte "fontes.audio" pro arquivo que tem a sua voz')
    ini, total = linha_do_tempo(pl)
    print(f'{"bloco":10s} {"tipo":8s} {"entra":>7s} {"dura":>6s}  observação')
    for b, t0 in zip(pl.blocos, ini):
        d = pl.dur(b); obs = []
        if d <= 0:
            erros.append(f'{b["id"]}: duração zero ou negativa')
        if b['tipo'] in ('telao', 'janela'):
            rec = b.get('recorte')
            if rec and not os.path.exists(pl.p(rec)):
                obs.append('recorte ainda não existe')
            elif rec and os.path.exists(pl.trecho_cam(b)):
                n1 = sonda(pl.trecho_cam(b), 'stream=nb_frames'); n2 = sonda(pl.p(rec), 'stream=nb_frames')
                if n1 and n2 and n1.isdigit() and n2.isdigit() and abs(int(n1) - int(n2)) > 2:
                    erros.append(f'{b["id"]}: o recorte tem {n2} quadros e o trecho tem {n1}: não foi feito deste trecho')
            if not rec:
                obs.append('sem recorte: a janela/pessoa não fica em camadas')
        if b['tipo'] == 'telao' and 'estudio' not in pl.d:
            erros.append(f'{b["id"]}: bloco "telao" precisa de "estudio" no plano')
        if b['tipo'] == 'motion' and not os.path.exists(pl.p(b['arquivo'])):
            obs.append('motion ainda não renderizado')
        if b.get('som') and not os.path.exists(pl.p(b['som'])):
            obs.append('pista de som do motion não existe')
        if b['tipo'] == 'gerado':
            if not os.path.exists(pl.p(b['arquivo'])):
                obs.append('cena gerada ainda não existe')
            elif d > 5.01:
                avisos.append(f'{b["id"]}: cena gerada com {d:.1f} s (o combinado é no máximo 5 s)')
        a = b.get('audio')
        if a and 'arquivo' in a and not os.path.exists(pl.p(a['arquivo'])):
            obs.append('áudio gerado ainda não existe')
        print(f'{b["id"]:10s} {b["tipo"]:8s} {t0:7.2f} {d:6.2f}  {"; ".join(obs)}')
    print(f'{"TOTAL":10s} {"":8s} {"":7s} {total:6.2f}')
    if total > 120:
        avisos.append(f'o Short tem {total:.1f} s (o combinado é até 2 min; não existe mínimo)')
    ger = sum(pl.dur(b) for b in pl.blocos if b['tipo'] == 'gerado')
    if total and ger / total > 0.25:
        avisos.append(f'{ger / total:.0%} do Short é cena gerada: passou do limite de 25%')
    for x in avisos:
        print('AVISO ' + x)
    for x in erros:
        print('ERRO  ' + x)
    if erros:
        raise SystemExit(1)
    print('plano ok' + (' (com avisos)' if avisos else ''))

def cmd_quadro(pl, bid, ponta, saida):
    b = pl.bloco(bid); v = render_bloco(pl, b, so_video=True, saida=os.path.join(pl.tmp, bid + '-v.mkv'))
    n = round(pl.dur(b) * FPS)
    sel = '0' if ponta == 'inicio' else str(n - 1)
    run(['ffmpeg', '-v', 'error', '-y', '-i', v, '-vf', f"select='eq(n\\,{sel})'", '-frames:v', '1', saida])
    print(f'{ponta} de {bid} -> {saida}')

def cmd_montar(pl):
    cmd_conferir(pl)
    ini, total = linha_do_tempo(pl)
    lista = os.path.join(pl.tmp, 'lista.txt')
    with open(lista, 'w', encoding='utf-8') as f:
        for b in pl.blocos:
            print(f'  renderizando {b["id"]} ({b["tipo"]}, {pl.dur(b):.1f} s)', flush=True)
            v = render_bloco(pl, b)
            f.write(f"file '{os.path.basename(v)}'\n")
    leg = gerar_legendas(pl, ini)
    ent = ['-f', 'concat', '-safe', '0', '-i', 'lista.txt']
    fv = '[0:v]null[v]'
    if leg:
        fdir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets', 'fonts')
        extra = ''
        if os.path.isdir(fdir) and os.listdir(fdir):
            shutil.copytree(fdir, os.path.join(pl.tmp, 'fonts'), dirs_exist_ok=True); extra = ':fontsdir=fonts'
        fv = f'[0:v]subtitles=legendas.ass{extra}[v]'
    # O ÁUDIO É FEITO SEPARADO DO VÍDEO, em três passos, e só entra pronto no comando final.
    # Misturar efeitos e nivelar o volume no mesmo comando do vídeo abre buracos de ~3 s no áudio (visto em 12/11/2026).
    amostras = round(total * FPS) * SR // FPS
    cheio = f"apad,atrim=end_sample={amostras},asetpts=N/SR/TB"   # toda pista dura o Short inteiro, sem começar nem acabar no meio
    run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', 'lista.txt', '-vn', '-c:a', 'pcm_s16le', 'voz.wav'], cwd=pl.tmp)
    ent_a = ['-i', 'voz.wav']
    mix, k = [f'[0:a]aresample={SR},{cheio}[voz]'], 1
    nomes = ['[voz]']
    tr = pl.d.get('trilha')
    if tr and os.path.exists(pl.p(tr['arquivo'])):
        ent_a += ['-stream_loop', '-1', '-i', pl.p(tr['arquivo'])]
        mix.append(f"[{k}:a]aresample={SR},atrim=0:{total:.3f},volume={tr.get('volume', 0.10)},"
                   f"afade=t=in:st=0:d=0.4,afade=t=out:st={max(0, total - 1.2):.3f}:d=1.2,{cheio}[tr]")
        nomes.append('[tr]'); k += 1
    efeitos = list(pl.d.get('efeitos', []))
    for b, t0 in zip(pl.blocos, ini):   # pista de som de cada motion entra no começo do bloco
        if b.get('som') and os.path.exists(pl.p(b['som'])):
            efeitos.append({'arquivo': b['som'], 't': t0, 'volume': b.get('som_volume', 0.55)})
    for j, s in enumerate(efeitos):
        if not os.path.exists(pl.p(s['arquivo'])):
            print(f'AVISO efeito sonoro não existe, pulei: {s["arquivo"]}'); continue
        ms = int(s['t'] * 1000)
        ent_a += ['-i', pl.p(s['arquivo'])]
        mix.append(f"[{k}:a]aresample={SR},aformat=channel_layouts=stereo,adelay={ms}|{ms},volume={s.get('volume', 0.5)},{cheio}[fx{j}]")
        nomes.append(f'[fx{j}]'); k += 1
    junta = (f"{''.join(nomes)}amix=inputs={len(nomes)}:normalize=0:duration=first,asetpts=N/SR/TB[a]" if len(nomes) > 1
             else '[voz]anull[a]')
    run(['ffmpeg', '-v', 'error', '-y', *ent_a, '-filter_complex', ';'.join(mix) + ';' + junta, '-map', '[a]',
         '-c:a', 'pcm_s16le', 'mistura.wav'], cwd=pl.tmp)
    run(['ffmpeg', '-v', 'error', '-y', '-i', 'mistura.wav', '-af', f'loudnorm=I=-14:TP=-1.5:LRA=11,aresample={SR},{cheio}',
         '-c:a', 'pcm_s16le', 'audio-final.wav'], cwd=pl.tmp)
    saida = pl.p(pl.d.get('saida', 'saida/short.mp4')); os.makedirs(os.path.dirname(saida), exist_ok=True)
    run(['ffmpeg', '-v', 'error', '-y', *ent, '-i', 'audio-final.wav', '-filter_complex', fv, '-map', '[v]', '-map', '1:a',
         '-frames:v', str(round(total * FPS)), '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p',
         '-c:a', 'aac', '-b:a', '192k', '-ar', str(SR), '-movflags', '+faststart', saida], cwd=pl.tmp)
    print(f'pronto: {saida}  ({total:.1f} s, {W}x{H}, {"com" if leg else "sem"} legenda)')
    conferir_saida(pl, saida, ini, total)

def conferir_saida(pl, saida, ini, total):
    """Confere o arquivo final sem precisar ouvir: o áudio tem buraco? dura o mesmo que o vídeo? a fala de cada
    bloco caiu no instante planejado? Quem monta não ouve, então isto roda em toda montagem."""
    import numpy as np
    r = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'a:0', '-show_entries', 'packet=pts_time', '-of', 'csv=p=0', saida],
                       capture_output=True, text=True)
    ts = [float(x.strip().strip(',')) for x in r.stdout.splitlines() if x.strip().strip(',')]
    buracos = [(round(a, 2), round(b - a, 3)) for a, b in zip(ts, ts[1:]) if b - a > 0.03]
    def som(arq, cwd=None):
        raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', arq, '-vn', '-ac', '1', '-ar', '16000', '-f', 'f32le', '-'],
                             capture_output=True, cwd=cwd).stdout
        return np.frombuffer(raw, np.float32).astype(np.float64)
    S = som(saida); S = S - S.mean()
    problemas = []
    if buracos:
        problemas.append(f'o áudio tem {len(buracos)} buraco(s) (instante, tamanho em s): {buracos[:6]}')
    if abs(len(S) / 16000 - total) > 0.06:
        problemas.append(f'o áudio dura {len(S) / 16000:.2f} s e o vídeo {total:.2f} s')
    pior, conferidos = 0.0, 0
    for b, t0 in zip(pl.blocos, ini):
        a = b.get('audio'); d = pl.dur(b)
        if a is False or (b['tipo'] in ('gerado', 'motion') and not a) or d < 1.6:
            continue
        x = som(b['id'] + '.mkv', cwd=pl.tmp)[int(0.3 * 16000):int(min(d - 0.3, 4.0) * 16000)]; x = x - x.mean()
        if len(x) < 8000 or float(np.abs(x).max()) < 1e-3:
            continue
        n = 1 << int(np.ceil(np.log2(len(x) + len(S))))
        c = np.fft.irfft(np.fft.rfft(S, n) * np.conj(np.fft.rfft(x, n)), n)[:len(S) - len(x)]
        desvio = (int(np.argmax(c)) / 16000 - 0.3 - t0) * 1000
        conferidos += 1; pior = max(pior, abs(desvio))
        if abs(desvio) > 25:
            problemas.append(f'{b["id"]}: a fala está {desvio:+.0f} ms fora do lugar')
    if problemas:
        for x in problemas:
            print('ERRO DE SINCRONIA  ' + x)
        raise SystemExit('o Short montou com o áudio fora de sincronia: NÃO entregue este arquivo')
    print(f'sincronia conferida: áudio contínuo, {conferidos} blocos com a fala no lugar (maior desvio {pior:.0f} ms)')

if __name__ == '__main__':
    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    pl = Plano(sys.argv[1]); c = sys.argv[2]
    if c == 'conferir':
        cmd_conferir(pl)
    elif c == 'trechos':
        cmd_trechos(pl)
    elif c == 'bloco':
        print(render_bloco(pl, pl.bloco(sys.argv[3])))
    elif c == 'quadro':
        cmd_quadro(pl, sys.argv[3], sys.argv[4], sys.argv[5])
    elif c == 'montar':
        cmd_montar(pl)
    else:
        raise SystemExit(__doc__)
