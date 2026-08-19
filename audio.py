"""Os sons do jogo, sintetizados na hora com numpy — nenhum arquivo externo.

Cada som e uma sequencia curta de notas. Uma nota vira um array de amostras
(``onda``), as notas de uma receita sao emendadas numa onda so (``sintetizar``)
e o pygame transforma esse array em som (``iniciar``). Toda essa parte e
matematica pura: da para testar sem placa de som e sem abrir janela.

Maquina sem dispositivo de audio nao derruba o jogo: se o mixer nao subir, o
catalogo fica vazio e ``tocar`` simplesmente nao faz nada.
"""

import numpy
import pygame

import config

# Formas de onda. A senoide e macia; a quadrada e aspera, de console antigo.
SENOIDE = "senoide"
QUADRADA = "quadrada"

# Receita de cada som: a forma da onda e as notas (frequencia em Hz, duracao em
# segundos). Coletar sobe, errar desce e o game over desce mais fundo e mais
# devagar — da para saber o que aconteceu so de ouvido.
RECEITAS = {
    config.SOM_COLETA: (SENOIDE, ((660, 0.06), (880, 0.10))),
    config.SOM_IMPACTO: (QUADRADA, ((180, 0.08), (110, 0.14))),
    config.SOM_FIM: (QUADRADA, ((330, 0.18), (220, 0.18), (165, 0.30))),
    config.SOM_CONFIRMACAO: (SENOIDE, ((520, 0.08),)),
}

# Os sons prontos, preenchidos por ``iniciar``. Vazio significa jogo mudo.
_sons = {}


def envelope(quantidade):
    """Volume da nota ao longo do tempo: sobe rapido e desce ate o silencio.

    Sem isso a onda comeca e termina cortada no meio, e o alto-falante estala.
    """
    subida = max(int(quantidade * config.ATAQUE_DO_SOM), 1)
    ataque = numpy.linspace(0.0, 1.0, subida)
    queda = numpy.linspace(1.0, 0.0, quantidade - subida)
    return numpy.concatenate((ataque, queda))


def onda(forma, frequencia, duracao):
    """Uma nota como amostras entre -1 e 1, ja com o envelope aplicado."""
    quantidade = max(int(config.TAXA_AMOSTRAGEM * duracao), 1)
    tempo = numpy.arange(quantidade) / config.TAXA_AMOSTRAGEM
    amostras = numpy.sin(2 * numpy.pi * frequencia * tempo)
    if forma == QUADRADA:
        amostras = numpy.sign(amostras)
    return amostras * envelope(quantidade)


def sintetizar(nome):
    """Emenda as notas da receita numa onda so, no formato que o mixer espera."""
    forma, notas = RECEITAS[nome]
    amostras = numpy.concatenate(
        [onda(forma, frequencia, duracao) for frequencia, duracao in notas]
    )
    return (amostras * config.VOLUME_SOM * config.AMPLITUDE_SOM).astype(numpy.int16)


def iniciar():
    """Liga o mixer e sintetiza os sons. Sem dispositivo de audio, o jogo fica mudo."""
    _sons.clear()
    try:
        pygame.mixer.quit()  # o pygame.init ja pode ter subido o mixer noutro formato
        # Um canal so, porque a onda sintetizada e um array de uma dimensao.
        # Sem allowedchanges=0 o Windows abre em estereo assim mesmo e recusa o
        # array; com ele o SDL aceita o formato pedido e converte por conta.
        pygame.mixer.init(
            frequency=config.TAXA_AMOSTRAGEM, size=-16, channels=1, allowedchanges=0
        )
        for nome in RECEITAS:
            _sons[nome] = pygame.sndarray.make_sound(sintetizar(nome))
    except (pygame.error, ValueError):
        _sons.clear()  # nao ha o que tocar, mas a partida continua normalmente


def tocar(nome):
    """Toca um dos sons. Nome desconhecido ou jogo mudo: nao acontece nada."""
    som = _sons.get(nome)
    if som is not None:
        som.play()
