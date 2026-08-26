"""Testes das contas puras da rua: posicao dos elementos, variacao e grade de janelas.

Nenhuma delas toca pixel -- sao numeros sobre ``pista``, ``z`` e fracoes de
parede --, entao dao para testar sem abrir janela. O desenho em si, como toda a
camada grafica, fica de fora.
"""

import config
import cidade

ESPACAMENTO = 0.2


def zetas(distancia, espacamento=ESPACAMENTO, deslocamento=0.0):
    return [z for _, z in cidade.posicoes(distancia, espacamento, deslocamento)]


def indices(distancia, espacamento=ESPACAMENTO, deslocamento=0.0):
    return [indice for indice, _ in cidade.posicoes(distancia, espacamento, deslocamento)]


def test_a_rua_nunca_fica_vazia():
    """Sem elemento nenhum na faixa visivel a lateral voltaria a ser um vazio."""
    for distancia in (0.0, 0.37, 5.0, 123.4):
        assert cidade.posicoes(distancia, ESPACAMENTO)


def test_todo_elemento_visivel_esta_entre_o_horizonte_e_o_rodape():
    """Fora dessa faixa o elemento nao aparece, e desenha-lo seria trabalho perdido."""
    for distancia in (0.0, 0.37, 5.0, 123.4):
        for z in zetas(distancia):
            assert config.Z_FUNDO_TELA <= z <= config.Z_HORIZONTE


def test_os_elementos_ficam_igualmente_espacados():
    """Espacamento irregular denunciaria que a fila e sorteada, e nao plantada."""
    visiveis = zetas(3.3)
    vaos = [depois - antes for antes, depois in zip(visiveis, visiveis[1:])]
    for vao in vaos:
        assert abs(vao - ESPACAMENTO) < 1e-9


def test_os_indices_sao_consecutivos():
    assert indices(3.3) == list(range(indices(3.3)[0], indices(3.3)[-1] + 1))


def test_andar_para_a_frente_aproxima_a_rua():
    """A corrida passa pelos elementos: o mesmo indice tem que vir chegando."""
    antes = dict(cidade.posicoes(1.0, ESPACAMENTO))
    depois = dict(cidade.posicoes(1.05, ESPACAMENTO))
    repetidos = set(antes) & set(depois)
    assert repetidos
    for indice in repetidos:
        assert depois[indice] < antes[indice]


def test_o_indice_nunca_se_repete():
    """Ele e o lugar do elemento na rua, e nao uma vaga que se recicla: e o que
    faz a cidade nao repetir os mesmos predios a cada volta."""
    primeiro_perto = indices(1.0)[0]
    primeiro_longe = indices(1.0 + 10 * ESPACAMENTO)[0]
    assert primeiro_longe == primeiro_perto + 10


def test_o_deslocamento_desencontra_as_duas_filas():
    """Sem ele um lado da rua seria o espelho exato do outro."""
    de_um_lado = zetas(2.0)
    do_outro = zetas(2.0, deslocamento=0.5)
    for z in do_outro:
        assert all(abs(z - vizinho) > 1e-9 for vizinho in de_um_lado)


def test_a_variacao_cabe_entre_zero_e_um():
    for indice in range(200):
        for chave in (cidade.CHAVE_ALTURA, cidade.CHAVE_COR, cidade.CHAVE_JANELA):
            assert 0.0 <= cidade.variacao(indice, chave) < 1.0


def test_a_variacao_e_sempre_a_mesma_para_o_mesmo_predio():
    """Sem isso o predio mudaria de altura e de cor a cada quadro."""
    assert cidade.variacao(42, cidade.CHAVE_ALTURA) == cidade.variacao(
        42, cidade.CHAVE_ALTURA
    )


def test_a_variacao_espalha_pelos_quatro_quartos():
    """Concentrada num pedaco so, ela daria uma rua de predios todos iguais."""
    quartos = {int(cidade.variacao(indice, cidade.CHAVE_ALTURA) * 4) for indice in range(40)}
    assert quartos == {0, 1, 2, 3}


def test_duas_chaves_nao_andam_juntas():
    """Se a cor fosse so a altura deslocada, o predio mais alto teria sempre a
    mesma cor -- e a rua ficaria com um padrao visivel."""
    distancias = {
        round(
            cidade.variacao(indice, cidade.CHAVE_COR)
            - cidade.variacao(indice, cidade.CHAVE_ALTURA),
            6,
        )
        for indice in range(40)
    }
    assert len(distancias) > 1


def test_a_janela_cabe_na_parede():
    """Janela passando do canto vazaria para fora do predio."""
    for andares in (4, 9, 14):
        for colunas in (1, 3):
            for linha in range(andares):
                for coluna in range(colunas):
                    inicio, fim = cidade.faixa_da_coluna(coluna, colunas)
                    baixo, cima = cidade.faixa_do_andar(linha, andares)
                    assert 0.0 <= inicio < fim <= 1.0
                    assert 0.0 <= baixo < cima <= 1.0


def test_as_janelas_nao_se_encostam():
    """Sem parede entre uma e outra a grade viraria uma faixa continua."""
    colunas = config.PREDIO_JANELAS_POR_ANDAR
    for coluna in range(colunas - 1):
        _, fim = cidade.faixa_da_coluna(coluna, colunas)
        proximo_inicio, _ = cidade.faixa_da_coluna(coluna + 1, colunas)
        assert fim < proximo_inicio

    andares = 6
    for linha in range(andares - 1):
        _, cima = cidade.faixa_do_andar(linha, andares)
        proximo_baixo, _ = cidade.faixa_do_andar(linha + 1, andares)
        assert cima < proximo_baixo


def test_a_janela_fica_no_meio_da_celula():
    """Encostada num dos lados, a grade sairia torta na parede."""
    colunas = 3
    inicio, fim = cidade.faixa_da_coluna(1, colunas)
    assert abs((inicio + fim) / 2 - 0.5) < 1e-9
