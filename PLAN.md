# Plano — Food Runner

Plano de execução do jogo. **Documento vivo:** cada fase concluída é marcada aqui
(`[x]`), com o resumo do que ficou pronto e os desvios do plano anotados na
própria fase. As decisões travadas do projeto ficam no `CLAUDE.md`.

Status geral: **Fase 8 — redefinição visual** (Fases 0 a 7 concluídas:
ambiente uv, estrada em perspectiva rolando, jogador trocando de pista, comida
vindo do horizonte, a partida completa — peso, pontuação, HUD e game over —, a
rampa de dificuldade que aperta a corrida ao longo de 3 minutos, o ciclo fechado
de menu, pausa, game over e recorde em arquivo, os quatro sons sintetizados
com numpy e o balanceamento fechado — a corrida agora termina até para quem joga
bem —, com 104 testes verdes e o `README.md` no ar). O jogo está completo em
regras; o que vem pelas fases 8 a 12 é a redefinição visual descrita na
**Direção Visual** do `CLAUDE.md`: cartoon, personagem de costas, comidas
desenhadas em código, rua de cidade nas laterais e juice.

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

---

## Estrutura de arquivos

`[x]` = já existe no repositório. Desde a fase 6 todos os módulos previstos
existem, e a fase 7 mexeu em cinco deles sem criar nenhum. As fases 8 a 12
mexem sobretudo no `desenho.py` e no `config.py` (a paleta nova); se o desenho
do personagem, das comidas ou do cenário deixar o `desenho.py` grande demais,
cada um vira um arquivo seu — e a mudança é anotada aqui.

```
[x] main.py        # ponto de entrada: loop, eventos, troca entre menu/jogo/pausa/game over
[x] config.py      # todas as constantes: tela, cores, pistas, perspectiva, balanceamento
[x] perspectiva.py # projeta (pista, z) -> (x, y, escala). Lógica pura, testável
[x] jogador.py     # pista atual e troca de pista
[x] desenho.py     # desenha cenário, pistas, jogador, comidas e HUD
[x] testes/        # test_config, test_perspectiva, test_jogador, test_comida,
                   # test_jogo, test_dificuldade, test_recorde, test_telas,
                   # test_audio
[x] comida.py      # tipos de comida, spawn e avanço em z
[x] jogo.py        # estado da partida: peso, pontuação, dificuldade, colisões
[x] dificuldade.py # rampa: velocidade, intervalo de spawn e chance de comida ruim
[x] telas.py       # menu inicial (com instruções), pausa e game over
[x] audio.py       # síntese dos sons com numpy
[x] recorde.py     # lê e grava a maior pontuação em arquivo local
```

Até aqui a estrutura real bateu com a planejada, sem fusões nem divisões. Os
desvios foram dois: o ponto de entrada, que virou `main.py`, e o
`dificuldade.py`, arquivo novo que a fase 4 trouxe — o plano imaginava a rampa
dentro do `jogo.py`, mas ela é lógica pura sobre o tempo, do mesmo naipe da
`perspectiva.py`, e sozinha num arquivo dá para ler a curva inteira de uma vez.
O aviso de game over da fase 3 nasceu dentro do `desenho.py` e, como previsto,
mudou-se para o `telas.py` na fase 5, junto do menu e da pausa; o `desenho.py`
ficou com o cenário, o HUD e os utilitários de texto que as duas camadas usam
(`fonte`, `com_separador`, `escrever_no_meio` e `escurecer`). O `audio.py` da
fase 6 nasceu exatamente onde o plano previa, sem tocar em nenhum outro módulo
além de sete linhas no `main.py` e seis no `jogo.py`. Nada disso é
definitivo: se um arquivo ficar pequeno demais ou grande demais no caminho, ele
é fundido ou dividido — e a mudança é anotada aqui.

---

## Balanceamento inicial proposto

Números de partida para `config.py`; serão ajustados jogando (a fase 7 é para
isso). Ficam todos centralizados, nenhum espalhado pelo código.

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
- `comida.py`: tipos bons (maçã, brócolis, cenoura, carne grelhada) e ruins (hambúrguer, batata frita, refri, donut) como formas coloridas — verde = boa, vermelho = ruim.
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

### [ ] Fase 8 — Fundação Visual e Personagem
**Objetivo:** estabelecer a base do novo visual cartoon e substituir o
personagem-protótipo por um boneco de verdade visto de costas.
- [ ] Definir uma paleta central de cores harmônicas (constantes no código) e
  substituir todas as cores puras atuais por ela.
- [ ] Criar céu/fundo com gradiente vertical no lugar do preto chapado,
  mantendo a estrada em perspectiva já existente.
- [ ] Substituir o personagem (círculo + retângulo) por um boneco cartoon visto
  de costas, montado em partes separadas (cabeça, tronco, dois braços, duas
  pernas) para permitir animação futura.
- [ ] Adicionar sombra elíptica semi-transparente embaixo do personagem para dar
  profundidade.
- **Pronto quando:** o jogo roda com fundo em gradiente e um personagem de
  costas reconhecível como boneco, com sombra, sem quebrar a jogabilidade atual.

### [ ] Fase 9 — Animação e Game Feel do Personagem
**Objetivo:** dar vida ao personagem com animação de corrida e resposta tátil
aos controles.
- [ ] Animar a corrida alternando pernas e braços em ciclo contínuo enquanto o
  jogo roda.
- [ ] Adicionar squash & stretch leve no pulo e/ou na troca de faixa.
- [ ] Adicionar leve inclinação/lean do personagem ao mudar de faixa para dar
  sensação de peso.
- [ ] Sincronizar a velocidade da animação com a velocidade do jogo (correr mais
  rápido = animar mais rápido).
- **Pronto quando:** o personagem parece estar correndo de verdade e reage
  visualmente às ações do jogador.

### [ ] Fase 10 — Comidas Boas e Ruins
**Objetivo:** substituir as comidas-protótipo (losango/triângulo) por sprites de
comida desenhados em código, com leitura visual clara.
- [ ] Desenhar em código um conjunto de comidas BOAS (ex.: maçã, banana,
  brócolis) com identidade visual clara.
- [ ] Desenhar em código um conjunto de comidas RUINS (ex.: hambúrguer, donut,
  refrigerante) visualmente distintas das boas à primeira vista.
- [ ] Fazer cada comida respeitar a perspectiva: surgir pequena no horizonte e
  crescer ao se aproximar da câmera.
- [ ] Adicionar sombra elíptica embaixo de cada comida, coerente com a do
  personagem.
- [ ] Garantir que a lógica de spawn atual continue funcionando com os novos
  sprites.
- **Pronto quando:** dá para distinguir comida boa de ruim num relance, e elas se
  aproximam com perspectiva convincente.

### [ ] Fase 11 — Cenário de Rua da Cidade
**Objetivo:** preencher as laterais vazias transformando o vazio preto numa rua
de cidade em perspectiva.
- [ ] Adicionar prédios nas laterais que surgem pequenos no horizonte e crescem
  ao se aproximar, respeitando a perspectiva da estrada.
- [ ] Adicionar calçada entre a estrada e os prédios.
- [ ] Adicionar elementos de rua recorrentes (ex.: postes, faixas, árvores) que
  passam junto com o movimento.
- [ ] Aplicar efeito de parallax de profundidade (elementos ao fundo se movem
  mais devagar que os da frente).
- [ ] Variar levemente cores/alturas dos prédios para não ficar repetitivo.
- **Pronto quando:** as laterais parecem uma rua de cidade com sensação de
  velocidade e profundidade, sem preto vazio.

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
