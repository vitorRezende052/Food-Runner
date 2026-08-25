"""O corredor, visto de costas.

O boneco e montado peca por peca (pernas, tronco, shorts, bracos e cabeca) em
cima de um unico ponto de apoio: o lugar em que os pes tocam a pista. Cada
medida vem do ``config`` em fracao da altura ou da largura do personagem, entao
a perspectiva encolhe o corredor inteiro so multiplicando pela escala.

As pecas ficam separadas de proposito: e nelas que a animacao de corrida vai
pegar mais adiante, sem precisar redesenhar o resto.
"""

import pygame

import config
import desenho
import perspectiva


def desenhar(tela, jogador):
    """Poe o corredor de pe na pista em que ele esta deslizando."""
    x, y, escala = perspectiva.projetar(jogador.pista_visual, config.Z_JOGADOR)
    altura = config.ALTURA_JOGADOR * escala
    largura = config.LARGURA_JOGADOR * escala

    topo_das_pernas = y - config.JOGADOR_ALTURA_PERNA * altura
    topo_do_tronco = topo_das_pernas - config.JOGADOR_ALTURA_TRONCO * altura

    desenho.desenhar_sombra(tela, x, y, largura)
    _desenhar_pernas(tela, x, y, largura, altura)
    _desenhar_tronco(tela, x, topo_do_tronco, largura, altura)
    _desenhar_shorts(tela, x, topo_das_pernas, largura, altura)
    _desenhar_bracos(tela, x, topo_do_tronco, largura, altura)
    _desenhar_cabeca(tela, x, topo_do_tronco, altura)


def _peca(tela, cor, centro_x, topo, largura, altura):
    """Retangulo de cantos arredondados: o tijolo de que todas as pecas sao feitas."""
    caixa = pygame.Rect(0, 0, max(1, round(largura)), max(1, round(altura)))
    caixa.midtop = (round(centro_x), round(topo))
    arredondamento = max(1, round(caixa.width * config.JOGADOR_ARREDONDAMENTO))
    pygame.draw.rect(tela, cor, caixa, border_radius=arredondamento)


def _desenhar_pernas(tela, x, base, largura, altura):
    """As duas pernas descendo ate o chao, cada uma com o seu tenis na ponta."""
    altura_perna = config.JOGADOR_ALTURA_PERNA * altura
    altura_tenis = config.JOGADOR_ALTURA_TENIS * altura
    largura_perna = config.JOGADOR_LARGURA_PERNA * largura
    for lado in (-1, 1):
        centro = x + lado * config.JOGADOR_AFASTAMENTO_PERNAS * largura
        _peca(
            tela,
            config.COR_PELE,
            centro,
            base - altura_perna,
            largura_perna,
            altura_perna,
        )
        _peca(
            tela,
            config.COR_TENIS,
            centro,
            base - altura_tenis,
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


def _desenhar_shorts(tela, x, topo_das_pernas, largura, altura):
    """O shorts fecha a barra da camiseta e desce um pouco por cima das pernas."""
    altura_shorts = config.JOGADOR_ALTURA_SHORTS * altura
    base = topo_das_pernas + config.JOGADOR_SOBREPOSICAO_SHORTS * altura
    _peca(tela, config.COR_SHORTS, x, base - altura_shorts, largura, altura_shorts)


def _desenhar_bracos(tela, x, topo_do_tronco, largura, altura):
    """Um braco de cada lado do tronco, com a manga da camiseta cobrindo o ombro."""
    topo = topo_do_tronco + config.JOGADOR_OMBRO * altura
    largura_braco = config.JOGADOR_LARGURA_BRACO * largura
    for lado in (-1, 1):
        centro = x + lado * config.JOGADOR_AFASTAMENTO_BRACOS * largura
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
