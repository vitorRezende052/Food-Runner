"""Testes do recorde: le, so sobe e nunca derruba o jogo."""

import recorde


def caminho_de_teste(tmp_path):
    """Um arquivo de recorde dentro da pasta temporaria do proprio teste."""
    return tmp_path / "recorde.json"


def test_arquivo_ausente_vale_zero(tmp_path):
    assert recorde.ler(caminho_de_teste(tmp_path)) == 0


def test_arquivo_corrompido_vale_zero(tmp_path):
    caminho = caminho_de_teste(tmp_path)
    caminho.write_text("isto nao e json", encoding="utf-8")
    assert recorde.ler(caminho) == 0


def test_arquivo_sem_a_chave_esperada_vale_zero(tmp_path):
    caminho = caminho_de_teste(tmp_path)
    caminho.write_text('{"outra coisa": 10}', encoding="utf-8")
    assert recorde.ler(caminho) == 0


def test_recorde_negativo_no_arquivo_vale_zero(tmp_path):
    caminho = caminho_de_teste(tmp_path)
    caminho.write_text('{"recorde": -50}', encoding="utf-8")
    assert recorde.ler(caminho) == 0


def test_salvar_grava_a_primeira_pontuacao(tmp_path):
    caminho = caminho_de_teste(tmp_path)
    assert recorde.salvar(1200, caminho) == 1200
    assert recorde.ler(caminho) == 1200


def test_pontuacao_maior_vira_o_novo_recorde(tmp_path):
    caminho = caminho_de_teste(tmp_path)
    recorde.salvar(1200, caminho)
    assert recorde.salvar(1800, caminho) == 1800
    assert recorde.ler(caminho) == 1800


def test_pontuacao_menor_nao_apaga_o_recorde(tmp_path):
    caminho = caminho_de_teste(tmp_path)
    recorde.salvar(1800, caminho)
    assert recorde.salvar(300, caminho) == 1800
    assert recorde.ler(caminho) == 1800


def test_salvar_por_cima_de_arquivo_corrompido_funciona(tmp_path):
    caminho = caminho_de_teste(tmp_path)
    caminho.write_text("{{{", encoding="utf-8")
    assert recorde.salvar(500, caminho) == 500
    assert recorde.ler(caminho) == 500


def test_pasta_inexistente_nao_derruba_o_jogo(tmp_path):
    caminho = tmp_path / "pasta que nao existe" / "recorde.json"
    assert recorde.ler(caminho) == 0
    assert recorde.salvar(700, caminho) == 0
