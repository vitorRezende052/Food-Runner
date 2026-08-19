"""Testes da troca de telas: qual tecla leva o jogo de um estado para outro.

So a tabela de teclas do ``main`` e testada aqui — o desenho das telas fica de
fora, como toda a camada grafica.
"""

import random

import pygame

import config
import jogo
import main
import telas


def partida_nova():
    """Uma partida com sorteio reproduzivel, para os testes nao dependerem de sorte."""
    return jogo.Jogo(random.Random(7))


def test_espaco_no_menu_comeca_a_partida():
    partida = partida_nova()
    assert main.tratar_tecla(telas.MENU, partida, pygame.K_SPACE) == telas.JOGANDO


def test_esc_no_menu_fecha_o_jogo():
    partida = partida_nova()
    assert main.tratar_tecla(telas.MENU, partida, pygame.K_ESCAPE) == telas.SAINDO


def test_menu_ignora_tecla_que_nao_conhece():
    partida = partida_nova()
    assert main.tratar_tecla(telas.MENU, partida, pygame.K_LEFT) == telas.MENU


def test_esc_e_p_pausam_a_partida():
    partida = partida_nova()
    for tecla in (pygame.K_ESCAPE, pygame.K_p):
        assert main.tratar_tecla(telas.JOGANDO, partida, tecla) == telas.PAUSADO


def test_setas_trocam_de_pista_sem_mudar_de_tela():
    partida = partida_nova()
    estado = main.tratar_tecla(telas.JOGANDO, partida, pygame.K_LEFT)
    assert estado == telas.JOGANDO
    assert partida.corredor.pista == config.PISTA_INICIAL - 1

    main.tratar_tecla(telas.JOGANDO, partida, pygame.K_d)
    assert partida.corredor.pista == config.PISTA_INICIAL


def test_pausa_volta_a_partida_com_esc_ou_p():
    partida = partida_nova()
    for tecla in (pygame.K_ESCAPE, pygame.K_p):
        assert main.tratar_tecla(telas.PAUSADO, partida, tecla) == telas.JOGANDO


def test_m_na_pausa_volta_ao_menu():
    partida = partida_nova()
    assert main.tratar_tecla(telas.PAUSADO, partida, pygame.K_m) == telas.MENU


def test_pausa_nao_deixa_trocar_de_pista():
    partida = partida_nova()
    main.tratar_tecla(telas.PAUSADO, partida, pygame.K_LEFT)
    assert partida.corredor.pista == config.PISTA_INICIAL


def test_espaco_no_game_over_recomeca_do_zero():
    partida = partida_nova()
    partida.peso = config.PESO_GAME_OVER
    partida.acabou = True
    partida.bonus = 500

    assert main.tratar_tecla(telas.FIM, partida, pygame.K_SPACE) == telas.JOGANDO
    assert partida.acabou is False
    assert partida.peso == config.PESO_INICIAL
    assert partida.pontuacao == 0


def test_m_no_game_over_volta_ao_menu():
    partida = partida_nova()
    partida.acabou = True
    assert main.tratar_tecla(telas.FIM, partida, pygame.K_m) == telas.MENU
