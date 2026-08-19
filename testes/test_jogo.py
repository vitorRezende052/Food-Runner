"""Testes da partida: colisao, peso, pontuacao e game over."""

import random

import comida
import config
import jogo


def partida_limpa():
    """Uma partida com sorteio reproduzivel e a estrada vazia.

    O gerador e esvaziado de proposito: cada teste coloca a mao na comida que
    quer testar, sem depender do que o sorteio traria.
    """
    partida = jogo.Jogo(random.Random(7))
    partida.gerador.comidas = []
    return partida


def por_na_estrada(partida, tipo, pista, z=config.Z_JOGADOR):
    """Coloca uma comida do tipo pedido na pista e profundidade dadas."""
    alimento = comida.Comida(pista, tipo, "teste", comida.CIRCULO, z)
    partida.gerador.comidas.append(alimento)
    return alimento


def test_partida_comeca_no_peso_inicial_e_sem_pontos():
    partida = partida_limpa()
    assert partida.peso == config.PESO_INICIAL
    assert partida.pontuacao == 0
    assert not partida.acabou


def test_comida_ruim_na_mesma_pista_engorda_e_sai_da_estrada():
    partida = partida_limpa()
    por_na_estrada(partida, comida.RUIM, partida.corredor.pista)
    partida.atualizar(0)
    assert partida.peso == config.PESO_INICIAL + config.PESO_GANHO_COMIDA_RUIM
    assert partida.gerador.comidas == []


def test_comida_boa_na_mesma_pista_emagrece_e_da_bonus():
    partida = partida_limpa()
    por_na_estrada(partida, comida.BOA, partida.corredor.pista)
    partida.atualizar(0)
    assert partida.peso == config.PESO_INICIAL - config.PESO_PERDIDO_COMIDA_BOA
    assert partida.pontuacao == config.BONUS_COMIDA_BOA
    assert partida.gerador.comidas == []


def test_comida_em_outra_pista_passa_batido():
    partida = partida_limpa()
    outra_pista = (partida.corredor.pista + 1) % config.QTD_PISTAS
    por_na_estrada(partida, comida.RUIM, outra_pista)
    partida.atualizar(0)
    assert partida.peso == config.PESO_INICIAL
    assert len(partida.gerador.comidas) == 1


def test_comida_longe_do_jogador_ainda_nao_colide():
    partida = partida_limpa()
    por_na_estrada(partida, comida.RUIM, partida.corredor.pista, config.Z_SPAWN)
    partida.atualizar(0)
    assert partida.peso == config.PESO_INICIAL
    assert len(partida.gerador.comidas) == 1


def test_trocar_de_pista_desvia_da_comida_ruim():
    """A troca de pista vale na hora: a comida que ja ia acertar erra."""
    partida = partida_limpa()
    por_na_estrada(partida, comida.RUIM, partida.corredor.pista)
    partida.corredor.mover(-1)
    partida.atualizar(0)
    assert partida.peso == config.PESO_INICIAL


def test_comida_e_engolida_em_algum_quadro_da_travessia():
    """Passando pelo jogador quadro a quadro, a comida nao escapa sem colidir."""
    partida = partida_limpa()
    alimento = por_na_estrada(
        partida, comida.RUIM, partida.corredor.pista, config.Z_SPAWN
    )
    passo = 1 / config.FPS
    travessia = (config.Z_SPAWN - config.Z_SUMICO) / config.VELOCIDADE_INICIAL
    for _ in range(round(travessia * config.FPS) + 1):
        partida.atualizar(passo)
        if alimento not in partida.gerador.comidas:
            break

    assert alimento not in partida.gerador.comidas, "a comida ficou presa na estrada"
    assert partida.peso == config.PESO_INICIAL + config.PESO_GANHO_COMIDA_RUIM


def test_a_zona_de_colisao_aguenta_a_velocidade_maxima():
    """Nem no trecho mais rapido a comida pula a zona entre dois quadros."""
    avanco_por_quadro = config.VELOCIDADE_MAXIMA / config.FPS
    assert avanco_por_quadro < 2 * config.ZONA_COLISAO


def test_zona_de_colisao_cabe_dentro_da_estrada_visivel():
    """A comida so e descartada depois de sair da zona: nao da para escapar por fora."""
    assert config.Z_JOGADOR - config.ZONA_COLISAO > config.Z_SUMICO


def test_peso_trava_no_minimo():
    partida = partida_limpa()
    for _ in range(50):
        por_na_estrada(partida, comida.BOA, partida.corredor.pista)
        partida.atualizar(0)
    assert partida.peso == config.PESO_MINIMO


def test_peso_no_limite_termina_a_partida():
    partida = partida_limpa()
    while not partida.acabou:
        por_na_estrada(partida, comida.RUIM, partida.corredor.pista)
        partida.atualizar(0)
    assert partida.peso == config.PESO_GAME_OVER


def test_depois_do_game_over_nada_mais_anda():
    partida = partida_limpa()
    partida.acabou = True
    distancia = partida.distancia
    por_na_estrada(partida, comida.BOA, partida.corredor.pista)
    partida.atualizar(1.0)
    assert partida.distancia == distancia
    assert partida.tempo == 0
    assert partida.peso == config.PESO_INICIAL
    assert len(partida.gerador.comidas) == 1


def test_pontuacao_cresce_com_a_distancia():
    """Cada segundo corrido paga, e nunca menos que o segundo anterior."""
    partida = partida_limpa()
    partida.atualizar(1.0)
    primeiro_segundo = partida.pontuacao
    assert primeiro_segundo > 0
    partida.atualizar(1.0)
    assert partida.pontuacao - primeiro_segundo >= primeiro_segundo


def test_a_partida_fica_mais_rapida_com_o_tempo():
    """O mesmo segundo de corrida rende mais distancia (e mais pontos) la no fim."""
    partida = partida_limpa()
    partida.atualizar(1.0)
    no_comeco = partida.distancia

    partida.tempo = config.DURACAO_RAMPA
    antes = partida.distancia
    partida.atualizar(1.0)
    assert partida.distancia - antes > no_comeco


def test_bonus_soma_com_a_distancia():
    partida = partida_limpa()
    partida.atualizar(1.0)
    so_distancia = partida.pontuacao
    por_na_estrada(partida, comida.BOA, partida.corredor.pista)
    partida.atualizar(0)
    assert partida.pontuacao == so_distancia + config.BONUS_COMIDA_BOA


def test_reiniciar_volta_tudo_para_a_largada():
    partida = partida_limpa()
    partida.atualizar(5.0)
    por_na_estrada(partida, comida.RUIM, partida.corredor.pista)
    partida.atualizar(0)
    partida.corredor.mover(1)
    partida.acabou = True

    partida.reiniciar()
    assert partida.peso == config.PESO_INICIAL
    assert partida.pontuacao == 0
    assert partida.tempo == 0
    assert partida.corredor.pista == config.PISTA_INICIAL
    assert partida.gerador.comidas == []
    assert not partida.acabou


def test_comida_ruim_engorda_mais_do_que_a_boa_emagrece():
    """A regra de balanceamento do plano: sem erro nenhum o jogo ainda aperta."""
    assert config.PESO_GANHO_COMIDA_RUIM > config.PESO_PERDIDO_COMIDA_BOA
    assert config.PESO_MINIMO < config.PESO_INICIAL < config.PESO_GAME_OVER
