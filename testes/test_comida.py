"""Testes da comida: cardapio, sorteio do spawn, avanco em z e descarte."""

import random

import comida
import config
import dificuldade
import perspectiva

LARGADA = 0.0  # tempo de partida em que a dificuldade ainda esta no valor inicial
FIM_DA_RAMPA = config.DURACAO_RAMPA  # tempo em que a dificuldade chega no teto


def gerador_com_sorte_fixa(semente=7):
    """Gerador com sorteio reproduzivel, para o teste nao depender de sorte."""
    return comida.GeradorDeComida(random.Random(semente))


def sortear_no_tempo(aleatorio, tempo, pista=config.PISTA_INICIAL):
    """Sorteia uma comida com a chance de ultraprocessado daquele instante."""
    return comida.sortear(aleatorio, dificuldade.chance_de_comida_ruim(tempo), pista)


def contar_spawns(gerador, tempo, duracao):
    """Quantas comidas o gerador solta em ``duracao`` segundos, no ritmo de ``tempo``.

    A estrada e esvaziada a cada quadro so para a conta nao se confundir com o
    descarte de quem ja passou.
    """
    passo = 1 / config.FPS
    spawns = 0
    for _ in range(round(duracao * config.FPS)):
        gerador.atualizar(passo, tempo)
        spawns += len(gerador.comidas)
        gerador.comidas = []
    return spawns


def test_todo_alimento_do_cardapio_tem_nome_e_forma():
    for cardapio in (comida.COMIDAS_BOAS, comida.COMIDAS_RUINS):
        assert cardapio
        for nome, forma in cardapio:
            assert nome
            assert forma


def test_comida_nasce_no_horizonte():
    sorteada = sortear_no_tempo(random.Random(1), LARGADA)
    assert sorteada.z == config.Z_SPAWN


def test_spawn_sempre_cai_numa_pista_valida():
    aleatorio = random.Random(3)
    for _ in range(200):
        pistas = comida.sortear_pistas(aleatorio, config.COMIDAS_POR_SPAWN_MAXIMA)
        assert all(pista in range(config.QTD_PISTAS) for pista in pistas)


def test_rajada_nunca_repete_pista():
    """Duas comidas na mesma pista esconderiam uma atras da outra."""
    aleatorio = random.Random(17)
    for _ in range(200):
        pistas = comida.sortear_pistas(aleatorio, config.COMIDAS_POR_SPAWN_MAXIMA)
        assert len(set(pistas)) == len(pistas)


def test_a_comida_nasce_na_pista_pedida():
    for pista in range(config.QTD_PISTAS):
        assert sortear_no_tempo(random.Random(19), LARGADA, pista).pista == pista


def test_tipo_sorteado_combina_com_o_cardapio():
    aleatorio = random.Random(5)
    for _ in range(200):
        sorteada = sortear_no_tempo(aleatorio, LARGADA)
        cardapio = (
            comida.COMIDAS_RUINS if sorteada.tipo == comida.RUIM else comida.COMIDAS_BOAS
        )
        assert (sorteada.nome, sorteada.forma) in cardapio


def test_comida_ruim_e_mais_comum_que_a_boa():
    """A proporcao sorteada tem que ficar perto da chance pedida."""
    aleatorio = random.Random(11)
    amostras = 3000
    chance = config.CHANCE_COMIDA_RUIM_INICIAL
    ruins = sum(
        comida.sortear(aleatorio, chance, config.PISTA_INICIAL).tipo == comida.RUIM
        for _ in range(amostras)
    )
    assert abs(ruins / amostras - chance) < 0.05
    assert chance > 0.5


def test_ultraprocessado_fica_ainda_mais_comum_no_fim_da_partida():
    aleatorio = random.Random(13)
    amostras = 3000
    ruins_na_largada = sum(
        sortear_no_tempo(aleatorio, LARGADA).tipo == comida.RUIM for _ in range(amostras)
    )
    ruins_no_fim = sum(
        sortear_no_tempo(aleatorio, FIM_DA_RAMPA).tipo == comida.RUIM
        for _ in range(amostras)
    )
    assert ruins_no_fim > ruins_na_largada


def test_comida_se_aproxima_do_jogador():
    alimento = comida.Comida(0, comida.BOA, "maca", comida.CIRCULO)
    alimento.avancar(1.0, config.VELOCIDADE_INICIAL)
    assert alimento.z == config.Z_SPAWN - config.VELOCIDADE_INICIAL


def test_comida_anda_mais_no_fim_da_partida_do_que_na_largada():
    """Mesmo quadro, mesma comida: no fim da rampa ela avanca mais em z."""
    devagar = gerador_com_sorte_fixa()
    depressa = gerador_com_sorte_fixa()
    for gerador in (devagar, depressa):
        gerador.comidas = [comida.Comida(0, comida.BOA, "maca", comida.CIRCULO)]
    devagar.atualizar(1.0, LARGADA)
    depressa.atualizar(1.0, FIM_DA_RAMPA)
    assert depressa.comidas[0].z < devagar.comidas[0].z


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
    gerador.atualizar(config.INTERVALO_SPAWN_INICIAL / 2, LARGADA)
    assert gerador.comidas == []
    gerador.atualizar(config.INTERVALO_SPAWN_INICIAL / 2, LARGADA)
    assert len(gerador.comidas) == 1


def test_gerador_mantem_o_ritmo_de_spawn():
    """Uma comida por intervalo, mesmo somando o tempo quadro a quadro."""
    gerador = gerador_com_sorte_fixa()
    passo = 1 / config.FPS
    for _ in range(round(2 * config.INTERVALO_SPAWN_INICIAL * config.FPS)):
        gerador.atualizar(passo, LARGADA)
    assert len(gerador.comidas) == 2


def test_no_fim_da_rampa_cada_spawn_solta_uma_rajada():
    """Passada a metade da rampa a comida vem em dupla, em pistas diferentes."""
    gerador = gerador_com_sorte_fixa()
    gerador.atualizar(config.INTERVALO_SPAWN_INICIAL, FIM_DA_RAMPA)  # a primeira espera
    pistas = [alimento.pista for alimento in gerador.comidas]
    assert len(pistas) == config.COMIDAS_POR_SPAWN_MAXIMA
    assert len(set(pistas)) == len(pistas)


def test_a_estrada_enche_mais_no_fim_da_partida():
    """No mesmo tempo de jogo, o fim da rampa solta mais comida que a largada."""
    janela = 30.0
    na_largada = contar_spawns(gerador_com_sorte_fixa(), LARGADA, janela)
    no_fim = contar_spawns(gerador_com_sorte_fixa(), FIM_DA_RAMPA, janela)
    assert no_fim > na_largada


def test_gerador_joga_fora_a_comida_que_passou():
    gerador = gerador_com_sorte_fixa()
    gerador.atualizar(config.INTERVALO_SPAWN_INICIAL, LARGADA)
    assert len(gerador.comidas) == 1

    travessia = (config.Z_SPAWN - config.Z_SUMICO) / config.VELOCIDADE_INICIAL
    gerador.atualizar(travessia, LARGADA)
    assert all(alimento.z > config.Z_SUMICO for alimento in gerador.comidas)


def test_comidas_nao_se_acumulam_sem_fim():
    """Numa partida longa a lista para de crescer: o que passa e descartado."""
    gerador = gerador_com_sorte_fixa()
    passo = 1 / config.FPS
    for _ in range(60 * config.FPS):
        gerador.atualizar(passo, LARGADA)
    travessia = (config.Z_SPAWN - config.Z_SUMICO) / config.VELOCIDADE_INICIAL
    assert len(gerador.comidas) <= round(travessia / config.INTERVALO_SPAWN_INICIAL) + 1
