"""Os oito alimentos do jogo, desenhados em codigo.

Cada comida e montada dentro de uma caixa quadrada apoiada no asfalto: o lado
dessa caixa ja vem multiplicado pela escala da perspectiva, entao nenhuma
medida daqui precisa saber a que distancia a comida esta. Todas elas sao
fracoes do lado, tiradas do ``config``, como acontece com o corredor.

Cada alimento e pintado na cor de verdade -- a maca e verde, a cenoura e laranja,
o pao do lanche e dourado. Quem avisa se a comida e boa ou ruim e a **aureola**,
o disco atras dela: verde para o alimento saudavel, vermelho para o
ultraprocessado. La no horizonte, onde o alimento tem uma duzia de pixels, e a
aureola que chega aos olhos do jogador; de perto ela vira so uma moldura e o
desenho do alimento fala por si.

O disco e o mesmo para os dois tipos e so a cor muda, entao e a cor que carrega
o aviso sozinha.
"""

import pygame

import comida
import config
import desenho
import perspectiva


def desenhar_comidas(tela, comidas):
    """Desenha as comidas da mais distante para a mais proxima.

    Nessa ordem a comida que esta na frente cobre a que vem atras, que e o que a
    perspectiva pede.
    """
    for alimento in sorted(comidas, key=lambda item: item.z, reverse=True):
        _desenhar(tela, alimento)


def _desenhar(tela, alimento):
    """Poe um alimento em pe no asfalto, do tamanho que a distancia manda."""
    x, y, escala = perspectiva.projetar(alimento.pista, alimento.z)
    lado = max(config.TAMANHO_COMIDA_MINIMO, config.TAMANHO_COMIDA * escala)
    caixa = pygame.Rect(0, 0, max(1, round(lado)), max(1, round(lado)))
    caixa.midbottom = (round(x), round(y))

    desenho.desenhar_sombra(tela, x, y, lado)
    _desenhar_aureola(tela, alimento, caixa)
    DESENHOS[alimento.nome](tela, caixa)


def _desenhar_aureola(tela, alimento, caixa):
    """Disco atras do alimento: verde se ele for bom, vermelho se for ruim.

    O disco e montado em duas camadas, como as bagas do cacho de uva: o circulo
    inteiro na cor da borda e, por cima, um circulo menor no tom do miolo. O que
    sobra entre os dois e o anel, e ele tem espessura minima em pixels --
    calculado so como fracao do raio, arredondaria para zero justamente no
    horizonte, que e onde ele e a unica coisa que o jogador consegue ler.

    A forma e a mesma para os dois tipos: quem diz se a comida e boa ou ruim e a
    cor.
    """
    if alimento.tipo == comida.BOA:
        cor, cor_borda = config.COR_COMIDA_BOA, config.COR_COMIDA_BOA_BORDA
    else:
        cor, cor_borda = config.COR_COMIDA_RUIM, config.COR_COMIDA_RUIM_BORDA

    diametro = max(2, round(caixa.width * config.AUREOLA_TAMANHO))
    marca = pygame.Surface((diametro, diametro), pygame.SRCALPHA)
    raio = diametro / 2
    borda = max(config.AUREOLA_BORDA_MINIMA, round(raio * config.AUREOLA_BORDA))
    centro = (raio, raio)

    pygame.draw.aacircle(
        marca, (*cor_borda, config.OPACIDADE_AUREOLA_BORDA), centro, raio
    )
    pygame.draw.aacircle(
        marca, (*cor, config.OPACIDADE_AUREOLA), centro, max(1, raio - borda)
    )
    tela.blit(marca, marca.get_rect(center=caixa.center))


def _peca(tela, cor, centro_x, base, largura, altura):
    """Retangulo de cantos arredondados apoiado em ``base``: o tijolo das comidas."""
    retangulo = pygame.Rect(0, 0, max(1, round(largura)), max(1, round(altura)))
    retangulo.midbottom = (round(centro_x), round(base))
    arredondamento = max(1, round(retangulo.width * config.ARREDONDAMENTO_COMIDA))
    pygame.draw.rect(tela, cor, retangulo, border_radius=arredondamento)


def _trapezio(tela, cor, centro_x, base, altura, largura_topo, largura_base):
    """Quadrilatero de boca e fundo diferentes: serve a caixinha e ao copo."""
    topo = base - altura
    pygame.draw.polygon(
        tela,
        cor,
        [
            (centro_x - largura_topo / 2, topo),
            (centro_x + largura_topo / 2, topo),
            (centro_x + largura_base / 2, base),
            (centro_x - largura_base / 2, base),
        ],
    )


def _desenhar_maca(tela, caixa):
    """Bola verde com o cabinho espetado e uma folha ao lado dele."""
    lado = caixa.width
    raio = config.COMIDA_MACA_RAIO * lado
    centro_y = caixa.bottom - raio
    altura_cabo = config.COMIDA_MACA_CABO_ALTURA * lado
    topo_da_bola = centro_y - raio

    _peca(
        tela,
        config.COR_CABO,
        caixa.centerx,
        topo_da_bola,
        config.COMIDA_MACA_CABO_LARGURA * lado,
        altura_cabo,
    )
    folha = pygame.Rect(
        0,
        0,
        max(1, round(config.COMIDA_MACA_FOLHA_LARGURA * lado)),
        max(1, round(config.COMIDA_MACA_FOLHA_ALTURA * lado)),
    )
    folha.midleft = (round(caixa.centerx), round(topo_da_bola - altura_cabo / 2))
    pygame.draw.ellipse(tela, config.COR_FOLHA, folha)
    pygame.draw.aacircle(tela, config.COR_MACA, (caixa.centerx, centro_y), raio)


def _desenhar_brocolis(tela, caixa):
    """Talo claro segurando tres bolas verdes: a copa.

    A copa e desenhada acima do alto do talo, senao as bolas engoliriam o talo
    inteiro e o brocolis viraria um trevo.
    """
    lado = caixa.width
    _peca(
        tela,
        config.COR_BROCOLIS_TALO,
        caixa.centerx,
        caixa.bottom,
        config.COMIDA_BROCOLIS_TALO_LARGURA * lado,
        config.COMIDA_BROCOLIS_TALO_ALTURA * lado,
    )
    raio = config.COMIDA_BROCOLIS_COPA_RAIO * lado
    afastamento = config.COMIDA_BROCOLIS_COPA_AFASTAMENTO * lado
    meio_da_copa = caixa.bottom - config.COMIDA_BROCOLIS_COPA_CENTRO * lado
    for centro in (
        (caixa.centerx - afastamento, meio_da_copa),
        (caixa.centerx + afastamento, meio_da_copa),
        (caixa.centerx, meio_da_copa - afastamento),
    ):
        pygame.draw.aacircle(tela, config.COR_BROCOLIS, centro, raio)


def _desenhar_cenoura(tela, caixa):
    """Raiz laranja em triangulo apontando para baixo, com a rama espetada no topo."""
    lado = caixa.width
    largura = config.COMIDA_CENOURA_LARGURA * lado
    topo = caixa.bottom - config.COMIDA_CENOURA_ALTURA * lado
    altura_rama = config.COMIDA_CENOURA_RAMA_ALTURA * lado

    folhas = config.COMIDA_CENOURA_FOLHAS
    largura_folha = config.COMIDA_CENOURA_RAMA_FOLHA * lado
    for indice in range(folhas):
        folha = pygame.Rect(
            0, 0, max(1, round(largura_folha)), max(1, round(altura_rama))
        )
        folha.midbottom = (
            round(caixa.centerx + (indice - (folhas - 1) / 2) * largura_folha),
            round(topo),
        )
        pygame.draw.ellipse(tela, config.COR_FOLHA, folha)

    pygame.draw.polygon(
        tela,
        config.COR_CENOURA,
        [
            (caixa.centerx - largura / 2, topo),
            (caixa.centerx + largura / 2, topo),
            (caixa.centerx, caixa.bottom),
        ],
    )


def _desenhar_uva(tela, caixa):
    """Cacho roxo em piramide, com o cabinho e uma folha espetados no alto.

    Cada baga e um disco escuro com um miolo claro por dentro: o anel que sobra
    faz as vezes de contorno e e o que separa uma baga da vizinha, ja que as
    filas se encostam de proposito -- afastadas, o cacho viraria um punhado de
    bolinhas soltas.
    """
    lado = caixa.width
    raio = config.COMIDA_UVA_RAIO * lado
    espaco = config.COMIDA_UVA_ESPACO * lado
    fila = config.COMIDA_UVA_FILA * lado
    filas = config.COMIDA_UVA_FILAS
    altura_cabo = config.COMIDA_UVA_CABO_ALTURA * lado
    topo_do_cacho = caixa.bottom - 2 * raio - (filas - 1) * fila

    _peca(
        tela,
        config.COR_CABO,
        caixa.centerx,
        topo_do_cacho,
        config.COMIDA_UVA_CABO_LARGURA * lado,
        altura_cabo,
    )
    folha = pygame.Rect(
        0,
        0,
        max(1, round(config.COMIDA_UVA_FOLHA_LARGURA * lado)),
        max(1, round(config.COMIDA_UVA_FOLHA_ALTURA * lado)),
    )
    folha.midleft = (round(caixa.centerx), round(topo_do_cacho - altura_cabo / 2))
    pygame.draw.ellipse(tela, config.COR_FOLHA, folha)

    # De tras para a frente: a fila mais larga la em cima primeiro, a baga da
    # ponta por ultimo, para que a de baixo sempre cubra a de cima.
    for indice in reversed(range(filas)):
        meio_da_fila = caixa.bottom - raio - indice * fila
        for baga in range(indice + 1):
            centro = (caixa.centerx + (baga - indice / 2) * espaco, meio_da_fila)
            pygame.draw.aacircle(tela, config.COR_UVA_CONTORNO, centro, raio)
            pygame.draw.aacircle(
                tela, config.COR_UVA, centro, raio * config.COMIDA_UVA_MIOLO
            )


def _desenhar_hamburguer(tela, caixa):
    """Pilha montada de cima para baixo: domo, alface, carne e o pao de baixo.

    Nessa ordem cada camada tapa a metade de baixo da anterior, e e por isso que
    o domo do pao pode ser uma elipse inteira sem estufar o lanche.
    """
    lado = caixa.width
    largura = config.COMIDA_HAMBURGUER_LARGURA * lado
    altura_base = config.COMIDA_HAMBURGUER_BASE * lado
    altura_carne = config.COMIDA_HAMBURGUER_CARNE * lado
    altura_alface = config.COMIDA_HAMBURGUER_ALFACE * lado
    base_do_alface = caixa.bottom - altura_base - altura_carne

    domo = pygame.Rect(
        0, 0, max(1, round(largura)), max(1, round(config.COMIDA_HAMBURGUER_PAO * lado))
    )
    domo.midbottom = (caixa.centerx, round(base_do_alface))
    pygame.draw.ellipse(tela, config.COR_PAO, domo)

    _peca(tela, config.COR_ALFACE, caixa.centerx, base_do_alface, lado, altura_alface)
    _peca(
        tela,
        config.COR_HAMBURGUER,
        caixa.centerx,
        caixa.bottom - altura_base,
        largura,
        altura_carne,
    )
    _peca(tela, config.COR_PAO, caixa.centerx, caixa.bottom, largura, altura_base)


def _desenhar_batata_frita(tela, caixa):
    """Palitos amarelos espetados numa caixinha vermelha de fast food."""
    lado = caixa.width
    altura_caixa = config.COMIDA_BATATA_CAIXA_ALTURA * lado
    boca = caixa.bottom - altura_caixa
    largura_palito = config.COMIDA_BATATA_PALITO_LARGURA * lado
    altura_palito = config.COMIDA_BATATA_PALITO_ALTURA * lado
    base_dos_palitos = boca + config.COMIDA_BATATA_PALITO_MERGULHO * lado

    for lugar in (-1, 0, 1):
        curto = config.COMIDA_BATATA_PALITO_CURTO
        altura = altura_palito if lugar == 0 else altura_palito * curto
        _peca(
            tela,
            config.COR_BATATA,
            caixa.centerx + lugar * largura_palito * config.COMIDA_BATATA_PALITO_ESPACO,
            base_dos_palitos,
            largura_palito,
            altura,
        )

    _trapezio(
        tela,
        config.COR_EMBALAGEM,
        caixa.centerx,
        caixa.bottom,
        altura_caixa,
        config.COMIDA_BATATA_CAIXA_TOPO * lado,
        config.COMIDA_BATATA_CAIXA_BASE * lado,
    )


def _desenhar_refrigerante(tela, caixa):
    """Copo de fast food: trapezio vermelho, tampa clara e canudo espetado nela."""
    lado = caixa.width
    largura_topo = config.COMIDA_REFRIGERANTE_TOPO * lado
    boca = caixa.bottom - config.COMIDA_REFRIGERANTE_COPO_ALTURA * lado
    altura_tampa = config.COMIDA_REFRIGERANTE_TAMPA_ALTURA * lado

    _peca(
        tela,
        config.COR_TAMPA,
        caixa.centerx + config.COMIDA_REFRIGERANTE_CANUDO_DESVIO * lado,
        boca,
        config.COMIDA_REFRIGERANTE_CANUDO_LARGURA * lado,
        config.COMIDA_REFRIGERANTE_CANUDO_ALTURA * lado,
    )
    _trapezio(
        tela,
        config.COR_EMBALAGEM,
        caixa.centerx,
        caixa.bottom,
        config.COMIDA_REFRIGERANTE_COPO_ALTURA * lado,
        largura_topo,
        config.COMIDA_REFRIGERANTE_BASE * lado,
    )
    _peca(
        tela,
        config.COR_TAMPA,
        caixa.centerx,
        boca + altura_tampa / 2,
        largura_topo * config.COMIDA_REFRIGERANTE_TAMPA_SOBRA,
        altura_tampa,
    )


def _desenhar_donut(tela, caixa):
    """Anel de massa com o glace por cima; o furo deixa o asfalto aparecer."""
    lado = caixa.width
    raio = config.COMIDA_DONUT_RAIO * lado
    centro = (caixa.centerx, caixa.bottom - raio)
    pygame.draw.aacircle(
        tela,
        config.COR_DONUT,
        centro,
        raio,
        max(1, round(config.COMIDA_DONUT_MASSA * lado)),
    )
    pygame.draw.aacircle(
        tela,
        config.COR_COBERTURA,
        centro,
        raio - config.COMIDA_DONUT_RECUO_COBERTURA * lado,
        max(1, round(config.COMIDA_DONUT_COBERTURA * lado)),
    )


# Um desenho para cada alimento do cardapio. O ``_desenhar`` procura aqui pelo
# nome da comida sorteada, entao alimento novo precisa entrar nas duas pontas --
# e ha um teste cobrando exatamente isso.
DESENHOS = {
    comida.MACA: _desenhar_maca,
    comida.BROCOLIS: _desenhar_brocolis,
    comida.CENOURA: _desenhar_cenoura,
    comida.UVA: _desenhar_uva,
    comida.HAMBURGUER: _desenhar_hamburguer,
    comida.BATATA_FRITA: _desenhar_batata_frita,
    comida.REFRIGERANTE: _desenhar_refrigerante,
    comida.DONUT: _desenhar_donut,
}
