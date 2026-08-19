"""Ponto de entrada do Food Runner: abre a janela e roda o loop principal."""

import pygame

import comida
import config
import desenho
import jogador

TECLAS_ESQUERDA = (pygame.K_LEFT, pygame.K_a)
TECLAS_DIREITA = (pygame.K_RIGHT, pygame.K_d)


def executar():
    """Inicializa o pygame, roda o loop principal e encerra tudo no final."""
    pygame.init()
    tela = pygame.display.set_mode((config.LARGURA, config.ALTURA))
    pygame.display.set_caption(config.TITULO)
    relogio = pygame.time.Clock()

    corredor = jogador.Jogador()
    gerador = comida.GeradorDeComida()
    tempo = 0.0

    rodando = True
    while rodando:
        dt = relogio.tick(config.FPS) / 1000.0
        tempo += dt

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    rodando = False
                elif evento.key in TECLAS_ESQUERDA:
                    corredor.mover(jogador.ESQUERDA)
                elif evento.key in TECLAS_DIREITA:
                    corredor.mover(jogador.DIREITA)

        corredor.atualizar(dt)
        gerador.atualizar(dt)

        desenho.desenhar_cenario(tela, tempo)
        desenho.desenhar_comidas(tela, gerador.comidas)
        desenho.desenhar_jogador(tela, corredor)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    executar()
