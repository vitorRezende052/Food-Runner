"""As telas que nao sao a corrida: menu, pausa e game over.

Cada estado do jogo tem uma tela, e os nomes dos estados moram aqui junto delas.
O ``main`` guarda em qual deles o jogo esta; este modulo so sabe pintar cada um,
apoiado nos utilitarios de texto do ``desenho``.
"""

import config
import desenho

# Em que ponto o jogo esta. SAINDO e o unico que nao desenha nada: e o pedido
# para fechar a janela.
MENU = "menu"
JOGANDO = "jogando"
PAUSADO = "pausado"
FIM = "fim"
SAINDO = "saindo"


def desenhar_menu(tela, recorde):
    """Titulo, instrucoes curtas e o recorde, por cima da estrada parada."""
    desenho.escurecer(tela, config.OPACIDADE_VEU_MENU)
    linhas = [
        (config.TAMANHO_FONTE_TITULO, config.TITULO),
        (config.TAMANHO_FONTE_AVISO, "Coma o que faz bem e desvie dos ultraprocessados"),
        (config.TAMANHO_FONTE_AVISO, "Setas ou A e D trocam de pista"),
        (
            config.TAMANHO_FONTE_AVISO,
            f"Comida ruim engorda; a {round(config.PESO_GAME_OVER)} kg a corrida acaba",
        ),
        (config.TAMANHO_FONTE_HUD, f"Recorde: {desenho.com_separador(recorde)}"),
        (config.TAMANHO_FONTE_AVISO, "Espaço para começar · ESC para sair"),
    ]
    desenho.escrever_no_meio(tela, linhas)


def desenhar_pausa(tela):
    """Congela a corrida atras de um veu e lembra como sair da pausa."""
    desenho.escurecer(tela)
    linhas = [
        (config.TAMANHO_FONTE_TITULO, "Pausado"),
        (config.TAMANHO_FONTE_AVISO, "ESC ou P para continuar"),
        (config.TAMANHO_FONTE_AVISO, "M para voltar ao menu"),
    ]
    desenho.escrever_no_meio(tela, linhas)


def desenhar_game_over(tela, partida, recorde):
    """Anuncia o fim da partida com a pontuacao final e o recorde ja atualizado."""
    desenho.escurecer(tela)
    linhas = [
        (
            config.TAMANHO_FONTE_TITULO,
            f"Você chegou a {round(config.PESO_GAME_OVER)} kg",
        ),
        (
            config.TAMANHO_FONTE_HUD,
            f"Pontos: {desenho.com_separador(partida.pontuacao)}",
        ),
        (config.TAMANHO_FONTE_HUD, _linha_do_recorde(partida.pontuacao, recorde)),
        (config.TAMANHO_FONTE_AVISO, "Espaço para jogar de novo · M para o menu"),
    ]
    desenho.escrever_no_meio(tela, linhas)


def _linha_do_recorde(pontuacao, recorde):
    """Comemora quando a partida alcancou o recorde; se nao, so mostra qual e."""
    if pontuacao >= recorde:
        return "Novo recorde!"
    return f"Recorde: {desenho.com_separador(recorde)}"
