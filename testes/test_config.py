"""Testes das constantes de configuracao: pegam erro de digitacao cedo."""

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
