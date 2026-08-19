"""Os alimentos que vem pela estrada: tipos, sorteio do spawn e avanco em z.

Nada aqui sabe o que e um pixel. Cada comida guarda apenas a pista em que nasceu
e a profundidade ``z``, que cai de ``Z_SPAWN`` (horizonte) ate ``Z_SUMICO``,
quando ela ja passou pelo jogador e sai da lista.

O ritmo desse desfile nao e fixo: o gerador recebe o tempo de partida e pergunta
a ``dificuldade`` com que velocidade, de quanto em quanto tempo, com que chance
de vir ultraprocessado e em quantas pistas de uma vez a comida deve aparecer.
"""

import random

import config
import dificuldade

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

    def avancar(self, dt, velocidade):
        """Aproxima a comida do jogador no ritmo atual da corrida."""
        self.z -= velocidade * dt

    def passou(self):
        """Diz se a comida ja ficou para tras e pode sair da lista."""
        return self.z <= config.Z_SUMICO


def sortear(aleatorio, chance_de_ruim, pista):
    """Cria uma comida nova no horizonte, na pista dada e com o tipo sorteado."""
    if aleatorio.random() < chance_de_ruim:
        tipo, cardapio = RUIM, COMIDAS_RUINS
    else:
        tipo, cardapio = BOA, COMIDAS_BOAS
    nome, forma = aleatorio.choice(cardapio)
    return Comida(pista, tipo, nome, forma)


def sortear_pistas(aleatorio, quantidade):
    """Sorteia em quais pistas o proximo spawn solta comida, sem repetir nenhuma.

    Duas comidas na mesma pista ficariam uma escondida atras da outra, e a de
    tras nem chegaria a ser desviada: por isso o sorteio e sem reposicao.
    """
    return aleatorio.sample(range(config.QTD_PISTAS), quantidade)


class GeradorDeComida:
    """Mantem as comidas em cena: cria de tempos em tempos, empurra e descarta."""

    def __init__(self, aleatorio=None):
        self.aleatorio = aleatorio or random.Random()
        self.comidas = []
        self.ate_a_proxima = config.INTERVALO_SPAWN_INICIAL

    def atualizar(self, dt, tempo):
        """Avanca as comidas, joga fora as que passaram e solta as novas.

        ``tempo`` e ha quantos segundos a partida comecou: e ele que diz quanto
        do aperto da ``dificuldade`` ja vale neste quadro.
        """
        velocidade = dificuldade.velocidade(tempo)
        for comida in self.comidas:
            comida.avancar(dt, velocidade)
        self.comidas = [comida for comida in self.comidas if not comida.passou()]

        intervalo = dificuldade.intervalo_de_spawn(tempo)
        chance_de_ruim = dificuldade.chance_de_comida_ruim(tempo)
        quantidade = dificuldade.comidas_por_spawn(tempo)
        self.ate_a_proxima -= dt
        while self.ate_a_proxima <= 0:
            for pista in sortear_pistas(self.aleatorio, quantidade):
                self.comidas.append(sortear(self.aleatorio, chance_de_ruim, pista))
            self.ate_a_proxima += intervalo
