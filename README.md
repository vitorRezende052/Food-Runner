# Food Runner

Endless runner de mesa, no estilo Subway Surfers, com temática de alimentação
saudável. O personagem corre sozinho por três pistas em perspectiva; o jogador
só troca de faixa para desviar dos ultraprocessados e coletar comida de verdade.
Feito em Python com [pygame-ce](https://pyga.me/), como trabalho acadêmico
individual.

## Como rodar

O projeto usa [uv](https://docs.astral.sh/uv/) para o ambiente e as
dependências — não é preciso criar venv nem instalar nada à mão:

```sh
uv run main.py
```

Na primeira execução o `uv` baixa o Python 3.12 e as dependências
(`pygame-ce` e `numpy`) sozinho.

## Como jogar

| Tecla | O que faz |
|---|---|
| ← → ou A D | troca de pista |
| ESC ou P | pausa a corrida |
| Espaço ou Enter | começa a partida e joga de novo depois do game over |
| M | volta ao menu (na pausa e no game over) |
| ESC no menu | fecha o jogo |

As regras:

- **Comida ruim** (vermelha: hambúrguer, batata frita, refrigerante, donut)
  aumenta o peso.
- **Comida boa** (verde: maçã, brócolis, cenoura, carne grelhada) diminui o peso
  e ainda dá pontos de bônus.
- A pontuação é a distância percorrida mais os bônus.
- Chegou a **100 kg**, a corrida acaba. O número do peso fica alaranjado quando
  a balança se aproxima do limite.
- A partida vai **apertando**: em três minutos a corrida fica duas vezes mais
  rápida, a comida vem mais seguido, o ultraprocessado fica mais provável e,
  passada a metade da rampa, cada spawn solta duas comidas em pistas diferentes.
  Sempre sobra uma pista livre — quem perde escolheu mal, não deu azar.

A maior pontuação fica gravada em `recorde.json`, ao lado do jogo, e aparece no
menu e na tela de game over.

## Como testar

```sh
uv run pytest
```

A suíte cobre a lógica pura — perspectiva, troca de pista, spawn, peso,
pontuação, rampa de dificuldade, telas, recorde e síntese de áudio — sem abrir
janela nenhuma. A camada gráfica não é testada de propósito.

## Como está organizado

| Arquivo | Responsabilidade |
|---|---|
| `main.py` | ponto de entrada: loop, teclado e troca entre as telas |
| `config.py` | todas as constantes: tela, cores, balanceamento, áudio |
| `perspectiva.py` | projeta `(pista, profundidade)` em pixels de tela |
| `jogador.py` | pista atual e o deslize até a pista vizinha |
| `comida.py` | cardápio, sorteio do spawn e avanço dos alimentos |
| `dificuldade.py` | a rampa: velocidade, spawn, chance de comida ruim e rajada |
| `jogo.py` | o estado da partida: peso, pontuação, colisões e fim de jogo |
| `desenho.py` | cenário em perspectiva, comidas, personagem e HUD |
| `telas.py` | menu, pausa e game over |
| `audio.py` | os quatro sons, sintetizados com numpy — sem arquivo externo |
| `recorde.py` | lê e grava a maior pontuação |
| `testes/` | os testes pytest da lógica pura |

A ideia que sustenta o desenho: cada objeto do jogo é descrito por só dois
números — a **pista** (0, 1 ou 2) e a **profundidade `z`** (1,0 no horizonte,
0,0 na altura do jogador). Só o `perspectiva.py` sabe transformar isso em pixel,
então colisão, spawn e dificuldade continuam sendo matemática pura e testável.

O plano de execução, fase a fase, e as decisões tomadas no caminho estão no
[`PLAN.md`](PLAN.md).
