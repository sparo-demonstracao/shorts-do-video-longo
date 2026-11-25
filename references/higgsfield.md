# Higgsfield pelo MCP: o que pedir, com qual modelo e quanto custa

Tudo o que é gerado sai pelo conector `higgsfield` (ferramentas `mcp__higgsfield__*`). Se uma ferramenta aparecer
só pelo nome, carregue o esquema com ToolSearch (`select:mcp__higgsfield__<nome>`), várias de uma vez.

## A regra do crédito

O criador já interrompeu uma sessão pra dizer: não gerar nada nem consumir créditos sem ele mandar. Então:

1. Consultar preço é livre: toda ferramenta de geração aceita `get_cost: true` dentro de `params` e devolve o
   custo **sem gerar nada**. Ler catálogo (`models_explore`), saldo (`balance`) e vozes (`list_voices`) também é
   livre.
2. Gerar só depois da PARADA 2 (orçamento aprovado), e só o que está no orçamento.
3. Anote o saldo antes de começar e depois de terminar (`balance`). A diferença é o gasto real que vai pro
   relatório.
4. Nunca passe `use_unlim` nem `use_free_gens` por conta própria.
5. Se uma chamada demorar e cair, **não mande de novo**: confira primeiro se o pedido entrou
   (`show_generations` ou `transactions`). Reenviar no escuro paga duas vezes.

## A escada de um plano gerado: foto, rascunho, no Short, finalização

Cada degrau custa mais que o anterior, e o criador decide em cada um. Na última rodada, seguir a escada economizou 80
créditos: ele viu o rascunho dentro do Short, ao lado da versão atual, e ficou com a antiga.

1. **Foto** (`gpt_image_2_6`, 0,25 cada). Gere 2 ou 3, mostre lado a lado com um quadro real dele, espere a
   escolha. Toda discussão de enquadramento, fundo e rosto acontece aqui, onde errar é barato: foram 8 rodadas de
   foto por 6 créditos. Não mande o vídeo antes do "essa" (um rascunho de 15 foi cobrado à toa porque a foto
   tinha um defeito que ele só notou depois).
2. **Rascunho do vídeo** (Seedance em `draft: true`, 15; Kling não tem rascunho). Confira antes de mostrar:
   `conferir_take.py` (a boca segue a fala real?) e a folha de quadros (rosto, mãos, fundo parado).
3. **No Short.** Extraia os quadros do rascunho, ponha como camada `.ins` na cena, renderize e monte uma versão
   nova. Entregue o lado a lado com a versão atual (`lado_a_lado.py`). O rascunho em 480p ampliado fica mais mole
   que o resto: diga isso. Um plano de que ele gostou sozinho pode ser reprovado aqui.
4. **Finalização**, só com o "pode": rode o `get_cost` **da própria chamada de finalização** (com
   `draft_job_id`, o `prompt` e as mesmas `medias`) e mostre o número. Em 13/11/2026 deu 80 tanto em 720p quanto
   em 1080p, então peça 1080p.

Quando ele mandar parar no meio, confira com `jobs_wait` (`timeout_seconds: 0`) se o pedido já tinha terminado:
se terminou, foi cobrado. Baixe o resultado, guarde e conte a ele.

O saldo cai também por conta dele: ele gera coisas direto no site. Antes de dizer quanto a rodada custou, leia o
`transactions` e some só o que foi seu.

## Subir arquivo local e baixar resultado

- Subir: `media_upload` (devolve um `upload_url` e um `media_id`; aceita até 20 arquivos de uma vez em `files`) →
  `python S/gerados/pega_url.py <media_id> u.txt` (acha a URL no registro da sessão: ela é longa demais pra
  redigitar) → `curl -s -o /dev/null -w '%{http_code}' -X PUT -H 'Content-Type: image/jpeg' -H 'If-None-Match: *'
  --data-binary @<arquivo> "$(cat u.txt)"` (tem que dar 200; 412 depois de um 200 quer dizer que já subiu) →
  `media_confirm`. O `media_id` confirmado é o que entra em `medias[].value`. O resultado de uma geração
  também serve de referência: passe o id do pedido em `value`.
- Esperar: `jobs_wait` com os ids dos pedidos. Pedido rodando é pra esperar de novo, nunca reenviar.
- Baixar: pegue a URL do resultado e salve com `curl -sSL -o gerados/<nome> "<url>"`.

## Receitas

Preços medidos em 12/11/2026 com `get_cost`. Eles mudam: **consulte de novo ao montar o orçamento.**

A tabela abaixo é o cardápio original. **As três receitas que chegaram ao Short aprovado são outras** e estão mais
abaixo, em "O que foi testado depois" e "Câmera 2 com outro ângulo": câmera 2 = `seedance_2_5` `omni_reference`
com a fala real de referência; entrada no monitor = `kling4_0` `image-to-video` partindo de uma foto com a página
real já no monitor, alisada com o `entrada_suave.py`; tela do PC = foto com o monitor verde, `kling4_0` com
`start_image` igual a `end_image`, e o seu motion colado com o `colar_tela.py`. Estúdio com telão e segunda câmera
sem boca nunca chegaram a um Short.

| Peça | Ferramenta e modelo | Entrada | Custo medido |
|---|---|---|---|
| Recorte dele | `remove_background`, `media_type: "video"` | um vídeo só, com todos os trechos emendados | **1 por pedido** (2,4 s e 15,6 s custaram o mesmo) |
| Imagem do estúdio | `generate_image`, `gpt_image_2_6`, 9:16 | prompt + quadros reais do cenário | 0,25 (até ~4,5 em resolução alta) |
| Transição | `generate_video`, `kling4_0`, `mode: "image-to-video"`, 1080p, 9:16 | `start_image` + `end_image` | 13 por 4 s |
| Transição, mais barata | `generate_video`, `kling3_0`, `mode: "pro"`, `sound: "off"` | `start_image` + `end_image` | 6 por 4 s |
| Segunda câmera | `generate_video`, `kling4_0`, `mode: "reference-to-video"`, 1080p, 9:16 | `image_references` (2 ou 3 quadros dele) | 13 por 4 s |
| Segunda câmera, plano B | `generate_video`, `seedance_2_5`, `mode: "omni_reference"` | `image_references` | 28 por 4 s em 720p; 64 em 1080p |
| Fala de ligação | `generate_audio`, `seed_audio` ou `elevenlabs_v4` | texto + voz dele | 0,46 numa frase de 9 palavras |
| Trilha | `generate_audio`, `elevenlabs_music_v2_5`, `force_instrumental: true` | prompt + `duration` | 4,36 por 30 s; 6,5 por 45 s |
| Efeito sonoro gravado | `search_sound_effects` + `download_sound_effect` (catálogo da Epidemic Sound) | descrição em inglês | busca livre; download gasta a cota de downloads e **0 crédito** (medido em 24/11/2026: 8 downloads) |
| Efeito sonoro gerado | `generate_audio`, `mirelo_text_to_audio` | prompt + `duration` (1 a 3 s) | cerca de 0,4 cada |
| Rosto falando (só se ele pedir) | `generate_video`, `intone` | `character_images` + `location_image` + `audio_references` | **não medido** (o preço só sai com o áudio) |

Kling 4.0 e Seedance 2.5 eram os modelos mais novos de cada família em 12/11/2026 (não existia Seedance 3.0 no
catálogo). Antes de montar o orçamento, rode `models_explore` com `action: "search"` e `query: "kling"` e depois
`"seedance"`: se houver versão mais nova, use-a e consulte o preço.

**Por que Kling primeiro:** pra uma cena de 4 s, o Seedance 2.5 em 1080p custa 5 vezes o Kling 4.0. O Seedance
aceita várias referências dele de uma vez e pode manter o rosto mais fiel, então ele é o plano B da segunda câmera
quando o Kling errar o rosto. Trocar pro plano B muda o orçamento: avise antes.

**Rascunho no Seedance:** `draft: true` gera em 480p; se ficou bom, finalize com `draft_job_id` na resolução
final. Refação em rascunho custa bem menos que refação em 1080p.

### O recorte

Medido em 12/11/2026 (Short do ScrollCraft, versão 3):

- **Custa 1 crédito por pedido, não por segundo.** Junte todos os trechos em que ele aparece num vídeo só e peça
  uma vez. Entre um trecho e outro, repita 8 vezes o primeiro quadro do trecho seguinte (o recorte usa os quadros
  vizinhos, e um corte seco pode sujar os primeiros quadros); depois jogue esses quadros de espera fora.
- **O resultado NÃO é preto e branco:** vem ele, colorido, sobre preto puro, **sem o microfone** (fica um buraco no
  peito). Como a camiseta dele é preta, não dá pra separar camiseta de fundo pelo brilho.
- A receita que funcionou (programa `recorte_alfa.py`, na pasta do vídeo dos repositórios):
  1. suba o vídeo com os **pretos levantados** (`lutrgb` com `val*0.8+51`: nada fica abaixo de 51), em 1280x720;
  2. a transparência de cada ponto é a **razão** entre o resultado e o vídeo que subiu (0 no fundo, 1 nele);
  3. a **cor** vem do quadro original da câmera, não do resultado; na borda, use a cor de dentro dele espalhada
     (a parede clara atrás do cabelo escuro deixa franja se a cor da borda for a original);
  4. o **microfone volta**: dentro da área dele, cada linha é preenchida da ponta esquerda à ponta direita do corpo.
  Saem quadros WebP com transparência, que a cena usa como qualquer outra sequência.
- Confira numa folha sobre fundo laranja e sobre fundo claro: cabelo e ombros sem buraco, sem franja da parede.
- **Só recorte onde ele olha pra câmera** (veja a folha do rosto, ampliada: cabeça de frente com os olhos de lado não
  conta). Ele em destaque olhando a tela foi reprovado; nesses trechos a voz vai por cima do material e não
  precisa de recorte.
- **Um pedido serve a várias versões do mesmo Short** (18/11/2026): monte o vídeo com os trechos da versão mais longa,
  rode o `recorte_alfa.py` nela e copie os `.webp` pras outras trocando só o número do quadro (as imagens da câmera
  são as mesmas). Foram 31 s, 943 quadros, 1 crédito.
- **Câmera em close, microfone fora do centro:** a área `MIC` do programa não bate e fica um buraco no peito. Não
  importa se a camada do recorte tiver uma máscara que some antes do peito (opaca até 30% da altura, zero em 46%):
  ela só precisa cobrir cabeça e ombros, que é onde a janela passa.
- **O recorte entra depois que a janela assentou** (0,34 a 0,56 s depois de ele começar a subir) e a janela só desce
  atrás da cabeça junto com ele; se entrar antes, aparece uma cabeça fantasma em cima do material que ainda está
  encolhendo. Na saída, o recorte some em 0,15 s e o material cobre tudo.
- Com o recorte dá pra pôr **um título atrás da cabeça dele**, com o material escurecido ao fundo. A
  câmera é um close sem espaço embaixo: esconda a borda de baixo do recorte com uma máscara que some no escuro.

### Segunda câmera: o que veio

O pedido de 4 s do Kling 4.0 (referência: 2 quadros dele de frente) veio com **dois planos** num vídeo só, com corte
no meio: ele de costas no computador e um close das mãos no teclado, os dois sem defeito visível e com a estante
dele ao fundo. Dá pra usar os dois (0,5 s cada) e ainda deixar as mãos, escurecidas e desfocadas, de fundo. O vídeo
vem a 24 quadros por segundo: toque quadro por quadro (fica 25% mais rápido, liso) em vez de converter.

### A voz dele

- Voz clonada: a que o criador tiver na conta dele. Ache com `list_voices` (`voice_type: "element"`) e use o
  `voice_id` que vier de lá. Se não houver nenhuma, avise: criar uma voz é decisão dele.
- Funcionam com a voz dele: `seed_audio` e `elevenlabs_v4`. No Eleven v4, `stability` de 0,3 a 0,5 e
  `similarity_boost` 0,9 deixam menos monótono. O Qwen Audio falhou duas vezes com ela.
- Vozes prontas do catálogo têm sotaque americano em português: não use.
- Vários pedidos de voz ao mesmo tempo dão erro 429. Mande um por vez.
- Depois de gerar, transcreva o áudio (`transcrever.py`) pra conferir se ela falou o que estava escrito e pra
  tirar os tempos das palavras da legenda.

### A trilha nova (sempre, parecida com a aprovada)

O criador pediu (24/11/2026): **todo Short ganha uma trilha nova, parecida com a `assets/audio/trilha-ia.mp3`**, a
única de que ele gostou. Ela vai sempre no orçamento da PARADA 2 e só é gerada com o "pode".

- **Modelo:** `elevenlabs_music_v2_5`, `force_instrumental: true`, `duration` igual à do Short (18/11/2026: 9,45 por
  65 s e 16,72 por 115 s). Preço pelo `estimate_audio_cost` (o `get_cost` dentro de `generate_audio` não é aceito).
  `batch_size` até 4 traz variações numa chamada só: consulte o preço com ele, porque multiplica.
- **Nenhum modelo de música do catálogo aceita áudio de referência** (conferido em 24/11/2026). "Parecida" sai da
  descrição do som medido da `trilha-ia.mp3`: eletrônica, 112 bpm, pulso regular de semicolcheias (7,4 ataques por
  segundo), grave cheio, quase nada acima de 4 kHz, volume constante. Não cite artista. Ponto de partida pro pedido:

  ```
  Instrumental electronic track for a tech tutorial about AI agents. 112 BPM, steady driving pulse of
  sixteenth-note synth plucks from the very first second, full warm sub bass, soft dark top end with almost
  nothing bright above 4 kHz, constant energy and volume from start to end. No intro, no breakdown, no build-up,
  no drop, no vocals. Ends cleanly on the last bar.
  ```

- **Meça antes de mostrar** e compare com a `trilha-ia.mp3`: andamento pelos ataques acima de 200 Hz, ataques por
  segundo, energia acima de 4 kHz, volume por segundo. A de 115 s de 18/11 veio com 19 s de introdução 7 dB mais
  baixa, apesar do pedido de energia constante: subi o trecho em 6 dB (`volume` com expressão por tempo) em vez de
  cortar. Se a faixa nova ficou longe da padrão em algum número, diga qual ao entregar.
- **A faixa termina sozinha no último segundo**, então não há emenda. Volume ~16 dB abaixo da voz (`estilo.md`).
- **Quem escolhe é ele:** monte a versão com a trilha nova, corte os primeiros ~15 s dela e da mesma versão na
  trilha padrão (`ffmpeg -t 15`) e junte os dois em sequência com `comparar.py seq` (ele só aceita arquivos
  inteiros). Ele já reprovou quatro faixas geradas seguidas; se
  reprovar a nova, o Short fica com a padrão (estendida com `trilha_ia_estender.py` quando passar de 42 s).

### Efeitos sonoros

O criador pediu (24/11/2026): **no acabamento, cada animação ganha um efeito gravado escolhido pra ela.** A versão 1
usa os sons de `assets/audio/` e os sintetizados do `motion.py`, que ele chamou de "acabamento de máquina".

1. **A lista.** Cada `Motion.sfx` da cena é uma linha: tempo, o que se mexe e o som que aquilo pede ("painel entra
   pela direita: passagem curta e brilhante, 0,4 s"; "número gigante: impacto seco"; "pedido digitado: teclado
   mecânico, toques curtos").
2. **A biblioteca primeiro.** `~\shorts-canal\_sons\sons.json` guarda cada som já baixado (id do catálogo, título,
   duração, arquivo, onde o som começa, pico, volume médio e pra que movimento serviu). O que já existe ali não se
   baixa de novo.
3. **Busca no catálogo** (`search_sound_effects`, livre), em inglês, descrevendo o movimento: "user interface swipe
   whoosh short", "keyboard typing mechanical short", "impact hit short punchy", "digital data glitch",
   "riser short". Escolha pelo título e pela duração: você não ouve, então não gaste a cota de prévia
   (`preview_sound_effect`) à toa.
4. **Baixe só os escolhidos** (`download_sound_effect`, qualidade `normal`): cada chamada gasta a cota de downloads.
   A resposta é um link que vence (~24 h): salve na hora com `curl -sSL -o` em `_sons\`, reaproveite o link se
   precisar de novo e nunca repita a chamada no escuro depois de uma falha. Medido em 24/11/2026: 8 downloads
   seguidos não mexeram no saldo de créditos (só na cota de downloads). A duração que a busca devolve é
   arredondada pra baixo ("0 s" quer dizer menos de 1 s), e alguns arquivos chegam com pico acima de 0 dB ou com
   mais de 1 s de silêncio no começo: meça antes de escolher o volume e o `corte`.
5. **Meça e apare** (onde o som começa, pico, volume médio) e anote no `sons.json`. Na cena,
   `Motion.sfx(t, 'caminho.mp3', volume, {corte, dur, entra, sai})` usa o arquivo; `motion.py som <pasta>` refaz só
   a pista, sem renderizar a imagem de novo.
6. **Faltou no catálogo:** gere com o `mirelo_text_to_audio` (cerca de 0,4 cada; o catálogo diz que é de outro
   fluxo, mas aceita). Os dele chegam com silêncio no começo e volume de −44 a −55 dB: meça e aumente. Sintetizado
   do `motion.py` ('vuush', 'pop', 'tique'...) não entra no Short final.

Os sons do catálogo chegam pela integração do Higgsfield com a Epidemic Sound. Antes do primeiro Short publicado com
eles, confira nos termos do Higgsfield se o uso em vídeo publicado está coberto.

## O que mais o catálogo tem (preços consultados em 13/11/2026; o que já foi testado está logo abaixo da tabela)

Preços por `get_cost` em 13/11/2026, vertical, 1080p quando não diz outra coisa:

| Recurso | Ferramenta ou modelo | Preço consultado | Serve pra quê nos Shorts |
|---|---|---|---|
| Estender o vídeo dele pra vertical | `reframe` (9:16) | 11 s: 36 em 480p, 52 em 720p; 13 s em 1080p: 159 | a câmera é um close 16:9: gera a sala acima e abaixo dele |
| Estender uma foto do cenário | `outpaint_image` | não consultado (precisa da imagem) | mesmo fim, só pro alto, onde não há corpo dele |
| Plano novo com referências | `kling4_0` (`reference-to-video` ou `image-to-video`), 5 s | 16,25 | segunda câmera, transição com quadro inicial e final |
| Idem, modelos caros | `seedance_2_5` omni, `cinematic_studio_video_4_0`, 5 s | 80 cada | só se o Kling errar o rosto |
| Plano a partir de uma imagem | `veo3_1`, 4 s | 16 | animar uma foto gerada do segundo ângulo |
| Imagem de referência | `gpt_image_2_6` | 0,25 | acertar o segundo ângulo em foto antes de pagar o vídeo |
| Boca sincronizada com áudio novo | `sync_so` (vídeo + áudio), 5 s | 18 | fala gerada com ele em cena |
| Mapa de profundidade | `depth_anything_video` | pede `frames_count` e `frame_rate` | efeitos com profundidade real |
| Nitidez, 60 fps, HDR | `topaz_video`, `fps_boost`, `topaz_hyperion_2_5` | sem consulta de preço | mexem na imagem dele: só com ordem dele |
| Efeitos prontos pra vídeo de rosto | workflow `reel-effects` (roda no sandbox do Higgsfield) | só o recorte (1) | janela do app atrás da cabeça, texto atrás, legendas, sons gravados |
| Análise de gancho e retenção | `virality_predictor` | sem consulta de preço | diagnóstico do Short pronto |
| Capa | workflow `thumbnail-generation` | não consultado | capa do Short |
| Outros idiomas | modelo `dubbing`, workflow `creator-dub` | não consultado | versão em inglês ou espanhol |

A voz clonada do criador continuava na conta nessa data.

### O que foi testado depois (13/11/2026, vídeo "Clona Qualquer App", pasta `testes-higgsfield/`)

Rodada autorizada pelo criador com teto de 200; gastou 86,73. O veredito dele sobre cada teste ainda não tinha
chegado quando isto foi escrito: aqui está só o que funcionou tecnicamente.

- **`reframe` (25,5 por 4,9 s em 720p).** Recebe o recorte 1:1 dele (1080x1080) e devolve 9:16 com a estante em
  cima e o corpo embaixo. Devolve a **24 quadros por segundo, sem som**, com o tempo preservado, e o original cai
  dentro dele com escala ~0,66 e alguns pixels de deslocamento. Não use o resultado direto: o rosto ali é
  regenerado. Componha com `compor_vertical.py` (em `S/gerados`): mede o encaixe com SIFT, iguala a cor e põe
  o **original nítido por cima**, com borda macia de 70 px embaixo e só 22 px em cima (a cabeça gerada fica um
  pouco mais alta que a real e, com borda larga em cima, aparece uma sombra acima do cabelo).
- **`outpaint_image` (2).** Estende uma foto dele pra 9:16; saiu sem defeito. Serve de quadro inicial pro Kling.
- **Segunda câmera em dois passos.** Primeiro a foto no `gpt_image_2_6` (0,25) com um quadro dele de referência,
  depois o vídeo no `kling4_0` `image-to-video` com `start_image` (16,25 por 5 s em 1080p). Peça o monitor
  "completamente fora de foco, sem texto legível". A foto por cima do ombro e a das mãos no teclado saíram
  usáveis de primeira; o vídeo das mãos também (24 quadros por segundo, 1076x1924).
- **Entrada no monitor.** `kling4_0` com `start_image` = a foto por cima do ombro e `end_image` = a tela real
  (recorte da página montado em 1080x1920): a câmera passa pelo ombro e termina na página real, legível. Chega
  na página por volta de 3 s e segura; no Short use o trecho de 0,6 a 3,3 s acelerado ~1,8 vez. No meio do
  caminho a tela é inventada (some rápido).
- **Por que a entrada no monitor "bugou" (palavra do criador, 13/11/2026):** a foto inicial tinha uma tela inventada
  no monitor e o quadro final era a página real em layout vertical. O modelo teve que trocar o conteúdo no meio
  do caminho: a página aparece nítida antes de a câmera chegar, surge uma barra de navegador inventada e o zoom
  acontece em dois tempos. Conserto a testar: colar a **página real no monitor já na foto inicial** (em
  perspectiva, desfocada como o resto), terminar num quadro que seja o close daquela mesma tela, e fazer o último
  meio segundo de entrada com os pixels reais, na cena.
- **O conserto funcionou (segundo pacote, 13/11/2026):** a foto inicial foi refeita no `gpt_image_2_6` com duas
  referências (a foto por cima do ombro + a captura real da página) pedindo "mude só o que o monitor mostra", e o
  quadro final passou a ser um recorte vertical da captura real (810x1440 ampliado pra 1080x1920). O Kling fez um
  dolly contínuo, sem barra inventada e sem zoom em dois tempos. Só o parágrafo de letra pequena ainda embaralha
  por alguns quadros na chegada: o `fundir_real.py` (em `S/gerados`) acha com SIFT onde a captura real cai em
  cada quadro e troca a página gerada pela real, acompanhando a câmera (mistura de 0 a 100% em ~0,5 s).
- **Câmera 2 aberta, por trás** (foto no `gpt_image_2_6` com um quadro aberto real da sala de referência + Kling
  `image-to-video`): saiu limpa de primeira, com gesto natural e a sala coerente. A foto inventou uma câmera no
  tripé com telinha (a dele é um celular): diga no prompt o que é a câmera principal.
- **Câmera 2 de lado, com ele falando:** `seedance_2_5` `omni_reference` em rascunho (15) com `start_image` = foto
  de três quartos gerada antes, `image_references` = quadro real do rosto, `video_references` = a tomada real e
  `audio_references` = o áudio real. Devolveu 480x854 a 24 quadros por segundo com o **áudio real no mesmo tempo**
  (correlação de envelope 0,70, atraso 0 ms), então a boca foi gerada em cima da fala de verdade. Com três Kling
  rodando o Seedance devolve 429 sem cobrar: reenvie quando um terminar.
- **Como os planos gerados entram na cena (versão 4 do "Clona Qualquer App"):** cada plano vira uma pasta de
  quadros já no tempo do encaixe (`cena/quadros/insX/00001.jpg`, 30 por segundo, 1080x1920) e uma camada
  `<div class="ins"><img data-dir="quadros/insX"></div>` logo antes de `#legendas`, ligada por uma função
  `ins(id, t, [início, fim, n])` que escreve `img.dataset.quadro`. A legenda continua por cima. Câmera 2 com ele
  falando entra **no mesmo tempo da fala** (nada de acelerar). A entrada no monitor fica por baixo do escurecido
  do pé do quadro e a página da cena começa exatamente onde ela termina (`z = 1080/810`, `sx = 1055`, `sy = 480`
  com `ay = 640` pro recorte 650..1460 da captura): assim a emenda não aparece.
- **Emenda entre plano gerado e cena (versão 5, palavra do criador: "levemente bugado, não ficou fluido"):** a causa não
  era o modelo. Medido quadro a quadro com SIFT: (1) Kling a 24 q/s acelerado 2,19x e amostrado a 30 andava
  "76, 76, 36 %/s" (um quadro em cada quatro pela metade); (2) o zoom parava de vez na chegada; (3) a cena começava
  outro movimento logo depois. Conserto, no `entrada_suave.py` de `S/gerados`: longe da tela, quadros do clipe
  de 2 em 2 (2,5x exato); perto, a posição da câmera vira uma curva de Hermite em log da escala que desacelera até a
  velocidade do empurrão lento da cena, e cada quadro do Kling é deformado pra cair nela, com a captura real por cima;
  na cena, o zoom continua dessa mesma velocidade (sem `dentroFora` logo depois da chegada) e o deslize lateral virou
  um movimento só, lento. **Antes de trocar de modelo, meça a velocidade quadro a quadro.**
- **Motion real na tela de um plano gerado (versão 6):** peça a foto com o monitor em **verde de recorte** ("solid,
  flat, uniform pure green, no reflections"), gere o vídeo com `start_image` e `end_image` iguais e câmera travada, e
  cole o motion com `colar_tela.py`: acha o quadrilátero da tela pela união do verde (reta ajustada em cada lado, a
  direita mesmo meio coberta pela cabeça), recorta pelo verde em cada quadro (a cabeça passa na frente) e tira o
  reflexo verde em volta. A tela fica com os pixels exatos do motion. O criador sugeriu mandar o motion como referência
  pro modelo; não fiz porque o modelo redesenha a tela e embaralha o texto.
- **Não existe gravação do Claude gerando o app** nos brutos desse vídeo (a conversa aparece pronta): o "time-lapse"
  é um motion (`timelapse_tela.py`) com a captura real do pedido e o clone real se montando painel por painel.
- **Finalizar rascunho do Seedance custou mais que o consultado (erro meu, 13/11/2026):** o `get_cost` de uma
  geração direta em 720p deu 35; a finalização com `draft_job_id` e `resolution: "720p"` cobrou **80** e devolveu
  1080x1920. O criador tinha aprovado 35. Antes de finalizar, rode o `get_cost` **da própria chamada de finalização**
  (com `draft_job_id`) e mostre esse número a ele. A finalização também exige `prompt` e as mesmas `medias` do
  rascunho (sem elas dá erro 422).
- **O filtro do Higgsfield pode bloquear um vídeo comum** (status "nsfw" num plano dele de costas na cadeira): o
  crédito é estornado. Não insista sem falar com o criador.
- **Uma tela real virando outra** (Kling com `start_image` e `end_image` reais): funciona, mas o meio do caminho
  enche de itens inventados; tela escura em recorte vertical rende pouco como abertura.
- **Preços consultados em 13/11/2026 pra segunda câmera com ele falando**: `seedance_2_5`
  `omni_reference` de 5 s com foto + vídeo + áudio de referência: 15 em rascunho 480p, 35 em 720p, 80 em 1080p;
  `video_extension` de 4 s em 720p: 28; `intone` (foto dele + áudio real) em 1080p: 112 por ~6,5 s.
- **`sync_so` (16,2 por 4 s).** Vídeo dele + áudio gerado, `sync_mode: "cut_off"`. Só a boca muda, o resto do
  rosto fica igual; alguns quadros saem com biquinho exagerado. É o rosto dele passando por IA: só com ordem dele.
- **Workflow `reel-effects`.** Roda no `sandbox_exec` com `effects.py` (prepare, transcribe, link, build, render).
  `render --stills` pede os tempos assim: `1.9s,3.6s`. O `katana-app-window` aceita a tela real em `screen`. Pra
  trazer vários resultados com um upload só, junte tudo num arquivo no servidor e separe aqui. O upload do
  servidor às vezes devolve 520: guarde a URL num arquivo lá e repita.
- **`virality_predictor`.** Não cobrou crédito; aceita no máximo 16 s. Devolve um HTML com as notas num JSON
  (`analysisJson`): gancho (0 a 3 s), sustentação, pico. São estimativas, não promessa.
- **Efeitos do Mirelo** vieram com volume médio de −44 a −55 dB (pico de −14 a −28): aumente antes de usar.
- **URL de upload sem redigitar:** a resposta do `media_upload` fica gravada no registro da sessão (`.jsonl` em
  `~/.claude/projects/...`); um programa pequeno acha a URL pelo `media_id` e grava num arquivo pro `curl`.

### Câmera 2 com outro ângulo: rosto e fundo (13/11/2026, pasta `testes-higgsfield/r4/`)

O pedido: "só parece que eu girei a cadeira e não mudei o ângulo da câmera". Oito rodadas de foto, um rascunho
bom, e no fim ele preferiu a câmera 2 antiga. O que vale pra próxima:

- **Rosto parecido pede várias referências reais.** Com um quadro de frente, o modelo inventa o perfil: "não ficou
  parecido comigo em nenhuma das versões". Com 9 quadros reais (2 de frente, 3 de três quartos, 3 de perfil, 1 da
  sala) no `gpt_image_2_6`, ficou. Ache os quadros com `miniaturas.py` (ele vira o rosto pra tela várias vezes por
  gravação) e tire cada um em tamanho cheio. No prompt, diga o que conferir: "same nose, thin mustache, mole on
  the cheek, ears, short fade haircut". Depois recorte o rosto gerado ao lado dos reais e compare antes de mostrar.
- **Referência gerada contamina.** Uma foto gerada da sala usada como referência trouxe objetos que não existem
  no estúdio dele. Referência de cenário é sempre quadro real.
- **Mudar o ângulo é mudar o fundo.** Peça onde a câmera está (altura, lado, graus em relação à principal) e o
  que isso faz com o fundo ("the shelf wall runs diagonally and recedes", "we look down onto..."). O ângulo de que
  ele mais gostou foi o alto, olhando de cima, do lado dele.
- **O fundo tem que parecer o mesmo estúdio**, sem copiar a estante: "another corner of the same home studio...
  same interior design: light warm-wood surfaces, warm LED strips under wooden shelves, the same grey vertical
  slat paneling, same warm amber light". Estúdio genérico escuro (espuma acústica, parede preta) ele recusou:
  "tem que ter alguma relação com o vídeo original".
- **Sem objeto de cena inventado.** Um celular num tripé "filmando ele", com a imagem dele na telinha, derrubou a
  foto ("ficou ruim"). Um tripé com softbox no canto passou.
- **Defeito de objeto: gere de novo, não edite.** A mesa saiu com um recorte curvo. Pedir pra editar só a mesa
  manteve o defeito ("continua errado"); gerar de novo com o mesmo prompt resolveu de primeira, por 0,25.
- **Manter o ângulo e trocar o fundo**: passe a foto aprovada como PRIMEIRA referência e escreva "from the first
  reference image keep only the camera angle, the framing and his pose; replace the whole background with...".
- **Duas chamadas de imagem ao mesmo tempo** podem devolver 429 (`rate_limit_reached`) numa delas, sem cobrar:
  reenvie a que falhou. Pra variações do mesmo prompt, use `count` (até 4) numa chamada só.
- **O vídeo** (`seedance_2_5`, `omni_reference`, rascunho de 5 s): `start_image` = a foto escolhida,
  `image_references` = 6 quadros reais do rosto, `video_references` = a tomada real da frente (os gestos),
  `audio_references` = o áudio real, `generate_audio: true`. Prompt: câmera travada ("locked-off tripod shot, no
  camera movement, no cuts, the background stays exactly as in the start image"), "he speaks the reference audio
  exactly, in Brazilian Portuguese, with accurate lip sync: use the reference audio as the soundtrack, unchanged",
  olhar pra câmera principal fora do quadro, "five fingers on each hand". Saiu com correlação 0,82 com a fala real.
- **No Short**: o trecho da palavra, no mesmo tempo da fala, com corte mais fechado
  (`crop=400:711:76:37,scale=1080:1920,unsharp=5:5:0.6` no rascunho de 480x854).

## Modelo de orçamento

Salve em `orcamento.md` e mostre na conversa antes da PARADA 2. O que o Short aprovado usou de verdade: trilha (6),
recorte dele (1 por pedido), câmera 2 (rascunho 15 + finalização 80), entrada no monitor (foto 0,25 + Kling 16,25)
e a tela do PC em verde (foto 0,25 + Kling 16,25): cerca de 135 créditos. O resto do gasto daquela rodada foi teste.
Exemplo de como escrever:

```
Short 01: Humanizer (41 s)
  Sempre no pacote:
    trilha nova de 41 s, parecida com a padrão ... 7
    efeitos gravados: 14 movimentos ............. 9 sons novos (cota de downloads), 5 já na biblioteca
    recorte, 3 trechos num pedido só ............ 1
  Planos gerados:
    entrada no monitor (foto + Kling 4.0, 5 s) .. 16,5
    câmera 2 (foto + Kling 4.0, 5 s) ............ 16,5
Total conhecido: 41 créditos + cota de downloads. Reserva pra refação (uma por plano): 33.
Saldo agora: 1.820.
```
