"""Como a partida vai apertando conforme o relogio corre.

Tres numeros mudam com o tempo de jogo: a velocidade da corrida, o intervalo
entre uma comida e a proxima e a chance de a comida sorteada ser ruim. Todos
saem da largada no valor inicial do ``config`` e caminham em linha reta ate o
teto, que e alcancado em ``DURACAO_RAMPA`` segundos e nao passa disso.

E logica pura, como a ``perspectiva``: sem estado guardado e sem pygame, entao
basta perguntar o valor de um instante qualquer para testar a rampa inteira.
"""

import config


def progresso(tempo):
    """O quanto da rampa ja foi vencido: 0.0 na largada, 1.0 do teto em diante."""
    return min(tempo / config.DURACAO_RAMPA, 1.0)


def _rampa(inicial, final, tempo):
    """Caminha em linha reta de ``inicial`` ate ``final`` no compasso do progresso."""
    return inicial + (final - inicial) * progresso(tempo)


def velocidade(tempo):
    """Ritmo da corrida, em z por segundo, no instante pedido."""
    return _rampa(config.VELOCIDADE_INICIAL, config.VELOCIDADE_MAXIMA, tempo)


def intervalo_de_spawn(tempo):
    """Segundos de espera entre uma comida e a proxima, no instante pedido."""
    return _rampa(
        config.INTERVALO_SPAWN_INICIAL, config.INTERVALO_SPAWN_MINIMO, tempo
    )


def chance_de_comida_ruim(tempo):
    """Probabilidade de a proxima comida ser um ultraprocessado, no instante pedido."""
    return _rampa(
        config.CHANCE_COMIDA_RUIM_INICIAL, config.CHANCE_COMIDA_RUIM_MAXIMA, tempo
    )
