# O estilo dos Shorts do canal: o que o criador aprovou e reprovou

Tudo aqui veio de veredito dele sobre vídeo pronto, em duas rodadas (12 e 13/11/2026, 13 versões no total). As
frases entre aspas são dele. O formato a que isso levou está em `formato.md`; a ordem em que as coisas aconteceram,
em `historico.md`.

## A ideia central

O criador aparece de verdade, falando o que ele falou no vídeo longo. A IA trabalha **em volta dele e entre os
trechos**, e **melhora o material real**: nunca o substitui. Nenhum trecho do Short é uma cena solta de IA
ilustrando a fala. Cenas de apoio geradas (um robô, cartas voando) seriam "as piores partes", com "estilo AI slop".

Na dúvida sobre incluir algo, pergunte: isso mostra melhor o que ele já gravou, ou é enfeite? Enfeite sai.
**Motion não é enfeite**: o efeito decora a frase, o motion mostra a ideia.

**Rascunho é julgado como vídeo pronto.** "Ficaram ruins, mesmo pra um esboço." Não existe "é só um esboço": o
que você mostra já tem trilha, efeitos, motions e acabamento.

## Vereditos, por assunto

### Roteiro e ritmo
- **Não é o vídeo longo espremido.** A versão que abria com a frase de apresentação do vídeo longo e levava 14 s
  pra mostrar o resultado foi "quase inaproveitável". O resultado vai no primeiro quadro.
- **Mas não é correria.** A de 25 s: "tá pouco explicativo, tá muito rápido e a pessoa não prende nada". Gancho
  curto e depois explicar com calma: o que é, como ele fez, o resultado sem pressa, veredito. Sem mínimo, até 2 min
  (17/11/2026: "quero que os vídeos possam ter até 2 minutos de duração"); o tamanho é o que a tese pede.
- **Em vídeo de lista, ele pode querer o Short da tese**: "achei que íamos criar um shorts que mostra pelo menos 3
  repositórios. Esse vídeo tem que ter a mesma tese do vídeo longo". Pergunte na PARADA 1 se é por item ou da tese.
- **Ele não regrava nada**: "quero testar a sua capacidade e a capacidade do Higgsfield de resolverem esse
  problema". Não proponha regravação.
- **Ele aprova as falas antes de qualquer coisa ser montada** (18/11/2026): "O que vai ser falado no vídeo? Me envie
  antes de criar". Na PARADA 1 mande o texto exato de cada candidato (conferido no áudio), a duração e uma linha de
  ponto forte e ponto fraco. Só monte depois do sim.
- **Frases costuradas de pontos diferentes soam "robotizado"**: a lista de definições (4 pilares, sete frases de sete
  lugares) foi recusada no papel: "achei ruim as falas, vai acabar ficando robotizado". Prefira uma tomada contínua,
  ou blocos inteiros de poucas tomadas, na ordem em que ele falou.
- **O gancho tem que ter nascido como abertura.** Três trechos cujo começo era o meio de um raciocínio foram
  recusados: "não tô gostando do gancho, de fato parece que foi cortado de outro vídeo". O que passou foi uma fala
  que ele gravou solta pro editor encaixar (procure os recados dele pro editor: "vou gravar uma outra parte...") e, em
  geral, frases que abrem um assunto do zero, sem "então", "e" ou "isso" apontando pra trás.
- **Ele pede o Short "que ensine algo e que tenha necessariamente um excelente gancho"**, e pode querer, depois do
  gancho, uma passada rápida pelo que a coisa faz ("sem demorar tanto nessa seção"). Ofereça as falas curtas da
  própria introdução do vídeo, com os segundos de cada uma.
- **"O vídeo tem que ensinar algo pra essa pessoa que está assistindo, e ela tem que sair do vídeo sentindo que
  aprendeu algo, sentindo que eu agreguei valor pra ela."** (24/11/2026.) Duas listas de falas escolhidas pelos
  momentos de impacto (resultados, números, demonstrações) foram recusadas no papel: "ficaram ruins as duas
  versões". Escolha as falas pelo que elas ensinam: uma definição simples, o porquê, um exemplo concreto, a pergunta
  que quem assiste faria, a ressalva honesta, a lição no fim. O que impressiona continua entrando, como prova do que
  foi ensinado, não no lugar dele. Um teste (leitura minha): o que a pessoa consegue explicar pra outra depois de
  assistir? Se a resposta for só "ficou bonito", troque as falas.
- **Short que leva pro vídeo completo aproveita a introdução do vídeo longo** (24/11/2026). Uma proposta pra "fazer
  a pessoa ficar interessada em ver o vídeo completo", feita de frases soltas de vários pontos do vídeo, foi
  recusada: "achei que cortou muito a introdução do vídeo longo, acho que aproveitar mais a introdução seria uma
  abordagem bem melhor, o objetivo desse vídeo tem que ser deixar a pessoa curiosa pra ver o vídeo completo que
  ensina isso no detalhe". Com a introdução quase inteira e só dois relances depois: "ficou bem melhor, mas achei que
  ficou muito crua só com a intro"; e pediu pra ver como ficaria aproveitando "o máximo possível da intro, mas
  aproveitando também outros momentos do vídeo". O que ficou: a introdução é a espinha, na ordem em que ele falou, e
  depois de cada coisa que ela afirma entra um trecho que mostra aquilo acontecendo na tela. Receita em
  `tipos-de-video.md`, "O objetivo do Short". Isso não desfaz o primeiro veredito desta lista: lá o defeito era levar
  14 s pra mostrar alguma coisa; aqui o resultado está na tela desde o primeiro quadro, enquanto ele fala. (Decidido
  no papel: nenhum Short pronto nesse molde foi julgado ainda.)
- **Na dúvida entre curto e completo, ele pede as duas versões** pra comparar. Escreva a cena uma vez só, com as
  partes extras ligadas pelo roteiro (um `secoes.js` por pasta), em vez de duas cenas.

### A fala e o som
- **"Muitos trechos ficaram com o áudio cortado no final."** A sílaba final fraca continua ~0,2 s depois do ponto
  que a transcrição dá. Corte pelo volume (`pontas.py`, `pedacos.py`), nunca pela transcrição.
- **"Silêncios desnecessários."** Frases inteiras, mas toda pausa de 0,25 s ou mais vira ~0,12 s.
- **"No final do vídeo tem meio segundo de pausa... remova essa pausa pra ficar perfeito."** O Short acaba 0,12 s
  depois do último som. Eu tinha segurado 0,55 s pra ele "sustentar o olhar": não segure.
- **"Quero [música] que remeta a inteligência artificial."** Trilha eletrônica, não trilha genérica. E efeitos
  gravados em cada movimento: sem trilha e com efeito sintetizado foi "acabamento de máquina".
- **"Tem alguns trechos onde a última palavra da frase foi cortada e outras que a pausa está mais longa que
  deveria."** (agente de WhatsApp, v2.) As duas causas: o fim da tomada marcado pela transcrição comeu a sílaba
  forte de "ofici-AL" (ela vinha 0,2 s depois do fim que o Whisper deu), e pausa com respiração acima do limite não
  foi vista como pausa. O corte passou a ser todo pelo volume: pausa é qualquer trecho abaixo de -36 dB por 0,17 s
  ou mais; fim de frase é o último som forte mais a cauda, com fade. **Depois de montar, transcreva o mp4 pronto e
  compare o texto com o da versão anterior**: palavra que sumiu aparece ali (foi assim que peguei um "que" que eu
  mesmo tinha tirado). Antes de mudar uma palavra de tomada, confira o tempo dela numa janela curta: a transcrição
  da gravação inteira joga palavra da tomada repetida pra tomada de antes.
- **"Quero que a trilha sonora tenha um estilo mais parecido com Hans Zimmer, mais ficção científica, mas que
  comporte em um vídeo tutorial de inteligência artificial."** Trilha de cinema (grave sustentado, pulso lento,
  camadas que crescem), discreta embaixo da voz. ("Pulso lento" deu trilha calma demais: veja o veredito seguinte.) No pedido ao gerador, descreva o som, sem citar o artista. Trilha
  nova gasta crédito: mesmo ele tendo pedido a trilha, precisa do "pode" com o valor (o próprio aplicativo barra a
  geração sem isso).
- **"A trilha sonora ficou calma demais, relaxante até, não combinou com o ritmo do vídeo."** (agente de WhatsApp,
  v4, a trilha de cinema.) Corrigi com uma faixa gerada de 128 bpm, brilhante e marcada (v5), e foi pior: **"Ambas as
  versões ficaram ruins, a música do primeiro reels que criamos juntos ficou bem melhor"**; e, ao refazer o pedido,
  **"quero algo que remeta mais à Inteligência Artificial e Agentes de IA"**. Foram quatro faixas geradas pra esse
  vídeo (59,89 créditos) e nenhuma serviu. **A trilha padrão é a `assets/audio/trilha-ia.mp3`**, a do Short "Clona
  Qualquer App": eletrônica, 112 bpm cravados, pulso regular de semicolcheias (7,4 ataques por segundo), grave cheio,
  quase nada acima de 4 kHz, volume constante.
- **"Vamos sempre gerar uma nova versão de música parecida com a que eu gostei."** (24/11/2026.) Todo Short ganha uma
  trilha nova no acabamento, pedida com o som medido da `trilha-ia.mp3` (receita em `higgsfield.md`, "A trilha
  nova"). Ela vai sempre no orçamento e precisa do "pode" como qualquer crédito. Entregue a versão com ela em
  sequência com a mesma versão na trilha padrão: se ele preferir a padrão, fica a padrão.
- **Efeito gravado pra cada animação** (24/11/2026). No acabamento, cada `Motion.sfx` ganha um som escolhido pra
  aquele movimento, do catálogo de sons do Higgsfield (`higgsfield.md`, "Efeitos sonoros"). Os sons de
  `assets/audio/` ficam só na versão 1.
- **Short maior que 42 s: estenda a `trilha-ia.mp3`, não deixe a montagem dar a volta sozinha.** O `compor.py` repete
  o arquivo do começo: a faixa some de 38,75 s em diante e recomeça em 42 s fora da batida (buraco de 2 s). Monte um
  arquivo do tamanho do Short com `scripts/trilha_ia_estender.py` (ajuste as chamadas do fim pra cada vídeo): saltos de
  compassos exatos (compasso = 2,14265 s) nos pontos em que a onda dos dois lados é igual, de 36,368 s pra 2,085 s
  (16 compassos) e de 31,805 s pra 14,664 s (8 compassos), cruzando 80 ms, com o final natural da faixa no fim do
  vídeo. Pra achar andamento e pontos de volta em qualquer faixa, use os ataques acima de 200 Hz: a correlação da onda
  inteira é enganada pelo grave sustentado.
- **Volume da trilha: a mesma distância da voz do Short aprovado, ~16 dB.** Lá foi 0,1 com a voz em -16,5 LUFS. Meça a
  voz (junte os blocos do `lista.txt` da pasta `tmp` da montagem e passe o `ebur128`) e corrija: voz em -18,2 pede
  0,084.
- **Áudio fora de sincronia** reprovou um dos primeiros rascunhos. Sincronia se mede (`boca_cv.py`, e a linha
  "sincronia conferida" do `montar`), não se presume.

### Ele em cena
- **"Tem muitas cenas que eu não tô olhando pra câmera e mesmo assim eu apareço, como o foco da cena… fica
  esquisito."** Ele só entra grande onde olha pra lente (`rostos.py`).
- **"No segundo 42, eu tô falando mas olhando para a tela do computador, então fica meio esquisito nesse short.
  Quero uma animação muito bem trabalhada e em tela cheia nesse momento que estou olhando levemente para o lado."**
  (agente de WhatsApp, v6.) Olhar um pouco pro lado já conta como não olhar pra câmera. Miniatura do quadro inteiro
  não mostra isso: pra cada janela em que ele aparece, monte uma folha só com o rosto ampliado (recorte de ~35% da
  largura do quadro da câmera) a cada 0,3 s e veja os olhos. Onde o olhar sai da lente, mesmo por 1 s, ele sai de
  cena e entra **animação de tela cheia que continua a história** (não um cartão parado): aqui, o painel se
  construindo peça por peça até virar a tela em que a próxima frase acontece.
- **"O recorte no fundo ficou muito ruim, bem amador."** Era ele recortado sobre fundo escuro. Ele fica no cenário
  real da câmera; o recorte só serve pra janela passar atrás da cabeça.
- **O rosto e a fala reais não passam por IA** sem ordem dele naquele vídeo.

### Texto na tela
- **"Os textos ficaram com estilo AI Slop."** Eram um comando de terminal falso, linhas como "→ todos prometem
  melhorar", um rótulo "peça 6 de 6", cartões genéricos. Texto só entra se for fato: nome, número ou frase da fala
  dele, da tela dele ou de uma fonte real que dá pra mostrar. Nada de "%", código ou paráfrase.
- **Tipografia**: Montserrat ExtraBold; número grande em laranja com rótulo curto. Fonte de terminal só quando o
  assunto na tela é mesmo um terminal.

### Motions
- **"Tem poucas animações e as que tem não ficaram muito boas."** Depois: "senti falta de mais motions que ajudem
  na explicação". Depois, com 6 versões feitas: "quero mais motion graphics nesse vídeo, acho que as explicações
  podem ficar melhor melhorando os motions e adicionando ainda mais motions". **O pedido por mais motion se
  repetiu em toda rodada: comece com muitos.** Toda fala sem ele em cena tem um motion que a explica.
- **Tela pequena não era o problema**: "isso daria pra melhorar com os motions".
- **"As animações ficaram fracas, dava pra fazer algo muito mais trabalhado, as partes que usam print ficaram mal
  formatadas, criar uma animação pra demonstrar vai ficar visualmente melhor e vai deixar mais fácil entender os
  conceitos."** (agente de WhatsApp, v2.) Captura parada da tela dele (painel, planilha, calendário, conversa) não
  serve de cena, nem aproximada, nem com lente. **Redesenhe a tela em HTML com os textos e números reais e anime o
  que acontece nela**: a mensagem que chega, o botão que vira, o cursor que clica, a linha da planilha sendo
  escrita, o evento voando pro calendário, o funil enchendo. A captura fica só como fonte dos dados.
- **"Ficou bem melhor, mas em algum momento do início [...] nós precisamos mostrar o painel do dono original porque
  ficou muito abstrato pra entender que de fato esse é um agente de IA criado 100% no Claude Code e do zero."**
  (agente de WhatsApp, v4, toda desenhada.) Desenhar tudo resolve a formatação, mas tira a prova de que a coisa
  existe. **O produto real aparece cedo, uma vez, em movimento**: a gravação da tela dele (não captura parada) numa
  janela grande com borda laranja, enquadrada a partir do canto de cima à esquerda (a barra lateral e o título seguram
  a composição), em tamanho em que o texto se lê (1,0 a 1,3 vez o tamanho original da gravação), com a câmera chegando
  perto devagar, as páginas reais trocando em corte seco no clique de um cursor desenhado e etiquetas só com fatos da
  fala. Escolha trechos sem texto selecionado nem janela por cima. Depois disso as telas desenhadas são lidas como a
  versão simplificada da real. (Foi mostrado na v5; o veredito dele sobre a v5 falou da música, do painel real
  nada em separado.)
- Imagem parada com fade é "muito básico"; traço que se desenha, número que conta, texto que se digita e bolinha
  viajando na linha são os recursos que ele elogiou.

### A abertura
- **Abertura gerada por IA com tela de app foi reprovada**: "ficou ruim, tá mal formatado e poluiu o início do
  vídeo". Era um vídeo 16:9 do Kling recortado no vertical. Ele chegou a gostar dela num teste isolado e reprovou
  quando viu no Short inteiro: **julgue o plano dentro do Short, não sozinho**.
- **O que ele pediu no lugar**: "começar com um motion muito bem criado pra demonstrar isso, em tela cheia, e esse
  motion termina comigo em tela dividida". Motion próprio, com as capturas reais inteiras, e só depois ele entra.
- **O que a abertura promete tem que aparecer.** Na versão em que a câmera 2 cobria o clone sendo feito, ele
  notou: "acaba sendo cortado... porque você me botou em tela cheia". Nada de plano gerado por cima do momento
  que o gancho anuncia.

### Planos gerados
- **Gostou**: a câmera entrando no monitor até a página real; a câmera 2 mais fechada com ele falando; o
  time-lapse do app se montando na tela do PC ("tem que ficar perfeito").
- **"Dá uma bugada quando, de fato, entra no monitor"** e, depois do primeiro conserto, "levemente bugado, não
  ficou fluido". Não era o modelo: era a velocidade pulando na emenda. Meça quadro a quadro antes de trocar de
  modelo (`higgsfield.md`).
- **"Achei que o take poderia ser mais aproximado, ficou meio longe em comparação com a gravação original."**
  Câmera 2 no mesmo tamanho de rosto da câmera real, ou mais perto.
- **"Menos tempo com a segunda câmera ficou [melhor]."** ~1,2 s.
- **"As demais achei inaproveitáveis"**: câmera aberta por trás, câmera de lado distante, o monitor virando o
  clone com ele em cena. Plano gerado longo e aberto mostra o defeito.

### Câmera 2 com outro ângulo, rosto e fundo gerados
Ele pediu um ângulo novo ("só parece que eu girei a cadeira e não mudei o ângulo da câmera") e, depois de 8
rodadas de foto e um rascunho, **preferiu a câmera 2 antiga**. O que ficou:
- **"Não ficou parecido comigo em nenhuma das versões."** Com um quadro só de referência, o perfil é inventado.
  Mande 8 ou 9 quadros reais (frente, três quartos, perfil): aí ficou parecido. Ele usa o GPT Image 2 e diz que
  "mantém bem a minha aparência".
- **Mudar de ângulo é mudar a perspectiva do fundo.** Se a estante continua reta atrás dele, parece que só o
  corpo girou.
- **"Tem que ter alguma relação com o vídeo original, tem de certa forma parecer que está no mesmo ambiente."** E
  depois: "não precisa ter o mesmo fundo do vídeo original, só precisa parecer que está no mesmo estúdio". Mesmos
  materiais e mesma luz (madeira clara, LED quente, painel ripado), outro canto. Estúdio genérico escuro não.
- **Objeto de cena inventado denuncia** (um celular no tripé filmando ele: "ficou ruim"). E defeito de objeto (o
  recorte torto na mesa) não se conserta editando a foto: gere de novo com o mesmo prompt.
- **Lição de processo**: pôr o rascunho barato dentro do Short e mostrar lado a lado com a versão atual, antes de
  pagar a finalização. Foi assim que ele decidiu ficar com a antiga sem gastar os 80 créditos.

### Limpeza
- Ele reprova tela poluída e prefere pouca coisa à vista. Entre a janela grande com uma varredura e dois cartões
  pequenos com peças voando, escolheu a janela grande.
- Na dúvida entre mais efeito e mais limpo, mais limpo.

## Como ele decide (e como entregar pra ele decidir)

- **Ele compara.** Pediu: "crie um vídeo com essas 3 versões lado a lado, quero comparar elas", e depois "quero
  as duas lado a lado no final". Sempre que houver duas versões de um trecho ou do Short, entregue o lado a lado
  (`lado_a_lado.py`) junto, sem esperar ele pedir.
- **Ele pede opções.** "Gere 2 versões novas muito melhoradas dessa parte", "gere 3 novas versões". Opção de
  verdade é ideia diferente, não a mesma com outro número. Diga em uma linha a diferença de cada uma.
- **Ele mistura.** "Preferi a versão A mas a duração da B ficou melhor." A próxima versão junta o que ele gostou
  de cada uma.
- **Ele volta atrás, e tudo bem.** Preferiu a versão 6 depois de ver a 7; ficou com a câmera 2 antiga depois de
  explorar a nova. Por isso nenhuma versão é sobrescrita (`_versao-N`) e voltar tem que ser trocar uma linha.
- **Ele acompanha o Higgsfield pelo site** e às vezes vê o resultado antes de você mostrar ("ficou ruim, vi no
  Higgsfield"). Também gera coisas por conta própria lá: o saldo pode cair sem ter sido você.
- **Ele quer saber onde está o arquivo.** Toda entrega traz o link clicável do vídeo e o caminho da pasta.
- **"Quero que me dê sugestões de melhorias quando tudo estiver finalizado."** (24/11/2026.) A entrega final traz de 3
  a 5 ideias concretas do que ainda deixaria o Short melhor, com o trecho, o que muda na tela e o preço quando custa.
  Só ideias que melhoram o material real. Nenhuma é feita sem ele pedir.
- **Resposta curta, em português simples**, o que importa primeiro. Se uma etapa demorar ou parecer exagero
  ("precisa de tirar tantos prints assim? por quê?"), diga em uma linha pra que serve.

## O que ficou na reserva

Ingredientes do desenho original da skill que nunca chegaram a um Short aprovado. Só use se ele pedir:

- **Bloco `tela` parado** (tela em cima, ele embaixo) e cortes secos entre blocos: é o formato da versão 1,
  reprovada. O `compor.py` ainda monta (ver `plano.md`), como último recurso.
- **Telão num estúdio gerado**, com ele recortado na frente: nunca testado com material real.
- **Fala de ligação na voz clonada**: no máximo uma frase de até 12 palavras, que só apresenta o que ele mesmo
  mostra, escrita como se fala ("mostrá", "pra", vírgula no lugar de ponto). A voz clonada dele, se houver, está na conta do
  Higgsfield. Avise na entrega: ele decide se marca "conteúdo alterado" no YouTube. Rosto falando gerado sobre
  fala gerada, só com ordem dele.
- **Efeitos de texto** (palavra gigante atrás da cabeça como enfeite, quadro congelado com nome): ele recusou. O
  nome da coisa atrás dele no fecho passou porque é o assunto da frase, não decoração.
- **Objeto 3D** passando atrás e na frente dele: nunca feito.

## Como reprovar uma cena gerada

Olhe a folha de quadros de cada cena antes de usar. Refaça ou descarte se:
- o rosto, o cabelo, a barba ou a roupa dele mudaram;
- apareceu mão com dedos errados, objeto que surge do nada, texto derretendo;
- a cena tem corte no meio, ou o último quadro não bate com o quadro real seguinte;
- o cenário virou outro lugar.

Uma refação por cena está dentro do orçamento aprovado. Se a segunda também falhar, tire a cena (a cena animada
cobre o trecho com material real) e conte a ele: insistir é como o Short vira vitrine de defeito de IA.

## Marca

- Laranja `#FF6B18`, creme `#F3EDE6`, fundo quase preto `#0c0a0a`, Montserrat ExtraBold.
- Logo (só se ele pedir): peça o arquivo a ele.
- Nada de vinheta, logo ou "se inscreve".

## Vídeo patrocinado

Num Short que vai dentro de publicidade (campanha do Higgsfield, CapCut...), marcas de terceiros na tela podem
reprovar o vídeo. Mostre o resultado dele e não a página ou o logo de outra empresa, e avise quando não der pra
evitar.
