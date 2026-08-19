"""Testes da comida: cardapio, sorteio do spawn, avanco em z e descarte."""

import random

import comida
import config
import perspectiva


def gerador_com_sorte_fixa(semente=7):
    """Gerador com sorteio reproduzivel, para o teste nao depender de sorte."""
    return comida.GeradorDeComida(random.Random(semente))


def test_todo_alimento_do_cardapio_tem_nome_e_forma():
    for cardapio in (comida.COMIDAS_BOAS, comida.COMIDAS_RUINS):
        assert cardapio
        for nome, forma in cardapio:
            assert nome
            assert forma


def test_comida_nasce_no_horizonte():
    sorteada = comida.sortear(random.Random(1))
    assert sorteada.z == config.Z_SPAWN


def test_spawn_sempre_cai_numa_pista_valida():
    aleatorio = random.Random(3)
    for _ in range(200):
        assert comida.sortear(aleatorio).pista in range(config.QTD_PISTAS)


def test_tipo_sorteado_combina_com_o_cardapio():
    aleatorio = random.Random(5)
    for _ in range(200):
        sorteada = comida.sortear(aleatorio)
        cardapio = (
            comida.COMIDAS_RUINS if sorteada.tipo == comida.RUIM else comida.COMIDAS_BOAS
        )
        assert (sorteada.nome, sorteada.forma) in cardapio


def test_comida_ruim_e_mais_comum_que_a_boa():
    """A proporcao sorteada tem que ficar perto da chance configurada."""
    aleatorio = random.Random(11)
    amostras = 3000
    ruins = sum(comida.sortear(aleatorio).tipo == comida.RUIM for _ in range(amostras))
    assert abs(ruins / amostras - config.CHANCE_COMIDA_RUIM) < 0.05
    assert config.CHANCE_COMIDA_RUIM > 0.5


def test_comida_se_aproxima_do_jogador():
    alimento = comida.Comida(0, comida.BOA, "maca", comida.CIRCULO)
    alimento.avancar(1.0)
    assert alimento.z == config.Z_SPAWN - config.VELOCIDADE_JOGO


def test_comida_so_some_depois_de_passar_pelo_jogador():
    alimento = comida.Comida(0, comida.RUIM, "donut", comida.ROSQUINHA)
    assert not alimento.passou()
    alimento.z = config.Z_JOGADOR
    assert not alimento.passou()
    alimento.z = config.Z_SUMICO
    assert alimento.passou()


def test_comida_some_so_depois_de_sair_da_tela():
    """No ponto do descarte a comida ja tem que estar abaixo do rodape."""
    _, y, _ = perspectiva.projetar(config.PISTA_INICIAL, config.Z_SUMICO)
    assert y > config.ALTURA


def test_primeira_comida_espera_o_intervalo():
    gerador = gerador_com_sorte_fixa()
    gerador.atualizar(config.INTERVALO_SPAWN / 2)
    assert gerador.comidas == []
    gerador.atualizar(config.INTERVALO_SPAWN / 2)
    assert len(gerador.comidas) == 1


def test_gerador_mantem_o_ritmo_de_spawn():
    """Uma comida por intervalo, mesmo somando o tempo quadro a quadro."""
    gerador = gerador_com_sorte_fixa()
    passo = 1 / config.FPS
    for _ in range(round(2 * config.INTERVALO_SPAWN * config.FPS)):
        gerador.atualizar(passo)
    assert len(gerador.comidas) == 2


def test_gerador_joga_fora_a_comida_que_passou():
    gerador = gerador_com_sorte_fixa()
    gerador.atualizar(config.INTERVALO_SPAWN)
    assert len(gerador.comidas) == 1

    travessia = (config.Z_SPAWN - config.Z_SUMICO) / config.VELOCIDADE_JOGO
    gerador.atualizar(travessia)
    assert all(alimento.z > config.Z_SUMICO for alimento in gerador.comidas)


def test_comidas_nao_se_acumulam_sem_fim():
    """Numa partida longa a lista para de crescer: o que passa e descartado."""
    gerador = gerador_com_sorte_fixa()
    passo = 1 / config.FPS
    for _ in range(60 * config.FPS):
        gerador.atualizar(passo)
    travessia = (config.Z_SPAWN - config.Z_SUMICO) / config.VELOCIDADE_JOGO
    assert len(gerador.comidas) <= round(travessia / config.INTERVALO_SPAWN) + 1
