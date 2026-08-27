"""Testes do juice: a vida de uma fagulha, o decaimento dos avisos e a cortina.

E tudo conta pura sobre o tempo, entao nada aqui abre janela nem toca pixel: o
desenho fica de fora, como manda o projeto. O que se cobra e o comportamento --
o que acende, o que apaga sozinho e o que nunca passa do limite.
"""

import math
import random

import config
import efeitos
import jogo

SEMENTE = 7


def partida_com_eventos(*eventos):
    """Uma partida parada, com a lista de eventos que o quadro teria produzido."""
    partida = jogo.Jogo(random.Random(SEMENTE))
    partida.eventos = list(eventos)
    return partida


def efeitos_novos():
    """Um ``Efeitos`` com sorteio de semente fixa, para as fagulhas repetirem."""
    return efeitos.Efeitos(random.Random(SEMENTE))


# --- O que acende ---


def test_comeca_sem_efeito_nenhum():
    efeito = efeitos_novos()
    assert efeito.particulas == []
    assert efeito.flash == 0.0
    assert efeito.tremor == 0.0


def test_comida_boa_solta_fagulhas_e_nao_sacode_a_tela():
    """O tranco e castigo: coletar comida boa nao pode dar o mesmo aviso do impacto."""
    efeito = efeitos_novos()
    efeito.reagir(partida_com_eventos(config.SOM_COLETA))
    assert len(efeito.particulas) == config.PARTICULAS_POR_COLETA
    assert efeito.tremor == 0.0
    assert efeito.flash == 0.0


def test_comida_ruim_acende_o_flash_e_o_tremor_no_maximo():
    efeito = efeitos_novos()
    efeito.reagir(partida_com_eventos(config.SOM_IMPACTO))
    assert efeito.flash == 1.0
    assert efeito.tremor == 1.0
    assert efeito.particulas == []


def test_quadro_sem_evento_nao_acende_nada():
    efeito = efeitos_novos()
    efeito.reagir(partida_com_eventos())
    assert efeito.particulas == []
    assert efeito.flash == 0.0


def test_evento_que_nao_e_coleta_nem_impacto_passa_batido():
    """O fim de jogo e a troca de tela tem som, mas nao tem juice proprio."""
    efeito = efeitos_novos()
    efeito.reagir(partida_com_eventos(config.SOM_FIM, config.SOM_CONFIRMACAO))
    assert efeito.particulas == []
    assert efeito.flash == 0.0
    assert efeito.tremor == 0.0


def test_duas_coletas_no_mesmo_quadro_somam_fagulhas():
    efeito = efeitos_novos()
    efeito.reagir(partida_com_eventos(config.SOM_COLETA, config.SOM_COLETA))
    assert len(efeito.particulas) == 2 * config.PARTICULAS_POR_COLETA


def test_limpar_apaga_tudo():
    """Comecar uma partida nova nao pode herdar a fagulha da partida anterior."""
    efeito = efeitos_novos()
    efeito.reagir(partida_com_eventos(config.SOM_COLETA, config.SOM_IMPACTO))
    efeito.limpar()
    assert efeito.particulas == []
    assert efeito.flash == 0.0
    assert efeito.tremor == 0.0


# --- O que apaga sozinho ---


def test_o_flash_e_o_tremor_caem_com_o_tempo():
    efeito = efeitos_novos()
    efeito.reagir(partida_com_eventos(config.SOM_IMPACTO))
    efeito.atualizar(config.FLASH_DURACAO / 2)
    assert 0.0 < efeito.flash < 1.0


def test_o_flash_some_no_fim_da_duracao():
    efeito = efeitos_novos()
    efeito.reagir(partida_com_eventos(config.SOM_IMPACTO))
    efeito.atualizar(config.FLASH_DURACAO)
    assert efeito.flash == 0.0


def test_o_tremor_some_no_fim_da_duracao():
    efeito = efeitos_novos()
    efeito.reagir(partida_com_eventos(config.SOM_IMPACTO))
    efeito.atualizar(config.TREMOR_DURACAO)
    assert efeito.tremor == 0.0


def test_nenhum_aviso_fica_negativo():
    """Um quadro demorado nao pode empurrar a intensidade para baixo de zero."""
    efeito = efeitos_novos()
    efeito.reagir(partida_com_eventos(config.SOM_IMPACTO))
    efeito.atualizar(10 * config.FLASH_DURACAO)
    assert efeito.flash == 0.0
    assert efeito.tremor == 0.0


# --- A vida de uma fagulha ---


def test_a_fagulha_sobe_antes_de_cair():
    """Cuspida para cima, ela tem de subir na tela (y menor) no primeiro instante."""
    fagulha = efeitos.Particula(0.0, 0.0, 0.0, config.PARTICULA_VELOCIDADE)
    fagulha.atualizar(0.01)
    assert fagulha.y < 0.0


def test_a_gravidade_traz_a_fagulha_de_volta():
    fagulha = efeitos.Particula(0.0, 0.0, 0.0, config.PARTICULA_VELOCIDADE)
    for _ in range(200):
        fagulha.atualizar(0.01)
    assert fagulha.y > 0.0


def test_a_fagulha_reta_para_cima_nao_anda_de_lado():
    fagulha = efeitos.Particula(0.0, 0.0, 0.0, config.PARTICULA_VELOCIDADE)
    fagulha.atualizar(0.1)
    assert math.isclose(fagulha.x, 0.0, abs_tol=1e-9)


def test_o_angulo_positivo_joga_a_fagulha_para_a_direita():
    fagulha = efeitos.Particula(0.0, 0.0, 0.4, config.PARTICULA_VELOCIDADE)
    fagulha.atualizar(0.1)
    assert fagulha.x > 0.0


def test_a_fagulha_encolhe_ate_sumir():
    fagulha = efeitos.Particula(0.0, 0.0, 0.0, config.PARTICULA_VELOCIDADE)
    inicial = fagulha.raio
    fagulha.atualizar(config.PARTICULA_VIDA / 2)
    assert 0.0 < fagulha.raio < inicial


def test_a_fagulha_morre_no_fim_da_vida():
    fagulha = efeitos.Particula(0.0, 0.0, 0.0, config.PARTICULA_VELOCIDADE)
    assert fagulha.viva
    fagulha.atualizar(config.PARTICULA_VIDA)
    assert not fagulha.viva
    assert fagulha.raio == 0.0


def test_as_fagulhas_saem_da_lista_quando_morrem():
    efeito = efeitos_novos()
    efeito.reagir(partida_com_eventos(config.SOM_COLETA))
    efeito.atualizar(config.PARTICULA_VIDA)
    assert efeito.particulas == []


def test_as_fagulhas_saem_no_leque_combinado():
    """Nenhuma pode sair para tras nem apontada para baixo: o leque e para cima."""
    efeito = efeitos_novos()
    efeito.reagir(partida_com_eventos(config.SOM_COLETA))
    for fagulha in efeito.particulas:
        assert fagulha.vy < 0.0, "fagulha nascendo apontada para baixo"


def test_as_fagulhas_nao_saem_todas_iguais():
    """Sem variacao elas viajariam coladas e leriam como uma bola so."""
    efeito = efeitos_novos()
    efeito.reagir(partida_com_eventos(config.SOM_COLETA))
    assert len({round(fagulha.vx, 3) for fagulha in efeito.particulas}) > 1


def test_as_fagulhas_nascem_acima_do_chao_do_corredor():
    """Elas saem da altura do peito de quem comeu, nao dos pes."""
    partida = partida_com_eventos(config.SOM_COLETA)
    efeito = efeitos_novos()
    efeito.reagir(partida)
    assert all(fagulha.y < config.BASE_Y for fagulha in efeito.particulas)


# --- O tranco da tela ---


def test_tela_parada_nao_sai_do_lugar():
    assert efeitos_novos().deslocamento() == (0, 0)


def test_o_tranco_tira_a_tela_do_lugar():
    efeito = efeitos_novos()
    efeito.reagir(partida_com_eventos(config.SOM_IMPACTO))
    assert efeito.deslocamento() != (0, 0)


def test_o_tranco_nunca_passa_da_amplitude():
    """Passando disso, a beirada escura que o quadro descobre viraria uma tarja."""
    efeito = efeitos_novos()
    efeito.reagir(partida_com_eventos(config.SOM_IMPACTO))
    passo = config.TREMOR_DURACAO / 60
    while efeito.tremor > 0.0:
        x, y = efeito.deslocamento()
        assert math.hypot(x, y) <= config.TREMOR_AMPLITUDE + 1
        efeito.atualizar(passo)


def test_o_tranco_vai_se_acalmando():
    """No fim ele tem de estar menor que no comeco, senao para de repente."""
    efeito = efeitos_novos()
    efeito.reagir(partida_com_eventos(config.SOM_IMPACTO))
    comeco = math.hypot(*efeito.deslocamento())
    efeito.atualizar(0.8 * config.TREMOR_DURACAO)
    assert math.hypot(*efeito.deslocamento()) < comeco


def test_a_tela_volta_ao_lugar_quando_o_tranco_acaba():
    efeito = efeitos_novos()
    efeito.reagir(partida_com_eventos(config.SOM_IMPACTO))
    efeito.atualizar(config.TREMOR_DURACAO)
    assert efeito.deslocamento() == (0, 0)


# --- A cortina entre telas ---


def test_a_cortina_comeca_aberta():
    assert efeitos.Transicao().opacidade == 0


def test_a_troca_de_tela_fecha_a_cortina_de_uma_vez():
    transicao = efeitos.Transicao()
    transicao.comecar()
    assert transicao.opacidade == config.OPACIDADE_TRANSICAO


def test_a_cortina_vai_abrindo():
    transicao = efeitos.Transicao()
    transicao.comecar()
    transicao.atualizar(config.TRANSICAO_DURACAO / 2)
    assert 0 < transicao.opacidade < config.OPACIDADE_TRANSICAO


def test_a_cortina_abre_de_todo_no_fim():
    transicao = efeitos.Transicao()
    transicao.comecar()
    transicao.atualizar(config.TRANSICAO_DURACAO)
    assert transicao.opacidade == 0


def test_a_cortina_nao_abre_alem_do_aberto():
    """Um quadro demorado nao pode deixar a opacidade negativa."""
    transicao = efeitos.Transicao()
    transicao.comecar()
    transicao.atualizar(10 * config.TRANSICAO_DURACAO)
    assert transicao.opacidade == 0
