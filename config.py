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
COR_COMIDA_BOA = (132, 214, 116)  # a aureola de quem e saudavel
COR_COMIDA_RUIM = (232, 110, 96)  # a aureola de quem e ultraprocessado
COR_VEU = (14, 16, 22)  # escurece a corrida por tras do menu, da pausa e do game over
COR_SOMBRA = (32, 38, 46)  # mancha no chao embaixo do que esta em pe

# Corredor: cores separadas por peca, para o boneco ser montado em partes.
COR_PELE = (226, 178, 138)
COR_CABELO = (62, 48, 44)
COR_CAMISETA = (232, 124, 82)
COR_SHORTS = (66, 96, 142)
COR_TENIS = (240, 238, 230)

# Alimentos: cada um na cor de verdade. Quem diz se a comida e boa ou ruim e a
# aureola atras dela, e nao a cor do alimento (ver COR_COMIDA_BOA/RUIM).
COR_MACA = (198, 74, 72)
COR_CABO = (122, 92, 62)  # o cabinho da maca
COR_FOLHA = (110, 168, 92)  # a folha da maca e a rama da cenoura
COR_BROCOLIS = (74, 130, 66)
COR_BROCOLIS_TALO = (176, 198, 142)
COR_CENOURA = (222, 138, 66)
COR_CARNE = (146, 92, 68)  # o bife da carne grelhada
COR_GRELHA = (86, 54, 42)  # as marcas escuras que o bife traz da grelha
COR_PAO = (214, 166, 104)
COR_HAMBURGUER = (128, 82, 60)  # o disco de carne do lanche, mais escuro que o bife
COR_ALFACE = (128, 176, 96)
COR_BATATA = (232, 196, 104)
COR_EMBALAGEM = (198, 84, 78)  # a caixinha da batata frita e o copo do refrigerante
COR_TAMPA = (232, 230, 222)  # a tampa e o canudo do refrigerante
COR_DONUT = (196, 148, 100)  # a massa
COR_COBERTURA = (222, 132, 158)  # o glace por cima do donut

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

# Animacao da corrida. A fase da passada vem da distancia percorrida, e nao de um
# cronometro proprio: quando a rampa acelera a corrida, a passada acelera junto.
PASSADAS_POR_Z = 3.0  # ciclos completos de passada a cada unidade de z andada
JOGADOR_LEVANTAR_PE = 0.12  # em fracao da altura: o quanto o pe sobe do chao no passo
JOGADOR_ELEVACAO = 0.05  # em fracao da altura: o quique do corpo entre uma pisada e outra
JOGADOR_BALANCO_BRACO = 0.05  # em fracao da altura: o vaivem do braco, contrario ao da perna
JOGADOR_ESTICAMENTO = 0.05  # squash & stretch: altura ganha no ar e perdida na pisada
JOGADOR_INCLINACAO = 0.22  # em fracao da largura: o quanto o tronco se joga na troca de pista

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
ARREDONDAMENTO_COMIDA = 0.18  # canto arredondado das pecas retangulares, em fracao

# A aureola e o disco translucido atras do alimento, verde se ele for bom e
# vermelho se for ruim. E ela que da o aviso la do horizonte, onde a comida tem
# menos de dez pixels e so a cor dominante chega aos olhos do jogador.
AUREOLA_TAMANHO = 1.15  # diametro, em fracao do tamanho da comida
OPACIDADE_AUREOLA = 105  # de 0 (invisivel) a 255 (disco solido)

# Medidas de cada alimento, todas em fracao do lado da caixa dele: mudar
# TAMANHO_COMIDA redimensiona os oito juntos, e a perspectiva so multiplica pela
# escala. As verticais sao contadas do chao para cima, que e onde a comida se
# apoia.
COMIDA_MACA_RAIO = 0.40
COMIDA_MACA_CABO_ALTURA = 0.18
COMIDA_MACA_CABO_LARGURA = 0.07
COMIDA_MACA_FOLHA_LARGURA = 0.30
COMIDA_MACA_FOLHA_ALTURA = 0.15

COMIDA_BROCOLIS_TALO_LARGURA = 0.24
COMIDA_BROCOLIS_TALO_ALTURA = 0.36
COMIDA_BROCOLIS_COPA_RAIO = 0.24
COMIDA_BROCOLIS_COPA_AFASTAMENTO = 0.22  # do meio da copa ate o meio de cada bola
COMIDA_BROCOLIS_COPA_CENTRO = 0.50  # do chao ate o meio da copa: o talo fica a mostra

COMIDA_CENOURA_LARGURA = 0.46  # a raiz e um triangulo: essa e a largura do topo
COMIDA_CENOURA_ALTURA = 0.68
COMIDA_CENOURA_RAMA_ALTURA = 0.26  # as folhas espetadas no topo da raiz
COMIDA_CENOURA_RAMA_FOLHA = 0.15  # largura de cada folha, e tambem o espaco entre elas
COMIDA_CENOURA_FOLHAS = 3

COMIDA_CARNE_ALTURA = 0.60  # o bife e uma elipse achatada, larga como a caixa
COMIDA_CARNE_MARCAS = 3
COMIDA_CARNE_MARCA_ESPESSURA = 0.07
COMIDA_CARNE_MARCA_TAMANHO = 0.11  # metade do risco diagonal, na horizontal e na vertical
COMIDA_CARNE_MARCA_ESPACO = 0.24  # de um risco da grelha para o vizinho

# O lanche e uma pilha, montada de cima para baixo: cada camada tapa a de cima.
COMIDA_HAMBURGUER_PAO = 0.50  # altura do domo do pao; a metade de baixo fica escondida
COMIDA_HAMBURGUER_ALFACE = 0.12  # a folha e a unica camada tao larga quanto a caixa
COMIDA_HAMBURGUER_CARNE = 0.20
COMIDA_HAMBURGUER_BASE = 0.22  # o pao de baixo
COMIDA_HAMBURGUER_LARGURA = 0.90  # das camadas que nao sao a alface

COMIDA_BATATA_CAIXA_ALTURA = 0.50
COMIDA_BATATA_CAIXA_TOPO = 0.86  # a caixinha e um trapezio: largura da boca
COMIDA_BATATA_CAIXA_BASE = 0.62  # e largura do fundo
COMIDA_BATATA_PALITO_LARGURA = 0.15
COMIDA_BATATA_PALITO_ALTURA = 0.46
COMIDA_BATATA_PALITO_MERGULHO = 0.08  # o quanto os palitos afundam na caixinha
COMIDA_BATATA_PALITO_CURTO = 0.75  # os palitos das pontas sao mais baixos que o do meio
COMIDA_BATATA_PALITO_ESPACO = 1.2  # de um palito ao vizinho, em fracao da largura deles

COMIDA_REFRIGERANTE_COPO_ALTURA = 0.64
COMIDA_REFRIGERANTE_TOPO = 0.62  # o copo tambem e um trapezio, de boca mais larga
COMIDA_REFRIGERANTE_BASE = 0.44
COMIDA_REFRIGERANTE_TAMPA_ALTURA = 0.10
COMIDA_REFRIGERANTE_TAMPA_SOBRA = 1.10  # a tampa passa um pouco da boca do copo
COMIDA_REFRIGERANTE_CANUDO_ALTURA = 0.22
COMIDA_REFRIGERANTE_CANUDO_LARGURA = 0.09
COMIDA_REFRIGERANTE_CANUDO_DESVIO = 0.14  # o canudo sai fora do meio da tampa

COMIDA_DONUT_RAIO = 0.46
COMIDA_DONUT_MASSA = 0.30  # espessura do anel de massa; o que sobra dentro e o furo
COMIDA_DONUT_COBERTURA = 0.20  # espessura do anel de glace, por cima da massa
COMIDA_DONUT_RECUO_COBERTURA = 0.05  # o quanto o glace para antes da borda da massa

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
