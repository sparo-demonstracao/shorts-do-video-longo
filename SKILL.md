---
name: shorts-do-video-longo
description: Transforma um vídeo longo do YouTube em Shorts verticais de até 2 min, num formato já testado, com o Short inteiro numa cena só, a fala real do criador sem pausas, a gravação da tela em tela cheia e animações explicativas feitas em HTML, montado das gravações brutas com programas próprios. No acabamento, o Higgsfield traz trilha nova parecida com a aprovada, um efeito sonoro gravado pra cada animação, o recorte do criador e poucos planos gerados. Use SEMPRE que o usuário mandar o link de um vídeo do próprio canal e/ou as gravações brutas e pedir Shorts, cortes, reels, clipes ou "os melhores momentos", ou disser "faz os shorts desse vídeo", "corta esse vídeo em shorts", "roda a skill de shorts", "cria os motions desse short". Use também pra ajustar, refazer, comparar lado a lado ou trocar a abertura de um Short já feito com ela. Serve pra qualquer tipo de vídeo (lista, comparativo, lançamento, app, tutorial, notícia). NÃO usar pra short 100% animado sem o criador em cena, nem pra editar o vídeo longo em si.
---

# Shorts a partir do vídeo longo

O criador do canal (quem aparece no vídeo e quem te pede os Shorts; daqui em diante, "ele") te dá **o link do vídeo publicado**, **as gravações brutas** e diz quantos Shorts quer. Você entrega os
Shorts prontos em MP4, o que gastou e o que ele precisa conferir.

**Quem faz o quê.** O criador gravado é a matéria-prima: a fala e o rosto são os reais. Você é o roteirista, o editor
e o motion designer: escolhe as frases, tira as pausas, **cria a cena animada inteira**, confere quadro a quadro e
monta. O Higgsfield entra no fim, no acabamento: trilha nova parecida com a aprovada, um efeito sonoro gravado pra
cada animação, o recorte e dois ou três planos curtos. Os programas em
`scripts/` cortam, medem, fotografam e montam; eles não inventam nada sozinhos.

**Fale com ele em português simples, sem jargão de programação.** Resposta curta, o que importa primeiro.

## O formato, em um minuto

O Short é **uma animação só**, do primeiro ao último quadro (não é "tela em cima, ele embaixo" com cortes):

1. **Gancho** (até ~4,5 s): o resultado já acontece na tela no primeiro quadro, num motion seu de tela cheia; ele
   aparece em ~1,5 s com o resultado numa janela atrás da cabeça; o número da fala em letra gigante.
2. **Como ele fez**: o material real em tela cheia com a câmera andando, miras, diagrama, o pedido real digitado.
3. **Resultado**, com calma: lentes ampliando o que ele cita, selos.
4. **Veredito**: ele olhando pra lente, o nome da coisa atrás, e o vídeo acaba na última palavra.

Antes de planejar, **abra com Read `assets/cena/exemplo-aprovado/folha-v8.jpg`**: é o Short que ele escolheu
depois de 9 versões. `references/formato.md` explica cada parte e por quê.

## Leia antes de começar

| Arquivo | Quando |
|---|---|
| `references/formato.md` | Sempre, antes de planejar. A receita do formato aprovado. |
| `references/estilo.md` | Sempre. O que ele aprovou e reprovou, com as palavras dele, e como ele decide. |
| `references/tipos-de-video.md` | Antes de escolher os momentos. Cada formato do canal pede um Short diferente. |
| `references/motions.md` | Antes de escrever a cena. O ofício dos motions, o kit e o palco. |
| `references/plano.md` | Ao escrever o `roteiro.json` e montar. |
| `references/higgsfield.md` | Antes do orçamento e de qualquer pedido ao Higgsfield. Receitas, preços e armadilhas. |
| `references/historico.md` | Se precisar do contexto de uma decisão. |

Os vereditos do `estilo.md` e o diário do `historico.md` vieram do canal em que este formato foi desenvolvido. Valem
como ponto de partida pra qualquer canal; o que o criador da vez pedir diferente passa na frente e entra nesses
arquivos.

## Os programas (`S` = pasta `scripts` desta skill)

Use `PYTHONIOENCODING=utf-8` e o `python` normal do PC. Os de `S/cena` rodam **da pasta do vídeo**.

**Entender o material**

| Comando | Pra quê |
|---|---|
| `python S/transcrever.py <gravação> <saida.json>` | Fala com o tempo de cada palavra. Lento: em segundo plano. |
| `python S/achar.py <transcricao.json> "começo" "fim"` | Tempo de um trecho pela fala. `--entre t0 t1` lista palavras e pausas. |
| `python S/folha.py <saida.jpg> <vídeo...>` | Folha de quadros com o tempo. É como você assiste: abra com Read. |
| `python S/atraso.py <referência> <outra> <t1> ...` | Quanto uma gravação está adiantada em relação à outra, pelo som. |
| `python S/gerados/miniaturas.py <gravação> <pasta>` | Miniaturas numeradas da gravação inteira em ~1 min (achar ele de perfil, rindo, etc.). |
| `S/capitulos.js` | No navegador do app: título, descrição e capítulos do vídeo publicado. |

**A fala e a cena** (`S/cena`)

| Comando | Pra quê |
|---|---|
| `python S/cena/pontas.py t0 t1 ...` | As pontas certas de cada frase, pelo volume (a transcrição corta a sílaba final). |
| `python S/cena/palavras_falas.py <roteiro.json>` | Transcreve cada fala separadamente e acerta o começo das palavras. |
| `python S/cena/pedacos.py <falas.json> <pedacos.json>` | Tira as pausas de dentro das frases sem cortar palavra; o fim do Short fica na última palavra. |
| `python S/cena/roteiro_pedacos.py <base.json> <pedacos.json> <roteiro.json>` | Monta o roteiro sem pausas e as palavras de cada pedaço. |
| `python S/cena/conferir_pontas.py <roteiro.json>` | Reprova o roteiro que começa ou termina em cima de som. |
| `python S/cena/rostos.py <roteiro.json> <folha.jpg>` | O rosto dele em cada fala: onde ele olha pra lente. |
| `python S/cena/preparar_cena.py <roteiro.json> [--so-dados]` | Cria `cena/` (quadros dele na ordem do Short, `dados.js`, `kit.js`) e `comum/palco.*`. |
| `python S/cena/fundo_sala.py <quadro da câmera> material/sala-fundo.jpg` | O cenário dele desfocado, pra preencher o alto do quadro. |
| `python S/cena/gravar_site_vertical.py <endereço> <pasta>` | Regrava um site em formato de celular, por posição de rolagem. |
| `python S/motion.py olhar\|render <short>/cena [tempos]` | Fotografa instantes da cena pra conferir; renderiza `cena.mp4` e a pista de efeitos. De graça. |
| `python S/cena/plano_da_cena.py <roteiro.json> --trilha ...` | Escreve o `plano.json` da montagem. |
| `python S/compor.py <plano.json> montar` | Junta cena, voz, trilha e efeitos; termina em "sincronia conferida". |
| `python S/cena/boca_cv.py <roteiro.json>` e `S/boca.py` | Sincronia da boca sem ouvir. |
| `python S/cena/recorte_alfa.py <short>` | Transforma o recorte do Higgsfield em quadros transparentes (`quadros/rec`). Leia o cabeçalho dele e "O recorte" no `higgsfield.md`: precisa do vídeo que subiu e do mapa de quadros. |
| `python S/cena/guardar_versao.py <short> <N>` | Guarda a versão antes de mexer. |

**Comparar e entregar**

| Comando | Pra quê |
|---|---|
| `python S/lado_a_lado.py <saida> <som> <v1> "rótulo" <v2> "rótulo" ... [--de --ate] [--leve]` | 2 a 4 versões lado a lado. Entregue sempre que houver mais de uma. |
| `python S/comparar.py seq ...` | Versões em sequência, com rótulo. |

**Planos gerados** (`S/gerados`, detalhes em `references/higgsfield.md`): `pega_url.py` (URL de upload sem
redigitar), `conferir_take.py` (a boca do take segue a fala real?), `entrada_suave.py` e `fundir_real.py` (entrada
no monitor fluida e terminando na página real), `colar_tela.py` (motion real na tela verde de um plano),
`timelapse_tela.py` (exemplo de motion pra tela do PC), `alinhar.py`, `compor_vertical.py`, `encaixar.py`.

## Pastas

```
~\shorts-canal\_sons\                  efeitos gravados já baixados e o sons.json (servem pra todos os vídeos)
~\shorts-canal\<nome-do-video>\        (~ é a pasta do usuário no PC)
  video.json  fontes.json  momentos.json  orcamento.md
  transcricao\              um .json e um .txt por gravação com fala; legenda.json corrigida
  material\                 capturas reais em 2560 px, sala-fundo.jpg, audio\ (trilha e efeitos)
  comum\                    palco.js e palco.css (o preparar_cena.py copia)
  testes-higgsfield\        fotos, rascunhos e comparações de plano gerado, uma pasta por rodada (r1, r2...)
  short-01\
    roteiro.json  plano.json  palavras-*.json
    cena\  motion.html  variante.js  dados.js  kit.js  quadros\{cam,rec,insA...}  cena.mp4  cena-sfx.wav
    _versao-1\ _versao-2\ ...   toda versão que ele já viu
    saida\short-01-v1.mp4 ...   e as cópias -leve pra mandar
```

## O caminho

Tudo o que é de graça vem antes de tudo o que custa crédito: a versão 1 já sai completa (cena, motions, trilha e
efeitos reaproveitados) sem gastar nada, e ele aprova o conteúdo antes de pagar por acabamento.

### 1. Entradas e vídeo publicado
Link do YouTube, gravações brutas e quantos Shorts (padrão: 1 a 3). Faltou algo, peça numa linha e pare. Anote o
saldo do Higgsfield (`balance`): é o "antes". Abra o link no navegador do app, rode o `capitulos.js` e salve em
`video.json`. Não baixe o vídeo do YouTube.

### 2. Inventário das gravações
`ffprobe` e uma folha de 8 quadros de cada arquivo; classifique em `fontes.json` (câmera, tela, composto, voz
separada). Ele costuma gravar **três arquivos que não começam juntos**: voz no Audition, tela no OBS, câmera no
celular. Meça o atraso de cada um em relação à voz com `atraso.py`, **perto de cada trecho que vai usar**: em
gravação longa o atraso muda décimos de segundo (vira tabela `"atraso": [[tempo, atraso], ...]`).

O som alinhado não garante a boca alinhada: o celular grava som e imagem com relógios diferentes (0 no começo e
0,16 s com 1h35, numa gravação). Confira os lábios num trecho do começo e num do fim (`boca.py`, `boca_cv.py`).

### 3. Transcrição
`transcrever.py` na gravação da voz, em segundo plano. Mais de 30 min: em 4 partes ao mesmo tempo
(`--inicio`/`--fim`, 15 s de sobreposição) e `juntar_transcricao.py`. Faça uma cópia corrigida pra legenda
(`transcricao/legenda.json`): o Whisper escreve "Cloud Code". Enquanto roda, leia `formato.md` e `estilo.md`.

### 4. Momentos
Descubra o tipo do vídeo (`tipos-de-video.md`) e escolha os candidatos. Pra cada um, escreva as frases que entram
(na ordem do Short, não do vídeo) e a ideia de motion de cada frase. Salve em `momentos.json`.

**PARADA 1.** Mostre os candidatos numa tabela curta: a tese de cada Short, as frases, a duração estimada. Pergunte
se ele quer **um Short por item ou o Short da tese do vídeo inteiro**. Se ele já disse "escolhe você", siga.

### 5. O roteiro de falas
1. Ache cada frase (`achar.py`) e acerte as pontas pelo volume (`pontas.py`). Leia a transcrição em volta: recado
   dele pro editor ("vou refalar essa frase") marca tomada ruim.
2. Escreva o `roteiro-base.json` (frases inteiras; formato em `plano.md`) e o `falas.json`.
3. `palavras_falas.py` no roteiro-base; corrija nomes de produto à mão.
4. `pedacos.py` e `roteiro_pedacos.py`: sai o `roteiro.json` sem as pausas. Confira com `conferir_pontas.py`.
5. `rostos.py`: marque em quais falas ele olha pra lente. Só nelas ele aparece.
6. `preparar_cena.py`. Duração: até 2 min (120 s), sem mínimo; o tamanho é o que a tese pede (regra em
   `formato.md`, "Quanto dura"). Se passou de 120 s, tire uma frase inteira, não aperte as outras.

### 6. O material real
- **Capturas** da gravação de tela no instante certo, em resolução cheia:
  `ffmpeg -ss <t + atraso da tela> -i <tela> -frames:v 1 -q:v 2 material/<nome>.jpg`. Uma por tela que a cena usa.
- `fundo_sala.py` pro cenário dele. Copie `assets/audio/*` desta skill pra `material/audio/`: são a trilha e os
  efeitos da versão 1, que não custa nada. No acabamento eles são trocados (passo 9).
- O que ele digitou na gravação (o pedido, o comando): copie o texto exato, pra redigitar na cena.
- Texto e número que vão aparecer: liste de onde cada um vem (fala ou tela). O que não tem origem não entra.

### 7. A cena
Copie `assets/cena/esqueleto-cena.html` pra `cena/motion.html`. Os ajudantes já vêm prontos; as cenas você escreve
do zero, uma por parte do roteiro, cada entrada amarrada à palavra em que ele diz a coisa (`motions.md`).
`assets/cena/exemplo-aprovado/motion.html` mostra como a versão aprovada resolveu cada parte: é pra consultar a
técnica, não pra trocar os textos.

Trabalhe em voltas curtas: escreva uma parte, `motion.py olhar cena <tempos>`, abra o `olhar.jpg`, conserte. Olhe
sempre as passagens (ele entrando e saindo, troca de material) em 4 ou 5 instantes seguidos. Depois `render`,
`plano_da_cena.py` e `compor.py montar`. Faça a revisão quadro a quadro de `formato.md` antes de mostrar.

### 8. A versão 1 e o orçamento
**PARADA 2.** Entregue a versão 1 (link clicável, caminho da pasta e a cópia leve pelo app) dizendo o que ela tem e
o que você não consegue conferir (você não ouve). Junto, o orçamento do acabamento (`orcamento.md`, modelo em
`higgsfield.md`), com o preço de cada item consultado na hora e o saldo:

- **Sempre no pacote:**
  - **trilha nova** do tamanho do Short, parecida com a `trilha-ia.mp3` (preço pelo `estimate_audio_cost`);
  - **um efeito sonoro gravado pra cada animação**, do catálogo de sons do Higgsfield: diga quantos sons novos
    vão ser baixados e quantos já estão na biblioteca `_sons`;
  - **recorte dele** (1 crédito por pedido): é o que faz a janela passar atrás da cabeça; sem ele, ela fica acima.
- **Planos gerados**, os que fizerem sentido pro vídeo: câmera 2, entrada no monitor, tela do PC.

Sem o "pode", nada é gerado nem baixado. Um teto dado no pedido ("pode gastar até 200") vale só pra aquela rodada.

### 9. Acabamento pago
Antes de trocar qualquer coisa, `guardar_versao.py`: a versão 1 que ele viu não é sobrescrita.

**Trilha e efeitos** (detalhes em `higgsfield.md`, "A trilha nova" e "Efeitos sonoros"):
- **Trilha:** gere a faixa com o som da `trilha-ia.mp3` descrito no pedido e meça antes de mostrar (andamento,
  pulso, graves, volume constante). Monte a versão com ela, corte os primeiros ~15 s dela e da mesma versão na
  trilha padrão (`ffmpeg -t 15`) e junte os dois em sequência com `comparar.py seq`, pra ele escolher. Ele pode
  ficar com a padrão.
- **Efeitos:** liste cada `Motion.sfx` da cena (tempo e o que se mexe), escolha um som gravado pra cada movimento
  (busca no catálogo é livre; baixe só os escolhidos), meça, apare, troque o arquivo no `Motion.sfx` e refaça só a
  pista com `motion.py som`. Som que já está em `_sons` não se baixa de novo. Depois, `compor.py montar`.

**Planos gerados**, um item por vez, do mais barato pro mais caro, sempre nesta escada (`higgsfield.md`):
**foto** (0,25) → ele escolhe → **rascunho do vídeo** (15) → você confere e **põe o rascunho dentro do Short** →
lado a lado com a versão atual → ele decide → **preço da finalização consultado na hora** → finalização.
Um plano que ele aprova sozinho pode ser reprovado dentro do Short; por isso a decisão é sempre no Short.

### 10. Rodadas de ajuste
Ele vai pedir mudanças, e cada rodada vira uma versão nova:

- Antes de mexer: `guardar_versao.py`. O nome do arquivo sobe (`-v2`, `-v3`...). Nada que ele viu é sobrescrito.
- Duas ideias pro mesmo trecho: escreva as duas na mesma cena, escolhidas por uma linha em `cena/variante.js`
  (`window.VARIANTE = 'a'`), renderize uma depois da outra (o render sobrescreve `cena.mp4`) e entregue as duas
  mais o lado a lado só do trecho (`--de`/`--ate`).
- Se ele gostar de uma coisa de cada versão, a próxima junta as duas.
- Mudou o roteiro (cortou o fim, tirou uma frase): `preparar_cena.py --so-dados`, `plano_da_cena.py`, `render`.
- Voltar pra uma versão anterior tem que ser trocar uma linha ou copiar a pasta `_versao-N`.

### 11. Entrega
**PARADA 3.** Em poucas linhas:
- link clicável do vídeo final e o caminho da pasta; o lado a lado, se houve mais de uma versão;
- o que mudou e o que você conferiu (quadros, pontas da fala, sincronia de 0 ms);
- **o que você não consegue conferir**: você não ouve. Peça pra ele checar o volume da trilha e os efeitos novos;
- se há plano gerado dele ou fala gerada (ele decide se marca "conteúdo alterado" no YouTube);
- créditos gastos de verdade (saldo antes menos depois, conferido com `transactions`: ele também gera coisas no
  site) e o saldo;
- **sugestões de melhoria**, só depois que tudo estiver finalizado: de 3 a 5 ideias concretas do que ainda deixaria
  o Short melhor (no corte, nos motions, no som ou no que o Higgsfield pode criar), cada uma com o trecho, o que
  muda na tela e o preço consultado quando custa. Só ideias que melhoram o material real (cena de IA ilustrando a
  fala foi reprovada, `estilo.md`). Nenhuma é feita sem ele pedir.

Arquivo acima de ~10 MB falha no envio pelo app: mande a cópia leve
(`ffmpeg -i v.mp4 -vf scale=720:-2 -crf 24 -c:a aac -b:a 128k v-leve.mp4`) e diga onde está o de qualidade cheia.

Não publique nada. No fim, atualize `references/historico.md` e, se uma regra nova apareceu, `estilo.md`.

## Regras que valem sempre

- **Crédito só com o "pode" dele**, e o "pode" vale pra aquela rodada. Consultar preço, saldo e catálogo é livre.
  Se um pedido já tinha sido cobrado quando ele mandou parar, diga.
- **O rosto e a fala reais dele não passam por IA** sem ordem dele naquele vídeo. Plano gerado dele é sempre uma
  câmera a mais, curta, nunca a principal.
- **Texto na tela só se for fato** da fala ou da tela dele. Nada de "%", código, rótulo ou paráfrase inventados.
- **Não ponha palavra na boca dele** e não corte a ressalva que torna uma afirmação verdadeira.
- **Ele só aparece onde olha pra lente**, no cenário real dele.
- **O que você mostra é julgado como vídeo pronto.** Revise no detalhe e melhore antes de mostrar.
- **Na dúvida entre mais efeito e mais limpo, mais limpo.** Na dúvida entre menos motion e mais motion que
  explica, mais motion.
- **Meça antes de trocar de ferramenta.** Emenda que "buga" quase sempre é velocidade pulando, não o modelo.
- **Não batize nada com o tema do vídeo da vez.** Pastas são `short-01`; a skill serve pro canal inteiro.
- **Nada de nome próprio nos arquivos da skill.** Ao atualizar `historico.md` e `estilo.md`, escreva "o criador" e
  "o canal", sem o nome da pessoa nem do canal: a skill é compartilhada com outras pessoas.
- **As gravações brutas ficam onde estão**; você só lê. Nenhuma versão entregue é apagada.

## Se algo não bater

- `motion.py` imprime "ERRO NA PÁGINA": erro de JavaScript no `motion.html`. Movimento pulando entre renders:
  algo não é função do tempo (`transition`, `animation`, `setTimeout`, `Math.random`).
- Quadro dele congelado ou faltando: o `dados.js` não bate com `quadros/cam` (rode o `preparar_cena.py` sem
  `--so-dados`) ou a cena pede um quadro além do fim.
- A legenda adianta uma palavra depois de pausa: use as palavras do `palavras_falas.py`, não as da transcrição
  inteira.
- `compor.py` falhou: ele mostra o fim do erro do ffmpeg; quase sempre é caminho errado no plano.
- Um modelo mudou de nome ou de preço: confie no que o catálogo responder hoje e atualize o `higgsfield.md`.
- Texto de tela gravada em 2560 px fica pequeno no celular: aproxime, ponha lente, ou redigite o texto real.
- Gravação só em **composto** (tela com a webcam no canto): a webcam ampliada fica borrada. Avise na PARADA 1 e
  deixe ele pequeno, com mais material e motion.
