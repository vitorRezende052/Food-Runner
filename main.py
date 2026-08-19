"""Ponto de entrada do Food Runner: abre a janela e roda o loop principal."""

import pygame

import audio
import config
import desenho
import jogador
import jogo
import recorde
import telas

TECLAS_ESQUERDA = (pygame.K_LEFT, pygame.K_a)
TECLAS_DIREITA = (pygame.K_RIGHT, pygame.K_d)
TECLAS_COMECAR = (pygame.K_SPACE, pygame.K_RETURN, pygame.K_KP_ENTER)
TECLAS_PAUSA = (pygame.K_ESCAPE, pygame.K_p)
TECLA_MENU = pygame.K_m


def tratar_tecla(estado, partida, tecla):
    """Devolve o estado em que o jogo fica depois desta tecla.

    Cada tela entende as suas teclas e ignora as outras; quem nao muda de tela
    devolve o mesmo estado que recebeu.
    """
    if estado == telas.MENU:
        if tecla in TECLAS_COMECAR:
            partida.reiniciar()
            return telas.JOGANDO
        if tecla == pygame.K_ESCAPE:
            return telas.SAINDO
    elif estado == telas.JOGANDO:
        if tecla in TECLAS_PAUSA:
            return telas.PAUSADO
        if tecla in TECLAS_ESQUERDA:
            partida.corredor.mover(jogador.ESQUERDA)
        elif tecla in TECLAS_DIREITA:
            partida.corredor.mover(jogador.DIREITA)
    elif estado == telas.PAUSADO:
        if tecla in TECLAS_PAUSA:
            return telas.JOGANDO
        if tecla == TECLA_MENU:
            return telas.MENU
    elif estado == telas.FIM:
        if tecla in TECLAS_COMECAR:
            partida.reiniciar()
            return telas.JOGANDO
        if tecla == TECLA_MENU:
            return telas.MENU
    return estado


def desenhar(tela, estado, partida, melhor_pontuacao):
    """Pinta um quadro inteiro: a estrada no fundo e a tela da vez por cima."""
    if estado == telas.MENU:
        desenho.desenhar_cenario(tela, 0.0)  # estrada parada, so de cenario
        telas.desenhar_menu(tela, melhor_pontuacao)
        return

    desenho.desenhar_cenario(tela, partida.distancia)
    desenho.desenhar_comidas(tela, partida.gerador.comidas)
    desenho.desenhar_jogador(tela, partida.corredor)
    desenho.desenhar_hud(tela, partida)
    if estado == telas.PAUSADO:
        telas.desenhar_pausa(tela)
    elif estado == telas.FIM:
        telas.desenhar_game_over(tela, partida, melhor_pontuacao)


def executar():
    """Inicializa o pygame, roda o loop principal e encerra tudo no final."""
    pygame.init()
    audio.iniciar()
    tela = pygame.display.set_mode((config.LARGURA, config.ALTURA))
    pygame.display.set_caption(config.TITULO)
    relogio = pygame.time.Clock()

    partida = jogo.Jogo()
    melhor_pontuacao = recorde.ler()
    estado = telas.MENU

    while estado != telas.SAINDO:
        dt = relogio.tick(config.FPS) / 1000.0

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                estado = telas.SAINDO
            elif evento.type == pygame.KEYDOWN:
                proximo = tratar_tecla(estado, partida, evento.key)
                if proximo != estado:  # trocou de tela: confirma para o jogador
                    audio.tocar(config.SOM_CONFIRMACAO)
                estado = proximo

        if estado == telas.SAINDO:
            continue  # pediram para fechar: nao vale desenhar mais um quadro

        if estado == telas.JOGANDO:
            partida.atualizar(dt)
            for som in partida.eventos:  # o que a partida acabou de fazer soar
                audio.tocar(som)
            if partida.acabou:  # unico ponto em que a partida termina
                melhor_pontuacao = recorde.salvar(partida.pontuacao)
                estado = telas.FIM

        desenhar(tela, estado, partida, melhor_pontuacao)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    executar()
