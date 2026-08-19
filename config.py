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
COR_VEU = (10, 10, 14)  # escurece a tela por tras do aviso de game over

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

# --- Ritmo da corrida ---
# A dificuldade sobe em rampa: cada par abaixo e o valor da largada e o do teto,
# alcancado depois de DURACAO_RAMPA segundos de partida (ver dificuldade.py).
DURACAO_RAMPA = 180.0  # em segundos: quando a partida chega no maximo aperto
VELOCIDADE_INICIAL = 0.5  # em z por segundo: vale para o chao e para a comida
VELOCIDADE_MAXIMA = 1.0  # no fim da rampa a corrida esta duas vezes mais rapida

# --- Chao rolando (so sensacao de velocidade, nao afeta a jogabilidade) ---
QTD_LINHAS_CHAO = 14
ESPESSURA_LINHA_CHAO = 5  # em pixels, na base; encolhe junto com a perspectiva
ESPESSURA_DIVISORIA = 2  # em pixels, das linhas que separam as pistas

# --- Jogador ---
LARGURA_JOGADOR = 130
ALTURA_JOGADOR = 150
RAIO_CABECA_JOGADOR = 46
ARREDONDAMENTO_JOGADOR = 32  # canto arredondado do corpo, em pixels
DURACAO_TROCA_PISTA = 0.12  # segundos para deslizar de uma pista para a vizinha

# --- Comida ---
Z_SPAWN = Z_HORIZONTE  # toda comida nasce no fundo da estrada
Z_SUMICO = Z_MINIMO  # ja saiu pelo rodape: e o piso da projecao, nao adianta ir alem
TAMANHO_COMIDA = 90  # lado da comida em pixels quando chega no jogador
INTERVALO_SPAWN_INICIAL = 1.1  # segundos entre uma comida e a proxima
INTERVALO_SPAWN_MINIMO = 0.45  # no fim da rampa a estrada fica bem mais cheia
CHANCE_COMIDA_RUIM_INICIAL = 0.60  # o resto sai comida boa
CHANCE_COMIDA_RUIM_MAXIMA = 0.85  # no fim da rampa quase tudo e ultraprocessado
ESPESSURA_ROSQUINHA = 0.28  # largura do anel do donut, em fracao do tamanho dele
LARGURA_GARRAFA = 0.45  # largura do refrigerante, em fracao do tamanho dele
ARREDONDAMENTO_COMIDA = 0.18  # canto arredondado das comidas quadradas, em fracao

# --- Peso e pontuacao ---
PESO_INICIAL = 45.0
PESO_GAME_OVER = 100.0  # chegou nele, acabou a partida
PESO_MINIMO = 30.0  # nem comendo so comida boa da para emagrecer alem disso
PESO_GANHO_COMIDA_RUIM = 4.0  # em kg, por ultraprocessado engolido
PESO_PERDIDO_COMIDA_BOA = 2.0  # em kg: devolve menos do que a ruim cobra
BONUS_COMIDA_BOA = 50  # pontos por alimento saudavel coletado
PONTOS_POR_Z = 20.0  # com VELOCIDADE_INICIAL em 0,5 da os 10 pontos por segundo
ZONA_COLISAO = 0.04  # a comida acerta enquanto o z dela estiver a essa distancia do jogador

# --- HUD e avisos ---
TAMANHO_FONTE_HUD = 40
TAMANHO_FONTE_TITULO = 76
TAMANHO_FONTE_AVISO = 36
MARGEM_HUD = 24  # respiro entre o texto e a borda da tela
ESPACO_ENTRE_LINHAS = 40  # separacao das linhas do aviso de game over
OPACIDADE_VEU = 200  # de 0 (invisivel) a 255 (tampa a tela toda)
