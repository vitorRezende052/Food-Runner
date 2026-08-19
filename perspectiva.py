"""Converte a posicao logica de um objeto em pixels de tela.

O resto do jogo descreve cada objeto com apenas dois numeros:

- ``pista``: 0, 1 ou 2 (aceita valor quebrado enquanto o jogador desliza entre
  duas faixas);
- ``z``: a profundidade, ``1.0`` no horizonte e ``0.0`` na altura do jogador.

Este modulo e o unico que sabe traduzir isso para pixels. Assim colisao, spawn e
dificuldade continuam sendo matematica pura sobre ``pista`` e ``z``.
"""

import config


def fator(z):
    """Quanto um objeto na profundidade z encolhe: 1.0 na base, perto de 0 no fundo.

    Passando do jogador (z negativo) o objeto fica maior que 1.0, como manda a
    perspectiva. Um piso em ``Z_MINIMO`` segura o z bem antes do ponto em que a
    divisao explodiria.
    """
    return 1.0 / (1.0 + max(z, config.Z_MINIMO) * config.PROFUNDIDADE)


def deslocamento_da_pista(pista):
    """Distancia horizontal, em pixels, do centro da pista ate o meio da estrada."""
    pista_central = (config.QTD_PISTAS - 1) / 2
    return (pista - pista_central) * config.LARGURA_PISTA_BASE


def projetar(pista, z):
    """Devolve (x, y, escala) na tela para um objeto na pista e profundidade dadas."""
    escala = fator(z)
    x = config.MEIO_X + deslocamento_da_pista(pista) * escala
    y = config.HORIZONTE_Y + (config.BASE_Y - config.HORIZONTE_Y) * escala
    return x, y, escala
