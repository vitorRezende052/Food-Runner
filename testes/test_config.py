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
