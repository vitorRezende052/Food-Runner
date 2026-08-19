"""Testes da projecao (pista, z) -> tela: o coracao do desenho em perspectiva."""

import config
import perspectiva


def test_escala_e_cheia_na_altura_do_jogador():
    assert perspectiva.fator(config.Z_JOGADOR) == 1.0


def test_objeto_encolhe_conforme_se_afasta():
    perto = perspectiva.fator(config.Z_JOGADOR)
    meio = perspectiva.fator(0.5)
    longe = perspectiva.fator(config.Z_HORIZONTE)
    assert longe < meio < perto


def test_objeto_que_passou_do_jogador_fica_maior_que_a_base():
    assert perspectiva.fator(config.Z_FUNDO_TELA) > perspectiva.fator(config.Z_JOGADOR)


def test_profundidade_muito_negativa_para_no_piso():
    """Sem o piso em Z_MINIMO a divisao estouraria; com ele, so satura."""
    assert perspectiva.fator(-50.0) == perspectiva.fator(config.Z_MINIMO)
    assert perspectiva.fator(config.Z_MINIMO) > 0


def test_estrada_passa_do_rodape_da_tela():
    """O asfalto tem que sair pela borda de baixo, sem deixar tira de fundo."""
    _, y_perto, _ = perspectiva.projetar(config.PISTA_INICIAL, config.Z_FUNDO_TELA)
    assert y_perto > config.ALTURA


def test_horizonte_fica_acima_da_base():
    _, y_fundo, _ = perspectiva.projetar(config.PISTA_INICIAL, config.Z_HORIZONTE)
    _, y_base, _ = perspectiva.projetar(config.PISTA_INICIAL, config.Z_JOGADOR)
    assert y_fundo < y_base  # na tela, y menor quer dizer mais alto
    assert y_base == config.BASE_Y


def test_pista_central_fica_no_meio_da_tela():
    for z in (config.Z_JOGADOR, 0.5, config.Z_HORIZONTE):
        x, _, _ = perspectiva.projetar(config.PISTA_INICIAL, z)
        assert x == config.MEIO_X


def test_pistas_aparecem_da_esquerda_para_a_direita():
    xs = [perspectiva.projetar(pista, config.Z_JOGADOR)[0] for pista in range(config.QTD_PISTAS)]
    assert xs == sorted(xs)
    assert len(set(xs)) == config.QTD_PISTAS


def test_pistas_convergem_para_o_horizonte():
    def largura_da_estrada(z):
        primeira, _, _ = perspectiva.projetar(0, z)
        ultima, _, _ = perspectiva.projetar(config.QTD_PISTAS - 1, z)
        return ultima - primeira

    assert largura_da_estrada(config.Z_HORIZONTE) < largura_da_estrada(config.Z_JOGADOR)


def test_estrada_cabe_na_janela():
    """A estrada inteira, incluindo as bordas, precisa aparecer na tela."""
    borda_esquerda, _, _ = perspectiva.projetar(-0.5, config.Z_JOGADOR)
    borda_direita, _, _ = perspectiva.projetar(config.QTD_PISTAS - 0.5, config.Z_JOGADOR)
    assert 0 <= borda_esquerda
    assert borda_direita <= config.LARGURA
