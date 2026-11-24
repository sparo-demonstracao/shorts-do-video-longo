# -*- coding: utf-8 -*-
"""Acha uma fala dentro de uma transcrição e devolve o tempo exato, ou lista as palavras de um intervalo.

Uso:
  python achar.py <transcricao.json> "primeiras palavras do trecho" ["últimas palavras do trecho"]
      -> início e fim do trecho (corte no começo da 1ª palavra e no fim da última), com folga de respiro
  python achar.py <transcricao.json> --entre 95.0 140.0
      -> cada palavra do intervalo com o tempo, pra escolher onde cortar

Serve pra duas coisas: levar um momento escolhido no vídeo publicado até o tempo certo na gravação bruta
(as palavras são as mesmas, os tempos não), e achar o ponto de corte de cada bloco do plano.
A busca tolera diferença de acento, pontuação e uma ou outra palavra que o Whisper ouviu diferente.
"""
import difflib, json, re, sys, unicodedata

def norm(x):
    x = unicodedata.normalize('NFD', x.lower())
    x = ''.join(c for c in x if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z0-9]', '', x)

def achar(pal, frase, a_partir=0):
    alvo = [norm(w) for w in frase.split() if norm(w)]
    n = len(alvo)
    melhor = (0.0, None)
    for k in range(a_partir, len(pal) - n + 1):
        janela = [norm(w['p']) for w in pal[k:k + n]]
        nota = difflib.SequenceMatcher(None, ' '.join(alvo), ' '.join(janela), autojunk=False).ratio()
        if nota > melhor[0]:
            melhor = (nota, k)
            if nota == 1.0:
                break
    return melhor[0], melhor[1], n

d = json.load(open(sys.argv[1], encoding='utf-8'))
pal = d['palavras']

if sys.argv[2] == '--entre':
    t0, t1 = float(sys.argv[3]), float(sys.argv[4])
    ant = None
    for w in pal:
        if t0 <= w['i'] <= t1:
            pausa = f'   (pausa {w["i"] - ant:.2f}s)' if ant is not None and w['i'] - ant > 0.35 else ''
            print(f'{w["i"]:8.2f}  {w["p"]}{pausa}')
            ant = w['f']
    sys.exit()

nota, k, n = achar(pal, sys.argv[2])
if k is None or nota < 0.72:
    print(f'NAO ACHEI (melhor semelhança {nota:.2f}). Confira o texto em {sys.argv[1].replace(".json", ".txt")}')
    sys.exit(1)
ini, k_fim = pal[k]['i'], k + n - 1
if len(sys.argv) > 3:
    nota2, k2, n2 = achar(pal, sys.argv[3], a_partir=k)
    if k2 is None or nota2 < 0.72:
        print(f'achei o começo em {ini:.2f}s, mas NAO achei o fim (semelhança {nota2:.2f})')
        sys.exit(1)
    k_fim = k2 + n2 - 1
fim = pal[k_fim]['f']
# folga: o corte entra um pouco antes da 1ª palavra e sai um pouco depois da última, sem invadir a vizinha
antes = pal[k - 1]['f'] if k > 0 else 0.0
depois = pal[k_fim + 1]['i'] if k_fim + 1 < len(pal) else d['duracao']
entra = max(antes + 0.02, ini - 0.08)
sai = min(depois - 0.02, fim + 0.18)
print(json.dumps({'in': round(entra, 2), 'out': round(sai, 2), 'duracao': round(sai - entra, 2),
                  'semelhanca': round(nota, 2), 'palavras': k_fim - k + 1,
                  'texto': ' '.join(w['p'] for w in pal[k:k_fim + 1])}, ensure_ascii=False, indent=1))
