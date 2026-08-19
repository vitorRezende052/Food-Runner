"""Testes da troca de pista: limites da estrada e deslizada suave entre faixas."""

import config
import jogador


def test_comeca_na_pista_do_meio():
    corredor = jogador.Jogador()
    assert corredor.pista == config.PISTA_INICIAL
    assert corredor.pista_visual == float(config.PISTA_INICIAL)


def test_move_para_os_dois_lados():
    corredor = jogador.Jogador()
    corredor.mover(jogador.ESQUERDA)
    assert corredor.pista == config.PISTA_INICIAL - 1
    corredor.mover(jogador.DIREITA)
    assert corredor.pista == config.PISTA_INICIAL


def test_nao_passa_da_borda_esquerda():
    corredor = jogador.Jogador()
    for _ in range(config.QTD_PISTAS + 3):
        corredor.mover(jogador.ESQUERDA)
    assert corredor.pista == 0


def test_nao_passa_da_borda_direita():
    corredor = jogador.Jogador()
    for _ in range(config.QTD_PISTAS + 3):
        corredor.mover(jogador.DIREITA)
    assert corredor.pista == config.QTD_PISTAS - 1


def test_personagem_nao_teleporta_para_a_pista_nova():
    """Logo depois da troca ele ainda esta no caminho, entre as duas pistas."""
    corredor = jogador.Jogador()
    corredor.mover(jogador.DIREITA)
    corredor.atualizar(config.DURACAO_TROCA_PISTA / 2)
    assert config.PISTA_INICIAL < corredor.pista_visual < corredor.pista


def test_deslizada_termina_exatamente_na_pista():
    corredor = jogador.Jogador()
    corredor.mover(jogador.DIREITA)
    corredor.atualizar(config.DURACAO_TROCA_PISTA)
    assert corredor.pista_visual == float(corredor.pista)


def test_deslizada_nao_passa_do_destino_com_quadro_demorado():
    """Um quadro travado nao pode jogar o personagem para fora da pista."""
    corredor = jogador.Jogador()
    corredor.mover(jogador.ESQUERDA)
    corredor.atualizar(config.DURACAO_TROCA_PISTA * 10)
    assert corredor.pista_visual == float(corredor.pista)
