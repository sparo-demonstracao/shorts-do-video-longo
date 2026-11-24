# -*- coding: utf-8 -*-
# Estende a trilha-ia.mp3 (42 s, 112 bpm, a do reels aprovado) pro tamanho de cada versao, sem mexer no som dela:
# repete trechos inteiros de compassos, com a emenda num ponto em que os dois lados soam iguais, e deixa o final
# natural da musica cair no fim do video. Tambem escolhe o deslocamento (ate meia batida) que poe as batidas mais
# perto das trocas de cena.  Uso: python tmp/trilha_ia_monta.py
import subprocess, json, io, numpy as np

SR = 44100
SRC = 'material/audio/trilha-ia.mp3'
# andamento medido pelos ataques (sem o grave): 112,01 bpm, constante do começo ao fim; compasso de 2,14265 s
COMP = 2.14265; BAT = COMP / 4; BPM = 60 / BAT; T0 = 0.290

def carrega(arq):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', arq, '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32).reshape(-1, 2).astype(np.float64)

x = carrega(SRC); m = x.mean(axis=1)

def refina(a0, ncomp):
    """ponto de volta: de b (= a + n compassos EXATOS) pra a. O ritmo desta faixa e de maquina: qualquer salto de n
    compassos cai na batida. O que muda e o som sustentado (grave, teclados): procura, a ate 1 compasso de a0, o
    instante em que os dois lados soam mais iguais numa janela de 80 ms, pra cruzar ali."""
    D = int(round(ncomp * COMP * SR)); ia = int(a0 * SR); j = int(0.08 * SR); best = (-9, ia)
    for p in range(max(int(0.3 * SR), ia - int(0.25 * SR)), ia + int(0.25 * SR), 22):
        A = m[p: p + j]; B = m[p + D: p + D + j]
        c = float((A * B).sum() / (np.sqrt((A * A).sum() * (B * B).sum()) + 1e-12))
        if c > best[0]: best = (c, p)
    return best[1], best[1] + D, best[0], 0.0

def monta(passos, xf=0.08):
    """passos: [(ini_amostra, fim_amostra), ...]; cada troca de passo cruza xf segundos (o fim de um e o comeco do outro
    sao o mesmo instante musical)."""
    n = int(xf * SR); out = x[passos[0][0]: passos[0][1]].copy(); juntas = []
    for (a, b) in passos[1:]:
        # o trecho [fim_anterior, fim_anterior + n] e o trecho [a, a + n] sao equivalentes: cruza
        fim_ant = monta.fim
        A = x[fim_ant: fim_ant + n]; B = x[a: a + n]
        c = float((A.mean(axis=1) * B.mean(axis=1)).sum() / (np.sqrt((A.mean(axis=1) ** 2).sum() * (B.mean(axis=1) ** 2).sum()) + 1e-12))
        r = np.linspace(0, 1, n)[:, None]
        if c > 0.5: mix = A * (1 - r) + B * r
        else: mix = A * np.cos(r * np.pi / 2) + B * np.sin(r * np.pi / 2)
        juntas.append((len(out) / SR, c))
        out = np.concatenate([out, mix, x[a + n: b]]); monta.fim = b
    return out, juntas

def faz(nome, total, s_ini, saltos, e_fim, eventos):
    """saltos: lista de (a_seg, ncomp) na ordem: toca ate b = a + n compassos, volta pra a."""
    pts = [refina(a, nc) for a, nc in saltos]
    for (a, b, c, e), (a0, nc) in zip(pts, saltos):
        print('  volta de %.3f s pra %.3f s (%d compassos exatos): onda parecida no ponto %.2f' % (b / SR, a / SR, nc, c))
    # duracao sem deslocamento: (b1 - s) + soma(b_{i+1} - a_i) + (E - a_ultimo)
    meio = sum(pts[i + 1][1] - pts[i][0] for i in range(len(pts) - 1)) / SR
    # s e E andam juntos (delta): total = (b1/SR - s) + meio + (E - a_ult/SR)
    s_base = pts[0][1] / SR + meio + (e_fim - pts[-1][0] / SR) - total
    print('  comeca em %.3f s da musica (pedido %.3f)' % (s_base, s_ini))
    # fase das batidas: batida da musica em T0 + k*BAT (fonte). No video: t_video = t_fonte - s  (ate a 1a volta; as voltas
    # sao multiplas de compasso, a grade continua).
    def custo(delta):
        s = s_base + delta; fase = (T0 - s) % BAT
        d = [min((ev - fase) % BAT, BAT - (ev - fase) % BAT) for ev in eventos]
        return float(np.mean(d))
    ds = np.arange(-BAT / 2, BAT / 2, 0.002); cs = [custo(d) for d in ds]
    delta = float(ds[int(np.argmin(cs))])
    if s_base + delta < 0.02: delta = 0.02 - s_base
    print('  distancia media das trocas de cena ate a batida: %.3f s sem deslocar, %.3f s com deslocamento de %+.3f s (pior caso possivel %.3f)' % (custo(0), custo(delta), delta, BAT / 2))
    s = s_base + delta; E = e_fim + delta
    passos = [(int(round(s * SR)), pts[0][1])]
    for i, (a, b, c, e) in enumerate(pts):
        fim = pts[i + 1][1] if i + 1 < len(pts) else int(round(E * SR))
        passos.append((a, fim))
    monta.fim = passos[0][1]
    out, juntas = monta(passos)
    alvo = int(round(total * SR))
    print('  montada: %.3f s (alvo %.3f)  emendas em: %s' % (len(out) / SR, total, ', '.join('%.2f s (%.2f)' % j for j in juntas)))
    if len(out) < alvo + SR: out = np.concatenate([out, np.zeros((alvo + SR - len(out), 2))])
    wav = 'material/audio/%s.wav' % nome; mp3 = 'material/audio/%s.mp3' % nome
    pcm = (np.clip(out, -1, 1) * 32767).astype('<i2').tobytes()
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 's16le', '-ar', str(SR), '-ac', '2', '-i', '-', '-c:a', 'libmp3lame', '-b:a', '192k', mp3], input=pcm, check=True)
    fase = (T0 - s) % BAT
    json.dump({'arquivo': mp3, 'total': total, 'comeca_na_musica': s, 'acaba_na_musica': E, 'emendas_no_video': [j[0] for j in juntas],
               'batida': BAT, 'fase_no_video': fase}, io.open('tmp/%s.json' % nome, 'w', encoding='utf-8'), indent=1)
    print('  gravada %s  (1a batida no video em %.3f s, depois a cada %.4f s)' % (mp3, fase, BAT))

def secoes(pasta):
    s = io.open(pasta + '/secoes.js', encoding='utf-8').read(); return json.loads(s[s.index('{'): s.rindex('}') + 1])

if __name__ == '__main__':
    S1 = secoes('short-01'); S2 = secoes('short-02')
    comuns = [5.8, 6.9667, 8.45, 10.51, 11.47, 12.6667, 15.29, 16.3, 21.1333]
    print('CURTA')
    ev1 = comuns + [v for k, v in S1.items() if v > 22 and k != '_fim']
    faz('trilha-ia-curta', S1['_fim'], 9.95, [(2.09, 16)], 40.40, ev1)
    print('COMPLETA')
    ev2 = comuns + [v for k, v in S2.items() if v > 22 and k != '_fim']
    faz('trilha-ia-completa', S2['_fim'], 11.65, [(2.09, 16), (14.66, 8), (2.09, 16)], 40.40, ev2)
