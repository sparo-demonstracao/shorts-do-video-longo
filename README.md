# Shorts do vídeo longo

Skill pro Claude Code que transforma um vídeo longo do seu canal em Shorts verticais prontos (até 2 min), a partir
das gravações brutas.

O Short sai como uma animação só, do primeiro ao último quadro:

- a sua fala real, sem as pausas;
- o material real da tela em tela cheia, com a câmera andando;
- motions que explicam quase toda frase, criados pelo próprio Claude;
- você em cena só nos trechos em que olha pra câmera;
- legenda palavra por palavra, trilha e efeitos sonoros.

Pra ver como fica: [folha de quadros de um Short pronto](assets/cena/exemplo-aprovado/folha-v8.jpg) e
[o vídeo](assets/cena/exemplo-aprovado/short-aprovado.mp4).

## O que você precisa

- **Claude Code no Windows.** O app de computador é o caminho mais simples: a skill usa o navegador do app pra ler o
  título e os capítulos do vídeo publicado. Os programas foram feitos e testados só no Windows.
- **Python 3.10 ou mais novo** e o **ffmpeg**.
- **As gravações brutas do vídeo** (voz, tela e câmera, juntas ou em arquivos separados) e o link do vídeo publicado.
- **Opcional: uma conta no Higgsfield conectada ao Claude.** Só entra no acabamento pago (trilha nova parecida com a
  aprovada, um efeito sonoro gravado pra cada animação, recorte, planos gerados). A primeira versão do Short sai
  completa sem gastar crédito nenhum.

## Instalar

### Jeito fácil

Cole isto no Claude Code:

```
Instala a skill do repositório https://github.com/sparo-demonstracao/shorts-do-video-longo na minha pasta de skills (.claude/skills/shorts-do-video-longo) e instala o que ela precisa pra rodar, seguindo o README.
```

Depois abra uma conversa nova.

### Na mão

1. Baixe a skill pra pasta de skills do Claude:

```powershell
git clone https://github.com/sparo-demonstracao/shorts-do-video-longo "$env:USERPROFILE\.claude\skills\shorts-do-video-longo"
```

2. Instale as bibliotecas do Python:

```powershell
pip install numpy pillow opencv-python playwright faster-whisper
```

3. Instale o navegador que renderiza as cenas (se você tem o Microsoft Edge, ele já serve e este passo é opcional):

```powershell
python -m playwright install chromium
```

4. Se ainda não tem o ffmpeg:

```powershell
winget install Gyan.FFmpeg
```

5. Abra uma conversa nova no Claude Code.

Na primeira transcrição o programa baixa o modelo de voz (uns 3 GB). É uma vez só.

## Usar

Numa conversa nova, mande o link do vídeo e diga onde estão as gravações:

```
Faz 2 Shorts desse vídeo: https://www.youtube.com/watch?v=XXXXXXXX
As gravações brutas estão em C:\Users\voce\Videos\meu-video
```

O Claude para três vezes pra você decidir:

1. **Os momentos.** Ele mostra os candidatos, com o que cada um ensina, as falas exatas e a duração. Você escolhe os
   momentos e o objetivo do Short: ensinar a ideia inteira ou deixar a pessoa curiosa pra ver o vídeo completo.
2. **A versão 1 e o orçamento.** O Short já vem completo, sem gastar nada. Junto vem a lista do que o Higgsfield pode
   acrescentar, com o preço de cada item. Nada é gerado sem o seu "pode".
3. **A entrega.** O vídeo final, o que foi conferido e o que só você consegue conferir: o Claude não ouve o áudio,
   então cheque o volume da trilha e os efeitos. Junto vêm de 3 a 5 sugestões do que ainda melhoraria o Short; ele
   não faz nenhuma sem você pedir.

Depois é só pedir ajuste do jeito que você falaria com um editor: "a abertura ficou fraca, faz 2 opções", "quero ver
as duas lado a lado", "tira essa frase". Cada rodada vira uma versão nova e nenhuma versão é apagada.

Os arquivos de cada vídeo ficam em `shorts-canal\<nome-do-video>\`, dentro da sua pasta de usuário. As gravações
brutas não são alteradas.

## O que tem aqui

| Pasta | O que é |
|---|---|
| `SKILL.md` | O passo a passo que o Claude segue. |
| `references/` | A receita do formato, o guia de estilo, como criar os motions e as receitas e preços do Higgsfield. |
| `scripts/` | Os programas que transcrevem, cortam, medem a sincronia, renderizam a cena e montam o vídeo. |
| `assets/` | O palco das cenas, o esqueleto de uma cena nova, um Short de exemplo, a trilha e os efeitos sonoros. |

## A skill aprende com você

O `references/estilo.md` guarda o que foi aprovado e reprovado no canal em que este formato nasceu, e o
`references/historico.md` conta como se chegou nele. São o ponto de partida. Conforme você usa, o Claude anota os
seus vereditos nesses arquivos, e o que você pedir diferente passa na frente.

## Atualizar

```powershell
git -C "$env:USERPROFILE\.claude\skills\shorts-do-video-longo" pull
```

Se a skill já anotou vereditos seus, o `pull` pode reclamar de conflito nesses dois arquivos. Peça pro Claude juntar
as duas versões.
