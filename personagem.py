"""O corredor, visto de costas, correndo.

O boneco e montado peca por peca (pernas, tronco, shorts, bracos e cabeca) em
cima de um unico ponto de apoio: o lugar em que os pes tocam a pista. Cada
medida vem do ``config`` em fracao da altura ou da largura do personagem, entao
a perspectiva encolhe o corredor inteiro so multiplicando pela escala.

A animacao sai de quatro contas puras sobre a fase da passada, logo abaixo. A
fase, por sua vez, vem da distancia percorrida, e nao de um cronometro proprio:
e assim que a corrida acelerando pela rampa de dificuldade acelera a passada
junto, sem uma linha de codigo a mais.
"""

import math

import pygame

import config
import desenho
import perspectiva


def fase_da_passada(distancia):
    """Onde o corredor esta no ciclo: 0.0 numa pisada, 1.0 na pisada seguinte."""
    return (distancia * config.PASSADAS_POR_Z) % 1.0


def balanco(fase):
    """De -1 a 1: para onde vao os membros, uma volta a cada passada.

    Um lado do corpo usa o valor e o outro usa o oposto, entao quando um sobe o
    outro desce.
    """
    return math.sin(2 * math.pi * fase)


def elevacao(fase):
    """De 0 a 1: o quanto o corpo esta no alto, duas voltas a cada passada.

    Vale zero nas duas pisadas do ciclo (no comeco e no meio) e chega ao maximo
    entre elas, quando o corredor esta no ar.
    """
    return (1 - math.cos(4 * math.pi * fase)) / 2


def esticamento(fase):
    """Squash & stretch: menor que 1 na pisada, maior que 1 no ar.

    Acompanha a ``elevacao``, entao o boneco comprime exatamente quando o pe
    bate no chao e estica quando o quique o joga para cima.
    """
    return 1 + config.JOGADOR_ESTICAMENTO * (2 * elevacao(fase) - 1)


def desenhar(tela, jogador, distancia):
    """Poe o corredor de pe na pista em que ele esta deslizando, no passo da vez."""
    x, y, escala = perspectiva.projetar(jogador.pista_visual, config.Z_JOGADOR)
    fase = fase_da_passada(distancia)
    estica = esticamento(fase)
    altura = config.ALTURA_JOGADOR * escala * estica
    largura = config.LARGURA_JOGADOR * escala / estica  # comprimiu, alargou
    passo = balanco(fase)

    chao = y - config.JOGADOR_ELEVACAO * altura * elevacao(fase)  # o corpo quica
    desvio = config.JOGADOR_INCLINACAO * largura * jogador.inclinacao
    quadril = chao - config.JOGADOR_ALTURA_PERNA * altura
    topo_do_tronco = quadril - config.JOGADOR_ALTURA_TRONCO * altura

    desenho.desenhar_sombra(tela, x, y, largura)  # a sombra fica no chao, parada
    _desenhar_pernas(tela, x, chao, quadril, largura, altura, passo)
    _desenhar_tronco(tela, x + desvio, topo_do_tronco, largura, altura)
    _desenhar_shorts(tela, x + desvio, quadril, largura, altura)
    _desenhar_bracos(tela, x + desvio, topo_do_tronco, largura, altura, passo)
    _desenhar_cabeca(tela, x + desvio, topo_do_tronco, altura)


def _peca(tela, cor, centro_x, topo, largura, altura):
    """O tijolo do boneco: um retangulo de cantos arredondados, sempre no mesmo raio."""
    desenho.desenhar_peca(
        tela, cor, centro_x, topo, largura, altura, config.JOGADOR_ARREDONDAMENTO
    )


def _desenhar_pernas(tela, x, chao, quadril, largura, altura, passo):
    """As duas pernas penduradas no quadril, cada uma com o seu tenis na ponta.

    A perna que levanta e desenhada mais curta, com o tenis subindo junto: e
    essa alternancia que se le como corrida.
    """
    altura_tenis = config.JOGADOR_ALTURA_TENIS * altura
    largura_perna = config.JOGADOR_LARGURA_PERNA * largura
    for lado in (-1, 1):
        centro = x + lado * config.JOGADOR_AFASTAMENTO_PERNAS * largura
        levantar = max(0.0, lado * passo) * config.JOGADOR_LEVANTAR_PE * altura
        pe = chao - levantar
        _peca(tela, config.COR_PELE, centro, quadril, largura_perna, pe - quadril)
        _peca(
            tela,
            config.COR_TENIS,
            centro,
            pe - altura_tenis,
            largura_perna * config.JOGADOR_LARGURA_TENIS,
            altura_tenis,
        )


def _desenhar_tronco(tela, x, topo, largura, altura):
    """A camiseta: a peca mais larga, que define os ombros."""
    _peca(
        tela,
        config.COR_CAMISETA,
        x,
        topo,
        largura,
        config.JOGADOR_ALTURA_TRONCO * altura,
    )


def _desenhar_shorts(tela, x, quadril, largura, altura):
    """O shorts fecha a barra da camiseta e desce um pouco por cima das pernas."""
    altura_shorts = config.JOGADOR_ALTURA_SHORTS * altura
    base = quadril + config.JOGADOR_SOBREPOSICAO_SHORTS * altura
    _peca(tela, config.COR_SHORTS, x, base - altura_shorts, largura, altura_shorts)


def _desenhar_bracos(tela, x, topo_do_tronco, largura, altura, passo):
    """Um braco de cada lado do tronco, com a manga da camiseta cobrindo o ombro.

    O braco balanca ao contrario da perna do mesmo lado, que e como se corre de
    verdade: perna direita na frente, braco direito atras.
    """
    ombro = topo_do_tronco + config.JOGADOR_OMBRO * altura
    largura_braco = config.JOGADOR_LARGURA_BRACO * largura
    for lado in (-1, 1):
        centro = x + lado * config.JOGADOR_AFASTAMENTO_BRACOS * largura
        topo = ombro + lado * passo * config.JOGADOR_BALANCO_BRACO * altura
        _peca(
            tela,
            config.COR_PELE,
            centro,
            topo,
            largura_braco,
            config.JOGADOR_ALTURA_BRACO * altura,
        )
        _peca(
            tela,
            config.COR_CAMISETA,
            centro,
            topo,
            largura_braco,
            config.JOGADOR_ALTURA_MANGA * altura,
        )


def _desenhar_cabeca(tela, x, topo_do_tronco, altura):
    """A cabeca de costas: um circulo de cabelo por cima e a nuca aparecendo embaixo."""
    raio = config.JOGADOR_RAIO_CABECA * altura
    centro_y = topo_do_tronco - raio + config.JOGADOR_PESCOCO * altura
    pygame.draw.aacircle(tela, config.COR_PELE, (x, centro_y), raio)
    pygame.draw.aacircle(
        tela,
        config.COR_CABELO,
        (x, centro_y - config.JOGADOR_DESLOCAMENTO_CABELO * raio),
        raio,
    )
