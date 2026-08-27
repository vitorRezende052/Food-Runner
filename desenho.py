"""Desenha o cenario em perspectiva e o HUD da partida.

Este e o lado grafico do jogo: recebe as posicoes logicas prontas, pergunta a
``perspectiva`` onde elas caem na tela e pinta. Nenhuma regra do jogo mora aqui.
"""

import pygame

import config
import perspectiva


def desenhar_cenario(tela, distancia):
    """Pinta o ceu, o chao, a estrada, as linhas rolando e as divisorias das pistas.

    ``distancia`` e o quanto a partida ja andou em z: e so ela que faz o chao
    rolar, entao o asfalto acompanha qualquer mudanca de velocidade.
    """
    _desenhar_ceu(tela)
    _desenhar_chao(tela)
    _desenhar_calcadas(tela)
    _desenhar_estrada(tela)
    _desenhar_linhas_de_chao(tela, distancia)
    _desenhar_divisorias(tela)


def desenhar_sombra(tela, x, y, largura):
    """Mancha elipsoide translucida no chao, para o objeto nao parecer flutuando.

    ``x`` e ``y`` sao o ponto em que o objeto toca o chao e ``largura`` e a
    largura dele ja em pixels, com a escala da perspectiva aplicada.
    """
    largura_sombra = max(2, round(largura * config.SOMBRA_LARGURA))
    altura_sombra = max(2, round(largura_sombra * config.SOMBRA_ALTURA))
    mancha = pygame.Surface((largura_sombra, altura_sombra), pygame.SRCALPHA)
    pygame.draw.ellipse(
        mancha, (*config.COR_SOMBRA, config.OPACIDADE_SOMBRA), mancha.get_rect()
    )
    tela.blit(mancha, mancha.get_rect(center=(round(x), round(y))))


def desenhar_peca(tela, cor, centro_x, topo, largura, altura, arredondamento=0.0):
    """Retangulo de cantos arredondados pendurado pelo meio do topo.

    E o tijolo de que sao feitos o corredor, os postes e os troncos das arvores.
    ``arredondamento`` e a fracao da largura que vira canto redondo; zero deixa o
    canto vivo.
    """
    caixa = pygame.Rect(0, 0, max(1, round(largura)), max(1, round(altura)))
    caixa.midtop = (round(centro_x), round(topo))
    raio = round(caixa.width * arredondamento)
    pygame.draw.rect(tela, cor, caixa, border_radius=max(0, raio))


def desenhar_hud(tela, partida):
    """Escreve o peso num canto de cima e a pontuacao no outro."""
    letra = fonte(config.TAMANHO_FONTE_HUD)
    peso = _com_sombra(
        letra,
        f"{round(partida.peso)} / {round(config.PESO_GAME_OVER)} kg",
        _cor_do_peso(partida.peso),
    )
    pontos = _com_sombra(
        letra, f"Pontos: {com_separador(partida.pontuacao)}", config.COR_TEXTO
    )
    _numa_capsula(tela, peso, config.MARGEM_HUD)
    _numa_capsula(
        tela, pontos, config.LARGURA - config.MARGEM_HUD - pontos.get_width()
    )


def _numa_capsula(tela, imagem, x):
    """Poe o texto do HUD por cima de uma capsula translucida de pontas redondas.

    O jogo passa atras do HUD o tempo todo -- ora o ceu claro, ora o asfalto
    escuro, ora um predio. A capsula da ao texto um fundo proprio, para ele nao
    depender do que estiver passando, e as pontas redondas sao as do resto do
    desenho cartoon.
    """
    folga = config.PAINEL_HUD_FOLGA
    texto = imagem.get_rect(topleft=(x, config.MARGEM_HUD))
    caixa = texto.inflate(2 * folga, 2 * folga)
    capsula = pygame.Surface(caixa.size, pygame.SRCALPHA)
    pygame.draw.rect(
        capsula,
        (*config.COR_PAINEL_HUD, config.OPACIDADE_PAINEL_HUD),
        capsula.get_rect(),
        border_radius=round(caixa.height * config.PAINEL_HUD_ARREDONDAMENTO),
    )
    tela.blit(capsula, caixa)
    tela.blit(imagem, texto)


def _cor_do_peso(peso):
    """Perto do limite o numero fica alaranjado: e o aviso de que a corrida vai acabar."""
    if peso >= config.PESO_DE_ALERTA:
        return config.COR_ALERTA
    return config.COR_TEXTO


def veu(tela, cor, opacidade):
    """Cobre a tela inteira com uma camada translucida da cor pedida.

    E o mesmo gesto do escuro que fica atras do menu, do vermelho que pisca no
    impacto e da cortina que abre a cada troca de tela; opacidade zero nao
    desenha nada.
    """
    if opacidade <= 0:
        return
    camada = pygame.Surface((config.LARGURA, config.ALTURA))
    camada.fill(cor)
    camada.set_alpha(opacidade)
    tela.blit(camada, (0, 0))


def escurecer(tela, opacidade=config.OPACIDADE_VEU):
    """Joga um veu escuro por cima do jogo, para o texto da tela por cima aparecer."""
    veu(tela, config.COR_VEU, opacidade)


_fontes = {}


def fonte(tamanho):
    """Fonte padrao do pygame no tamanho pedido, guardada para nao recriar todo quadro."""
    if tamanho not in _fontes:
        _fontes[tamanho] = pygame.font.Font(None, tamanho)
    return _fontes[tamanho]


def com_separador(numero):
    '''1240 vira "1.240", do jeito que se escreve numero em portugues.'''
    return f"{numero:,}".replace(",", ".")


def misturar_cores(inicial, final, fracao):
    """Cor no meio do caminho entre duas outras: 0.0 devolve a primeira, 1.0 a segunda."""
    passo = min(max(fracao, 0.0), 1.0)
    return tuple(
        round(componente_inicial + (componente_final - componente_inicial) * passo)
        for componente_inicial, componente_final in zip(inicial, final)
    )


def _com_sombra(letra, texto, cor):
    """Escreve o texto com um sombreado escuro atras.

    O ceu do jogo e claro e o veu das telas e escuro; com a sombra o mesmo texto
    continua legivel nos dois.
    """
    frente = letra.render(texto, True, cor)
    fundo = letra.render(texto, True, config.COR_SOMBRA_TEXTO)
    recuo = config.DESLOCAMENTO_SOMBRA_TEXTO
    imagem = pygame.Surface(
        (frente.get_width() + recuo, frente.get_height() + recuo), pygame.SRCALPHA
    )
    imagem.blit(fundo, (recuo, recuo))
    imagem.blit(frente, (0, 0))
    return imagem


def escrever_no_meio(tela, linhas):
    """Empilha as linhas centralizadas na tela.

    Cada linha e ``(tamanho da fonte, texto)`` ou, quando quiser fugir da cor
    padrao, ``(tamanho da fonte, texto, cor)``.
    """
    imagens = [
        _com_sombra(fonte(tamanho), texto, cor)
        for tamanho, texto, cor in map(_com_cor, linhas)
    ]
    alturas = sum(imagem.get_height() for imagem in imagens)
    altura_total = alturas + config.ESPACO_ENTRE_LINHAS * (len(imagens) - 1)

    y = (config.ALTURA - altura_total) // 2
    for imagem in imagens:
        tela.blit(imagem, ((config.LARGURA - imagem.get_width()) // 2, y))
        y += imagem.get_height() + config.ESPACO_ENTRE_LINHAS


def _com_cor(linha):
    """Completa a linha com a cor padrao do texto quando ela nao trouxe uma."""
    if len(linha) == 2:
        return (*linha, config.COR_TEXTO)
    return linha


def bordas_da_estrada():
    """Pistas imaginarias meia faixa alem da primeira e da ultima: os limites do asfalto."""
    return -0.5, config.QTD_PISTAS - 0.5


def ponto_no_chao(pista, z):
    """Coordenada (x, y) na tela, sem a escala, do jeito que o pygame quer."""
    x, y, _ = perspectiva.projetar(pista, z)
    return x, y


_ceu = None


def _desenhar_ceu(tela):
    """Cobre a metade de cima da tela com o gradiente do ceu.

    O gradiente e pintado linha a linha uma unica vez e fica guardado: e sempre o
    mesmo desenho, nao vale refaze-lo sessenta vezes por segundo.
    """
    global _ceu
    if _ceu is None:
        _ceu = pygame.Surface((config.LARGURA, config.HORIZONTE_Y))
        ultima_linha = config.HORIZONTE_Y - 1
        for y in range(config.HORIZONTE_Y):
            cor = misturar_cores(
                config.COR_CEU_TOPO, config.COR_CEU_HORIZONTE, y / ultima_linha
            )
            pygame.draw.line(_ceu, cor, (0, y), (config.LARGURA, y))
    tela.blit(_ceu, (0, 0))


def _desenhar_chao(tela):
    """Pinta de grama tudo o que fica abaixo da linha do horizonte."""
    chao = pygame.Rect(
        0, config.HORIZONTE_Y, config.LARGURA, config.ALTURA - config.HORIZONTE_Y
    )
    pygame.draw.rect(tela, config.COR_GRAMA, chao)


def _desenhar_calcadas(tela):
    """Faixa de concreto de cada lado do asfalto, na mesma perspectiva da estrada.

    A calcada e medida em pistas, entao ela converge para o horizonte junto com o
    resto da rua sem precisar de conta propria.
    """
    esquerda, direita = bordas_da_estrada()
    for borda, lado in ((esquerda, -1), (direita, 1)):
        fora = borda + lado * config.LARGURA_CALCADA
        cantos = [
            ponto_no_chao(borda, config.Z_HORIZONTE),
            ponto_no_chao(fora, config.Z_HORIZONTE),
            ponto_no_chao(fora, config.Z_FUNDO_TELA),
            ponto_no_chao(borda, config.Z_FUNDO_TELA),
        ]
        pygame.draw.polygon(tela, config.COR_CALCADA, cantos)


def _desenhar_estrada(tela):
    """Preenche o trapezio do asfalto, estreito no horizonte e largo na base."""
    esquerda, direita = bordas_da_estrada()
    cantos = [
        ponto_no_chao(esquerda, config.Z_HORIZONTE),
        ponto_no_chao(direita, config.Z_HORIZONTE),
        ponto_no_chao(direita, config.Z_FUNDO_TELA),
        ponto_no_chao(esquerda, config.Z_FUNDO_TELA),
    ]
    pygame.draw.polygon(tela, config.COR_PISTA, cantos)


def _profundidades_das_linhas(distancia):
    """Profundidade de cada linha de chao depois de a partida andar ``distancia``.

    As linhas ficam igualmente espacadas em z e caminham juntas em direcao ao
    jogador; ao sair pelo rodape cada uma reaparece la no horizonte.
    """
    trecho_visivel = config.Z_HORIZONTE - config.Z_FUNDO_TELA
    espacamento = trecho_visivel / config.QTD_LINHAS_CHAO
    return [
        config.Z_FUNDO_TELA + (indice * espacamento - distancia) % trecho_visivel
        for indice in range(config.QTD_LINHAS_CHAO)
    ]


def _desenhar_linhas_de_chao(tela, distancia):
    """Risca o asfalto de lado a lado para dar a sensacao de velocidade."""
    esquerda, direita = bordas_da_estrada()
    for z in _profundidades_das_linhas(distancia):
        escala = perspectiva.fator(z)
        espessura = max(1, round(config.ESPESSURA_LINHA_CHAO * escala))
        pygame.draw.line(
            tela, config.COR_LINHA_CHAO, ponto_no_chao(esquerda, z), ponto_no_chao(direita, z), espessura
        )


def _desenhar_divisorias(tela):
    """Traca as linhas que separam as pistas, do horizonte ate a base."""
    esquerda, _ = bordas_da_estrada()
    for indice in range(config.QTD_PISTAS + 1):
        divisoria = esquerda + indice
        pygame.draw.line(
            tela,
            config.COR_FAIXA,
            ponto_no_chao(divisoria, config.Z_HORIZONTE),
            ponto_no_chao(divisoria, config.Z_FUNDO_TELA),
            config.ESPESSURA_DIVISORIA,
        )
