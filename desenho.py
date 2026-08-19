"""Desenha o cenario em perspectiva, as comidas e o jogador.

Este e o lado grafico do jogo: recebe as posicoes logicas prontas, pergunta a
``perspectiva`` onde elas caem na tela e pinta. Nenhuma regra do jogo mora aqui.
"""

import pygame

import comida
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


def desenhar_comidas(tela, comidas):
    """Desenha as comidas da mais distante para a mais proxima.

    Nessa ordem a comida que esta na frente cobre a que vem atras, que e o que a
    perspectiva pede.
    """
    for alimento in sorted(comidas, key=lambda item: item.z, reverse=True):
        _desenhar_comida(tela, alimento)


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
    andado = tempo * config.VELOCIDADE_JOGO
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


def _cor_da_comida(alimento):
    """Verde para a comida boa, vermelho para a ruim."""
    if alimento.tipo == comida.BOA:
        return config.COR_COMIDA_BOA
    return config.COR_COMIDA_RUIM


def _desenhar_comida(tela, alimento):
    """Coloca a comida apoiada no asfalto, do tamanho que a distancia manda."""
    x, y, escala = perspectiva.projetar(alimento.pista, alimento.z)
    lado = config.TAMANHO_COMIDA * escala
    caixa = pygame.Rect(0, 0, lado, lado)
    caixa.midbottom = (x, y)
    _DESENHOS_POR_FORMA[alimento.forma](tela, _cor_da_comida(alimento), caixa)


def _desenhar_circulo(tela, cor, caixa):
    pygame.draw.circle(tela, cor, caixa.center, caixa.width / 2)


def _desenhar_quadrado(tela, cor, caixa):
    arredondamento = round(caixa.width * config.ARREDONDAMENTO_COMIDA)
    pygame.draw.rect(tela, cor, caixa, border_radius=arredondamento)


def _desenhar_triangulo(tela, cor, caixa):
    pygame.draw.polygon(tela, cor, [caixa.midtop, caixa.bottomleft, caixa.bottomright])


def _desenhar_losango(tela, cor, caixa):
    pygame.draw.polygon(
        tela, cor, [caixa.midtop, caixa.midright, caixa.midbottom, caixa.midleft]
    )


def _desenhar_garrafa(tela, cor, caixa):
    """Retangulo alto e estreito: o refrigerante."""
    estreitamento = caixa.width * (1 - config.LARGURA_GARRAFA)
    garrafa = caixa.inflate(-estreitamento, 0)
    arredondamento = round(garrafa.width * config.ARREDONDAMENTO_COMIDA)
    pygame.draw.rect(tela, cor, garrafa, border_radius=arredondamento)


def _desenhar_rosquinha(tela, cor, caixa):
    """Anel: o furo do donut deixa o asfalto aparecer."""
    raio = caixa.width / 2
    espessura = max(1, round(caixa.width * config.ESPESSURA_ROSQUINHA))
    pygame.draw.circle(tela, cor, caixa.center, raio, espessura)


_DESENHOS_POR_FORMA = {
    comida.CIRCULO: _desenhar_circulo,
    comida.QUADRADO: _desenhar_quadrado,
    comida.TRIANGULO: _desenhar_triangulo,
    comida.LOSANGO: _desenhar_losango,
    comida.GARRAFA: _desenhar_garrafa,
    comida.ROSQUINHA: _desenhar_rosquinha,
}
