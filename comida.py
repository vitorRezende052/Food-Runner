"""Os alimentos que vem pela estrada: tipos, sorteio do spawn e avanco em z.

Nada aqui sabe o que e um pixel. Cada comida guarda apenas a pista em que nasceu
e a profundidade ``z``, que cai de ``Z_SPAWN`` (horizonte) ate ``Z_SUMICO``,
quando ela ja passou pelo jogador e sai da lista.
"""

import random

import config

BOA = "boa"
RUIM = "ruim"

# Formas geometricas do desenho. A cor ja diz se a comida e boa ou ruim; a forma
# so serve para o jogador diferenciar um alimento do outro de longe.
CIRCULO = "circulo"
TRIANGULO = "triangulo"
QUADRADO = "quadrado"
LOSANGO = "losango"
GARRAFA = "garrafa"
ROSQUINHA = "rosquinha"

# Cardapio: (nome, forma) de cada alimento.
COMIDAS_BOAS = (
    ("maca", CIRCULO),
    ("brocolis", TRIANGULO),
    ("cenoura", LOSANGO),
    ("carne grelhada", QUADRADO),
)
COMIDAS_RUINS = (
    ("hamburguer", QUADRADO),
    ("batata frita", TRIANGULO),
    ("refrigerante", GARRAFA),
    ("donut", ROSQUINHA),
)


class Comida:
    """Um alimento numa pista, caminhando do horizonte ate o jogador."""

    def __init__(self, pista, tipo, nome, forma, z=config.Z_SPAWN):
        self.pista = pista
        self.tipo = tipo
        self.nome = nome
        self.forma = forma
        self.z = z

    def avancar(self, dt):
        """Aproxima a comida do jogador no ritmo da corrida."""
        self.z -= config.VELOCIDADE_JOGO * dt

    def passou(self):
        """Diz se a comida ja ficou para tras e pode sair da lista."""
        return self.z <= config.Z_SUMICO


def sortear(aleatorio):
    """Cria uma comida nova no horizonte, em pista e tipo sorteados."""
    if aleatorio.random() < config.CHANCE_COMIDA_RUIM:
        tipo, cardapio = RUIM, COMIDAS_RUINS
    else:
        tipo, cardapio = BOA, COMIDAS_BOAS
    nome, forma = aleatorio.choice(cardapio)
    return Comida(aleatorio.randrange(config.QTD_PISTAS), tipo, nome, forma)


class GeradorDeComida:
    """Mantem as comidas em cena: cria de tempos em tempos, empurra e descarta."""

    def __init__(self, aleatorio=None):
        self.aleatorio = aleatorio or random.Random()
        self.comidas = []
        self.ate_a_proxima = config.INTERVALO_SPAWN

    def atualizar(self, dt):
        """Avanca as comidas, joga fora as que passaram e solta as novas."""
        for comida in self.comidas:
            comida.avancar(dt)
        self.comidas = [comida for comida in self.comidas if not comida.passou()]

        self.ate_a_proxima -= dt
        while self.ate_a_proxima <= 0:
            self.comidas.append(sortear(self.aleatorio))
            self.ate_a_proxima += config.INTERVALO_SPAWN
