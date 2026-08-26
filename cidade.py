"""A rua da cidade que ladeia o asfalto: predios, postes, arvores e faixa de pedestres.

Tudo aqui e descrito com uma ``pista`` e um ``z``, como o resto do jogo. Quem
mede em pistas converge para o horizonte de graca, na mesma projecao da estrada
-- foi assim que a calcada nasceu, e e em cima dela que os predios sobem.

E tudo anda pela **distancia percorrida**, nunca por um cronometro proprio: e o
mesmo truque das linhas do asfalto e da passada do corredor, e ele resolve de
graca a sincronia com a rampa de dificuldade e o congelamento na pausa.

Cada elemento da rua tem um **indice inteiro que nunca se repete** (ver
``posicoes``), e e desse numero que saem a altura, a cor e as janelas acesas de
cada predio (ver ``variacao``). Duas consequencias: a rua nao repete, porque o
indice sempre cresce, e nao existe estado guardado entre um quadro e outro -- o
mesmo quadro desenhado duas vezes sai identico.
"""

import math

import pygame

import config
import desenho
import perspectiva

# Os passos da ``variacao``, um por caracteristica. Sao irracionais de proposito:
# a parte fracionaria dos multiplos deles nunca cai duas vezes no mesmo lugar,
# entao os valores se espalham sem repetir e sem precisar de sorteio nenhum.
PASSO_INDICE = 0.6180339887  # razao aurea
PASSO_CHAVE = 0.4142135624  # raiz de dois, menos um
PASSO_MISTURA = 0.7320508076  # raiz de tres, menos um

# As chaves de cada caracteristica de um predio. As janelas contam a partir da
# ultima: cada uma soma a sua posicao na grade e fica com um numero so dela.
CHAVE_ALTURA = 1
CHAVE_COR = 2
CHAVE_JANELA = 3

# As quatro filas de predios da rua: a fileira do fundo e a da frente, cada uma
# de um lado do asfalto. E o que separa a identidade de predios de mesmo indice.
FILAS_DE_PREDIOS = 4
FILEIRA_DA_FRENTE = 0
FILEIRA_DO_FUNDO = 1

LADOS = (-1, 1)  # esquerda e direita da rua


def posicoes(distancia, espacamento, deslocamento=0.0):
    """Os elementos visiveis de uma fila, como pares ``(indice, z)``, do perto ao longe.

    Os elementos ficam plantados na rua de ``espacamento`` em ``espacamento`` e e
    a corrida que passa por eles: o de indice ``i`` esta em
    ``(i + deslocamento) * espacamento - distancia``. Ficam de fora os que ainda
    nao chegaram ao horizonte e os que ja sairam pelo rodape.

    O ``deslocamento`` desencontra duas filas: com meio espacamento, um lado da
    rua deixa de ser o espelho do outro.

    Como o indice diz o lugar do elemento na rua (e nao uma vaga que se recicla),
    ele so cresce enquanto a partida anda -- e por isso serve de identidade
    permanente para a ``variacao``.
    """
    primeiro = math.ceil((distancia + config.Z_FUNDO_TELA) / espacamento - deslocamento)
    ultimo = math.floor((distancia + config.Z_HORIZONTE) / espacamento - deslocamento)
    return [
        (indice, (indice + deslocamento) * espacamento - distancia)
        for indice in range(primeiro, ultimo + 1)
    ]


def variacao(indice, chave):
    """Numero de 0 a 1 preso ao par ``(indice, chave)``: o mesmo par sempre da o mesmo.

    O indice e a chave entram multiplicados por irracionais diferentes, e o
    produto dos dois entra por um terceiro. E esse ultimo termo que faz duas
    chaves darem sequencias sem parentesco, em vez de uma ser a outra deslocada
    -- sem ele, o predio mais alto teria sempre a mesma cor.
    """
    return (
        indice * PASSO_INDICE + chave * PASSO_CHAVE + indice * chave * PASSO_MISTURA
    ) % 1.0


def faixa_da_coluna(coluna, colunas):
    """Onde uma coluna de janelas comeca e acaba, em fracao da largura da parede.

    A parede e dividida em colunas iguais e a janela ocupa o meio de cada uma; o
    que sobra dos dois lados e a parede entre uma janela e a vizinha.
    """
    return _faixa_centrada(coluna, colunas, config.PREDIO_JANELA_LARGURA)


def faixa_do_andar(linha, andares):
    """Onde uma janela comeca e acaba, em fracao da altura da parede.

    Mesma ideia da ``faixa_da_coluna``, na vertical: um andar por fileira, com a
    janela no meio dele.
    """
    return _faixa_centrada(linha, andares, config.PREDIO_JANELA_ALTURA)


def _faixa_centrada(posicao, quantidade, ocupacao):
    """O pedaco que a janela ocupa dentro da sua celula, em fracao da parede inteira."""
    meia = ocupacao / quantidade / 2
    meio = (posicao + 0.5) / quantidade
    return meio - meia, meio + meia


def desenhar(tela, distancia):
    """Pinta a rua inteira por cima do cenario, do fundo para a frente."""
    _desenhar_fileira(
        tela,
        distancia,
        FILEIRA_DO_FUNDO,
        config.PREDIO_FUNDO_AFASTAMENTO,
        config.PREDIO_FUNDO_ANDARES_EXTRAS,
        config.PREDIO_FUNDO_PARALLAX,
    )
    _desenhar_fileira(tela, distancia, FILEIRA_DA_FRENTE, 0.0, 0, 1.0)
    _desenhar_faixas_de_pedestre(tela, distancia)
    _desenhar_postes_e_arvores(tela, distancia)


def _desenhar_fileira(tela, distancia, fileira, afastamento, andares_extras, parallax):
    """Uma fileira de predios de cada lado da rua, desenhada do fundo para a frente.

    ``parallax`` e a fracao da distancia que essa fileira anda: a de tras usa
    menos de 1 e por isso se arrasta enquanto a da frente passa voando.
    """
    andado = distancia * parallax
    bordas = zip(desenho.bordas_da_estrada(), LADOS)
    for numero_do_lado, (borda, lado) in enumerate(bordas):
        pista = borda + lado * (config.LARGURA_CALCADA + afastamento)
        deslocamento = numero_do_lado * config.PREDIO_DESENCONTRO
        semente = fileira * len(LADOS) + numero_do_lado
        visiveis = posicoes(andado, config.PREDIO_ESPACAMENTO, deslocamento)
        for indice, z in reversed(visiveis):  # o predio da frente tapa o de tras
            identidade = indice * FILAS_DE_PREDIOS + semente
            _desenhar_predio(tela, identidade, pista, lado, z, andares_extras)


def _desenhar_predio(tela, identidade, pista_interna, lado, z, andares_extras):
    """Uma caixa de duas paredes: a lateral, virada para a rua, e a fachada, para a camera.

    A altura e sempre um numero inteiro de andares, entao a grade de janelas
    fecha certinho por mais alto que o predio saia.
    """
    variedade = config.PREDIO_ANDARES_MAXIMOS - config.PREDIO_ANDARES_MINIMOS
    andares = (
        config.PREDIO_ANDARES_MINIMOS
        + andares_extras
        + round(variacao(identidade, CHAVE_ALTURA) * variedade)
    )
    altura = andares * config.PREDIO_ALTURA_ANDAR
    pista_externa = pista_interna + lado * config.PREDIO_LARGURA
    fundo = z + config.PREDIO_PROFUNDIDADE
    if not _na_tela(pista_interna, pista_externa, z, fundo):
        return

    fachada = desenho.misturar_cores(
        config.COR_PREDIO_CLARO,
        config.COR_PREDIO_ESCURO,
        variacao(identidade, CHAVE_COR),
    )
    lateral = desenho.misturar_cores(
        fachada, config.COR_SOMBRA, config.PREDIO_SOMBRA_LATERAL
    )
    _desenhar_parede(
        tela,
        (pista_interna, fundo),
        (pista_interna, z),
        altura,
        lateral,
        andares,
        identidade,
    )
    _desenhar_parede(
        tela,
        (pista_interna, z),
        (pista_externa, z),
        altura,
        fachada,
        andares,
        identidade,
    )


def _na_tela(pista_interna, pista_externa, z, fundo):
    """Diz se o predio ainda aparece na janela, olhando os quatro pes dele.

    Chegando perto da camera o predio sai inteiro pela lateral da tela, e a
    grade de janelas dele seria trabalho jogado fora. A altura nao entra na
    conta: predio nenhum flutua, entao o pe sempre cai na parte visivel.
    """
    laterais = [
        perspectiva.projetar(pista, profundidade)[0]
        for pista in (pista_interna, pista_externa)
        for profundidade in (z, fundo)
    ]
    return max(laterais) >= 0 and min(laterais) <= config.LARGURA


def _desenhar_parede(tela, canto_a, canto_b, altura, cor, andares, identidade):
    """O retangulo em perspectiva de uma parede, com a grade de janelas por cima.

    Os cantos sao os dois pes da parede, cada um uma ``(pista, z)``: e a
    interpolacao entre eles que faz a parede convergir para o horizonte.
    """
    pe_a = _pe_da_parede(canto_a, canto_b, 0.0)
    pe_b = _pe_da_parede(canto_a, canto_b, 1.0)
    pygame.draw.polygon(
        tela,
        cor,
        [
            _no_alto(pe_a, 0.0, altura),
            _no_alto(pe_a, 1.0, altura),
            _no_alto(pe_b, 1.0, altura),
            _no_alto(pe_b, 0.0, altura),
        ],
    )
    _desenhar_janelas(tela, canto_a, canto_b, altura, andares, identidade)


def _pe_da_parede(canto_a, canto_b, avanco):
    """Onde a parede toca o chao a ``avanco`` de caminho de um pe dela ao outro.

    Devolve o ``(x, y, escala)`` da perspectiva: com ele, subir na parede vira
    uma multiplicacao, sem projetar de novo (ver ``_no_alto``).
    """
    pista = canto_a[0] + (canto_b[0] - canto_a[0]) * avanco
    z = canto_a[1] + (canto_b[1] - canto_a[1]) * avanco
    return perspectiva.projetar(pista, z)


def _no_alto(pe, subida, altura):
    """Sobe de um pe da parede ate ``subida`` da altura dela, ja em pixels."""
    x, y, escala = pe
    return x, y - altura * escala * subida


def _desenhar_janelas(tela, canto_a, canto_b, altura, andares, identidade):
    """Uma fileira de janelas por andar, algumas acesas.

    Longe demais a janela nao chega a um pixel e a grade so suja a fachada: nesse
    caso o predio fica liso, que e o que o jogador enxergaria de qualquer jeito.
    """
    perto = perspectiva.fator(min(canto_a[1], canto_b[1]))
    janela = altura * perto * config.PREDIO_JANELA_ALTURA / andares
    if janela < config.PREDIO_JANELA_MINIMA:
        return
    colunas = config.PREDIO_JANELAS_POR_ANDAR
    for coluna in range(colunas):
        # As duas bordas de uma coluna sao as mesmas em todos os andares dela:
        # projetamos os dois pes uma vez so e cada janela vira uma conta de altura.
        pes = [
            _pe_da_parede(canto_a, canto_b, avanco)
            for avanco in faixa_da_coluna(coluna, colunas)
        ]
        for linha in range(andares):
            chave = CHAVE_JANELA + linha * colunas + coluna
            acesa = variacao(identidade, chave) < config.PREDIO_CHANCE_JANELA_ACESA
            baixo, cima = faixa_do_andar(linha, andares)
            pygame.draw.polygon(
                tela,
                config.COR_JANELA_ACESA if acesa else config.COR_JANELA,
                [_no_alto(pes[0], baixo, altura), _no_alto(pes[0], cima, altura)]
                + [_no_alto(pes[1], cima, altura), _no_alto(pes[1], baixo, altura)],
            )


def _desenhar_postes_e_arvores(tela, distancia):
    """Postes e arvores se revezando na calcada, dos dois lados da rua.

    Sao os elementos que passam mais perto da camera, entao e deles que vem a
    maior parte da sensacao de velocidade.
    """
    bordas = zip(desenho.bordas_da_estrada(), LADOS)
    for numero_do_lado, (borda, lado) in enumerate(bordas):
        pista = borda + lado * config.POSTE_RECUO
        deslocamento = numero_do_lado * config.POSTE_DESENCONTRO
        visiveis = posicoes(distancia, config.POSTE_ESPACAMENTO, deslocamento)
        for indice, z in reversed(visiveis):
            if indice % 2 == 0:
                _desenhar_poste(tela, pista, z, lado)
            else:
                _desenhar_arvore(tela, pista, z)


def _desenhar_poste(tela, pista, z, lado):
    """Haste na calcada com um braco avancando sobre o asfalto e a luminaria na ponta."""
    x, y, escala = perspectiva.projetar(pista, z)
    altura = config.POSTE_ALTURA * escala
    largura = config.POSTE_LARGURA * escala
    braco = -lado * config.POSTE_BRACO * escala  # o braco aponta para o meio da rua
    topo = y - altura

    desenho.desenhar_sombra(tela, x, y, largura)
    desenho.desenhar_peca(tela, config.COR_POSTE, x, topo, largura, altura)
    desenho.desenhar_peca(
        tela, config.COR_POSTE, x + braco / 2, topo, abs(braco) + largura, largura
    )
    desenho.desenhar_peca(
        tela,
        config.COR_LUMINARIA,
        x + braco,
        topo + largura,
        config.POSTE_LUMINARIA * escala,
        largura,
    )


def _desenhar_arvore(tela, pista, z):
    """Tronco na calcada e uma copa de tres bolas, como a do brocolis."""
    x, y, escala = perspectiva.projetar(pista, z)
    altura_tronco = config.ARVORE_TRONCO_ALTURA * escala
    raio = config.ARVORE_COPA_RAIO * escala
    centro_da_copa = y - altura_tronco - raio
    afastamento = config.ARVORE_COPA_AFASTAMENTO * raio

    desenho.desenhar_sombra(tela, x, y, 2 * raio)
    desenho.desenhar_peca(
        tela,
        config.COR_TRONCO,
        x,
        y - altura_tronco,
        config.ARVORE_TRONCO_LARGURA * escala,
        altura_tronco,
    )
    for desvio_x, desvio_y in ((-1, 0), (1, 0), (0, -1)):
        pygame.draw.aacircle(
            tela,
            config.COR_COPA,
            (x + desvio_x * afastamento, centro_da_copa + desvio_y * afastamento),
            raio,
        )


def _desenhar_faixas_de_pedestre(tela, distancia):
    """As listras brancas que atravessam o asfalto de tempos em tempos.

    Cada listra corre no sentido da corrida -- que e como uma faixa de verdade
    aparece para quem vem pela rua -- e por isso nao se confunde com as linhas de
    chao, que cruzam a pista de lado a lado.
    """
    esquerda, direita = desenho.bordas_da_estrada()
    celula = (direita - esquerda) / config.FAIXA_LISTRAS
    meia_listra = celula * config.FAIXA_LARGURA_LISTRA / 2
    for _, z in reversed(posicoes(distancia, config.FAIXA_ESPACAMENTO)):
        fundo = z + config.FAIXA_COMPRIMENTO
        for listra in range(config.FAIXA_LISTRAS):
            meio = esquerda + (listra + 0.5) * celula
            pygame.draw.polygon(
                tela,
                config.COR_FAIXA,
                [
                    desenho.ponto_no_chao(meio - meia_listra, z),
                    desenho.ponto_no_chao(meio + meia_listra, z),
                    desenho.ponto_no_chao(meio + meia_listra, fundo),
                    desenho.ponto_no_chao(meio - meia_listra, fundo),
                ],
            )
