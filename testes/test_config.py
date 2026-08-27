"""Testes das constantes de configuracao: pegam erro de digitacao cedo."""

import math

import config


def test_janela_tem_medidas_utilizaveis():
    assert config.LARGURA > 0
    assert config.ALTURA > 0
    assert config.FPS > 0


def cores_configuradas():
    """Devolve (nome, valor) de cada constante de cor do config."""
    return [
        (nome, valor) for nome, valor in vars(config).items() if nome.startswith("COR_")
    ]


def test_existe_pelo_menos_uma_cor():
    assert cores_configuradas()


def test_toda_cor_e_um_rgb_valido():
    for nome, cor in cores_configuradas():
        assert len(cor) == 3, f"{nome} deveria ter 3 componentes"
        for componente in cor:
            assert 0 <= componente <= 255, f"{nome} tem componente fora de 0-255"


def test_nenhuma_cor_e_pura():
    """A direcao visual pede tons macios: nada de (255, 0, 0) ou (0, 255, 0)."""
    for nome, cor in cores_configuradas():
        assert not (255 in cor and 0 in cor), f"{nome} e uma cor pura"


def test_ceu_vai_de_um_tom_a_outro():
    assert config.COR_CEU_TOPO != config.COR_CEU_HORIZONTE


def test_medidas_do_boneco_sao_fracoes_positivas():
    """Cada peca do corredor e uma fracao da altura ou da largura dele."""
    medidas = [
        (nome, valor)
        for nome, valor in vars(config).items()
        if nome.startswith("JOGADOR_")
    ]
    assert medidas
    for nome, valor in medidas:
        assert 0 < valor <= 1.5, f"{nome} nao parece uma fracao do personagem"


def test_boneco_cabe_na_altura_dele():
    """Pernas, tronco e cabeca empilhados nao passam do alto do personagem."""
    empilhado = (
        config.JOGADOR_ALTURA_PERNA
        + config.JOGADOR_ALTURA_TRONCO
        + 2 * config.JOGADOR_RAIO_CABECA
        - config.JOGADOR_PESCOCO  # a cabeca encaixa um pouco para dentro do tronco
    )
    assert round(empilhado, 6) <= 1.0


def test_medidas_das_comidas_sao_positivas():
    """Cada alimento e montado com fracoes do lado da caixa dele: zero nao desenha nada."""
    medidas = [
        (nome, valor)
        for nome, valor in vars(config).items()
        if nome.startswith("COMIDA_")
    ]
    assert medidas
    for nome, valor in medidas:
        assert valor > 0, f"{nome} nao desenharia nada"


def test_aureola_sobra_para_fora_da_comida():
    """Menor que o alimento, o disco deixaria de ser moldura e sumiria atras dele."""
    assert config.AUREOLA_TAMANHO > 1


def test_o_anel_da_aureola_nao_engole_o_miolo():
    """Anel tao grosso quanto o raio apagaria o miolo: a marca viraria um borrao."""
    assert 0 < config.AUREOLA_BORDA < 1


def test_o_anel_da_aureola_nunca_arredonda_para_zero():
    """La no fundo a fracao do raio da menos de um pixel, e e justamente onde o
    jogador ainda tem tempo de trocar de pista: o piso e o que salva o aviso."""
    assert config.AUREOLA_BORDA_MINIMA >= 1


def test_o_piso_da_comida_e_menor_que_o_tamanho_de_chegada():
    """Piso maior que o tamanho cheio congelaria a comida na estrada inteira."""
    assert 0 < config.TAMANHO_COMIDA_MINIMO < config.TAMANHO_COMIDA


def test_a_maca_e_esverdeada():
    """Vermelha, ela se confundia com a marca de comida ruim e com a embalagem do
    refrigerante -- era o unico alimento cuja cor mentia sobre o proprio tipo."""
    vermelho, verde, azul = config.COR_MACA
    assert verde > vermelho and verde > azul


def test_o_donut_tem_furo():
    """Anel de massa tao grosso quanto o raio fecharia o meio: viraria bolacha."""
    assert config.COMIDA_DONUT_MASSA < config.COMIDA_DONUT_RAIO


def test_o_cacho_de_uvas_cabe_na_caixa_dele():
    """A piramide de bagas mais o cabinho nao passam do alto nem das laterais."""
    empilhado = (
        2 * config.COMIDA_UVA_RAIO
        + (config.COMIDA_UVA_FILAS - 1) * config.COMIDA_UVA_FILA
        + config.COMIDA_UVA_CABO_ALTURA
    )
    fila_mais_larga = (config.COMIDA_UVA_FILAS - 1) * config.COMIDA_UVA_ESPACO + (
        2 * config.COMIDA_UVA_RAIO
    )
    assert round(empilhado, 6) <= 1.0
    assert round(fila_mais_larga, 6) <= 1.0


def test_as_bagas_do_cacho_se_encostam():
    """Filas e bagas afastadas alem do diametro soltariam o cacho em bolinhas."""
    assert config.COMIDA_UVA_FILA < 2 * config.COMIDA_UVA_RAIO
    assert config.COMIDA_UVA_ESPACO < 2 * config.COMIDA_UVA_RAIO


def test_a_baga_tem_contorno():
    """Miolo do tamanho da baga apagaria o anel escuro que separa uma da outra."""
    assert config.COMIDA_UVA_MIOLO < 1


def test_o_lanche_cabe_na_caixa_dele():
    """A pilha do hamburguer nao passa do alto da caixa.

    A alface nao entra na conta: ela tapa justamente a metade de baixo do domo
    do pao, entao o que o domo acrescenta a pilha ja e a altura dele inteira.
    """
    empilhado = (
        config.COMIDA_HAMBURGUER_BASE
        + config.COMIDA_HAMBURGUER_CARNE
        + config.COMIDA_HAMBURGUER_PAO
    )
    assert round(empilhado, 6) <= 1.0


def test_opacidades_cabem_em_um_byte():
    for nome, valor in vars(config).items():
        if nome.startswith("OPACIDADE_"):
            assert 0 <= valor <= 255, f"{nome} tem opacidade fora de 0-255"


def test_os_predios_nao_se_atravessam():
    """Predio mais fundo que o espacamento entraria dentro do vizinho de tras."""
    assert 0 < config.PREDIO_PROFUNDIDADE <= config.PREDIO_ESPACAMENTO


def test_a_fileira_do_fundo_se_arrasta():
    """O parallax e isso: andando o mesmo tanto que a da frente, ela nao daria
    profundidade nenhuma; parada, descolaria da rua."""
    assert 0 < config.PREDIO_FUNDO_PARALLAX < 1


def test_a_fileira_do_fundo_aparece_por_cima_da_da_frente():
    """Mais baixa, ela ficaria escondida atras da primeira fileira e nao seria vista."""
    assert config.PREDIO_FUNDO_ANDARES_EXTRAS > 0


def test_o_predio_tem_pelo_menos_um_andar():
    assert 0 < config.PREDIO_ANDARES_MINIMOS <= config.PREDIO_ANDARES_MAXIMOS


def test_a_janela_nao_ocupa_o_andar_inteiro():
    """Ocupando tudo, uma janela encostaria na vizinha e a grade sumiria."""
    assert 0 < config.PREDIO_JANELA_LARGURA < 1
    assert 0 < config.PREDIO_JANELA_ALTURA < 1


def test_a_faixa_de_pedestres_nao_se_repete_em_cima_de_si_mesma():
    """Mais comprida que o espacamento, uma faixa comecaria antes de a outra acabar."""
    assert 0 < config.FAIXA_COMPRIMENTO < config.FAIXA_ESPACAMENTO


def test_as_listras_da_faixa_deixam_asfalto_entre_elas():
    """Listra do tamanho da celula pintaria o asfalto inteiro de branco."""
    assert 0 < config.FAIXA_LARGURA_LISTRA < 1
    assert config.FAIXA_LISTRAS > 1


def test_as_duracoes_do_juice_sao_positivas():
    """Duracao zero dividiria por zero na hora de calcular o que ja passou."""
    assert config.FLASH_DURACAO > 0
    assert config.TREMOR_DURACAO > 0
    assert config.PARTICULA_VIDA > 0
    assert config.TRANSICAO_DURACAO > 0


def test_o_juice_e_curto():
    """Efeito que dura mais que um segundo vira atrapalho, e nao resposta."""
    assert config.FLASH_DURACAO <= 1.0
    assert config.TREMOR_DURACAO <= 1.0
    assert config.PARTICULA_VIDA <= 1.0
    assert config.TRANSICAO_DURACAO <= 1.0


def test_as_opacidades_cabem_num_canal_alfa():
    for nome, valor in vars(config).items():
        if nome.startswith("OPACIDADE_"):
            assert 0 <= valor <= 255, f"{nome} esta fora de 0-255"


def test_o_flash_nao_esconde_a_estrada():
    """Vermelho solido tiraria do jogador justamente o quadro em que ele reage."""
    assert 0 < config.OPACIDADE_FLASH < 255


def test_a_capsula_do_hud_deixa_o_jogo_aparecer_atras():
    assert 0 < config.OPACIDADE_PAINEL_HUD < 255
    assert config.PAINEL_HUD_FOLGA > 0
    assert 0 < config.PAINEL_HUD_ARREDONDAMENTO <= 0.5


def test_o_tranco_e_pequeno_perto_da_tela():
    """A beirada escura que o quadro descobre ao tremer nao pode virar uma tarja."""
    assert 0 < config.TREMOR_AMPLITUDE < config.ALTURA / 20
    assert config.TREMOR_VOLTAS > 1


def test_o_leque_das_fagulhas_aponta_para_cima():
    """Meia volta de abertura ja jogaria fagulha para os lados; mais que isso,
    para tras."""
    assert 0 < config.PARTICULA_ABERTURA < math.pi


def test_a_fagulha_nao_sai_toda_igual_nem_para_tras():
    """Variacao de 1.0 ou mais deixaria uma fagulha parada ou saindo ao contrario."""
    assert 0 < config.PARTICULA_VARIACAO_VELOCIDADE < 1


def test_as_fagulhas_nascem_no_corpo_do_corredor():
    assert 0 < config.PARTICULA_ALTURA <= 1
    assert config.PARTICULAS_POR_COLETA > 0
    assert config.PARTICULA_RAIO > 0


def test_a_gravidade_puxa_as_fagulhas_para_baixo():
    """Gravidade zero deixaria a fagulha subindo para sempre, sem arco nenhum."""
    assert config.PARTICULA_GRAVIDADE > 0
    assert config.PARTICULA_VELOCIDADE > 0
