"""Valores centralizados do jogo.

Todo numero que da para ajustar (tamanho, cor, velocidade, balanceamento) mora
aqui, nunca espalhado pelo resto do codigo.
"""

# --- Janela ---
LARGURA = 960
ALTURA = 720
FPS = 60
TITULO = "Food Runner"

# --- Paleta (R, G, B) ---
# Cartoon de dia claro: tons macios, nenhuma cor pura. Todo desenho do jogo tira
# a cor daqui.
COR_CEU_TOPO = (92, 158, 216)  # o azul mais forte, la em cima
COR_CEU_HORIZONTE = (206, 230, 242)  # o ceu clareia ate encostar na linha do horizonte
COR_GRAMA = (122, 168, 104)  # o chao de fora da cidade, alem da calcada
COR_CALCADA = (198, 194, 182)  # a faixa de concreto que ladeia o asfalto
COR_PISTA = (84, 86, 96)  # asfalto
COR_FAIXA = (236, 234, 224)  # divisorias pintadas entre as pistas
COR_LINHA_CHAO = (148, 148, 156)  # riscos que atravessam o asfalto e dao velocidade
COR_TEXTO = (244, 244, 238)
COR_SOMBRA_TEXTO = (34, 38, 46)  # contorno atras do texto: legivel no ceu claro e no veu
COR_TITULO = (118, 194, 128)  # verde do titulo do menu, no tom da comida boa
COR_ALERTA = (232, 138, 62)  # peso perto do limite e titulo do game over
COR_COMIDA_BOA = (108, 186, 98)
COR_COMIDA_RUIM = (204, 88, 74)
COR_VEU = (14, 16, 22)  # escurece a corrida por tras do menu, da pausa e do game over
COR_SOMBRA = (32, 38, 46)  # mancha no chao embaixo do que esta em pe

# Corredor: cores separadas por peca, para o boneco ser montado em partes.
COR_PELE = (226, 178, 138)
COR_CABELO = (62, 48, 44)
COR_CAMISETA = (232, 124, 82)
COR_SHORTS = (66, 96, 142)
COR_TENIS = (240, 238, 230)

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
LARGURA_CALCADA = 0.7  # em fracao da distancia entre pistas, de cada lado do asfalto

# --- Sombra no chao ---
SOMBRA_LARGURA = 1.25  # em fracao da largura do objeto que faz a sombra
SOMBRA_ALTURA = 0.22  # em fracao da largura da propria sombra: uma elipse achatada
OPACIDADE_SOMBRA = 100  # de 0 (invisivel) a 255 (mancha solida)

# --- Jogador ---
# O boneco e visto de costas e montado em pecas. Cada medida abaixo e uma fracao
# da altura (as verticais) ou da largura (as horizontais) do personagem inteiro,
# entao mudar ALTURA_JOGADOR ou LARGURA_JOGADOR redimensiona tudo junto.
ALTURA_JOGADOR = 185  # do chao ao alto da cabeca, em pixels, na altura do jogador
LARGURA_JOGADOR = 88  # largura dos ombros
JOGADOR_ALTURA_PERNA = 0.38
JOGADOR_LARGURA_PERNA = 0.28
JOGADOR_AFASTAMENTO_PERNAS = 0.19  # do meio do corpo ate o meio de cada perna
JOGADOR_ALTURA_TENIS = 0.06
JOGADOR_LARGURA_TENIS = 1.25  # em fracao da largura da perna: o pe e mais largo
JOGADOR_ALTURA_TRONCO = 0.38
JOGADOR_ALTURA_SHORTS = 0.20
JOGADOR_SOBREPOSICAO_SHORTS = 0.05  # o quanto o shorts desce por cima das pernas
JOGADOR_ALTURA_BRACO = 0.36
JOGADOR_LARGURA_BRACO = 0.20
JOGADOR_AFASTAMENTO_BRACOS = 0.48  # do meio do corpo ate o meio de cada braco
JOGADOR_ALTURA_MANGA = 0.09  # a manga da camiseta cobrindo o alto do braco
JOGADOR_OMBRO = 0.03  # o quanto os bracos comecam abaixo do alto do tronco
JOGADOR_RAIO_CABECA = 0.13
JOGADOR_PESCOCO = 0.02  # o quanto a cabeca encosta dentro do tronco
JOGADOR_DESLOCAMENTO_CABELO = 0.30  # em fracao do raio: sobra nuca aparecendo embaixo
JOGADOR_ARREDONDAMENTO = 0.35  # cantos das pecas, em fracao da largura de cada uma
DURACAO_TROCA_PISTA = 0.12  # segundos para deslizar de uma pista para a vizinha

# --- Comida ---
Z_SPAWN = Z_HORIZONTE  # toda comida nasce no fundo da estrada
Z_SUMICO = Z_MINIMO  # ja saiu pelo rodape: e o piso da projecao, nao adianta ir alem
TAMANHO_COMIDA = 90  # lado da comida em pixels quando chega no jogador
INTERVALO_SPAWN_INICIAL = 1.1  # segundos entre uma comida e a proxima
INTERVALO_SPAWN_MINIMO = 0.35  # no fim da rampa a estrada fica bem mais cheia
CHANCE_COMIDA_RUIM_INICIAL = 0.60  # o resto sai comida boa
CHANCE_COMIDA_RUIM_MAXIMA = 0.85  # no fim da rampa quase tudo e ultraprocessado
COMIDAS_POR_SPAWN_INICIAL = 1  # na largada a estrada solta uma comida por vez
COMIDAS_POR_SPAWN_MAXIMA = 2  # na metade da rampa passa a soltar duas, em pistas diferentes
ESPESSURA_ROSQUINHA = 0.28  # largura do anel do donut, em fracao do tamanho dele
LARGURA_GARRAFA = 0.45  # largura do refrigerante, em fracao do tamanho dele
ARREDONDAMENTO_COMIDA = 0.18  # canto arredondado das comidas quadradas, em fracao

# --- Peso e pontuacao ---
PESO_INICIAL = 45.0
PESO_GAME_OVER = 100.0  # chegou nele, acabou a partida
PESO_MINIMO = 30.0  # nem comendo so comida boa da para emagrecer alem disso
PESO_DE_ALERTA = 80.0  # daqui para cima o HUD muda de cor: a balanca esta perto do fim
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
DESLOCAMENTO_SOMBRA_TEXTO = 3  # em pixels, o quanto a sombra do texto sai por tras dele
ESPACO_ENTRE_LINHAS = 40  # separacao entre as linhas de texto das telas
OPACIDADE_VEU = 200  # de 0 (invisivel) a 255 (tampa a tela toda)
OPACIDADE_VEU_MENU = 130  # no menu o veu e mais leve: a estrada fica a vista

# --- Audio ---
# Os quatro sons do jogo. Os nomes moram aqui, e nao no audio.py, porque a
# partida avisa o que aconteceu e o audio toca: assim os dois falam a mesma
# lingua sem a logica pura precisar importar o pygame.
SOM_COLETA = "coleta"  # engoliu comida boa
SOM_IMPACTO = "impacto"  # engoliu ultraprocessado
SOM_FIM = "fim"  # a balanca bateu no limite
SOM_CONFIRMACAO = "confirmacao"  # o jogador trocou de tela

TAXA_AMOSTRAGEM = 44100  # amostras por segundo das ondas sintetizadas
AMPLITUDE_SOM = 32767  # maior valor de uma amostra em 16 bits
VOLUME_SOM = 0.35  # fracao da amplitude maxima: som audivel e sem estouro
ATAQUE_DO_SOM = 0.05  # fracao da nota gasta subindo do silencio, para nao estalar
