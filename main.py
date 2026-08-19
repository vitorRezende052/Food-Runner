"""Ponto de entrada do Food Runner: abre a janela e roda o loop principal."""

import pygame

import config
import desenho
import jogador
import jogo

TECLAS_ESQUERDA = (pygame.K_LEFT, pygame.K_a)
TECLAS_DIREITA = (pygame.K_RIGHT, pygame.K_d)
TECLAS_RECOMECAR = (pygame.K_SPACE, pygame.K_RETURN, pygame.K_KP_ENTER)


def tratar_tecla(partida, tecla):
    """Manda a tecla para quem sabe o que fazer com ela na situacao atual."""
    if partida.acabou:
        if tecla in TECLAS_RECOMECAR:
            partida.reiniciar()
    elif tecla in TECLAS_ESQUERDA:
        partida.corredor.mover(jogador.ESQUERDA)
    elif tecla in TECLAS_DIREITA:
        partida.corredor.mover(jogador.DIREITA)


def desenhar(tela, partida):
    """Pinta um quadro inteiro: cenario, comidas, jogador, HUD e o aviso de fim."""
    desenho.desenhar_cenario(tela, partida.distancia)
    desenho.desenhar_comidas(tela, partida.gerador.comidas)
    desenho.desenhar_jogador(tela, partida.corredor)
    desenho.desenhar_hud(tela, partida)
    if partida.acabou:
        desenho.desenhar_game_over(tela, partida)


def executar():
    """Inicializa o pygame, roda o loop principal e encerra tudo no final."""
    pygame.init()
    tela = pygame.display.set_mode((config.LARGURA, config.ALTURA))
    pygame.display.set_caption(config.TITULO)
    relogio = pygame.time.Clock()

    partida = jogo.Jogo()

    rodando = True
    while rodando:
        dt = relogio.tick(config.FPS) / 1000.0

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    rodando = False
                else:
                    tratar_tecla(partida, evento.key)

        partida.atualizar(dt)
        desenhar(tela, partida)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    executar()
