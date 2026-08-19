"""O estado de uma partida: peso, pontuacao, colisoes e fim de jogo.

Aqui moram as regras, e so elas: o peso que sobe com o ultraprocessado e desce
com o alimento saudavel, a pontuacao que cresce com a distancia, o cronometro
que faz a ``dificuldade`` apertar e o momento em que a balanca bate no limite e
a corrida acaba. Nada disso sabe o que e um pixel, entao tudo pode ser testado
sem abrir janela nenhuma.
"""

import comida
import config
import dificuldade
import jogador


class Jogo:
    """Uma partida do comeco ao game over.

    Junta o corredor e o gerador de comida e cuida do que acontece quando os
    dois se encontram. ``aleatorio`` e repassado ao gerador: no jogo fica em
    ``None`` (sorteio normal) e nos testes recebe uma semente fixa.

    ``eventos`` guarda, so pelo quadro atual, o que aconteceu de notavel — e
    dai que o ``main`` tira os sons a tocar, sem a partida precisar do pygame.
    """

    def __init__(self, aleatorio=None):
        self.aleatorio = aleatorio
        self.reiniciar()

    def reiniciar(self):
        """Volta tudo ao estado da largada, para comecar uma partida nova."""
        self.corredor = jogador.Jogador()
        self.gerador = comida.GeradorDeComida(self.aleatorio)
        self.peso = config.PESO_INICIAL
        self.tempo = 0.0
        self.distancia = 0.0
        self.bonus = 0
        self.eventos = []
        self.acabou = False

    @property
    def pontuacao(self):
        """Distancia percorrida mais os bonus das comidas boas, em pontos inteiros."""
        return round(self.distancia * config.PONTOS_POR_Z) + self.bonus

    def atualizar(self, dt):
        """Avanca a partida em ``dt`` segundos. Depois do game over nada mais anda."""
        if self.acabou:
            return
        self.eventos = []  # o que acontecer neste quadro, para o main sonorizar
        self.tempo += dt
        self.distancia += dificuldade.velocidade(self.tempo) * dt
        self.corredor.atualizar(dt)
        self.gerador.atualizar(dt, self.tempo)
        self._resolver_colisoes()

    def _resolver_colisoes(self):
        """Come o que estiver encostando no jogador e tira da estrada."""
        sobreviventes = []
        for alimento in self.gerador.comidas:
            if self._encostou(alimento):
                self._comer(alimento)
            else:
                sobreviventes.append(alimento)
        self.gerador.comidas = sobreviventes

    def _encostou(self, alimento):
        """Mesma pista e perto o bastante do plano do jogador para valer como acerto."""
        return (
            alimento.pista == self.corredor.pista
            and abs(alimento.z - config.Z_JOGADOR) <= config.ZONA_COLISAO
        )

    def _comer(self, alimento):
        """Aplica no peso e na pontuacao o efeito do alimento coletado."""
        if alimento.tipo == comida.RUIM:
            self.peso = min(
                self.peso + config.PESO_GANHO_COMIDA_RUIM, config.PESO_GAME_OVER
            )
            self.eventos.append(config.SOM_IMPACTO)
            self.acabou = self.peso >= config.PESO_GAME_OVER
            if self.acabou:
                self.eventos.append(config.SOM_FIM)
        else:
            self.peso = max(
                self.peso - config.PESO_PERDIDO_COMIDA_BOA, config.PESO_MINIMO
            )
            self.bonus += config.BONUS_COMIDA_BOA
            self.eventos.append(config.SOM_COLETA)
