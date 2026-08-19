"""Testes da rampa de dificuldade: valores da largada, crescimento e tetos."""

import pytest

import config
import dificuldade

# Instantes espalhados pela partida, da largada ate bem depois do fim da rampa.
INSTANTES = [passo / 40 * 1.5 * config.DURACAO_RAMPA for passo in range(41)]


def test_progresso_vai_de_zero_a_um():
    assert dificuldade.progresso(0) == 0
    assert dificuldade.progresso(config.DURACAO_RAMPA / 2) == 0.5
    assert dificuldade.progresso(config.DURACAO_RAMPA) == 1


def test_progresso_nao_passa_de_um():
    """Passado o fim da rampa a partida continua, mas o aperto para de crescer."""
    assert dificuldade.progresso(config.DURACAO_RAMPA * 10) == 1


def test_largada_usa_os_valores_iniciais():
    assert dificuldade.velocidade(0) == config.VELOCIDADE_INICIAL
    assert dificuldade.intervalo_de_spawn(0) == config.INTERVALO_SPAWN_INICIAL
    assert dificuldade.chance_de_comida_ruim(0) == config.CHANCE_COMIDA_RUIM_INICIAL


def test_fim_da_rampa_bate_nos_tetos():
    fim = config.DURACAO_RAMPA
    assert dificuldade.velocidade(fim) == pytest.approx(config.VELOCIDADE_MAXIMA)
    assert dificuldade.intervalo_de_spawn(fim) == pytest.approx(
        config.INTERVALO_SPAWN_MINIMO
    )
    assert dificuldade.chance_de_comida_ruim(fim) == pytest.approx(
        config.CHANCE_COMIDA_RUIM_MAXIMA
    )


def test_a_corrida_so_acelera():
    valores = [dificuldade.velocidade(tempo) for tempo in INSTANTES]
    assert valores == sorted(valores)
    assert max(valores) == pytest.approx(config.VELOCIDADE_MAXIMA)


def test_a_comida_so_vem_mais_seguido():
    valores = [dificuldade.intervalo_de_spawn(tempo) for tempo in INSTANTES]
    assert valores == sorted(valores, reverse=True)
    assert min(valores) == pytest.approx(config.INTERVALO_SPAWN_MINIMO)


def test_o_ultraprocessado_so_fica_mais_provavel():
    valores = [dificuldade.chance_de_comida_ruim(tempo) for tempo in INSTANTES]
    assert valores == sorted(valores)
    assert max(valores) == pytest.approx(config.CHANCE_COMIDA_RUIM_MAXIMA)


def test_a_rampa_aperta_de_verdade():
    """Os tetos do config tem que ser mais duros que a largada, nunca o contrario."""
    assert config.VELOCIDADE_MAXIMA > config.VELOCIDADE_INICIAL
    assert config.INTERVALO_SPAWN_MINIMO < config.INTERVALO_SPAWN_INICIAL
    assert config.CHANCE_COMIDA_RUIM_INICIAL < config.CHANCE_COMIDA_RUIM_MAXIMA <= 1
    assert config.DURACAO_RAMPA > 0


def test_comida_boa_nunca_some_do_sorteio():
    """Mesmo no aperto maximo ainda da para emagrecer: sobra chance de comida boa."""
    assert dificuldade.chance_de_comida_ruim(config.DURACAO_RAMPA) < 1
