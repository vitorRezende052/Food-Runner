"""Testes da geometria da estrela que marca a comida ruim.

Sao contas puras sobre angulo e raio, entao dao para testar sem abrir janela. O
desenho em si, como toda a camada grafica, fica de fora.
"""

import math

import config
import desenho_comida

CENTRO = (0.0, 0.0)
RAIO = 10.0


def estrela(pontas=config.AUREOLA_PONTAS, recuo=config.AUREOLA_RECUO_PONTA):
    return desenho_comida.pontos_da_estrela(*CENTRO, RAIO, pontas, recuo)


def distancia_do_centro(ponto):
    return math.hypot(ponto[0] - CENTRO[0], ponto[1] - CENTRO[1])


def test_a_estrela_tem_uma_ponta_e_um_vale_por_espeto():
    assert len(estrela()) == 2 * config.AUREOLA_PONTAS


def test_a_estrela_alterna_ponta_e_vale():
    """Os pontos pares vao ate a borda; os impares recuam e formam o entalhe."""
    for indice, ponto in enumerate(estrela()):
        esperado = RAIO if indice % 2 == 0 else RAIO * config.AUREOLA_RECUO_PONTA
        assert math.isclose(distancia_do_centro(ponto), esperado, abs_tol=1e-9)


def test_a_estrela_cabe_no_raio_pedido():
    """Vertice alem do raio estouraria a superficie em que a marca e pintada."""
    for ponto in estrela():
        assert distancia_do_centro(ponto) <= RAIO + 1e-9


def test_a_primeira_ponta_olha_para_cima():
    """Estrela deitada dependeria do numero de espetos para parecer em pe."""
    primeira = estrela()[0]
    assert math.isclose(primeira[0], CENTRO[0], abs_tol=1e-9)
    assert primeira[1] < CENTRO[1]  # em tela, para cima e y menor
