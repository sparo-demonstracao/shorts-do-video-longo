# Como escolher os momentos, por tipo de vídeo

Esta lista nasceu num canal de tecnologia (IA e automação pra quem não programa, vídeos de 10 a 33 min); os títulos
em itálico são exemplos desse tipo de canal. Os vídeos caem em seis tipos. Descubra o tipo pelo
título, pela descrição e pelos capítulos antes de ler a transcrição: ele decide o que é um bom Short.

## O que todo momento precisa ter

Um Short é assistido por quem nunca viu o vídeo longo. Então o momento:

1. **Faz sentido sozinho.** Nada de "como eu falei", "voltando àquele exemplo", "esse aqui" sem dizer o quê. Um
   Short pode juntar frases de pontos diferentes da gravação (o da versão aprovada tem 7 frases de 5 momentos), desde
   que cada uma seja inteira e a ordem conte uma história: tese, como, resultado, veredito.
2. **Tem uma recompensa que se vê na tela** já no primeiro quadro e cabe em até 2 min: um resultado, um antes e depois, um número, um
   veredito. Explicação sem nada pra ver é o Short mais fraco.
3. **Começa numa frase inteira e termina numa frase inteira.** Use `achar.py --entre` pra ver as pausas: corte
   bom cai numa pausa, nunca no meio de um "é...".
4. **Não é pedido, propaganda nem aviso**: fora "se inscreve", o merchan de produto próprio (curso, comunidade), o patrocinador e os
   agradecimentos, a não ser que ele peça.

Sinais de que um trecho é forte: "olha isso", "ficou assim", "o resultado", "de graça", "o melhor", "nunca mais",
um número dito em voz alta, uma risada ou surpresa dele, um antes e depois na tela. Os capítulos do YouTube são o
mapa: cada capítulo costuma ter um momento assim perto do meio ou do fim.

**Gravação bruta tem erro e repetição.** Quando a mesma frase aparece duas ou três vezes seguidas, a última é a que
valeu. Trecho com muito "é...", tosse ou silêncio longo no meio pede outro corte ou outro momento.

Proponha o dobro de momentos que ele pediu, ordenados do mais forte pro mais fraco, e deixe ele escolher.

**O Short da tese.** Em qualquer tipo de vídeo ele pode preferir um Short que carrega a tese do vídeo inteiro em
vez de um por item ("esse vídeo tem que ter a mesma tese do vídeo longo"). Ofereça sempre as duas coisas na PARADA 1.
O da tese abre com a frase da tese, mostra como se faz, prova com um ou dois resultados e fecha no veredito;
em vídeo de lista, pelo menos 3 itens, cada um com a frase que o apresenta e o resultado na tela.

## Os seis tipos

### 1. Lista ou curadoria
*"Instalei esses repositórios...", "Configure esses 5 mods", "Testei +100 skills: só estas 5".*
Cada item já é um Short pronto: um Short por item, nunca dois itens no mesmo.
- **Gancho:** o que o item faz, em uma frase ("isso aqui tira a cara de IA do seu texto").
- **Meio:** o item funcionando na tela, de preferência com antes e depois.
- **Fecho:** o veredito dele ("esse eu não tiro mais").
- **Cuidado:** a introdução da lista ("existem milhares de...") não entra; o Short começa no item.

### 2. Comparativo
*"Claude Code X Antigravity", "Comparando os 3 melhores modelos", "Fable 5 X Opus".*
Um Short por rodada do teste, ou um só com o vencedor e o motivo.
- **Gancho:** a pergunta do teste ("qual dos dois faz o site mais bonito com o mesmo pedido?").
- **Meio:** os dois resultados, um depois do outro, cada um com a sua `regiao` da tela.
- **Fecho:** quem ganhou e por quê, na voz dele.
- **Cuidado:** um resultado sem o outro não é comparativo. Os dois cabem com folga agora que o Short pode ir a 2 min; se nem assim couberem, escolha outra rodada.

### 3. Lançamento ou novidade
*"Claude 2.0 é INSANO", "O Antigravity 2.0 ficou ABSURDO", "N8N 2.0 chegou".*
Um Short por novidade, começando pela mais surpreendente.
- **Gancho:** a consequência, não o nome do recurso ("agora ele trabalha em quatro coisas ao mesmo tempo").
- **Meio:** a novidade acontecendo na tela.
- **Fecho:** pra quem isso muda o jogo.
- **Cuidado:** corte o que envelhece ("saiu ontem", "ainda tá em beta"). Novidade explicada sem demonstração
  fica pra trás na fila.

### 4. Construção ou tutorial
*"Crie sites de nível agência", "Clona qualquer app", "Automatize sua empresa inteira", "Guia prático".*
O Short mostra o resultado, não o passo a passo.
- **Gancho:** o resultado pronto, já na tela ("esse site saiu de um pedido só").
- **Meio:** o pedido ou o passo que fez a diferença, bem curto.
- **Fecho:** o resultado de novo, funcionando.
- **Cuidado:** instalação, configuração e espera não entram. Se o resultado só aparece no fim do vídeo longo,
  o Short pode abrir com 3 a 4 s desse resultado (um bloco `tela` com os tempos de lá) e depois voltar pro
  trecho escolhido.

### 5. Notícia ou explicação
*"É o fim da API oficial do WhatsApp?", "O Fim dos Agentes de IA".*
Quase tudo é ele falando. Um Short por afirmação.
- **Gancho:** a afirmação forte, como ele disse.
- **Meio:** o motivo, com a fonte na janela flutuante (a página, o anúncio, o print).
- **Fecho:** o que a pessoa faz com isso.
- **Cuidado:** não corte a ressalva que torna a afirmação verdadeira. Short que distorce o que ele disse é pior
  que Short nenhum.

### 6. Curso ou aula longa
*"CURSO COMPLETO de Claude Code + Antigravity" (1h33).*
Trate cada capítulo como um vídeo: descubra o tipo de cada um (quase sempre 4) e aplique a regra dele. Rende de
8 a 15 Shorts; combine com ele quantos fazer por vez.

## O arquivo de momentos

Salve em `momentos.json`, um por candidato:

```json
{
  "tipo_do_video": "lista",
  "momentos": [
    {
      "n": 1,
      "titulo": "Humanizer tira a cara de IA do texto",
      "capitulo": "Humanizer: texto de IA com cara de humano",
      "in": 512.4, "out": 556.9,
      "primeira_fala": "esse aqui pega o texto que a IA escreveu",
      "ultima_fala": "esse eu não tiro mais",
      "o_que_se_ve": "texto antes e depois lado a lado, marcações em laranja",
      "por_que_funciona": "antes e depois visível, veredito no fim, não depende do resto",
      "ideia_de_motion": "no 'tira a cara de IA', a tela recua e as marcações laranja saem do texto uma a uma, com um contador de trechos reescritos",
      "precisa_de_ligacao": "não"
    }
  ]
}
```

`in` e `out` são tempos da **gravação bruta**, achados com `achar.py`. `ideia_de_motion` é opcional: muitos
momentos não pedem motion, e nesse caso o campo fica `"nenhum"`. No topo do arquivo, anote também
`"estilo_dos_motions"`: a linguagem visual escolhida pra este vídeo, em uma frase.

Na conversa, mostre a lista como uma tabela curta (número, título, duração, o que se vê, ideia de motion) e
espere a escolha dele.

## Que motion costuma caber em cada tipo

São pontos de partida, não regra: o que manda é a fala do trecho.

| Tipo | Onde o motion ajuda |
|---|---|
| Lista | O que o item faz por dentro; o antes e o depois lado a lado com a diferença marcada |
| Comparativo | Placar que sobe a cada rodada; os dois resultados numa grade com o critério em destaque |
| Lançamento | O que mudou: a versão antiga e a nova, com a novidade acendendo |
| Construção | O caminho do pedido até o resultado; as peças que formam o app |
| Notícia | A afirmação em tipografia grande; a linha do tempo do que aconteceu |
| Curso | O mapa do que a aula cobre; a camada que cada conceito ocupa |
