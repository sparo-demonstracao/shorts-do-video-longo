# Motions: animações feitas por você, de graça

Um motion é uma animação que você escreve em HTML e o `motion.py` renderiza quadro a quadro. Não usa o Higgsfield
e não gasta crédito. **No formato aprovado o Short inteiro é um motion só** (a "cena",
`short-XX/cena/motion.html`), com um motion de explicação pra quase toda frase; os que ele aprovou nesse formato
estão listados em `formato.md`. É o que mais diferencia os vídeos do canal: os melhores motions que o criador já teve foram
feitos assim, e ele pediu que continuem melhorando.

**O que ele pediu, com as palavras dele:** a skill deve usar "a mesma lógica" dos exemplos, e não fazer "sempre
idêntica". Ela é "livre pra criar outros estilos de animação caso faça mais sentido pro vídeo". Então este
arquivo ensina a lógica e o ofício. O visual você decide a cada vídeo.

## Os exemplos

Em `assets/motion/exemplos/` há quatro folhas de quadros de motions que ele aprovou (feitos pro vídeo longo, em
16:9). Abra as quatro com Read antes de criar o primeiro motion de uma sessão:

| Folha | O que acontece | A ideia por trás |
|---|---|---|
| `1-como-foi-feito-por-dentro` | A tela recua; ao lado, uma curva se desenha ponto a ponto com as coordenadas, vira uma peça em arame e depois sólida; entram "33 pontos girados em torno de um eixo" e "0 modelos baixados" | Mostrar **como a coisa foi feita por dentro**, que a tela sozinha não mostra |
| `2-grade-de-resultados-com-numeros` | A tela recua e vira uma de seis miniaturas reais; sobem "1 prompt cada" e "0 correções"; cada miniatura ganha o tamanho do arquivo | Juntar **vários resultados reais** num quadro só, com os números que ele fala |
| `3-fluxo-de-dados-em-volta-da-tela` | O painel real recua; em volta surgem a loja, a lista de pedidos, o sistema da empresa, com linhas e bolinhas levando os dados até o painel, que continua vivo | Desenhar **o caminho** que explica o que a tela está mostrando |
| `4-camadas-em-3d-e-lista` | As telas passam em carrossel ("front-end"), uma delas inclina em 3D e revela as camadas de trás ("back-end"), que viram a lista de aulas | Dar **profundidade literal** a uma ideia de "o que está por trás" |

## A lógica que não muda

1. **Nasce da fala.** O motion existe pra mostrar o que ele está dizendo naquele instante e a tela não mostra:
   como funciona por dentro, quantos, comparado com o quê, de onde vem e pra onde vai. Se a gravação de tela já
   mostra a ideia, não faça motion.
2. **Parte do material real e volta pra ele.** A gravação continua viva dentro do motion (recua, vira cartão,
   inclina, ganha camadas) e no fim retoma o quadro. O motion é uma explicação montada em volta do que é real,
   nunca um slide que substitui o vídeo.
3. **Desenhado pra aquele momento.** As formas vêm do próprio assunto: a curva da peça, as miniaturas dos
   resultados reais, o caminho do pedido. Ícone genérico, card de template e gráfico inventado são o que faz um
   motion parecer feito por máquina.
4. **Cada coisa entra na palavra em que é dita.** Tire os tempos das palavras com `achar.py --entre` e amarre
   cada entrada a uma palavra. Motion adiantado ou atrasado em relação à fala perde o efeito.
5. **O que está escrito é verdade.** Número, nome e afirmação vêm da fala dele ou da tela. Cartão ilustrativo
   (uma lista de pedidos de exemplo) pode, desde que ilustre o que ele descreve e não passe por dado real.
6. **Tem som.** Cada movimento importante leva um efeito curto no mesmo instante (`Motion.sfx`).

## A liberdade de estilo

Os quatro exemplos são de uma mesma família (palco quase preto, brilho laranja embaixo, cartões escuros,
Montserrat). É um bom padrão, e não é o único. Antes de desenhar, pergunte: **que linguagem visual o assunto
deste vídeo já tem?** Alguns caminhos, pra abrir a cabeça:

- **A linguagem do próprio produto na tela:** as cores, a tipografia e os cantos do app que ele está mostrando,
  estendidos pra fora da janela.
- **Desenho técnico:** grade fina, cotas, traço que se desenha, fonte de código. Bom pra "como foi construído".
- **Terminal e código vivos:** texto que se digita, linhas que acendem, diff que entra. Bom pra Claude Code.
- **Tipografia em movimento:** a frase dele ocupando o quadro, palavra por palavra, com peso e escala mudando.
  Bom pra afirmação forte de vídeo de notícia.
- **Placar ou ringue:** dois lados, pontos que sobem, uma faixa que pende. Bom pra comparativo.
- **Linha do tempo ou mapa:** uma régua que anda, pontos que acendem. Bom pra lançamento ("o que mudou").
- **Papel e rabisco:** traço de caneta, seta torta, círculo em volta. Bom quando o tom é de conversa.
- **Camadas em 3D:** planos que se separam em profundidade com `perspective` e `rotate`.

Três âncoras seguram a identidade enquanto o estilo muda:
- o laranja `#FF6B18` como cor de destaque (creme `#F3EDE6` e fundo `#0c0a0a` são o padrão, não a regra);
- texto que se lê num celular;
- **um estilo por vídeo longo**: todos os Shorts do mesmo vídeo usam a mesma linguagem. Entre vídeos, varie.

Se um motion anterior ficou bom, não o copie: descubra por que ficou bom e leve só isso adiante.

## Quando usar

- **Em toda fala em que ele não está em cena.** Ele pediu mais motion em todas as rodadas ("senti falta de mais
  motions que ajudem na explicação"; "quero mais motion graphics nesse vídeo"). A cena nunca fica só com a tela
  parada: ou a câmera anda por dentro da captura mostrando o que ele cita, ou um motion explica a frase.
- Nas falas com ele em cena, o motion é discreto e fica no alto: a janela viva atrás da cabeça, um número da
  fala em letra gigante, uma etiqueta, um selo.
- Proponha a ideia de cada um já na lista de momentos, em uma frase: "a página encolhe e vira cartão; a caixa do
  Claude Code entra no meio e o link voa até ela".
- Gatilhos na fala: "por trás disso", "funciona assim", um número ("em menos de 1 hora"), uma comparação, uma
  sequência ("primeiro... depois..." vira barra de passos), uma lista curta (uma lente por item), "virou",
  "transformei", "clonei" (uma coisa virando outra).
- Não use pra enfeitar frase sem conteúdo visual nem pra repetir o que a legenda já diz. Mais motion não é mais
  coisa na tela ao mesmo tempo: duas ou três se mexendo por vez.

## O quadro vertical

- 1080x1920, 30 fps. O que importa fica entre x 40 e 1040 e entre y 90 e 1520: abaixo disso a descrição e os
  botões do YouTube cobrem (uma barra de passos discreta coube em y 1640, mas texto que precisa ser lido, não).
- Texto: corpo com 34 px ou mais, rótulo com 28 ou mais, número de destaque com 120 ou mais.
- **Legenda:** desenhada pela própria cena (`Palco.legendas`), com o centro em y 1480 quando ele está em cena e
  1330 sobre material. Onde um texto da cena já diz a fala (o pedido digitado, o número gigante), desligue a
  legenda naquele intervalo (`mudos`). Passe os instantes de troca de cena em `quebras`, pra um grupo de
  palavras não atravessar a troca.
- **Abertura em tela cheia sem ele:** até ~1,3 s. Depois disso ele tem que estar em cena ou a caminho.
- **Passagens:** ele sobe de baixo ao entrar e desce ao sair, com a sala surgindo junto; a janela vira tela cheia
  e a tela cheia vira cartão por movimento, nunca por corte. Entre um plano gerado e a cena, a cena começa no
  mesmo enquadramento e na mesma velocidade em que o plano termina.

## Ofício

- **Nada linear.** Entrada desacelera (`ease.fora`, `fora5`), saída acelera (`dentro`) e é mais curta que a
  entrada. Mola e "passa e volta" só em um ou dois elementos por motion.
- **Escalonado.** Itens de um grupo entram com 60 a 120 ms de diferença, nunca juntos.
- **Tempo de leitura.** Todo texto fica parado pelo menos 1,2 s depois de entrar. Número grande, 1,5 s.
- **Duas ou três coisas se mexendo por vez.** O olho segue uma; o resto espera a vez.
- **Parado não é morto.** Elemento que já chegou respira de leve (`Motion.onda`): um flutuar de 3 a 5 px.
- **Cada tipo de momento tem a sua entrada.** A mesma entrada repetida no motion inteiro é o que mais denuncia
  template.
- **Traço que se desenha, número que conta, texto que se digita, bolinha que viaja na linha**: são os recursos
  que ele elogiou. Imagem parada com fade ele chamou de "muito básico".
- **Profundidade:** sombra, desfoque de entrada, leve inclinação em 3D. Achatado e centralizado parece slide.

## Passo a passo (cena única)

Depois do `preparar_cena.py` (ver `plano.md`), a pasta `short-XX/cena/` tem `dados.js`, `kit.js` e `quadros/cam`.

1. **Planeje no papel.** Liste as falas com o tempo em que cada uma entra (o `preparar_cena.py` imprime) e as
   palavras-chave de cada uma. Pra cada parte do roteiro, escreva o que está na tela e o que entra em cada palavra.
2. **Copie `assets/cena/esqueleto-cena.html` pra `cena/motion.html`** e escreva as cenas. Regra única do motor:
   tudo é função do tempo. `Motion.quadro(t => {...})` recebe o tempo e põe cada elemento no lugar. Sem
   `transition`, `animation`, `setTimeout`, `Date` ou `Math.random()` solto (acaso, só com semente).
   Amarre os tempos às palavras com `na(t0, t1, 'palavra')`: ele dá erro se a palavra não existir, o que é melhor
   do que animar na hora errada.
3. **Olhe os instantes que importam:** `python S/motion.py olhar short-01/cena 0 0.5 1.2 2.0 ...` (o começo, cada
   entrada assentando, o pico, cada passagem em 4 ou 5 instantes seguidos, o fim). Abra `cena/olhar.jpg`; pra ver
   um quadro em tamanho real, `cena/olhar/<tempo>.jpg`.
4. **Critique antes de renderizar:** com o som desligado, dá pra entender? Tem algo pra olhar em cada instante?
   Algum texto pequeno, cortado, inventado ou em cima do rosto? Parece um slide? Compare com a folha do exemplo
   aprovado e conserte tudo de uma vez.
5. **Renderize:** `python S/motion.py render short-01/cena` (uns 4 min pra 38 s; uns 13 min pra um Short de 2 min). Sai `cena.mp4` e `cena-sfx.wav`.
   Cada render sobrescreve os dois: variantes se renderizam uma depois da outra, montando cada uma antes da próxima.
6. **Monte:** `plano_da_cena.py` e `compor.py montar`. Olhe uma folha do vídeo montado nas passagens.

**Duas ideias pro mesmo trecho.** Ponha `<script src="variante.js"></script>` antes do `dados.js`, leia
`const VAR = window.VARIANTE || 'padrao'` e ramifique só o trecho que muda. O arquivo `cena/variante.js` tem uma
linha (`window.VARIANTE = 'a';`). Assim voltar atrás é trocar essa linha.

**Plano gerado dentro da cena.** Vira uma pasta de quadros no tempo do encaixe
(`ffmpeg -ss <de> -t <dur> -i take.mp4 -vf "fps=30,crop=...,scale=1080:1920:flags=lanczos" -frames:v <n> -q:v 2 cena/quadros/insX/%05d.jpg`)
e uma camada `<div class="ins" id="insX"><img data-dir="quadros/insX"></div>` logo antes de `#legendas`, ligada por
`ins('insX', t, [qd(k0), qd(k1), n])`. Câmera 2 com ele falando entra no mesmo tempo da fala (o `-ss` é o tempo
da palavra dentro do take), sem acelerar.

**Som.** `Motion.sfx(t, arquivo, volume, {dur, corte, entra, sai})` marca um efeito gravado no instante `t` (os
arquivos estão em `material/audio/`, copiados de `assets/audio/`). Um por movimento que importa: passagem no que
entra de lado, estalo no que acende, teclado em cada palavra digitada, impacto no número gigante e no fecho.

## O palco (`comum/palco.js`) e os ajudantes do esqueleto

`palco.js` (carregue depois do `kit.js`) faz a cena só carregar os quadros das gravações que estão visíveis e traz:

| Função | Pra quê |
|---|---|
| `Palco.legendas(palavras, {destaques, mudos, quebras, max, chars})` | Devolve `desenha(t, yCentro)`: legenda palavra por palavra |
| `Palco.entre(a, b, p)` | Mistura duas caixas `{x, y, w, h, r}` (janela virando tela cheia, cartão mudando de lugar) |
| `Palco.cartao`, `Palco.camera`, `Palco.fato` | Cartão com entrada/respiração/saída, ele mudando de tamanho, número com rótulo |
| `<img data-dir="quadros/cam">` + `img.dataset.quadro = n` | Gravação tocada pela cena: ela escolhe o quadro a cada instante |
| `img.dataset.dormindo = '1'` | A gravação que não está em cena não carrega quadro (o render fica rápido) |

O esqueleto traz, prontos pra usar: `mat` (captura real com caixa e câmera própria), `cartao`, `lente`, `mira`,
`etq` (etiqueta), `fio` e `bola` (linha que se desenha e bolinha que viaja), `selo`, `ins` (plano gerado), `ele`
(ele no cenário real, entrando e saindo), `rampa` (valor que anda entre instantes) e `na`/`entre` (tempo de palavra).

## O kit (`kit.js`)

Caixa de ferramentas. Ele não decide visual nenhum; use o que servir e escreva o que faltar.

| Função | Pra quê |
|---|---|
| `Motion.config({dur, fps})` | Duração do motion (use `MOTION_DADOS.dur`) |
| `Motion.quadro(fn)` | Registra uma função `fn(t)` chamada em todo quadro |
| `Motion.faixa(t, a, b, ease)` | Progresso de 0 a 1 entre dois tempos |
| `Motion.janela(t, a, b, dIn, dOut)` | Presença: sobe em `a`, desce antes de `b` |
| `Motion.mix(v0, v1, p)` | Mistura dois valores |
| `Motion.ease.*` | `fora`, `fora5`, `dentro`, `dentroFora`, `volta`, `mola`, `linear` |
| `Motion.entra(el, t, t0, {dur, dy, dx, blur, escala, ate})` | Entrada com subida e desfoque; saída opcional |
| `Motion.parte(el, 'palavra' \| 'letra')` | Parte um texto em pedaços animáveis |
| `Motion.escalona(els, t, t0, passo, fn)` | Aplica uma animação com atraso crescente |
| `Motion.conta(el, t, t0, dur, de, ate, {casas, antes, depois})` | Número que conta |
| `Motion.traca(path, t, t0, dur)` | Traço de SVG que se desenha |
| `Motion.noCaminho(path, p)` | Ponto ao longo de uma linha (bolinha que viaja) |
| `Motion.digita(el, t, t0, porSegundo)` | Texto que se digita |
| `Motion.onda(t, periodo, fase)` | Oscilação suave pra respirar e flutuar |
| `Motion.sfx(t, tipo, volume)` | Marca um som: `vuush`, `pop`, `tique`, `plim`, `subida`, `baque` |
| `<img data-seq="tela">`, `<img data-seq="cam">` | Gravação real tocando no motion; `data-inicio` atrasa o começo |

`assets/motion/exemplo-tecnicas.html` mostra todas essas técnicas num motion só (recuo, mira, fio, curva com
pontos, contador, palavras, mola, retorno). É pra consultar **como se escreve**; não é modelo de visual.

**GSAP** é opcional e funciona: carregue
`https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js`, monte uma `gsap.timeline({paused: true})` e
chame `Motion.gsap(tl)`. Vale quando a sequência é longa e encadeada; precisa de internet na hora de renderizar.
Fontes do Google Fonts também precisam.

## Se der errado

- `olhar` ou `render` imprime "ERRO NA PÁGINA": é erro de JavaScript no `motion.html`. Conserte e rode de novo.
- Quadro da gravação congelado: o `--out` passou do fim do arquivo (o `motion.py` avisa ao extrair).
- Fonte diferente da esperada: sem internet o Google Fonts não carrega e entra a Segoe UI.
- Movimento "pulando" entre um render e outro: alguma coisa não é função do tempo (procure `transition`,
  `animation`, `setTimeout`, `Math.random`).
