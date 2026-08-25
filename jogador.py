"""O personagem: em qual pista ele esta e como desliza para a pista vizinha."""

import config

ESQUERDA = -1
DIREITA = 1


class Jogador:
    """Guarda a pista logica (a que vale para colisao) e a posicao desenhada.

    A troca de pista e imediata na logica e suave no desenho: ``pista`` muda na
    hora e ``pista_visual`` corre atras dela, para o personagem nao teleportar.
    """

    def __init__(self):
        self.pista = config.PISTA_INICIAL
        self.pista_visual = float(config.PISTA_INICIAL)

    @property
    def inclinacao(self):
        """De -1 a 1: para que lado o corredor esta se jogando; zero parado numa pista.

        E o que falta da deslizada: no comeco da troca vale quase 1 e vai se
        desfazendo enquanto o boneco chega na faixa nova.
        """
        return min(max(self.pista - self.pista_visual, -1.0), 1.0)

    def mover(self, direcao):
        """Troca de pista na direcao dada (ESQUERDA ou DIREITA), sem sair da estrada."""
        ultima_pista = config.QTD_PISTAS - 1
        self.pista = min(max(self.pista + direcao, 0), ultima_pista)

    def atualizar(self, dt):
        """Aproxima a posicao desenhada da pista logica, no ritmo do delta time."""
        passo = dt / config.DURACAO_TROCA_PISTA
        distancia = self.pista - self.pista_visual
        if abs(distancia) <= passo:
            self.pista_visual = float(self.pista)
        elif distancia > 0:
            self.pista_visual += passo
        else:
            self.pista_visual -= passo
