# Plano — Food Runner

Plano de execução do jogo. **Documento vivo:** cada fase concluída é marcada aqui
(`[x]`), com o resumo do que ficou pronto e os desvios do plano anotados na
própria fase. As decisões travadas do projeto ficam no `CLAUDE.md`.

Status geral: **Fase 11 — cenário de rua da cidade** (Fases 0 a 10 concluídas:
ambiente uv, estrada em perspectiva rolando, jogador trocando de pista, comida
vindo do horizonte, a partida completa — peso, pontuação, HUD e game over —, a
rampa de dificuldade que aperta a corrida ao longo de 3 minutos, o ciclo fechado
de menu, pausa, game over e recorde em arquivo, os quatro sons sintetizados
com numpy e o balanceamento fechado — a corrida agora termina até para quem joga
bem —, com o `README.md` no ar, a fundação do visual cartoon — céu em
gradiente, grama e calçadas, paleta harmônica e o corredor de costas com sombra —
o corredor animado, com a passada puxada pela distância, e os oito alimentos
desenhados em código, cada um na cor de verdade, com um círculo verde ou uma
estrela vermelha atrás dizendo o tipo bem de longe, com 146 testes verdes). O
jogo está completo em regras; o que falta das fases 11 e 12 é o resto da
redefinição visual descrita na **Direção Visual** do `CLAUDE.md`: prédios nas
laterais e juice.

---

## Visão do jogo

Corredor infinito em 3 pistas com **perspectiva pseudo-3D**: as pistas convergem
para um horizonte, o jogador fica fixo na base da tela e a comida nasce pequena
no fundo e cresce conforme se aproxima. O jogador só troca de pista (← → e A/D)
para desviar da comida ruim e coletar a boa. Comida ruim engorda, comida boa
emagrece e pontua. Chegou a 100 kg, acabou.

### Como a perspectiva funciona (o coração do desenho)

Toda a lógica trabalha com dois valores por objeto: a **pista** (0, 1 ou 2) e a
**profundidade `z`** (`1.0` = horizonte, `0.0` = na altura do jogador). Só na
hora de desenhar isso vira pixel:

```
fator  = 1 / (1 + z * PROFUNDIDADE)      # 1.0 na base, 0.1 no horizonte
y_tela = HORIZONTE_Y + (BASE_Y - HORIZONTE_Y) * fator
x_tela = MEIO_X + deslocamento_da_pista * fator
escala = fator                            # tamanho do objeto na tela
```

Com `PROFUNDIDADE = 9.0`, um objeto no horizonte aparece com 1/10 do tamanho que
terá ao chegar no jogador. O `z` passa por `max(z, Z_MINIMO)` antes da conta: `z`
negativo é legítimo (objeto passando pela câmera fica **maior** que 1.0) e a
trava só evita o ponto em que a divisão explodiria.

Vantagem: colisão, spawn e dificuldade são matemática pura sobre `pista` e `z`,
sem pygame no meio — dá para testar tudo com pytest. A projeção fica isolada em
`perspectiva.py` e é a única parte que conhece pixels.

A `pista` aceita valor quebrado e fora do intervalo 0–2, e é assim que o cenário
é desenhado: as bordas do asfalto são as pistas `-0.5` e `2.5`, e a calçada da
fase 8 vai de cada borda até `LARGURA_CALCADA` de pista mais para fora. Quem
mede em pistas converge para o horizonte de graça — os prédios da fase 11 seguem
a mesma receita.

---

## Estrutura de arquivos

`[x]` = já existe no repositório. Desde a fase 6 todos os módulos previstos
existem, e a fase 7 mexeu em cinco deles sem criar nenhum. As fases 11 e 12
mexem sobretudo no `desenho.py` e no `config.py` (a paleta nova); se o desenho do
personagem, das comidas ou do cenário deixar o `desenho.py` grande demais, cada
um vira um arquivo seu — e a mudança é anotada aqui. Foi o que aconteceu duas
vezes: com o corredor na fase 8, que saiu para o `personagem.py`, e com as
comidas na fase 10, que saíram para o `desenho_comida.py`. Os prédios da fase 11
podem seguir o mesmo caminho se pedirem.

```
[x] main.py        # ponto de entrada: loop, eventos, troca entre menu/jogo/pausa/game over
[x] config.py      # todas as constantes: tela, cores, pistas, perspectiva, balanceamento
[x] perspectiva.py # projeta (pista, z) -> (x, y, escala). Lógica pura, testável
[x] jogador.py     # pista atual, troca de pista e inclinacao na troca
[x] desenho.py     # desenha céu, chão, rua, o HUD e os utilitários de texto
[x] desenho_comida.py # os oito alimentos e a auréola que diz o tipo deles
[x] personagem.py  # o corredor visto de costas, montado peça por peça e animado
[x] testes/        # test_config, test_perspectiva, test_jogador, test_comida,
                   # test_jogo, test_dificuldade, test_recorde, test_telas,
                   # test_audio, test_desenho, test_desenho_comida, test_personagem
[x] comida.py      # tipos de comida, spawn e avanço em z
[x] jogo.py        # estado da partida: peso, pontuação, dificuldade, colisões
[x] dificuldade.py # rampa: velocidade, intervalo de spawn e chance de comida ruim
[x] telas.py       # menu inicial (com instruções), pausa e game over
[x] audio.py       # síntese dos sons com numpy
[x] recorde.py     # lê e grava a maior pontuação em arquivo local
```

A estrutura real ficou bem perto da planejada. São quatro os desvios: o ponto de
entrada, que virou `main.py`; o `dificuldade.py`, arquivo novo que a fase 4
trouxe — o plano imaginava a rampa dentro do `jogo.py`, mas ela é lógica pura
sobre o tempo, do mesmo naipe da `perspectiva.py`, e sozinha num arquivo dá para
ler a curva inteira de uma vez; o `personagem.py`, que a fase 8 tirou do
`desenho.py` porque o corredor é a peça mais detalhada do jogo — e a fase 9 o
engordou mesmo, com o ciclo da passada; e o `desenho_comida.py`, que a fase 10
tirou do mesmo lugar pelo mesmo motivo, já que oito alimentos desenhados peça a
peça pesam mais do que o cenário inteiro.

O aviso de game over da fase 3 nasceu dentro do `desenho.py` e, como previsto,
mudou-se para o `telas.py` na fase 5, junto do menu e da pausa. O `desenho.py`
ficou com o cenário (céu, chão, calçadas, estrada), o HUD e os
utilitários que as outras camadas usam: os de texto (`fonte`, `com_separador`,
`escrever_no_meio`, `escurecer`) e, desde a fase 8, a `desenhar_sombra` e a
`misturar_cores`. O `audio.py` da fase 6 nasceu exatamente onde o plano previa,
sem tocar em nenhum outro módulo além de sete linhas no `main.py` e seis no
`jogo.py`. Nada disso é definitivo: se um arquivo ficar pequeno demais ou grande
demais no caminho, ele é fundido ou dividido — e a mudança é anotada aqui.

---

## Balanceamento

A tabela abaixo é a proposta original, já confirmada jogando na fase 7 (que
mexeu em dois números; o resto sobreviveu). Todos ficam centralizados no
`config.py`, nenhum espalhado pelo código.

| Item | Valor inicial |
|---|---|
| Peso inicial | 45 kg |
| Peso de game over | 100 kg |
| Peso mínimo (trava) | 30 kg |
| Comida ruim | +4 kg |
| Comida boa | −2 kg e +50 pontos |
| Pontos por distância | 10 por segundo (no ritmo inicial) |
| Chance de comida ruim | 60% no começo → 85% no fim |
| Velocidade | 0,5 z por segundo, subindo ~2× ao longo de ~3 min |
| Intervalo entre spawns | 1,1 s no começo → 0,35 s no fim |
| Comidas por spawn | 1 até a metade da rampa → 2, em pistas diferentes |
| Tamanho da comida | 90 px de lado ao chegar no jogador |
| Janela / FPS | 960×720, 60 FPS, movimento por delta time |

A comida boa é mais rara e devolve menos peso do que a ruim adiciona: sem erro
nenhum o jogo ainda aperta, e com o tempo termina.

Toda a tabela já está valendo no `config.py`. Desde a fase 4, os números que
mudam com o tempo viram pares (largada e teto): `VELOCIDADE_INICIAL` 0,5 →
`VELOCIDADE_MAXIMA` 1,0; `INTERVALO_SPAWN_INICIAL` 1,1 s →
`INTERVALO_SPAWN_MINIMO` 0,35 s; `CHANCE_COMIDA_RUIM_INICIAL` 60% →
`CHANCE_COMIDA_RUIM_MAXIMA` 85%; e, desde a fase 7,
`COMIDAS_POR_SPAWN_INICIAL` 1 → `COMIDAS_POR_SPAWN_MAXIMA` 2 — todos alcançados
em `DURACAO_RAMPA = 180` s. A pontuação por distância virou `PONTOS_POR_Z = 20`,
que no ritmo inicial de 0,5 z/s dá exatamente os 10 pontos por segundo da tabela
— e paga mais quando a corrida acelera.

Os dois números que a fase 7 mexeu foram o intervalo mínimo de spawn (0,45 s →
0,35 s) e a rajada, que é nova. O resto da tabela sobreviveu ao teste de jogo
sem ajuste.

---

## Fases

Cada fase deixa o jogo **rodando** (`uv run main.py`), com os testes da
lógica alterada passando, e termina em pelo menos um commit em português.
Trabalho fase a fase: ao terminar uma, paro para você ver rodando antes da próxima.

### [x] Fase 0 — Ambiente
- `uv init`, `uv add pygame-ce`, `uv add --dev pytest`, `.gitignore` (`.venv`, `__pycache__`, `dist`, `build`, `recorde.json`).
- `config.py` com tela e cores; `main.py` abrindo uma janela preta 960×720 que fecha no ESC/X.
- **Pronto quando:** `uv run main.py` abre a janela e `uv run pytest` roda.
- **Feito:** pygame-ce 2.5.8 e pytest 9.1.1 no ambiente; `config.py` (janela + paleta),
  `main.py` (loop com `relogio.tick`, saída no ESC/X) e `testes/test_config.py`.

### [x] Fase 1 — Perspectiva e jogador
- `perspectiva.py` com a projeção descrita acima.
- `desenho.py` desenhando o horizonte, as 3 pistas convergindo e linhas de chão rolando (sensação de velocidade).
- `jogador.py`: pista central, troca com ← → e A/D, com uma interpolação curta entre pistas (movimento não teleporta).
- Testes: projeção (horizonte menor que base, pistas na ordem certa) e troca de pista (não passa das bordas).
- **Pronto quando:** dá para correr pela pista e trocar de faixa, sem obstáculos.
- **Feito:** `perspectiva.py` (`fator`, `deslocamento_da_pista`, `projetar`),
  `jogador.py` (pista lógica + `pista_visual` deslizando) e `desenho.py`
  (estrada, linhas de chão rolando e o personagem). `main.py` passou a
  medir delta time e a tratar ← → e A/D. 20 testes verdes em
  `testes/test_perspectiva.py` e `testes/test_jogador.py`.

### [x] Fase 2 — Comida na pista
- `comida.py`: tipos bons (maçã, brócolis, cenoura, uva) e ruins (hambúrguer, batata frita, refri, donut) como formas coloridas — verde = boa, vermelho = ruim.
- Spawn em `z = 1.0` numa pista sorteada, avanço em direção ao jogador, remoção ao passar.
- Testes: spawn respeita as pistas válidas, comida some depois de passar, proporção bom/ruim.
- **Pronto quando:** a comida vem do horizonte crescendo e atravessa o jogador sem efeito.
- **Feito:** `comida.py` com o cardápio (nome + forma de cada alimento), `Comida`
  (pista, tipo, `z`, `avancar`, `passou`), `sortear` e `GeradorDeComida`
  (cronômetro de spawn, avanço e descarte). `desenho.desenhar_comidas` pinta da
  mais distante para a mais próxima, com uma função por forma. `main.py`
  atualiza e desenha o gerador. 12 testes novos em `testes/test_comida.py`
  (32 no total).

### [x] Fase 3 — Colisão, peso e pontuação
- `jogo.py`: colisão (mesma pista + `z` dentro da zona do jogador), peso, pontuação por distância e bônus.
- HUD em `desenho.py`: `45 / 100 kg` e a pontuação, ambos em pt-br.
- Game over ao atingir 100 kg (por enquanto, volta ao início).
- Testes: peso sobe/desce e trava nos limites, pontuação acumula, colisão só na mesma pista.
- **Pronto quando:** o jogo tem risco e recompensa de verdade, do início ao game over.
- **Feito:** `jogo.Jogo` juntando corredor e gerador, com `peso`, `distancia`,
  `bonus`, a propriedade `pontuacao` e o `acabou`; colisão por zona em torno do
  jogador, com a comida saindo da estrada ao ser engolida. `desenho.py` ganhou o
  HUD (`62 / 100 kg` à esquerda, `Pontos: 1.240` à direita) e o véu de game over
  com a pontuação final. `main.py` virou só loop, teclado e desenho. 15 testes
  novos em `testes/test_jogo.py` (47 no total).

### [x] Fase 4 — Dificuldade progressiva
- Velocidade, frequência de spawn e chance de comida ruim crescendo com o tempo de partida.
- Testes: os três valores crescem de forma monotônica e param nos tetos definidos.
- **Pronto quando:** uma partida longa fica visivelmente mais difícil e termina sozinha.
- **Feito:** `dificuldade.py` com `progresso`, `velocidade`, `intervalo_de_spawn`
  e `chance_de_comida_ruim` — rampa linear do valor de largada até o teto em
  `DURACAO_RAMPA = 180` s. A `Jogo` passou a guardar `self.tempo` e a repassá-lo
  ao `GeradorDeComida`, que pergunta à dificuldade os três números do quadro;
  `Comida.avancar` recebe a velocidade e `sortear` recebe a chance de ruim. O
  chão rolante acelerou junto sem uma linha de mudança no `desenho.py`, porque
  já vinha da distância. 14 testes novos (`testes/test_dificuldade.py` mais os
  de fim de rampa em `test_comida.py` e `test_jogo.py`): 61 no total.

### [x] Fase 5 — Telas, pausa e recorde
- `telas.py`: menu inicial com título, instruções curtas (controles + regra do peso) e recorde; tela de game over com pontuação final e recorde; overlay de pausa (ESC/P).
- `recorde.py`: grava a maior pontuação num arquivo local ao lado do jogo.
- Testes: recorde só sobe, arquivo ausente/corrompido não quebra o jogo.
- **Pronto quando:** dá para abrir, jogar, pausar, perder e recomeçar sem sair do jogo.
- **Feito:** `telas.py` com os nomes dos estados (`MENU`, `JOGANDO`, `PAUSADO`,
  `FIM`, `SAINDO`) e o desenho de cada tela; `recorde.py` gravando a maior
  pontuação num JSON ao lado do jogo. O `main.py` virou o despacho: guarda o
  estado, `tratar_tecla(estado, partida, tecla)` devolve o próximo e só o
  `JOGANDO` faz o tempo andar. 19 testes novos (`test_recorde.py` e
  `test_telas.py`): 80 no total.

### [x] Fase 6 — Áudio sintetizado
- `audio.py` com numpy: som de coleta (boa), impacto (ruim), game over e confirmação do menu. Sem arquivos externos.
- Falha de áudio (máquina sem dispositivo) não pode derrubar o jogo.
- **Pronto quando:** cada evento tem seu som e o jogo continua rodando mesmo sem placa de som.
- **Feito:** `audio.py` com `envelope`, `onda`, `sintetizar` (numpy puro) e o par
  `iniciar`/`tocar` (a única parte que fala com o pygame). As quatro receitas são
  uma tabela de notas: coleta sobe (senoide 660→880 Hz), impacto desce grave
  (quadrada 180→110 Hz), game over desce mais fundo e mais devagar (quadrada
  330→220→165 Hz) e a confirmação é um toque só (senoide 520 Hz). A `Jogo` ganhou
  a lista `eventos`, esvaziada a cada quadro, e o `main` a drena tocando o que
  vier. numpy 2.5.2 no ambiente. 18 testes novos: 98 no total.

### [x] Fase 7 — Polimento e balanceamento
- Jogar, ajustar os números do `config.py`, revisar nomes e comentários, garantir a suíte de testes verde.
- Atualizar o `README.md` (o que é, como rodar, como jogar, como testar).
- **Feito:** a rajada de spawn (`comidas_por_spawn` na `dificuldade`, mais o
  `sortear_pistas` no `comida.py`) fechou o buraco que a fase 4 tinha anotado —
  com uma comida por vez, um jogador atento nunca perdia. O
  `INTERVALO_SPAWN_MINIMO` caiu de 0,45 s para 0,35 s. No polimento, o peso do
  HUD fica alaranjado a partir de `PESO_DE_ALERTA = 80` kg e os títulos do menu
  e do game over ganharam cor própria (`escrever_no_meio` passou a aceitar uma
  cor por linha). `README.md` reescrito em português: o que é, como rodar, como
  jogar, como testar e o mapa dos arquivos. 6 testes novos: 104 no total.

### [x] Fase 8 — Fundação Visual e Personagem
**Objetivo:** estabelecer a base do novo visual cartoon e substituir o
personagem-protótipo por um boneco de verdade visto de costas.
- [x] Definir uma paleta central de cores harmônicas (constantes no código) e
  substituir todas as cores puras atuais por ela.
- [x] Criar céu/fundo com gradiente vertical no lugar do preto chapado,
  mantendo a estrada em perspectiva já existente.
- [x] Substituir o personagem (círculo + retângulo) por um boneco cartoon visto
  de costas, montado em partes separadas (cabeça, tronco, dois braços, duas
  pernas) para permitir animação futura.
- [x] Adicionar sombra elíptica semi-transparente embaixo do personagem para dar
  profundidade.
- **Pronto quando:** o jogo roda com fundo em gradiente e um personagem de
  costas reconhecível como boneco, com sombra, sem quebrar a jogabilidade atual.
- **Feito:** a hora do dia escolhida foi **dia claro** — o céu vai de um azul
  suave no topo ao branco-azulado do horizonte, pintado linha a linha uma vez só
  e guardado numa `Surface` (é sempre o mesmo desenho, não vale refazê-lo 60
  vezes por segundo). Abaixo do horizonte entrou grama e, dos dois lados do
  asfalto, uma **calçada** medida em pistas (`LARGURA_CALCADA`), o que a faz
  convergir para o horizonte de graça, na mesma projeção da estrada — é o
  terreno em que os prédios da fase 11 vão subir. A paleta inteira foi
  redesenhada em tons macios (nenhuma cor pura, e há um teste garantindo isso),
  e o asfalto clareou para conversar com o céu de dia.
- **Desvios:** dois. **(1)** O corredor saiu do `desenho.py` para um
  `personagem.py` novo — ele já é a peça mais detalhada do jogo e a fase 9 vai
  engordá-lo com a animação; o `desenho.py` ficou com o cenário, o HUD, os
  utilitários de texto e a `desenhar_sombra`, que a fase 10 reaproveita nas
  comidas. O `main.py` mudou uma linha, chamando `personagem.desenhar`. **(2)**
  O céu claro deixaria o HUD branco ilegível, e trocar a cor do texto quebraria
  as telas, que são escritas por cima de um véu escuro. Em vez de duas cores de
  texto, o `_com_sombra` desenha o texto duas vezes (um sombreado escuro atrás,
  a cor por cima) — legível no céu e no véu, e de quebra combina com o cartoon.
  Vale para o HUD e para as telas.
- **O boneco** é montado em peças (pernas, tênis, tronco, shorts, braços com manga e
  cabeça com cabelo) e cada medida no `config.py` é uma **fração** da altura ou
  da largura do personagem: mudar `ALTURA_JOGADOR` redimensiona tudo junto, e a
  perspectiva só multiplica pela escala. As proporções foram afinadas olhando
  quadros salvos em PNG com `SDL_VIDEODRIVER=dummy`, sem abrir o jogo. 10 testes
  novos (paleta sem cor pura, frações do boneco, gradiente do céu e a
  `misturar_cores` em `test_desenho.py`): 114 no total.

### [x] Fase 9 — Animação e Game Feel do Personagem
**Objetivo:** dar vida ao personagem com animação de corrida e resposta tátil
aos controles.
- [x] Animar a corrida alternando pernas e braços em ciclo contínuo enquanto o
  jogo roda.
- [x] Adicionar squash & stretch leve no pulo e/ou na troca de faixa.
- [x] Adicionar leve inclinação/lean do personagem ao mudar de faixa para dar
  sensação de peso.
- [x] Sincronizar a velocidade da animação com a velocidade do jogo (correr mais
  rápido = animar mais rápido).
- **Pronto quando:** o personagem parece estar correndo de verdade e reage
  visualmente às ações do jogador.
- **Feito:** a animação inteira sai de uma **fase da passada** — um número de 0
  a 1 dizendo em que ponto do ciclo o corredor está — e de quatro contas puras
  sobre ela, no topo do `personagem.py`: `balanco` (seno, uma volta por passada)
  alterna os dois lados do corpo, `elevacao` (cosseno, duas voltas por passada,
  porque são duas pisadas) faz o corpo quicar e `esticamento` pendura o squash &
  stretch nessa mesma elevação — o boneco comprime quando o pé bate no chão e
  estica quando o quique o joga para cima, alargando na mesma medida em que
  encolhe. A perna que levanta é desenhada mais curta, com o tênis subindo
  junto; os braços balançam ao contrário da perna do mesmo lado, como se corre
  de verdade; e a sombra fica parada no chão, que é o que dá o contraste do
  quique.
- **A fase vem da distância percorrida**, não de um cronômetro próprio:
  `(distancia * PASSADAS_POR_Z) % 1.0`. É o mesmo truque das linhas do asfalto
  (`desenho._profundidades_das_linhas`), e ele resolve de graça o quarto item da
  fase: quando a rampa de dificuldade acelera a corrida, a passada acelera
  junto, sem uma linha de código a mais. De quebra, nenhum estado novo — nada de
  acumular `dt` — e a animação congela sozinha na pausa e no game over.
- **A inclinação também não é conta de tempo:** é `pista - pista_visual`, o que
  falta da deslizada, travado entre -1 e 1 numa propriedade do `Jogador`. Vale
  quase 1 no começo da troca e se desfaz sozinha quando o boneco chega na faixa.
  No desenho ela vira um desvio horizontal do tronco, dos braços e da cabeça,
  com as pernas ficando no lugar: o pivô na cintura lê como *lean*.
- **Desvios:** nenhum. O `personagem.desenhar` passou a receber a distância
  (uma linha no `main.py`) e o `config.py` ganhou seis constantes no bloco do
  Jogador — cinco delas frações, já cobertas pelo teste que varre os
  `JOGADOR_*`. 15 testes novos (`testes/test_personagem.py`, com o ciclo, mais
  os da inclinação em `test_jogador.py`): 129 no total. As poses foram
  conferidas em PNG com `SDL_VIDEODRIVER=dummy`, sem abrir o jogo.

### [x] Fase 10 — Comidas Boas e Ruins
**Objetivo:** substituir as comidas-protótipo (formas geométricas chapadas:
círculo, triângulo, losango, quadrado, garrafa e rosquinha) por comidas
desenhadas em código, com leitura visual clara.
- [x] Desenhar em código um conjunto de comidas BOAS (ex.: maçã, banana,
  brócolis) com identidade visual clara.
- [x] Desenhar em código um conjunto de comidas RUINS (ex.: hambúrguer, donut,
  refrigerante) visualmente distintas das boas à primeira vista.
- [x] Fazer cada comida respeitar a perspectiva: surgir pequena no horizonte e
  crescer ao se aproximar da câmera.
- [x] Adicionar sombra elíptica embaixo de cada comida, coerente com a do
  personagem — a `desenho.desenhar_sombra` da fase 8 já serve, é só chamá-la.
- [x] Garantir que a lógica de spawn atual continue funcionando com os novos
  desenhos.
- **Pronto quando:** dá para distinguir comida boa de ruim num relance, e elas se
  aproximam com perspectiva convincente.
- **Feito:** os oito alimentos do cardápio agora são desenhados um a um, cada um
  **na cor de verdade**: a maçã é verde com cabinho e folha, o brócolis é um
  talo claro segurando três bolas verdes, a cenoura é um triângulo laranja com a
  rama espetada, a uva é um cacho roxo em pirâmide, o hambúrguer é uma
  pilha (domo de pão, alface, carne e o pão de baixo), a batata frita são
  palitos numa caixinha vermelha, o refrigerante é um copo de fast food com
  tampa e canudo, e o donut é um anel com glacê e furo de verdade. Cada um é
  montado dentro de uma **caixa quadrada apoiada no asfalto**, cujo lado já vem
  multiplicado pela escala da perspectiva — por isso nenhuma medida do desenho
  precisa saber a que distância a comida está, e a sombra elíptica da fase 8
  entrou sem uma linha de mudança.
- **A auréola resolveu a tensão entre cor real e regra travada.** O `CLAUDE.md`
  trava "verde = boa, vermelho = ruim", mas comida de verdade tem cor própria — e
  a maçã, que é saudável, é vermelha. A saída foi separar as duas informações:
  o alimento fica na cor dele e ganha atrás um **disco translúcido** verde ou
  vermelho. No horizonte, onde a comida tem menos de dez pixels e só a cor
  dominante chega aos olhos, é a auréola que se vê; de perto ela vira moldura e
  o desenho do alimento fala por si. As `COR_COMIDA_BOA` e `COR_COMIDA_RUIM`
  passaram a ser exatamente as cores dessa auréola, em tons mais claros, para
  contrastarem com o asfalto escuro por trás e com o alimento por cima.
- **O cardápio mudou uma vez, depois da fase.** A fase 10 fechou com os mesmos
  oito alimentos de sempre, mas a **carne grelhada** — elipse marrom com três
  riscos de grelha — era a leitura mais fraca do jogo: no horizonte virava uma
  mancha marrom, e marrom já era a cor do pão do hambúrguer e da massa do
  donut. Em 26/08/2026 ela deu lugar a um **cacho de uvas**, escolhido pela
  cor: roxo é o único tom vivo que a paleta ainda não usava, então nenhum
  outro alimento disputa com ele lá no fundo. O custo foi o cardápio bom
  ficar sem proteína — duas frutas e dois vegetais —, aceito porque o que o
  jogo cobra do jogador é reconhecer *boa ou ruim* num relance, não montar um
  prato equilibrado. O cacho é uma pirâmide de seis bagas (uma, duas, três),
  cada uma um disco escuro com um miolo claro por dentro: o anel que sobra faz
  as vezes de contorno e separa uma baga da vizinha, já que as filas se
  encostam de propósito. Três testes novos (137 no total) guardam o desenho:
  o cacho cabe na caixa, as bagas se encostam e o miolo deixa contorno.
- **A auréola foi refeita depois da fase, porque não estava sendo lida.** Jogando,
  ficava confuso saber de que desviar. A causa apareceu na conta: com
  `AUREOLA_TAMANHO = 1.15`, o disco sobrava só 7,5% do lado da comida para cada
  lado, e como tudo era multiplicado pela escala da perspectiva isso dava **meio
  pixel de anel no horizonte** — a auréola só virava moldura de verdade nos
  últimos 25% da aproximação, quando já não dá tempo de trocar de pista. Pior: a
  comida passa mais de 80% da travessia com menos de 30 px, então o jogador
  *precisa* decidir enquanto ela é pequena, que era justamente onde o aviso não
  existia. Em 26/08/2026 entraram quatro mudanças:
  - **A marca ganhou forma além de cor:** círculo liso para a comida boa,
    **estrela espetada** para a ruim. É a redundância que faz o aviso funcionar
    para quem não distingue verde de vermelho (cerca de 8% dos homens, e
    vermelho × verde é o eixo mais comum), e a silhueta é reconhecida antes de o
    olho registrar o tom. A forma vem do tipo, então alimento novo não escolhe.
  - **A auréola virou disco de duas camadas**, exatamente como as bagas do cacho
    de uva: a figura inteira na cor da borda e a mesma figura menor por cima, no
    tom do miolo. O que sobra entre as duas é um anel opaco que recorta a marca
    contra o asfalto. Também cresceu (1,15 → 1,45) e ficou mais firme (opacidade
    105 → 170 no miolo, 240 no anel).
  - **Dois pisos em pixels**, `AUREOLA_BORDA_MINIMA` e `TAMANHO_COMIDA_MINIMO`.
    São a única exceção consciente à regra das frações no jogo inteiro, e a razão
    é a de sempre com marcador de perigo: como fração, ele arredonda para zero
    no fundo da estrada. Com o piso de 12 px a comida no horizonte passou de 9
    para 12 px e a marca, de 10 para 17. O preço é o tamanho congelar enquanto
    `z > 0,72` — os 28% mais distantes da estrada, onde a comida mal aparece.
    Foram testados 14 px antes: aí o congelamento subia para 40% e dava a
    impressão de que a comida não estava se aproximando.
  - **A maçã ficou verde.** Era o único alimento cuja cor mentia sobre o próprio
    tipo: `(198, 74, 72)` é praticamente a `COR_COMIDA_RUIM` e a cor da
    embalagem do refri e da batata, então lá no fundo uma maçã era uma mancha
    vermelha e o jogador desviava do que devia comer — erro pior do que não
    conseguir ler. Maçã verde é uma cor real, então a decisão da fase 10
    ("alimento na cor de verdade") continua valendo inteira.

  De quebra, o menu inicial ganhou a legenda "Círculo verde: coma e emagreça" /
  "Estrela vermelha: desvie ou engorda", cada linha na cor do próprio marcador —
  usando a cor-por-linha que o `escrever_no_meio` já tinha desde a fase 7.
  9 testes novos (146 no total): 5 no `test_config.py` guardando os invariantes
  novos (o anel não engole o miolo, o piso em pixels não é zero, a estrela tem
  vale de verdade, o piso da comida é menor que o tamanho de chegada e a maçã é
  esverdeada) e um `test_desenho_comida.py` novo com 4 sobre a geometria da
  estrela — `pontos_da_estrela` nasceu **pública** pelo mesmo motivo que as
  contas da passada no `personagem.py`: é matemática pura num módulo gráfico, e
  o `CLAUDE.md` manda testá-la.
- **Desvios:** dois. **(1)** As comidas saíram do `desenho.py` para um
  `desenho_comida.py` novo, pelo mesmo motivo que o corredor saiu na fase 8 —
  oito alimentos montados peça a peça pesam mais do que o cenário inteiro. O
  `desenho.py` ficou só com cenário, HUD e utilitários, e perdeu o `import
  comida`; o `main.py` mudou uma linha. **(2)** A `Comida` perdeu um campo: com
  um desenho próprio por alimento, o `nome` e a `forma` viraram a mesma coisa, e
  as seis formas geométricas compartilhadas deram lugar a oito constantes de
  alimento no `comida.py`.
- **Testes:** 5 novos (134 no total). O que mais vale é o que cobra que **todo
  alimento do cardápio tenha um desenho registrado** — sem ele, um alimento novo
  derrubaria o jogo com `KeyError` no meio de uma partida, e nenhum outro teste
  pegaria isso. Os outros guardam invariantes do desenho que não tocam pixel: a
  pilha do hambúrguer cabe na caixa dele, o anel do donut é mais fino que o raio
  (senão não sobra furo) e a auréola sobra para fora da comida (senão não é
  moldura). As poses foram conferidas em PNG com `SDL_VIDEODRIVER=dummy`, sem
  abrir o jogo, e uma partida inteira de 200 s rodou sem janela para garantir
  que os oito alimentos são desenhados de verdade.

### [ ] Fase 11 — Cenário de Rua da Cidade
**Objetivo:** preencher as laterais transformando as faixas de grama vazias numa
rua de cidade em perspectiva.
- [ ] Adicionar prédios nas laterais que surgem pequenos no horizonte e crescem
  ao se aproximar, respeitando a perspectiva da estrada.
- [x] Adicionar calçada entre a estrada e os prédios. *(adiantado na fase 8: ela
  já ladeia o asfalto, medida em pistas, e é o terreno em que os prédios sobem.)*
- [ ] Adicionar elementos de rua recorrentes (ex.: postes, faixas, árvores) que
  passam junto com o movimento.
- [ ] Aplicar efeito de parallax de profundidade (elementos ao fundo se movem
  mais devagar que os da frente).
- [ ] Variar levemente cores/alturas dos prédios para não ficar repetitivo — a
  `desenho.misturar_cores` da fase 8 serve para isso.
- **Pronto quando:** as laterais parecem uma rua de cidade com sensação de
  velocidade e profundidade, sem faixas vazias.

### [ ] Fase 12 — Juice e Polimento Final
**Objetivo:** adicionar o feedback visual que separa protótipo de jogo
finalizado.
- [ ] Adicionar partículas ao coletar comida boa.
- [ ] Adicionar flash/feedback visual (ex.: tela avermelhada) ao pegar comida
  ruim.
- [ ] Adicionar leve screen shake em impactos/coletas importantes.
- [ ] Adicionar transições suaves (fade in/out) entre telas.
- [ ] Revisar HUD ("kg" e "Pontos") para combinar com o novo estilo cartoon.
- **Pronto quando:** o jogo tem resposta tátil e visual em todas as ações
  principais e transições limpas entre telas.
