"""Testes do audio: a sintese das ondas e a garantia de que jogo mudo nao quebra."""

import numpy
import pygame
import pytest

import audio
import config


def duracao_da_receita(nome):
    """Quanto tempo, em segundos, a receita inteira deve durar."""
    _, notas = audio.RECEITAS[nome]
    return sum(duracao for _, duracao in notas)


def test_existe_uma_receita_para_cada_som():
    assert set(audio.RECEITAS) == {
        config.SOM_COLETA,
        config.SOM_IMPACTO,
        config.SOM_FIM,
        config.SOM_CONFIRMACAO,
    }


def test_toda_receita_usa_uma_forma_de_onda_conhecida():
    for forma, _ in audio.RECEITAS.values():
        assert forma in (audio.SENOIDE, audio.QUADRADA)


def test_a_nota_tem_a_quantidade_de_amostras_da_sua_duracao():
    assert len(audio.onda(audio.SENOIDE, 440, 0.5)) == config.TAXA_AMOSTRAGEM // 2


def test_a_nota_fica_dentro_da_faixa_de_amplitude():
    amostras = audio.onda(audio.QUADRADA, 220, 0.2)
    assert numpy.abs(amostras).max() <= 1.0


def test_a_nota_comeca_e_termina_no_silencio():
    """Sem isso o alto-falante estala no corte da onda."""
    amostras = audio.onda(audio.SENOIDE, 440, 0.2)
    assert amostras[0] == pytest.approx(0.0)
    assert amostras[-1] == pytest.approx(0.0, abs=1e-3)


def test_o_envelope_tem_o_tamanho_da_nota():
    assert len(audio.envelope(1000)) == 1000


def test_nota_curtissima_nao_quebra():
    """Duracao menor que uma amostra ainda produz uma onda valida."""
    assert len(audio.onda(audio.SENOIDE, 440, 0.0)) == 1


def test_sintetizar_devolve_amostras_de_16_bits():
    assert audio.sintetizar(config.SOM_COLETA).dtype == numpy.int16


def test_o_som_dura_a_soma_das_notas_da_receita():
    for nome in audio.RECEITAS:
        _, notas = audio.RECEITAS[nome]
        esperado = duracao_da_receita(nome) * config.TAXA_AMOSTRAGEM
        # cada nota perde no maximo uma amostra ao arredondar a propria duracao
        assert len(audio.sintetizar(nome)) == pytest.approx(esperado, abs=len(notas))


def test_nenhum_som_estoura_a_amplitude():
    for nome in audio.RECEITAS:
        pico = numpy.abs(audio.sintetizar(nome)).max()
        assert 0 < pico <= config.VOLUME_SOM * config.AMPLITUDE_SOM


def test_a_onda_quadrada_e_mais_forte_que_a_senoide():
    """A senoide passeia pelos valores; a quadrada fica nos extremos e soa aspera."""
    senoide = numpy.abs(audio.onda(audio.SENOIDE, 220, 0.2)).mean()
    quadrada = numpy.abs(audio.onda(audio.QUADRADA, 220, 0.2)).mean()
    assert quadrada > senoide


def test_tocar_sem_mixer_nao_quebra_o_jogo():
    audio._sons.clear()
    audio.tocar(config.SOM_COLETA)  # so nao pode levantar excecao


def test_tocar_nome_desconhecido_nao_quebra_o_jogo():
    audio.tocar("som que nao existe")


def test_maquina_sem_placa_de_som_deixa_o_jogo_mudo(monkeypatch):
    """Se o mixer nao subir, o jogo continua — apenas sem som nenhum."""

    def sem_dispositivo(**_):
        raise pygame.error("nenhum dispositivo de audio")

    monkeypatch.setattr(pygame.mixer, "init", sem_dispositivo)
    audio.iniciar()
    assert audio._sons == {}
    audio.tocar(config.SOM_FIM)
