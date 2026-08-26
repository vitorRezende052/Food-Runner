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
COR_COMIDA_BOA = (132, 214, 116)  # o miolo da aureola de quem e saudavel
COR_COMIDA_RUIM = (232, 110, 96)  # o miolo da aureola de quem e ultraprocessado
COR_COMIDA_BOA_BORDA = (58, 146, 74)  # o anel opaco em volta: e ele que se ve la no fundo
COR_COMIDA_RUIM_BORDA = (186, 52, 46)
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
COR_MACA = (164, 196, 86)  # maca verde: o vermelho disputava com a aureola de comida ruim
COR_CABO = (122, 92, 62)  # o cabinho da maca e o do cacho de uvas
COR_FOLHA = (110, 168, 92)  # a folha da maca e da uva, e a rama da cenoura
COR_BROCOLIS = (74, 130, 66)
COR_BROCOLIS_TALO = (176, 198, 142)
COR_CENOURA = (222, 138, 66)
COR_UVA = (146, 106, 178)  # o roxo das bagas do cacho
COR_UVA_CONTORNO = (96, 66, 124)  # roxo mais fundo: separa uma baga da vizinha
COR_PAO = (214, 166, 104)
COR_HAMBURGUER = (128, 82, 60)  # o disco de carne do lanche, mais escuro que o pao
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

# --- Cidade ---
# A rua que ladeia o asfalto: duas fileiras de predios, postes, arvores e a faixa
# de pedestres. Como todo o resto do jogo, cada elemento e uma (pista, z) -- quem
# mede em pistas converge para o horizonte de graca, na mesma projecao da estrada.
# As alturas sao em pixels na base, e a perspectiva as encolhe pela escala.
COR_PREDIO_CLARO = (208, 200, 188)  # as duas pontas da variacao de cor das fachadas
COR_PREDIO_ESCURO = (146, 130, 136)
COR_JANELA = (98, 118, 140)  # vidro apagado, refletindo o ceu
COR_JANELA_ACESA = (244, 216, 142)  # a luz de dentro
COR_POSTE = (108, 112, 118)
COR_LUMINARIA = (232, 228, 210)
COR_TRONCO = (124, 92, 68)
COR_COPA = (94, 146, 84)

# Fileira da frente: os predios sobem na beirada da calcada.
PREDIO_LARGURA = 1.3  # em pistas: a fachada virada para a camera
PREDIO_PROFUNDIDADE = 0.16  # em z: o quanto o predio avanca rua adentro
PREDIO_ESPACAMENTO = 0.19  # em z, de um predio ao proximo da mesma fileira
PREDIO_DESENCONTRO = 0.5  # em fracao do espacamento: um lado nao fica de frente para o outro
PREDIO_ALTURA_ANDAR = 62  # em pixels na base: a altura e sempre um numero inteiro de andares
PREDIO_ANDARES_MINIMOS = 4
PREDIO_ANDARES_MAXIMOS = 9
PREDIO_SOMBRA_LATERAL = 0.35  # o quanto a parede virada para a rua puxa para COR_SOMBRA

# Fileira do fundo: mais afastada, mais alta e andando mais devagar. E ela que da
# o parallax de profundidade -- o resto da rua passa voando e o fundo se arrasta.
PREDIO_FUNDO_AFASTAMENTO = 1.9  # em pistas, do fim da calcada ate a parede de tras
PREDIO_FUNDO_ANDARES_EXTRAS = 5  # mais alta, para aparecer por cima da fileira da frente
PREDIO_FUNDO_PARALLAX = 0.55  # fracao da distancia percorrida que essa fileira anda

PREDIO_JANELAS_POR_ANDAR = 3  # colunas de janela em cada parede
PREDIO_JANELA_LARGURA = 0.45  # em fracao da coluna reservada a janela; o resto e parede
PREDIO_JANELA_ALTURA = 0.60  # em fracao do andar
PREDIO_JANELA_MINIMA = 5  # em pixels: abaixo disso a grade vira sujeira e nao e desenhada
PREDIO_CHANCE_JANELA_ACESA = 0.28  # a fracao das janelas com a luz acesa

# Postes e arvores se revezam na calcada, um elemento a cada POSTE_ESPACAMENTO.
POSTE_RECUO = 0.35  # em pistas, da borda do asfalto ate o pe do poste
POSTE_ESPACAMENTO = 0.26  # em z, de um elemento de rua ao proximo
POSTE_DESENCONTRO = 0.5  # em fracao do espacamento: um lado da rua nao espelha o outro
POSTE_ALTURA = 260  # em pixels na base
POSTE_LARGURA = 9
POSTE_BRACO = 70  # o quanto o braco avanca por cima do asfalto
POSTE_LUMINARIA = 26  # largura da luminaria pendurada na ponta do braco
ARVORE_TRONCO_ALTURA = 96
ARVORE_TRONCO_LARGURA = 16
ARVORE_COPA_RAIO = 52
ARVORE_COPA_AFASTAMENTO = 0.62  # em fracao do raio, do meio da copa ao meio de cada bola

# A faixa de pedestres e pintada por cima das marcacoes do asfalto, como na rua de
# verdade. As listras correm no sentido da corrida, ao contrario das linhas de
# chao, que atravessam a pista: assim uma nao se confunde com a outra.
FAIXA_ESPACAMENTO = 2.6  # em z, de uma faixa de pedestres a proxima
FAIXA_COMPRIMENTO = 0.09  # em z, o quanto ela ocupa do asfalto
FAIXA_LISTRAS = 7
FAIXA_LARGURA_LISTRA = 0.6  # em fracao do espaco de cada listra; o resto fica asfalto

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
# Os dois pisos abaixo sao em PIXELS, e nao em fracao, de proposito: tudo mais no
# jogo encolhe junto com a perspectiva, mas o aviso de boa ou ruim e a unica coisa
# que nao pode sumir la no fundo, que e justamente onde o jogador ainda tem tempo
# de trocar de pista. Com 12 px a trava so age enquanto z > 0,72 -- o pedaco mais
# distante da estrada, em que a comida mal aparece.
TAMANHO_COMIDA_MINIMO = 12  # a comida nunca fica menor que isso, nem no horizonte
INTERVALO_SPAWN_INICIAL = 1.1  # segundos entre uma comida e a proxima
INTERVALO_SPAWN_MINIMO = 0.35  # no fim da rampa a estrada fica bem mais cheia
CHANCE_COMIDA_RUIM_INICIAL = 0.60  # o resto sai comida boa
CHANCE_COMIDA_RUIM_MAXIMA = 0.85  # no fim da rampa quase tudo e ultraprocessado
COMIDAS_POR_SPAWN_INICIAL = 1  # na largada a estrada solta uma comida por vez
COMIDAS_POR_SPAWN_MAXIMA = 2  # na metade da rampa passa a soltar duas, em pistas diferentes
ARREDONDAMENTO_COMIDA = 0.18  # canto arredondado das pecas retangulares, em fracao

# A aureola e a marca atras do alimento que diz se ele e bom ou ruim: um circulo
# verde para a comida boa e uma estrela espetada vermelha para a ultraprocessada.
# E ela que da o aviso la do horizonte, onde o alimento tem uma duzia de pixels e
# so a cor dominante chega aos olhos do jogador -- e a forma repete o recado para
# quem nao distingue verde de vermelho.
#
# A marca e montada em duas camadas, como as bagas do cacho de uva: a forma
# inteira na cor da borda e, por cima, a mesma forma menor no tom do miolo. O que
# sobra entre uma e outra e o anel.
AUREOLA_TAMANHO = 1.45  # diametro, em fracao do tamanho da comida
OPACIDADE_AUREOLA = 170  # de 0 (invisivel) a 255 (solido): o miolo deixa o asfalto aparecer
OPACIDADE_AUREOLA_BORDA = 240  # o anel e quase solido: e o que recorta a forma
AUREOLA_BORDA = 0.22  # espessura do anel, em fracao do raio da marca
AUREOLA_BORDA_MINIMA = 2  # em pixels: o piso que impede o anel de arredondar para zero
AUREOLA_PONTAS = 8  # espetos da estrela que marca a comida ruim
AUREOLA_RECUO_PONTA = 0.68  # raio do vale entre dois espetos, em fracao do raio da ponta

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

# O cacho e uma piramide de bagas apontando para baixo: uma na ponta, duas na
# fila seguinte, tres na de cima. O cabinho sai do alto da ultima fila.
COMIDA_UVA_FILAS = 3
COMIDA_UVA_RAIO = 0.15  # raio de cada baga
COMIDA_UVA_ESPACO = 0.25  # de uma baga a vizinha, na mesma fila
COMIDA_UVA_FILA = 0.22  # de uma fila para a de cima; menor que o diametro, entao elas se encostam
COMIDA_UVA_MIOLO = 0.80  # fracao do raio pintada no tom claro: o resto vira contorno
COMIDA_UVA_CABO_ALTURA = 0.16
COMIDA_UVA_CABO_LARGURA = 0.07
COMIDA_UVA_FOLHA_LARGURA = 0.28
COMIDA_UVA_FOLHA_ALTURA = 0.14

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
