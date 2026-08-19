"""Valores centralizados do jogo.

Todo numero que da para ajustar (tamanho, cor, velocidade, balanceamento) mora
aqui, nunca espalhado pelo resto do codigo.
"""

# --- Janela ---
LARGURA = 960
ALTURA = 720
FPS = 60
TITULO = "Food Runner"

# --- Cores (R, G, B) ---
COR_FUNDO = (18, 18, 24)
COR_TEXTO = (240, 240, 240)
COR_PISTA = (58, 58, 68)
COR_FAIXA = (232, 232, 240)
COR_COMIDA_BOA = (72, 190, 90)
COR_COMIDA_RUIM = (206, 62, 52)
COR_LINHA_CHAO = (96, 96, 112)
COR_JOGADOR = (86, 156, 214)
COR_CABECA_JOGADOR = (226, 186, 148)

# --- Pistas ---
QTD_PISTAS = 3
PISTA_INICIAL = 1
LARGURA_PISTA_BASE = 250  # distancia em pixels entre pistas vizinhas na base

# --- Perspectiva ---
# A profundidade z vale 1.0 no horizonte e 0.0 na altura do jogador.
Z_HORIZONTE = 1.0
Z_JOGADOR = 0.0
Z_FUNDO_TELA = -0.03  # a estrada passa um pouco do jogador e sai pelo rodape
Z_MINIMO = -0.05  # piso de seguranca: abaixo disso a projecao explodiria
MEIO_X = LARGURA // 2
HORIZONTE_Y = 250
BASE_Y = 640  # altura, na tela, do plano onde o jogador corre
PROFUNDIDADE = 9.0  # com 9.0 um objeto no horizonte fica com 1/10 do tamanho

# --- Chao rolando (so sensacao de velocidade, nao afeta a jogabilidade) ---
QTD_LINHAS_CHAO = 14
VELOCIDADE_CHAO = 0.5  # em z por segundo
ESPESSURA_LINHA_CHAO = 5  # em pixels, na base; encolhe junto com a perspectiva
ESPESSURA_DIVISORIA = 2  # em pixels, das linhas que separam as pistas

# --- Jogador ---
LARGURA_JOGADOR = 130
ALTURA_JOGADOR = 150
RAIO_CABECA_JOGADOR = 46
ARREDONDAMENTO_JOGADOR = 32  # canto arredondado do corpo, em pixels
DURACAO_TROCA_PISTA = 0.12  # segundos para deslizar de uma pista para a vizinha
