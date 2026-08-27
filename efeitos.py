"""O juice do jogo: as fagulhas, o flash do impacto, o tranco e a cortina.

Tudo aqui e resposta a alguma coisa que acabou de acontecer, e nao cenario. E
por isso que este e o unico modulo puxado por um **cronometro proprio**: o resto
do jogo -- as linhas do asfalto, a passada do corredor, a rua da cidade -- anda
pela distancia percorrida, para ficar em sincronia com a rampa de dificuldade e
congelar sozinho na pausa. Um flash de tres decimos de segundo nao tem o que
sincronizar, e precisa acabar mesmo depois de a corrida ter parado, no game
over. Entao ele conta o proprio tempo, em segundos, e e a excecao consciente a
essa regra.

Nada disso e inventado aqui: a ``Efeitos`` le a lista ``eventos`` da partida, a
mesma de que o ``main`` ja tirava os sons. E a partida continua sem saber o que
e um pixel.

Fora o desenho, tudo neste modulo e conta pura sobre o tempo -- da para testar a
vida inteira de uma fagulha sem abrir janela nenhuma.
"""

import math
import random

import pygame

import config
import desenho
import perspectiva


class Particula:
    """Uma fagulha cuspida para o alto, que a gravidade traz de volta.

    O angulo e medido a partir do "para cima": zero sobe reto, positivo joga
    para a direita. Ela vive ``PARTICULA_VIDA`` segundos e encolhe ate sumir.
    """

    def __init__(self, x, y, angulo, velocidade):
        self.x = x
        self.y = y
        self.vx = math.sin(angulo) * velocidade
        self.vy = -math.cos(angulo) * velocidade  # na tela, subir e diminuir y
        self.vida = config.PARTICULA_VIDA

    def atualizar(self, dt):
        """Avanca a fagulha ``dt`` segundos e gasta esse tanto da vida dela."""
        self.vy += config.PARTICULA_GRAVIDADE * dt
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vida -= dt

    @property
    def viva(self):
        """Diz se a fagulha ainda tem vida; quando acaba, ela sai da lista."""
        return self.vida > 0.0

    @property
    def raio(self):
        """Em pixels: nasce cheia e encolhe junto com o que sobra de vida."""
        return config.PARTICULA_RAIO * max(self.vida, 0.0) / config.PARTICULA_VIDA


class Efeitos:
    """O feedback de uma partida: as fagulhas, o veu vermelho e o tranco da tela.

    ``flash`` e ``tremor`` sao intensidades de 0 (apagado) a 1 (no auge), e
    ambas caem sozinhas ate zero. ``aleatorio`` e o sorteio do leque das
    fagulhas: no jogo fica em ``None`` e nos testes recebe uma semente fixa,
    como ja acontece com o ``Jogo``.
    """

    def __init__(self, aleatorio=None):
        self.aleatorio = aleatorio or random.Random()
        self.limpar()

    def limpar(self):
        """Apaga tudo. E o estado de quem esta comecando uma partida nova."""
        self.particulas = []
        self.flash = 0.0
        self.tremor = 0.0

    def reagir(self, partida):
        """Acende os efeitos do que a partida acabou de fazer neste quadro.

        Le a mesma lista ``eventos`` de que o ``main`` tira os sons: e ela que
        conta o que aconteceu, sem a partida precisar saber o que e um pixel.
        """
        for evento in partida.eventos:
            if evento == config.SOM_COLETA:
                self._espalhar_fagulhas(partida.corredor)
            elif evento == config.SOM_IMPACTO:
                self.flash = 1.0
                self.tremor = 1.0

    def atualizar(self, dt):
        """Passa ``dt`` segundos: as fagulhas voam e os dois avisos vao se apagando."""
        for particula in self.particulas:
            particula.atualizar(dt)
        self.particulas = [
            particula for particula in self.particulas if particula.viva
        ]
        self.flash = max(0.0, self.flash - dt / config.FLASH_DURACAO)
        self.tremor = max(0.0, self.tremor - dt / config.TREMOR_DURACAO)

    def deslocamento(self):
        """Quanto o quadro inteiro sai do lugar neste instante, em pixels.

        O tranco e uma volta que se fecha: o angulo corre com o que ja passou do
        tremor e o raio encolhe com o que falta, entao a tela gira e se acalma
        sem cronometro nenhum alem da propria intensidade.
        """
        if self.tremor <= 0.0:
            return 0, 0
        angulo = (1.0 - self.tremor) * config.TREMOR_VOLTAS * 2 * math.pi
        raio = config.TREMOR_AMPLITUDE * self.tremor
        return round(math.cos(angulo) * raio), round(math.sin(angulo) * raio)

    def desenhar_fagulhas(self, tela):
        """As fagulhas verdes, cada uma menor que no quadro anterior."""
        for particula in self.particulas:
            raio = particula.raio
            if raio >= 1.0:  # menos de um pixel nao chega a ser desenhado
                pygame.draw.aacircle(
                    tela, config.COR_COMIDA_BOA, (particula.x, particula.y), raio
                )

    def desenhar_flash(self, tela):
        """O vermelho do ultraprocessado, por cima de tudo o que estava na tela."""
        desenho.veu(
            tela, config.COR_FLASH_RUIM, round(config.OPACIDADE_FLASH * self.flash)
        )

    def _espalhar_fagulhas(self, corredor):
        """Solta um punhado de fagulhas na altura dos ombros de quem acabou de comer."""
        x, y, escala = perspectiva.projetar(corredor.pista_visual, config.Z_JOGADOR)
        ombros = y - config.PARTICULA_ALTURA * config.ALTURA_JOGADOR * escala
        for _ in range(config.PARTICULAS_POR_COLETA):
            angulo = self.aleatorio.uniform(-0.5, 0.5) * config.PARTICULA_ABERTURA
            sobra = self.aleatorio.uniform(-1.0, 1.0)
            velocidade = config.PARTICULA_VELOCIDADE * (
                1.0 + sobra * config.PARTICULA_VARIACAO_VELOCIDADE
            )
            self.particulas.append(Particula(x, ombros, angulo, velocidade))


class Transicao:
    """A cortina que abre quando o jogo troca de tela.

    E so fade in: a tela nova nasce escura e clareia em ``TRANSICAO_DURACAO``
    segundos. A troca de estado acontece na hora, entao a tecla continua
    respondendo na hora -- que e o que a pausa pede de um jogo.
    """

    def __init__(self):
        self.restante = 0.0

    def comecar(self):
        """Fecha a cortina de uma vez; daqui em diante ela so abre."""
        self.restante = config.TRANSICAO_DURACAO

    def atualizar(self, dt):
        """Abre a cortina mais ``dt`` segundos, sem passar do aberto de todo."""
        self.restante = max(0.0, self.restante - dt)

    @property
    def opacidade(self):
        """Do escuro cheio, no instante da troca, ate zero quando a cortina abriu."""
        return round(
            config.OPACIDADE_TRANSICAO * self.restante / config.TRANSICAO_DURACAO
        )

    def desenhar(self, tela):
        """Escurece o quadro no tanto que ainda falta da cortina abrir."""
        desenho.escurecer(tela, self.opacidade)
