# Histórico das rodadas

Diário do que foi feito e do que o criador respondeu, na ordem. Consulte quando precisar do contexto de uma decisão;
as regras que saíram daqui já estão em `estilo.md` e `formato.md`. Acrescente uma seção por rodada nova.

## Rodada 1: "Instalei esses repositórios no Claude Code e não volto mais" (12/11/2026)

Pasta `shorts-canal\repositorios-github\`. 2h03 de gravação bruta. Gasto: 31,09 créditos.

| Versão | O que era | Veredito |
|---|---|---|
| v1 | Tela em cima, ele embaixo, cortes secos, um motion | Reprovada: "ficaram ruins, mesmo pra um esboço, os textos ficaram com estilo AI Slop, tem poucas animações"; um com áudio fora de sincronia |
| v2 | Cena animada única, 44 s, sem texto inventado | "Quase inaproveitável", "bem fraca": vídeo longo espremido, acabamento de máquina |
| v3 (só o ScrollCraft) | 25 s: site regravado em vertical, ele recortado na frente, pedido digitado, trilha e efeitos | Do visual não reclamou. Reprovada: áudio cortado no fim dos trechos; ele em destaque sem olhar pra câmera; rápida e pouco explicativa |
| v4 | 46,8 s, roteiro explicativo, ele só onde olha pra câmera | Sem veredito |

Pedidos dele nessa rodada: o Short da tese com pelo menos 3 repositórios; "antes de gerar os detalhes no
Higgsfield peça minha aprovação"; "não vou regravar nada".

## Rodada 2: "Agora Qualquer Pessoa Clona Qualquer App" (12 e 13/11/2026)

Pasta `shorts-canal\clonar-qualquer-app\`. 1h37 de gravação (voz no Audition, tela no OBS, câmera no
celular). Um Short, o da tese. Gasto total: cerca de 400 créditos, quase tudo em testes de plano gerado.

| Versão | O que mudou | Veredito |
|---|---|---|
| v1 | Formato da v2 dos repositórios | "Crie outra versão" |
| v2 (43 s) | Material real em tela cheia, ele recortado na frente, pedido digitado | "Silêncios desnecessários", recorte "bem amador", "senti falta de mais motions", música "que remeta a inteligência artificial", "revise o vídeo no detalhe e melhore ele" |
| v3 (38,6 s) | Sem as pausas; ele no cenário real com a janela atrás da cabeça; diagramas e lentes; trilha nova | Não comentou; pediu pra testar melhorias com o Higgsfield (teto de 200) |
| 7 testes | Cenário estendido, mãos digitando, entrada no monitor, boca sincronizada com fala gerada, efeitos prontos, trilha, diagnóstico | "O teste 3 [entrada no monitor] foi o que ficou melhor, mas... dá uma bugada quando, de fato, entra no monitor"; pediu segunda câmera com Seedance |
| Pacote 2 (A a D) e segundas versões (B2, C2, D2) | Entrada corrigida, câmera 2 por trás, câmera 2 de lado falando, Discord virando o clone | Gostou da abertura D e do take C2 ("poderia ser mais aproximado"); a entrada "quase boa", "não ficou fluido"; "as demais achei inaproveitáveis" |
| v4 | v3 + os 4 planos gerados | (o veredito acima) |
| v5 | Entrada no monitor refeita com movimento contínuo, sem os planos reprovados | |
| v6 | + câmera 2 (C2 finalizado e aproximado), time-lapse na tela do PC, barra de passos, link voando, selos | Preferiu a v6 entre três, mas o clone sendo feito ficou escondido atrás da câmera 2; pediu "2 versões novas muito melhoradas dessa parte" |
| v7a / v7b | A: varredura inteira antes da câmera 2. B: peças voando entre dois cartões, câmera 2 mais tarde | "Preferi a versão A mas a duração da B ficou melhor"; e a abertura gerada "ficou ruim, tá mal formatado e poluiu o início": quis um motion de tela cheia |
| **v8** | Abertura em motion próprio de tela cheia; câmera 2 só em "aplicativo"; depois, o fim cortado na última palavra | **A escolhida** |
| v9 | v8 com a câmera 2 trocada por um take de ângulo alto (rascunho 480p) | "Preferi a versão antiga, vou continuar com ela" |

Erros meus nessa rodada, pra não repetir:
- Ele aprovou finalizar um take por 35 créditos e a finalização do rascunho cobrou 80. Consulte o preço da própria
  chamada de finalização.
- Um rascunho de 15 créditos ficou pronto e foi cobrado depois que ele mandou parar pra corrigir a foto. Mostre a
  foto e espere o "essa" antes de mandar o vídeo, mesmo que ele já tenha escolhido: defeito de foto ele vê depois.
- Segurei 0,55 s no fim "pra ele sustentar o olhar". Ele mandou tirar.
- Gastei quase 10 minutos tentando achar quadros de perfil por programa. A folha de miniaturas resolve em 1.

O que essa gravação ensinou sobre sincronia: a imagem do celular estava junta com o som no começo e ~0,16 s
atrasada com 1h35. A medida automática por estalos (`medir_boca.py`) deu inconclusiva; o que funcionou foi o
`boca_cv.py` mais a folha do `boca.py` num trecho do começo e num do fim.

Como ele grava (vale pros próximos): três arquivos que não começam juntos (tela no OBS em `Videos\*.mkv`, voz no
Audition em `Documentos\Adobe\Audition\*VO.wav`, câmera no celular em `Videos\S23 FE\...` ou `Downloads`), umas
2 h de bruto pra 12 min de vídeo. A câmera é um close, sem espaço acima da cabeça, com o microfone na frente do
peito.

## Rodada 3: "Como criar o MELHOR Agente de IA para Whatsapp do Brasil?!" (18/11/2026)

Pasta `shorts-canal/agente-ia-whatsapp/`. 1h41 de bruto (voz em mp3 no Downloads, tela no OBS, câmera
no celular) e um remendo de 2 min. Um Short, em duas versões. Gasto até a versão 1: 0 crédito.

A escolha do trecho levou cinco idas e vindas, todas no texto, antes de qualquer montagem:

| O que eu propus | O que ele respondeu |
|---|---|
| 4 candidatos (tese, API oficial, 4 pilares, linear x agente) | "Quero que esse vídeo ensine algo e que tenha necessariamente um excelente gancho" |
| Os 4 pilares, com gancho e definições costuradas | "O que vai ser falado no vídeo? Me envie antes de criar"; depois "achei ruim as falas, vai acabar ficando robotizado, tem outro trecho?" |
| Três tomadas contínuas (cliente chato, API oficial, quando não usar agente) | "Não tô gostando do gancho, de fato parece que foi cortado de outro vídeo" |
| Três aberturas que nasceram como abertura (preço, agente sem ferramentas, janela de 24 h) | "Gostei da opção 1, mas queria explicar um pouco mais o que esse agente de IA é capaz de fazer, logo depois de 'por dezenas de milhares de reais', sem demorar tanto nessa seção" |
| Bloco de 15 s com falas da introdução; depois a lista do que ficou de fora | "Quero 2 versões, [uma] que inclui somente a funcionalidade de pausar o agente e outra com todas essas explicações também" |

Versões 1: `short-01` (curta, 64,6 s) e `short-02` (completa, 114,6 s), as duas com o aviso "COMENTA AGENTE" no modo
'b'. A mesma `motion.html` nas duas pastas; o `secoes.js` de cada uma liga ou desliga as partes extras.

O que essa gravação ensinou:
- **Material claro** (painel creme, planilha, calendário): a legenda creme some em cima dele. A cena ganhou um véu
  escuro no pé (`#veu`) sempre que há captura clara em tela cheia, e os pontos de interesse ficam acima de y 1150.
- **Tela cheia de branco vazio é feia.** O painel dele tem muito espaço em branco: aproxime na lista ou nos balões, ou
  leve a explicação pro palco escuro com lentes das faixas reais (foi o caso de "pausar o agente").
- **Câmera em close** (o rosto ocupa 55% da altura): com escala 1,15 e o quadro 126 px acima do pé, o queixo fica em
  ~1380 e a legenda de 1480 cai no peito; a janela (y 96 a 658) fica acima do cabelo. A máscara do alto da câmera
  desce só 7%, senão come o cabelo.
- **Sincronia**: som alinhado por `atraso.py`; no fim da gravação (1h38) a imagem do celular chegava ~2 quadros depois
  (medido nos lábios em "Botox", "empresas" e "painel"; o `boca_cv.py` deu +5 com semelhança perto de zero, não
  serviu). Somei 0,06 s ao atraso da câmera de 5870 em diante e conferi de novo nos quadros extraídos.
- **A transcrição** rodou na GPU com o python do venv de `Downloads/transcricao-masterclass` (o python normal caiu na
  CPU, lento demais pra 1h41); o `palavras_falas.py` roda bem na CPU.
- **Preço no Higgsfield mudou de lugar**: `get_cost` não é mais aceito em `generate_*`; use `estimate_audio_cost` e
  `estimate_video_cost` (trilha de 65 s: 9,45; de 115 s: 16,72; Kling 4.0 de 5 s: 16,25).

Finalização (mesmo dia): ele respondeu "Segue com ambas, quero finalizar as 2 versões". Fiz só o que eu tinha
recomendado no orçamento: uma trilha do tamanho de cada versão e um recorte dele (um pedido, usado nas duas). Gasto:
27,17 créditos (9,45 + 16,72 + 1). Versões 2: `short-01-v2.mp4` e `short-02-v2.mp4`, com a janela passando atrás da
cabeça e o volume das tomadas igualado (`ganho_db`, novo no `compor.py`: as falas da introdução estavam ~3 dB mais
altas que as do fim da gravação).

Veredito dele sobre as versões 2: "Quero que a trilha sonora tenha um estilo mais parecido com Hans Zimmer, um estilo
mais ficção científica mas que comporte em um vídeo tutorial de Inteligência Artificial. [...] tem alguns trechos
onde a última palavra da frase foi cortada e outras que a pausa está mais longa que deveria. Além disso as animações
ficaram fracas, dava pra fazer algo muito mais trabalhado, as partes que usam print ficaram mal formatadas, criar uma
animação pra demonstrar vai ficar visualmente melhor e vai deixar mais fácil entender os conceitos do vídeo."

Versões 3 (mesmo dia), sem crédito:
- **Voz**: cortador novo só pra este vídeo (`tmp/pedacos2.py` na pasta do vídeo: pausa = abaixo de -36 dB por 0,17 s;
  fim de frase com cauda e fade). A palavra cortada era "oficial" no fim do gancho (a v2 parava em "ofici-"). Na
  primeira tentativa eu tirei o "que" de "que você consegue vender" achando que ele estava na tomada anterior; a
  transcrição do mp4 pronto mostrou a falta e eu devolvi.
- **Cena**: `motion.html` refeita do zero, sem nenhuma captura. Conversa de WhatsApp, diagrama (WhatsApp, agente,
  painel do dono), relógio de 24 h, áudio e imagem virando texto, calendário, planilha, painel com botão de pausar e
  cursor clicando, CRM, remarketing; na completa, base de conhecimento, mensagem picotada, criador de modelos, agenda
  e funil. Tudo com os textos e números reais das telas dele.
- **Recorte dele**: o da v2 reaproveitado com `tmp/rec_remapa.py` (cada quadro novo acha o recorte do mesmo instante
  da gravação), sem pedir de novo.
- **Trilha**: a geração no estilo pedido (9,45 + 16,72 créditos) foi barrada pelo aplicativo por falta do "pode"
  explícito. As versões 3 saíram com a trilha da v2 e a pergunta foi feita na entrega.

Versões 4 (mesmo dia): ele respondeu "Pode gerar as duas trilhas novas". A de 115 s falhou uma vez e saiu na segunda
(16,72). A de 65 s falhou quatro vezes seguidas no Higgsfield ("Something went wrong", com 65 s e com 66 s), todas
reembolsadas: a curta ficou com os 64,7 s finais da trilha de 115 s, sem emenda no meio. A trilha de 115 s acabava em
~110 s e o vídeo tem 114,4 s: estiquei 3,5% (`atempo`) pra o final cair no fim. Gasto das versões 4: 16,72; saldo
1.901,81. Só troquei a trilha no plano e montei de novo, sem renderizar a cena.

Versões 5 (mesmo dia). Retorno dele sobre a v4: "Ficou bem melhor, mas em algum momento do início desse agente de IA
nós precisamos mostrar o painel do dono original porque ficou muito abstrato pra entender que de fato esse é um agente
de IA criado 100% no Claude Code e do zero. A trilha sonora ficou calma demais, relaxante até, não combinou com o ritmo
do vídeo." O que mudou:
- **Painel real na abertura** (8,45 a 12,4 s, na frase "e tem um painel do dono para contornar as limitações da API
  oficial"): saiu o cartão abstrato do diagrama e entrou a gravação da tela dele numa janela de 1020x1060 com borda
  laranja. Três trechos reais em sequência (Conversas 250 s, Agenda 327,8 s, Funil 368,1 s da gravação da tela), a
  câmera chegando perto o tempo todo (zoom 1,03 a 1,34, ancorado no canto de cima à esquerda), troca de página em
  corte seco no clique de um cursor desenhado sobre os ícones reais da barra lateral, e três etiquetas: "Painel do
  dono", "Criado do zero no Claude Code" (fato da fala dele aos 88 min: "foram criados 100% do zero") e "Limitações
  da API oficial", que é riscada. Quadros em `cena/quadros/pnA|pnB|pnC`, tocados por `data-dir`. O Funil precisou de
  outro trecho: no primeiro ele selecionava palavras com o mouse.
- **Trilha com pulso**: uma faixa só (16,72, saiu de primeira), pedida com 128 bpm, arpejo e cordas em staccato "desde
  o primeiro segundo". Medi antes de usar (`tmp/energia.py`): batida regular a 127,99 bpm, três vezes mais ataque que a
  calma e agudo de verdade. Veio com os primeiros 13 s 8 dB mais baixos e terminando em 105 s: nivelei o começo, repeti
  4 compassos na completa (a música se repete igual a cada 4 compassos, semelhança 0,95) e alinhei a última batida
  forte com o cartão do fim nas duas. Como ela é brilhante, a transcrição do mp4 pronto piorou em três palavras; um
  vale de 4,5 dB em 2,8 kHz na trilha resolveu.
Gasto das versões 5: 16,72; saldo 1.885,09; total do vídeo 60,61.

Veredito dele sobre as versões 5: "Ambas as versões ficaram ruins, a música do primeiro reels que criamos juntos ficou
bem melhor" (a mensagem foi interrompida aí). Em seguida ele voltou a conversa pro ponto da v4 e refez o pedido, com a
parte do painel igual e a da música assim: "A trilha sonora não combinou com o ritmo do vídeo, quero algo que remeta
mais à Inteligência Artificial e Agentes de IA". Do painel real ele não falou nada em separado.

Versões 6 (mesmo dia), sem crédito:
- **Cena**: a da v5, sem mexer nem renderizar de novo (o `cena.mp4` é o mesmo).
- **Trilha**: a `trilha-ia.mp3` do Short "Clona Qualquer App" (a v8 escolhida; era a "música do primeiro reels"),
  estendida pra 64,7 s e 114,4 s por `tmp/trilha_ia_monta.py` (cópia em `scripts/trilha_ia_estender.py` da skill). O
  andamento saiu dos ataques acima de 200 Hz (112,01 bpm cravados, compasso de 2,14265 s): pela onda inteira o grave
  sustentado dava vários picos iguais a cada 16 ms e um salto 22 ms fora do tempo. Saltos de compassos exatos, no
  instante em que a onda dos dois lados é igual (semelhança 0,93 e 0,94 em 80 ms): de 36,368 s pra 2,085 s (16
  compassos) e de 31,805 s pra 14,664 s (8 compassos). O final natural da faixa cai no fim do vídeo. Conferido depois:
  ataques antes e depois de cada emenda com desvio de até 3 ms, sem buraco de volume.
- **Volume**: 0,084 no plano, pra música ficar 16,3 dB abaixo da voz como no Short aprovado (lá a voz tinha -16,5 LUFS
  com volume 0,1; aqui tem -18,2).
Gasto das versões 6: 0; saldo 1.885,09; total do vídeo 60,61.

Veredito dele sobre as versões 6: "No segundo 42, eu tô falando mas olhando para a tela do computador, então fica meio
esquisito nesse short. Quero uma animação muito bem trabalhada e em tela cheia nesse momento que estou olhando
levemente para o lado." Da música (a `trilha-ia.mp3` estendida) e do painel real ele não reclamou.

Versões 7 (mesmo dia), sem crédito:
- **Ele sai de cena onde olha pro monitor.** Em "Claro que você vai criar um painel do dono de acordo com as
  necessidades desse cliente" (curta 40,8 a 44,9 s; completa 90,5 a 94,6 s) o olhar dele estava um pouco pro lado o
  trecho inteiro. A folha de miniaturas não mostrava: só apareceu numa folha com o rosto ampliado a cada 0,3 s. A
  mesma folha mostrou que ele vira o rosto em "tem esse painel do dono" (33,8 s): a janela dele ali acaba 1,25 s
  antes (`tP + 2.7`) e o painel desenhado vai pro palco mais cedo.
- **No lugar, uma animação de tela cheia** (`monta(t)` na `motion.html`): linhas de planta cruzam o quadro, o
  contorno do painel se desenha por duas pontas de luz, as vagas tracejadas piscam; uma linha de luz revela o painel
  sólido de cima pra baixo (960x1130, de 250 a 1380); cabeçalho "Painel do dono / Clínica de estética"; os quatro
  módulos reais (Conversas, Agenda, Funil, Templates, com dados reais em miniatura) chegam pelos lados em arco,
  encaixam nas vagas e acendem a aba correspondente; no "Então a gente poderia..." os módulos voam pra barra lateral,
  o painel encolhe pra 900 e mostra a lista de conversas, que é exatamente o estado em que a aba nova do CRM nasce.
  Legenda em 1480 enquanto o painel está alto; a troca de altura da legenda cai numa troca de grupo de palavras.
Gasto das versões 7: 0; saldo 1.885,09; total do vídeo 60,61.

Resposta dele sobre as versões 7 (19/11/2026): "Quero a versão reduzida e essa". Leitura minha (ele não disse
"aprovado"): ficou com as duas, a curta de 65 s ("reduzida" é o nome que ele dá a ela) e a completa de 114 s, sem
pedir ajuste. Nem da animação de tela cheia, nem dos efeitos sonoros novos, nem da trilha ele reclamou. Os dois
finais em qualidade total foram copiados pra `Downloads` com nome claro (a pasta `shorts-canal` fica fora das pastas
que o aplicativo abre; `Downloads` ele abre com um clique). Nada foi publicado.
O que deu certo neste vídeo, depois de sete versões: painel real do produto em movimento logo na abertura, telas
desenhadas depois, a `trilha-ia.mp3` estendida, e animação de tela cheia que continua a história em todo trecho em
que ele não olha pra lente.

O que a volta da conversa ensinou: quando ele edita uma mensagem antiga, o aplicativo desfaz o que eu mudei com as
ferramentas de edição (a `motion.html` da curta, estes arquivos de referência e a memória voltaram pra v4), mas não o
que os programas gravaram (os mp4 da v5, a trilha, a `motion.html` copiada pra completa, o `orcamento.md`). Antes de
começar uma rodada, olhe as datas da pasta `saida`: se houver versão mais nova do que a conversa conhece, leia o fim do
histórico da sessão anterior (`.jsonl` em `.claude/projects/...`) pra saber o que foi feito, quanto custou e o que ele
achou. Nome de arquivo novo sempre acima do maior que existe na pasta.

## 24/11/2026: o acabamento do Higgsfield virou pacote fixo

Pedido do criador, sem vídeo novo no meio: o Higgsfield entra no fim, depois que o Short já está cortado e animado, e
traz sempre o mesmo pacote.
- **Trilha:** "Vamos sempre gerar uma nova versão de música parecida com a que eu gostei." Antes a regra era não gerar
  trilha sem ele pedir, depois das quatro faixas reprovadas no vídeo do agente de WhatsApp. Agora a trilha nova vai
  sempre no orçamento, pedida com o som medido da `trilha-ia.mp3`, e ele escolhe entre ela e a padrão. Conferido no
  catálogo nesse dia: nenhum modelo de música aceita áudio de referência, então "parecida" depende da descrição e da
  medição.
- **Efeitos:** cada animação ganha um efeito gravado escolhido pra ela, do catálogo da Epidemic Sound que o Higgsfield
  dá acesso (`search_sound_effects` funcionou nesse dia; o download não foi testado, então o custo dele ainda não
  está medido). Os baixados ficam numa biblioteca comum (`shorts-canal\_sons`) pra não baixar duas vezes.
- **Ângulos:** continuam como estavam (câmera 2, entrada no monitor, tela do PC), escolhidos pelo que faz sentido no
  vídeo.
- **Sugestões no fim:** "Quero que me dê sugestões de melhorias quando tudo estiver finalizado." A entrega final traz
  de 3 a 5 ideias, sem fazer nenhuma.
- Uma avaliação automática do gancho pelo `virality_predictor` chegou a ser discutida e ficou de fora, a pedido dele.
- A descrição da skill tinha 1.127 caracteres, acima do limite de 1.024 das skills; foi reescrita.

## 24/11/2026: todo Short ensina, e o Short que leva pro vídeo completo

Nenhum Short montado: foram cinco rodadas de falas no papel, com três vídeos do canal (um lançamento de modelo, um
tutorial de 32 min e uma explicação de 19 min; deste último só existia o vídeo final editado, com a webcam no canto).
- **Falas pelos momentos de impacto** (resultados, números, demonstrações), em dois vídeos: "Ficaram ruins as duas
  versões, o vídeo tem que ensinar algo pra essa pessoa que está assistindo, e ela tem que sair do vídeo sentindo que
  aprendeu algo nesse vídeo, sentindo que eu agreguei valor pra ela".
- **Falas pelo que ensinam** (uma ideia por Short, com definição, exemplo, a pergunta que a pessoa faria e a lição):
  ele não comentou essa lista em separado e passou a perguntar pelo outro objetivo: "E se o objetivo fosse fazer a
  pessoa ficar interessada em ver o vídeo completo no YouTube?".
- **Trailer feito de frases soltas** de vários pontos do vídeo (promessa, um pedaço que ensina, uma pergunta sem
  resposta, corte no suspense): "Achei que cortou muito a introdução do vídeo longo, acho que aproveitar mais a
  introdução seria uma abordagem bem melhor, o objetivo desse vídeo tem que ser deixar a pessoa curiosa pra ver o
  vídeo completo que ensina isso no detalhe".
- **Introdução quase inteira** (uns 36 s de frente pra câmera), dois relances e o corte no suspense: "ficou bem
  melhor, mas achei que ficou muito crua só com a intro"; ele pediu pra ver como ficaria aproveitando "o máximo
  possível da intro, mas aproveitando também outros momentos do vídeo".
- **Introdução como espinha, intercalada com provas** (10 falas, uns 100 s no papel: cada afirmação da introdução
  seguida de um trecho que mostra aquilo acontecendo, a promessa do vídeo perto do fim, o corte no suspense e o
  cartão COMENTA). Ele não deu veredito: a conversa foi pra outro assunto. É a última proposta de pé.

Onde isso entrou: `estilo.md` ("Roteiro e ritmo"), `tipos-de-video.md` ("Forte não basta" e "O objetivo do Short"),
`formato.md` (nota depois da tabela da estrutura) e o passo 4 e a PARADA 1 do `SKILL.md`. Essas duas regras tinham
ficado guardadas só na memória de um projeto, fora da skill: quem rodava a skill em outra pasta não seguia nenhuma.
Regra de como fazer Short mora nestes arquivos.

## 24/11/2026: vídeo da base de conhecimento (explicação + tutorial, 17 min, 4 h de bruto)

Primeiro Short feito de ponta a ponta depois das regras "todo Short ensina" e "ele aprova as falas antes".
- **Brutos:** voz separada de 4h03, tela do OBS **sem som** e quatro arquivos de câmera que não cobrem a gravação
  inteira. A tela foi alinhada pelos relógios dos arquivos (o nome do .mkv e o `creation_time` do .wav: 1 s de
  diferença); a luz do monitor no rosto não serviu pra medir. As falas vinham de duas câmeras: juntei só os trechos
  usados num arquivo (`material/cam-junta.mp4`, quadros contados) e pus o atraso de cada trecho na tabela `atraso`.
- **PARADA 1:** três propostas com o texto exato (ensinar por inteiro, 80 s; levar pro vídeo, 52 s; uma ideia
  fechada, 38 s). O criador escolheu a de ensinar por inteiro sem mexer nas falas.
- **Versão 1** (78 s, sem crédito): gravação real do grafo em movimento na abertura, depois telas redesenhadas com
  os textos reais das notas. Dois pedidos dele:
  - "Tem alguns momentos em que eu não estou olhando pra câmera, acaba aparecendo que eu estou lendo o que eu estou
    falando. Quero as animações em tela cheia nesses momentos." A folha do `rostos.py` com o quadro inteiro não
    mostrou: só a folha dos olhos ampliados a cada 0,2 s. Era justamente o gancho (ele lê a frase de abertura na
    tela) e o começo de duas outras entradas.
  - "Os pontos ficam piscando. Acredito que tenha sido proposital mas pareceu bugado, ficaria melhor se os pontos
    piscando tivessem outra cor e se eles piscassem de forma mais constante." Eram bolinhas brancas na ponta de seis
    linhas, cada uma num tempo.
- **Versão 2:** ele só entra onde os olhos estão na lente (a abertura ficou 3,4 s em tela cheia, com a frase em
  letra gigante palavra por palavra); os pontos achados pulsam todos juntos, numa cor só deles (o roxo do produto).
  Resposta dele: seguir pro acabamento.
- **Acabamento (versão 3):** trilha nova 11,34 (veio com 73 s pra 78 pedidos: repeti 2 compassos no meio), 8 efeitos
  gravados (0 crédito), recorte 1 crédito (3 trechos, 385 quadros). Com o recorte o enquadramento dele fechou de
  1,25 pra 1,5, pra cabeça passar na frente da janela.
- **Erro meu de processo:** editei a `motion.html` antes de rodar o `guardar_versao.py` da versão 1; da v1 ficaram o
  vídeo, a `cena.mp4` e o plano, mas não a animação editável. Guardar a versão é o primeiro comando da rodada.
