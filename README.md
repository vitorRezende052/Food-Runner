# Food Runner

Jogo de corrida em três pistas para a disciplina de Fábrica de Software. O atleta corre sozinho por uma rua em perspectiva. Você escolhe a pista para coletar frutas e verduras e desviar dos ultraprocessados. Python facilita testar as regras da partida, e o pygame-ce reúne desenho, teclado e som na mesma janela.

## Jogar no Windows

[Baixe o Food-Runner.exe para Windows de 64 bits](https://github.com/vitorRezende052/Food-Runner/releases/download/v0.1.0/Food-Runner.exe). Salve-o em uma pasta onde você possa gravar arquivos e abra-o com um duplo clique. O executável inclui o Python. Ao fim da partida, o jogo salva o recorde em `recorde.json` nessa pasta.

## Rodar pelo código-fonte

Instale o [uv](https://docs.astral.sh/uv/getting-started/installation/) e baixe ou clone o repositório. Na pasta do projeto, execute os comandos abaixo. Na primeira vez, o uv precisa de internet para obter o Python 3.12 e as dependências.

```sh
uv sync --locked
uv run main.py
```

Para executar os testes, use `uv run pytest`.

## Controles e regras

| Tecla | Ação |
|---|---|
| Enter ou Espaço | Inicia a corrida ou joga novamente após o game over |
| ← / → ou A / D | Troca de pista |
| Esc ou P | Pausa ou retoma a partida |
| M | Volta ao menu durante a pausa ou após o game over |
| Esc no menu | Fecha o jogo |

Você começa com **45 kg**. Frutas e verduras (disco verde) reduzem o peso em 2 kg e somam 50 pontos. Ultraprocessados (disco vermelho) acrescentam 4 kg. Aos **100 kg**, a partida termina. A pontuação final soma os pontos da distância percorrida e os bônus de coleta.

Nos primeiros três minutos, a velocidade, a frequência de alimentos e a chance de ultraprocessados aumentam. A partir da metade desse período, os alimentos aparecem aos pares em pistas diferentes.

## As três sprints no histórico

| Sprint | Marcos registrados |
|---|---|
| 1 · Movimento e colisão | [Estrada e troca de pista](https://github.com/vitorRezende052/Food-Runner/commit/78f883e), [alimentos vindos do horizonte](https://github.com/vitorRezende052/Food-Runner/commit/9983faf) e [colisão na pista do jogador](https://github.com/vitorRezende052/Food-Runner/commit/b97d85e). |
| 2 · Peso, pontuação e dificuldade | O [mesmo commit da colisão](https://github.com/vitorRezende052/Food-Runner/commit/b97d85e) aplicou peso e pontos. Depois vieram a [rampa de dificuldade](https://github.com/vitorRezende052/Food-Runner/commit/fc4f469) e o [ajuste de balanceamento](https://github.com/vitorRezende052/Food-Runner/commit/9f21c36). |
| 3 · Arte, som, telas e testes | [Menu, pausa, game over e recorde](https://github.com/vitorRezende052/Food-Runner/commit/b4bdffb), [áudio sintético](https://github.com/vitorRezende052/Food-Runner/commit/c889ea2), [animação do corredor](https://github.com/vitorRezende052/Food-Runner/commit/8177dbe), [cenário urbano](https://github.com/vitorRezende052/Food-Runner/commit/689bebd) e [efeitos visuais com testes](https://github.com/vitorRezende052/Food-Runner/commit/4e7a9dc). |

O [plano do projeto](PLAN.md) registra as fases de desenvolvimento e a validação da entrega.
