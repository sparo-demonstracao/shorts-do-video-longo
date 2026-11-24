# O roteiro e o plano de um Short

Um Short no formato aprovado (cena única) tem dois arquivos em `short-XX/`: o **`roteiro.json`**, que diz quais
trechos da fala entram e de onde vem cada gravação, e o **`plano.json`**, que o `plano_da_cena.py` escreve a partir
dele e o `compor.py` monta. Exemplos reais em `assets/cena/exemplo-aprovado/`. Tempos em segundos, sempre os da
**gravação da voz**; caminhos relativos à pasta do Short.

## O roteiro.json (cena única)

```json
{
  "id": "cena",
  "palavras": "../transcricao/legenda.json",
  "fontes": {
    "audio": {"arquivo": "C:/.../[Video] VO_01.wav"},
    "cam":   {"arquivo": "C:/.../camera.mp4", "atraso": [[715, -3.181], [1955, -3.261], [5685, -3.061]]},
    "tela":  {"arquivo": "C:/.../tela.mkv", "atraso": [[715, 2.159], [1010, 2.089]]}
  },
  "falas": [[1028.2233, 1031.8566], [1032.0567, 1032.99]],
  "nomes_falas": ["G1", "G2"],
  "palavras_falas": "palavras-pedacos.json",
  "fades": {"11": {"out": 0.03}},
  "cam": {"largura": 1920},
  "telas": {"dpill": {"in": 2277.0, "dur": 3.4, "regiao": [1170, 1383, 220, 44], "largura": 660}}
}
```

- `fontes.audio`: a gravação da voz (referência de todos os tempos). Sem áudio separado, a voz é a da `cam`.
- `atraso`: quanto somar ao tempo da voz pra achar o mesmo instante naquela gravação. Número, ou tabela
  `[[tempo, atraso], ...]` quando muda ao longo da gravação (o programa interpola). Se a imagem do celular chega
  depois do próprio som, já some isso no ponto da tabela (ou use `"imagem_atras": {"base", "por_segundo", "desde"}`).
- `falas`: os trechos, na ordem do Short. Cada um dura um número inteiro de quadros (1/30 s); trechos vizinhos da
  mesma frase têm o `in` de um na grade do outro, senão o áudio ganha um pulinho na emenda. O `pedacos.py` cuida.
- `palavras_falas`: as palavras de cada fala, com tempos contados do começo da fala (do `palavras_falas.py` ou do
  `roteiro_pedacos.py`). É delas que saem a legenda e o tempo de cada motion.
- `fades`: fade no fim (ou começo) de uma fala cortada rente, pelo índice da fala. Só quando a frase emenda na
  seguinte sem silêncio.
- `ganho_db`: ganho em dB por índice de fala (`{"4": -2.0}`), pra igualar tomadas de pontos diferentes da gravação
  (a introdução costuma sair 2 a 3 dB mais alta que o resto). Meça cada frase com
  `ffmpeg -ss in -to out -i voz -af ebur128 -f null -` e **só reduza** as mais altas até a mais baixa: ganho positivo
  pode estourar. O `plano_da_cena.py` leva pro bloco e o `compor.py` aplica antes do nivelamento geral.
- `telas`: trechos de gravação de tela que tocam **em movimento** dentro da cena (viram `quadros/<nome>/`). Tela
  parada não entra aqui: é captura em `material/`.
- `abertura` (opcional): `{"quadros": N, "palavras": [...]}` pra um começo sem fala da gravação.

**Como nasce.** Você escreve o `roteiro-base.json` com as frases inteiras (mesmo formato, `falas` = uma por frase)
e um `falas.json` (`[{"nome": "G", "in": ..., "out": ...}]`, com `"piso": -46` em fala baixa e `"teto"` quando a
frase emenda na seguinte). Depois, da pasta do vídeo:

```
python S/cena/palavras_falas.py short-01/roteiro-base.json --prompt "Claude Code, GitHub, <nomes do vídeo>"
   (ponha "palavras_falas": "palavras-falas.json" no roteiro-base)
python S/cena/pedacos.py short-01/falas.json short-01/pedacos.json
python S/cena/roteiro_pedacos.py short-01/roteiro-base.json short-01/pedacos.json short-01/roteiro.json
python S/cena/conferir_pontas.py short-01/roteiro.json
python S/cena/preparar_cena.py short-01/roteiro.json
```

O `roteiro_pedacos.py` avisa as palavras "realocadas" (o começo delas caiu numa pausa cortada): confira a ordem
delas no `palavras-pedacos.json`, que às vezes inverte duas palavras curtas vizinhas ("é que").

O `preparar_cena.py` escreve `cena/dados.js` (`MOTION_DADOS`: `dur`, `fps`, `falas` com o quadro em que cada uma
começa, `palavras` no tempo do Short, `quadros`) e extrai `quadros/cam`. Mudou só tempo ou palavra? `--so-dados`.

## O plano.json (cena única)

```
python S/cena/plano_da_cena.py short-01/roteiro.json --saida saida/short-01-v1.mp4 --trilha ../material/audio/trilha-ia.mp3 --volume 0.1
python S/compor.py short-01/plano.json montar
```

Sai um bloco `motion` por fala, todos apontando pra `cena/cena.mp4`, cada um com o `audio` da fala e o `in` do
ponto da cena; o primeiro carrega a pista de efeitos (`cena/cena-sfx.wav`), o último um `fade_out` de 0,06 s.
`legendas.ligado` fica `false`: a legenda é desenhada dentro da cena. O `montar` tem que terminar em
**"sincronia conferida: áudio contínuo, N blocos com a fala no lugar (maior desvio 0 ms)"**.

Pra uma versão nova, mude só o `saida` (`-v2`, `-v3`...) depois de `guardar_versao.py`.

---

# O formato de blocos (reserva)

O que segue é o plano escrito à mão, com blocos de tipos diferentes. Foi o formato da primeira versão, reprovada;
continua funcionando no `compor.py` e serve de último recurso (gravação só em composto, por exemplo).


Cada Short tem uma pasta (`short-01/`) com um `plano.json`. O `compor.py` lê esse arquivo e monta o vídeo.
Os caminhos são relativos à pasta do plano. Tempos em segundos.

```json
{
  "saida": "saida/short-01.mp4",
  "fontes": {
    "cam":  {"arquivo": "D:/bruto/camera.mp4"},
    "tela": {"arquivo": "D:/bruto/tela.mp4", "atraso": 0.0}
  },
  "estudio": {"imagem": "../../_estudio/estudio-01.png",
              "tela_quad": [[100, 250], [980, 290], [980, 760], [100, 790]]},
  "legendas": {"ligado": true, "transcricao": "../transcricao/cam.json", "destaques": ["claude"]},
  "trilha": {"arquivo": "gerados/trilha.mp3", "volume": 0.10},
  "efeitos": [{"arquivo": "gerados/vuush.mp3", "t": 4.2, "volume": 0.5}],
  "blocos": [ ... ]
}
```

## Fontes

- `cam`: a gravação com o rosto dele. É também a fonte da voz, a não ser que exista `fontes.audio`
  (gravação de microfone separada).
- `tela`: a gravação de tela.
- `atraso`: quantos segundos somar ao tempo da fala pra achar o mesmo instante nesta fonte. Se a câmera e a
  tela começaram a gravar juntas (OBS), é 0. Os tempos `in`/`out` dos blocos são sempre os da fala (fonte `cam`).
- `caixa`: `[x, y, largura, altura]` recorta um pedaço fixo da fonte antes de tudo. É como se trata a
  **gravação única** (tela com a webcam num canto): `cam` e `tela` apontam pro mesmo arquivo, a `cam` com a caixa
  da webcam e a `tela` sem caixa (ou com a caixa da área sem webcam).

## Blocos

A linha do tempo é a lista `blocos`, na ordem. Todo bloco tem `id` (curto, único) e `tipo`.

| tipo | O que aparece | Campos |
|---|---|---|
| `camera` | Ele em quadro cheio, cortado em vertical | `in`, `out`, `foco_x` (0 a 1, onde está o rosto na largura), `empurra` |
| `tela` | Tela em cima, ele embaixo | `in`, `out`, `regiao`, `altura_max`, `camera_em_cima` |
| `telao` | Estúdio com a tela real no telão e ele recortado na frente | `in`, `out`, `regiao`, `recorte`, `pessoa` (`escala`, `x`, `sobe`), `empurra` |
| `janela` | Ele no cenário real, com a janela do app flutuando atrás | `in`, `out`, `regiao`, `recorte`, `largura`, `x`, `y`, `entra`, `escurece` |
| `gerado` | Uma cena gerada (transição, segunda câmera) | `arquivo`, `velocidade`, `in`/`out` (corte dentro da cena), `audio` |
| `motion` | Um motion renderizado pelo `motion.py` | `arquivo`, `som` (pista de efeitos do motion), `som_volume`, `audio`, `legenda` |

- `regiao`: `[x, y, largura, altura]` na gravação de tela: o pedaço que interessa. Tela inteira num celular fica
  ilegível, então quase sempre vale recortar a área onde a coisa acontece.
- `recorte`: caminho do matte (vídeo preto e branco, branco = ele) feito a partir de `trechos/<id>-cam.mp4`.
  Sem `recorte`, o `telao` fica sem ele na frente e a `janela` fica por cima do cenário, sem passar atrás dele.
- `empurra`: zoom lento do bloco inteiro, por exemplo `0.04` (4% do começo ao fim). Dá vida a plano parado.
- `entra`: `false` numa `janela` que continua a do bloco anterior, pra ela não deslizar de novo.
- `foco_x`: use o mesmo valor em todos os blocos da mesma gravação, senão ele pula de lugar a cada corte.
- `legenda`: `false` desliga a legenda só naquele bloco. Use num `motion` cujo desenho ocupa a faixa da legenda.
- Um `motion` leva `"audio": {"in": ..., "out": ...}` com os mesmos tempos usados no `motion.py novo`: a fala
  real continua por baixo e o motion dura exatamente isso.

### Tela de outro instante

- `tela_in`: num bloco `tela`, `telao` ou `janela`, a tela vem deste instante da gravação (tempo da fala), e não
  do instante em que ele fala. Serve pra abrir o Short já com o resultado na tela, ou pra mostrar um slide que
  ele só abriu depois.
- `tela_vel`: toca essa tela acelerada (`3.0` = três vezes mais rápido). Bom pra uma rolagem longa caber num
  gancho de 5 s.
- No `motion.json` de um motion valem os mesmos `tela_in` e `tela_vel`, e `cam_altura` fixa a altura dos quadros
  dele (use a mesma do `quadro_tela`).

### Câmera em close: `quadro_tela`

Quando a webcam é um close, ponha no topo do plano `"quadro_tela": {"altura": 810, "faixa": 130}`. Todo bloco
`tela` passa a ter três faixas fixas: a caixa da tela (o conteúdo encosta embaixo; o que sobrar em cima fica
escuro, sob os botões do YouTube), uma faixa escura só pra legenda, e ele embaixo, sempre do mesmo tamanho.
A legenda desses blocos vai sozinha pra faixa.

- `legenda_y` num bloco muda a altura da legenda só nele: `824` pra um `motion` desenhado nesse mesmo quadro,
  `1490` num `camera` em close (o padrão 1400 cai no queixo).
- `zoom` num bloco `camera` aproxima o rosto (`1.15`), pra um corte seco "pra dentro" entre dois blocos de câmera.
- `atraso` de uma fonte pode ser uma tabela `[[tempo_da_fala, atraso], ...]`, interpolada: use em gravação longa.

### Áudio de um bloco

- Sem o campo `audio`: a fala real, de `in` a `out`.
- `"audio": {"in": 41.2, "out": 43.0}` num bloco `gerado`: a fala real continua por baixo da cena gerada. A cena
  dura o que a fala durar (o último quadro congela se faltar; use `velocidade` pra encaixar).
- `"audio": {"arquivo": "gerados/ponte-01.wav"}`: fala gerada. Se o bloco não tiver `out`, ele dura o que o áudio
  durar. Pra legenda dessa fala, ponha `"palavras": [["Olha", 0.0, 0.3], ["isso", 0.3, 0.6]]` no bloco
  (tempos a partir do começo do bloco).
- `"audio": false`: silêncio (só a trilha e os efeitos).

## Ordem de trabalho com o compor.py

```
python compor.py plano.json conferir                     # linha do tempo, avisos, erros
python compor.py plano.json trechos                      # exporta os trechos que vão pro recorte
python compor.py plano.json quadro b3 fim   pontas/b3-fim.png      # ponta de uma transição
python compor.py plano.json quadro b4 inicio pontas/b4-inicio.png
python compor.py plano.json bloco b3                     # renderiza só um bloco em tmp/b3.mkv
python compor.py plano.json montar                       # o Short inteiro
```

`conferir` avisa quando o Short passa de 2 min (não existe mínimo), quando uma cena gerada passa de 5 s e quando mais de 25% do
Short é material gerado. São os limites combinados com o criador; se o plano estourar um deles, mude o plano.

## Onde marcar o telão no estúdio

`tela_quad` são os quatro cantos da tela dentro da imagem do estúdio já em 1080x1920, nesta ordem: cima-esquerda,
cima-direita, baixo-direita, baixo-esquerda. Pra achar os cantos, abra a imagem com Read, estime os pontos,
renderize um bloco `telao` de 1 s e olhe um quadro: a gravação tem que encostar na moldura sem vazar. Ajuste e
repita. Guarde os pontos no `estudio.json` ao lado da imagem, pra não medir de novo no próximo vídeo.
