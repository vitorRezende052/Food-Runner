"""Ponto de entrada do Food Runner: abre a janela e roda o loop principal."""

import pygame

import config


def executar():
    """Inicializa o pygame, roda o loop principal e encerra tudo no final."""
    pygame.init()
    tela = pygame.display.set_mode((config.LARGURA, config.ALTURA))
    pygame.display.set_caption(config.TITULO)
    relogio = pygame.time.Clock()

    rodando = True
    while rodando:
        relogio.tick(config.FPS)

        for evento in pygame.event.get():
            fechou_janela = evento.type == pygame.QUIT
            apertou_esc = evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE
            if fechou_janela or apertou_esc:
                rodando = False

        tela.fill(config.COR_FUNDO)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    executar()
