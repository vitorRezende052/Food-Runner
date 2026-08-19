"""Desenha o cenario em perspectiva, as comidas e o jogador.

Este e o lado grafico do jogo: recebe as posicoes logicas prontas, pergunta a
``perspectiva`` onde elas caem na tela e pinta. Nenhuma regra do jogo mora aqui.
"""

import pygame

import comida
import config
import perspectiva


def desenhar_cenario(tela, distancia):
    """Pinta o fundo, a estrada, as linhas de chao rolando e as divisorias das pistas.

    ``distancia`` e o quanto a partida ja andou em z: e so ela que faz o chao
    rolar, entao o asfalto acompanha qualquer mudanca de velocidade.
    """
    tela.fill(config.COR_FUNDO)
    _desenhar_estrada(tela)
    _desenhar_linhas_de_chao(tela, distancia)
    _desenhar_divisorias(tela)


def desenhar_comidas(tela, comidas):
    """Desenha as comidas da mais distante para a mais proxima.

    Nessa ordem a comida que esta na frente cobre a que vem atras, que e o que a
    perspectiva pede.
    """
    for alimento in sorted(comidas, key=lambda item: item.z, reverse=True):
        _desenhar_comida(tela, alimento)


def desenhar_jogador(tela, jogador):
    """Desenha o personagem em pe na pista onde ele esta deslizando."""
    x, y, escala = perspectiva.projetar(jogador.pista_visual, config.Z_JOGADOR)
    largura = config.LARGURA_JOGADOR * escala
    altura = config.ALTURA_JOGADOR * escala

    corpo = pygame.Rect(0, 0, largura, altura)
    corpo.midbottom = (x, y)
    arredondamento = round(config.ARREDONDAMENTO_JOGADOR * escala)
    pygame.draw.rect(tela, config.COR_JOGADOR, corpo, border_radius=arredondamento)

    raio = config.RAIO_CABECA_JOGADOR * escala
    pygame.draw.circle(tela, config.COR_CABECA_JOGADOR, (x, corpo.top - raio), raio)


def desenhar_hud(tela, partida):
    """Escreve o peso num canto de cima e a pontuacao no outro."""
    letra = fonte(config.TAMANHO_FONTE_HUD)
    peso = letra.render(
        f"{round(partida.peso)} / {round(config.PESO_GAME_OVER)} kg",
        True,
        _cor_do_peso(partida.peso),
    )
    pontos = letra.render(
        f"Pontos: {com_separador(partida.pontuacao)}", True, config.COR_TEXTO
    )
    tela.blit(peso, (config.MARGEM_HUD, config.MARGEM_HUD))
    largura_pontos = pontos.get_width()
    tela.blit(
        pontos, (config.LARGURA - config.MARGEM_HUD - largura_pontos, config.MARGEM_HUD)
    )


def _cor_do_peso(peso):
    """Perto do limite o numero fica alaranjado: e o aviso de que a corrida vai acabar."""
    if peso >= config.PESO_DE_ALERTA:
        return config.COR_ALERTA
    return config.COR_TEXTO


def escurecer(tela, opacidade=config.OPACIDADE_VEU):
    """Joga um veu escuro por cima do jogo, para o texto da tela por cima aparecer."""
    veu = pygame.Surface((config.LARGURA, config.ALTURA))
    veu.fill(config.COR_VEU)
    veu.set_alpha(opacidade)
    tela.blit(veu, (0, 0))


_fontes = {}


def fonte(tamanho):
    """Fonte padrao do pygame no tamanho pedido, guardada para nao recriar todo quadro."""
    if tamanho not in _fontes:
        _fontes[tamanho] = pygame.font.Font(None, tamanho)
    return _fontes[tamanho]


def com_separador(numero):
    '''1240 vira "1.240", do jeito que se escreve numero em portugues.'''
    return f"{numero:,}".replace(",", ".")


def escrever_no_meio(tela, linhas):
    """Empilha as linhas centralizadas na tela.

    Cada linha e ``(tamanho da fonte, texto)`` ou, quando quiser fugir da cor
    padrao, ``(tamanho da fonte, texto, cor)``.
    """
    imagens = [
        fonte(tamanho).render(texto, True, cor)
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


def _bordas_da_estrada():
    """Pistas imaginarias meia faixa alem da primeira e da ultima: os limites do asfalto."""
    return -0.5, config.QTD_PISTAS - 0.5


def _ponto(pista, z):
    """Coordenada (x, y) na tela, sem a escala, do jeito que o pygame quer."""
    x, y, _ = perspectiva.projetar(pista, z)
    return x, y


def _desenhar_estrada(tela):
    """Preenche o trapezio do asfalto, estreito no horizonte e largo na base."""
    esquerda, direita = _bordas_da_estrada()
    cantos = [
        _ponto(esquerda, config.Z_HORIZONTE),
        _ponto(direita, config.Z_HORIZONTE),
        _ponto(direita, config.Z_FUNDO_TELA),
        _ponto(esquerda, config.Z_FUNDO_TELA),
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
    esquerda, direita = _bordas_da_estrada()
    for z in _profundidades_das_linhas(distancia):
        escala = perspectiva.fator(z)
        espessura = max(1, round(config.ESPESSURA_LINHA_CHAO * escala))
        pygame.draw.line(
            tela, config.COR_LINHA_CHAO, _ponto(esquerda, z), _ponto(direita, z), espessura
        )


def _desenhar_divisorias(tela):
    """Traca as linhas que separam as pistas, do horizonte ate a base."""
    esquerda, _ = _bordas_da_estrada()
    for indice in range(config.QTD_PISTAS + 1):
        divisoria = esquerda + indice
        pygame.draw.line(
            tela,
            config.COR_FAIXA,
            _ponto(divisoria, config.Z_HORIZONTE),
            _ponto(divisoria, config.Z_FUNDO_TELA),
            config.ESPESSURA_DIVISORIA,
        )


def _cor_da_comida(alimento):
    """Verde para a comida boa, vermelho para a ruim."""
    if alimento.tipo == comida.BOA:
        return config.COR_COMIDA_BOA
    return config.COR_COMIDA_RUIM


def _desenhar_comida(tela, alimento):
    """Coloca a comida apoiada no asfalto, do tamanho que a distancia manda."""
    x, y, escala = perspectiva.projetar(alimento.pista, alimento.z)
    lado = config.TAMANHO_COMIDA * escala
    caixa = pygame.Rect(0, 0, lado, lado)
    caixa.midbottom = (x, y)
    _DESENHOS_POR_FORMA[alimento.forma](tela, _cor_da_comida(alimento), caixa)


def _desenhar_circulo(tela, cor, caixa):
    pygame.draw.circle(tela, cor, caixa.center, caixa.width / 2)


def _desenhar_quadrado(tela, cor, caixa):
    arredondamento = round(caixa.width * config.ARREDONDAMENTO_COMIDA)
    pygame.draw.rect(tela, cor, caixa, border_radius=arredondamento)


def _desenhar_triangulo(tela, cor, caixa):
    pygame.draw.polygon(tela, cor, [caixa.midtop, caixa.bottomleft, caixa.bottomright])


def _desenhar_losango(tela, cor, caixa):
    pygame.draw.polygon(
        tela, cor, [caixa.midtop, caixa.midright, caixa.midbottom, caixa.midleft]
    )


def _desenhar_garrafa(tela, cor, caixa):
    """Retangulo alto e estreito: o refrigerante."""
    estreitamento = caixa.width * (1 - config.LARGURA_GARRAFA)
    garrafa = caixa.inflate(-estreitamento, 0)
    arredondamento = round(garrafa.width * config.ARREDONDAMENTO_COMIDA)
    pygame.draw.rect(tela, cor, garrafa, border_radius=arredondamento)


def _desenhar_rosquinha(tela, cor, caixa):
    """Anel: o furo do donut deixa o asfalto aparecer."""
    raio = caixa.width / 2
    espessura = max(1, round(caixa.width * config.ESPESSURA_ROSQUINHA))
    pygame.draw.circle(tela, cor, caixa.center, raio, espessura)


_DESENHOS_POR_FORMA = {
    comida.CIRCULO: _desenhar_circulo,
    comida.QUADRADO: _desenhar_quadrado,
    comida.TRIANGULO: _desenhar_triangulo,
    comida.LOSANGO: _desenhar_losango,
    comida.GARRAFA: _desenhar_garrafa,
    comida.ROSQUINHA: _desenhar_rosquinha,
}
