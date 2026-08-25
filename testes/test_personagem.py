"""Testes do ciclo da passada: as quatro contas que animam o corredor.

Sao matematica pura sobre a fase, entao dao para testar sem abrir janela. O
desenho em si, como toda a camada grafica, fica de fora.
"""

import config
import personagem

PISADA = 0.0
MEIO_DO_PASSO = 0.25
PISADA_SEGUINTE = 0.5


def test_a_passada_comeca_no_zero():
    assert personagem.fase_da_passada(0.0) == 0.0


def test_a_passada_da_a_volta_e_recomeca():
    """Um ciclo inteiro de distancia devolve o corredor a mesma pose."""
    um_ciclo = 1 / config.PASSADAS_POR_Z
    assert personagem.fase_da_passada(um_ciclo) == personagem.fase_da_passada(0.0)
    assert personagem.fase_da_passada(3 * um_ciclo) == personagem.fase_da_passada(0.0)


def test_correr_mais_rapido_gira_a_passada_mais_rapido():
    """Andando o dobro no mesmo quadro, o corredor avanca o dobro no ciclo.

    E dai que sai a sincronia com a rampa de dificuldade, de graca.
    """
    devagar = personagem.fase_da_passada(0.05)
    rapido = personagem.fase_da_passada(0.10)
    assert round(rapido - 2 * devagar, 9) == 0


def test_os_dois_lados_do_corpo_se_alternam():
    """Meia passada depois, cada membro esta fazendo o oposto do que fazia."""
    for fase in (0.1, 0.25, 0.4):
        oposto = personagem.balanco(fase + 0.5)
        assert round(personagem.balanco(fase) + oposto, 6) == 0


def test_um_lado_sobe_enquanto_o_outro_desce():
    assert personagem.balanco(MEIO_DO_PASSO) > 0
    assert personagem.balanco(0.75) < 0


def test_o_corpo_esta_no_chao_nas_pisadas():
    assert round(personagem.elevacao(PISADA), 6) == 0
    assert round(personagem.elevacao(PISADA_SEGUINTE), 6) == 0


def test_o_corpo_sobe_ao_maximo_entre_as_pisadas():
    assert round(personagem.elevacao(MEIO_DO_PASSO), 6) == 1


def test_a_elevacao_nunca_sai_do_intervalo():
    for centesimo in range(100):
        altura = personagem.elevacao(centesimo / 100)
        assert 0 <= altura <= 1


def test_comprime_na_pisada_e_estica_no_ar():
    assert personagem.esticamento(PISADA) < 1 < personagem.esticamento(MEIO_DO_PASSO)


def test_o_esticamento_gira_em_torno_do_tamanho_normal():
    """O que o boneco perde na pisada ele ganha no ar: no fim das contas nao cresce."""
    comprimido = personagem.esticamento(PISADA)
    esticado = personagem.esticamento(MEIO_DO_PASSO)
    assert round((comprimido + esticado) / 2, 6) == 1


def test_o_esticamento_nunca_zera():
    """A largura do boneco e dividida por ele: zero ou negativo quebraria o desenho."""
    for centesimo in range(100):
        assert personagem.esticamento(centesimo / 100) > 0
