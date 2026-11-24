# O Short aprovado (versão 8, 13/11/2026)

"Agora qualquer pessoa clona qualquer app", 38,2 s. É a versão que o criador escolheu depois de 9.

| Arquivo | O que é |
|---|---|
| `folha-v8.jpg` | 28 quadros com o tempo. **Abra com Read antes de planejar um Short.** |
| `short-aprovado.mp4` | O vídeo (cópia leve, 720p). |
| `motion.html` | A cena inteira. Consulte pra ver como cada parte foi escrita; não é molde pra trocar texto. |
| `variante.js` | A linha que escolhe a abertura (`'c'` = a aprovada; `'a'` e `'b'` são as preteridas). |
| `roteiro.json`, `plano.json` | As falas (14 pedaços de 7 frases) e a montagem. |

Onde está cada coisa no `motion.html` (procure pelo nome da função ou do comentário):

| Tempo | Parte | No código |
|---|---|---|
| 0 a 1,63 s | Abertura de tela cheia: ler o original, a planta desce, o clone é impresso, a câmera desce | `aberturaC`, constantes `AB` e `ABP` |
| 1,6 a 2,47 s | Ele no cenário real com o clone atrás da cabeça | `ele`, bloco "G" do `M.quadro` |
| 2,47 a 3,63 s | Câmera 2 (plano gerado) | `ins('insC', ...)`, `INS.C` |
| 3,63 a 4,57 s | "MENOS DE 1 HORA" | `#fato` |
| 4,57 a 6,1 s | Entrada no monitor (plano gerado) emendando na página real | `ins('insA', ...)`, o `hermite` do bloco "M1" |
| 6,1 a 15,2 s | Página real com miras, diagrama, link voando, pedido digitado, barra de passos | bloco "M1", `chip`, `pedido`, `passos` |
| 15,2 a 19,5 s | Ele com o clone; time-lapse na tela do PC (plano gerado com motion colado) | `ins('insT', ...)` |
| 19,5 a 27 s | Lentes do que foi clonado e do que foi adicionado, com selos | bloco "M2", `selos` |
| 27 a 33,9 s | Os dois clones; áudio vira texto | bloco "M3" |
| 33,9 a 38,2 s | Recapitulação; ele com o nome do repositório atrás | bloco "M4", `nomes` |

O código das variantes `'a'`, `'b'` e a linha `window.CAM2` são restos das versões 7 e 9. Num Short novo, nada disso
entra: escreva a partir do `../esqueleto-cena.html`.

Os materiais (capturas, quadros dele, planos gerados) ficaram na pasta daquele vídeo e não acompanham a skill.
