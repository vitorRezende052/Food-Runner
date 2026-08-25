"""Testes da mistura de cores do ``desenho``.

E a unica conta do modulo que nao depende de pixel nenhum: o gradiente do ceu
sai dela. O resto do desenho, como toda a camada grafica, fica de fora.
"""

import config
import desenho

PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)


def test_fracao_zero_devolve_a_cor_inicial():
    assert desenho.misturar_cores(PRETO, BRANCO, 0.0) == PRETO


def test_fracao_um_devolve_a_cor_final():
    assert desenho.misturar_cores(PRETO, BRANCO, 1.0) == BRANCO


def test_meio_do_caminho_fica_entre_as_duas():
    assert desenho.misturar_cores(PRETO, BRANCO, 0.5) == (128, 128, 128)


def test_fracao_fora_do_intervalo_nao_estoura_a_cor():
    assert desenho.misturar_cores(PRETO, BRANCO, -3.0) == PRETO
    assert desenho.misturar_cores(PRETO, BRANCO, 9.0) == BRANCO


def test_gradiente_do_ceu_clareia_de_cima_para_baixo():
    """Perto do horizonte o ceu tem que estar mais claro do que la em cima."""
    topo = desenho.misturar_cores(
        config.COR_CEU_TOPO, config.COR_CEU_HORIZONTE, 0.0
    )
    embaixo = desenho.misturar_cores(
        config.COR_CEU_TOPO, config.COR_CEU_HORIZONTE, 1.0
    )
    assert sum(embaixo) > sum(topo)
