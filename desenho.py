"""Desenha o cenario em perspectiva e o jogador.

Este e o lado grafico do jogo: recebe as posicoes logicas prontas, pergunta a
``perspectiva`` onde elas caem na tela e pinta. Nenhuma regra do jogo mora aqui.
"""

import pygame

import config
import perspectiva


def desenhar_cenario(tela, tempo):
    """Pinta o fundo, a estrada, as linhas de chao rolando e as divisorias das pistas.

    ``tempo`` e o tempo de jogo em segundos: e so ele que faz o chao rolar.
    """
    tela.fill(config.COR_FUNDO)
    _desenhar_estrada(tela)
    _desenhar_linhas_de_chao(tela, tempo)
    _desenhar_divisorias(tela)


def desenhar_jogador(tela, jogador):
    """Desenha o personagem em pe na pista onde ele esta deslizando."""
    x, y, escala = perspectiva.projetar(jogador.pista_visual, config.Z_JOGADOR)
    largura = config.LARGURA_JOGADOR * escala
    altura = config.ALTURA_JOGADOR * escala

    corpo = pygame.Rect(0, 0, largura, altura)
    corpo.midbottom = (x, y)
    arredondamento = round(config.ARREDONDAMENTO_JOGADOR * escala)
    pygame.draw.rect(tela, config.COR_JOGADOR, corpo, border_radius=arredondamento)

    raio = config.RAIO_CABECA_JOGADOR * escala
    pygame.draw.circle(tela, config.COR_CABECA_JOGADOR, (x, corpo.top - raio), raio)


def _bordas_da_estrada():
    """Pistas imaginarias meia faixa alem da primeira e da ultima: os limites do asfalto."""
    return -0.5, config.QTD_PISTAS - 0.5


def _ponto(pista, z):
    """Coordenada (x, y) na tela, sem a escala, do jeito que o pygame quer."""
    x, y, _ = perspectiva.projetar(pista, z)
    return x, y


def _desenhar_estrada(tela):
    """Preenche o trapezio do asfalto, estreito no horizonte e largo na base."""
    esquerda, direita = _bordas_da_estrada()
    cantos = [
        _ponto(esquerda, config.Z_HORIZONTE),
        _ponto(direita, config.Z_HORIZONTE),
        _ponto(direita, config.Z_FUNDO_TELA),
        _ponto(esquerda, config.Z_FUNDO_TELA),
    ]
    pygame.draw.polygon(tela, config.COR_PISTA, cantos)


def _profundidades_das_linhas(tempo):
    """Profundidade de cada linha de chao no instante dado.

    As linhas ficam igualmente espacadas em z e caminham juntas em direcao ao
    jogador; ao sair pelo rodape cada uma reaparece la no horizonte.
    """
    trecho_visivel = config.Z_HORIZONTE - config.Z_FUNDO_TELA
    espacamento = trecho_visivel / config.QTD_LINHAS_CHAO
    andado = tempo * config.VELOCIDADE_CHAO
    return [
        config.Z_FUNDO_TELA + (indice * espacamento - andado) % trecho_visivel
        for indice in range(config.QTD_LINHAS_CHAO)
    ]


def _desenhar_linhas_de_chao(tela, tempo):
    """Risca o asfalto de lado a lado para dar a sensacao de velocidade."""
    esquerda, direita = _bordas_da_estrada()
    for z in _profundidades_das_linhas(tempo):
        escala = perspectiva.fator(z)
        espessura = max(1, round(config.ESPESSURA_LINHA_CHAO * escala))
        pygame.draw.line(
            tela, config.COR_LINHA_CHAO, _ponto(esquerda, z), _ponto(direita, z), espessura
        )


def _desenhar_divisorias(tela):
    """Traca as linhas que separam as pistas, do horizonte ate a base."""
    esquerda, _ = _bordas_da_estrada()
    for indice in range(config.QTD_PISTAS + 1):
        divisoria = esquerda + indice
        pygame.draw.line(
            tela,
            config.COR_FAIXA,
            _ponto(divisoria, config.Z_HORIZONTE),
            _ponto(divisoria, config.Z_FUNDO_TELA),
            config.ESPESSURA_DIVISORIA,
        )
