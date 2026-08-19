# Plano — Food Runner

Plano de execução do jogo. **Documento vivo:** cada fase concluída é marcada aqui
(`[x]`) e as decisões que surgirem no caminho são registradas na seção "Decisões
tomadas durante a execução". As decisões travadas do projeto ficam no `CLAUDE.md`.

Status geral: **Fase 8 — executável** (Fases 0 a 7 concluídas:
ambiente uv, estrada em perspectiva rolando, jogador trocando de pista, comida
vindo do horizonte, a partida completa — peso, pontuação, HUD e game over —, a
rampa de dificuldade que aperta a corrida ao longo de 3 minutos, o ciclo fechado
de menu, pausa, game over e recorde em arquivo, os quatro sons sintetizados
com numpy e o balanceamento fechado — a corrida agora termina até para quem joga
bem —, com 104 testes verdes e o `README.md` no ar).

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
existem; o que falta na fase 8 é empacotamento, não código novo. A fase 7 mexeu
em cinco módulos e não criou nenhum.

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

### [ ] Fase 8 — Executável
- `uv add --dev pyinstaller` e build (flags a confirmar antes de rodar).
- Testar o `.exe` gerado numa pasta limpa, inclusive o arquivo de recorde.

---

## Decisões tomadas durante a execução

*(preenchido conforme o projeto anda — o que foi decidido e por quê)*

- **2026-08-18** — Perspectiva **pseudo-3D** escolhida no lugar do top-down 2D: fica mais perto da referência (Subway Surfers). Custo aceito: a projeção `(pista, z) → tela` fica isolada em `perspectiva.py` para a lógica seguir testável.
- **2026-08-18** — Extras aprovados além do escopo original: recorde salvo em arquivo, pausa (ESC/P) e instruções no menu.
- **2026-08-18** — `uv` 0.12.5 instalado via winget (não existia na máquina).
- **2026-08-18** — Layout **achatado na raiz** em vez do `src/food_runner/` que o `uv init` criou: o alvo é um executável PyInstaller, não um pacote publicável, então `[project.scripts]` e `[build-system]` saíram do `pyproject.toml` e os módulos ficam na raiz (`uv run main.py`, como o plano previa).
- **2026-08-18** — Python **3.12** (`.python-version`) em vez do 3.14 do sistema: é a versão com suporte mais rodado em pygame-ce e PyInstaller, e a fase 8 depende dos dois.
- **2026-08-18** — pytest configurado no `pyproject.toml` (`testpaths = ["testes"]`, `pythonpath = ["."]`) para os testes importarem os módulos da raiz sem gambiarra de `sys.path`.
- **2026-08-19** — O ponto de entrada passou de `principal.py` para **`main.py`** (pedido do autor). É a única quebra da regra de nomes em pt-br: `main.py` é a convenção universal de projetos Python e é o primeiro arquivo que quem abre o repositório procura. Roda com `uv run main.py`; o build da fase 8 aponta para ele.
- **2026-08-19** — Constantes da perspectiva fechadas: `HORIZONTE_Y = 250`, `BASE_Y = 640` e `PROFUNDIDADE = 9.0` (com 9.0 o objeto no horizonte fica com 1/10 do tamanho). Pistas a 250 px de distância na base, o que deixa a estrada inteira dentro dos 960 px — há um teste garantindo isso.
- **2026-08-19** — A estrada é desenhada até `Z_FUNDO_TELA = -0.03`, um pouco **além** do plano do jogador, para o asfalto sair pelo rodapé em vez de terminar nos pés dele. Como isso exige `z` negativo, `perspectiva.fator` aceita profundidade negativa (objeto passando pela câmera fica maior que 1.0) e trava em `Z_MINIMO = -0.05`, longe do ponto em que a divisão explodiria.
- **2026-08-19** — Troca de pista com **duas posições**: `pista` (inteira, muda na hora, é a que vale para a colisão da fase 3) e `pista_visual` (quebrada, corre atrás em `DURACAO_TROCA_PISTA = 0,12 s`). Assim o desenho desliza sem que a lógica fique dependendo da animação.
- **2026-08-19** — Cada alimento tem sua **forma própria** (círculo, triângulo, losango, quadrado, garrafa e rosquinha) — a cor continua sendo o único sinal de bom/ruim. Assim os 8 nomes do cardápio têm serventia e o jogador diferencia os itens de longe, sem custo nenhum de complexidade: é uma função de desenho por forma, trocável por sprite depois.
- **2026-08-19** — `VELOCIDADE_CHAO` virou **`VELOCIDADE_JOGO`**, usada pelas linhas de chão e pela comida. Em ritmos diferentes a comida pareceria flutuar sobre o asfalto; de quebra, a fase 4 tem um único número para acelerar.
- **2026-08-19** — A comida é descartada em `Z_SUMICO = Z_MINIMO`: nesse ponto ela já saiu pelo rodapé (há um teste conferindo) e é onde a projeção satura, então não faz sentido segui-la além disso.
- **2026-08-19** — O `GeradorDeComida` recebe um `random.Random` opcional: no jogo ele usa o sorteio normal e nos testes recebe uma semente fixa, sem precisar de mock.
- **2026-08-19** — Desenho em uma passada só, do fundo para a frente, e o jogador por último. No instante em que a comida cruza o plano dele ela fica escondida atrás do personagem — invisível na prática, e na fase 3 esse é justamente o momento em que ela some ao ser coletada.
- **2026-08-19** — As linhas de chão são calculadas a partir de um único número (`_profundidades_das_linhas`), sem estado guardado: o cenário não precisa de objeto próprio. Esse número era o tempo de jogo e virou a distância percorrida na fase 3 — ver a última decisão desta lista.
- **2026-08-19** — Colisão por **zona em torno do jogador**: acerta quem estiver na mesma pista com `abs(z) <= ZONA_COLISAO = 0,04`. Foi preferida a "cruzou o plano do jogador" porque não deixa a comida já ultrapassada continuar valendo se o jogador entrar na pista dela depois, e porque a janela de 0,08 em z aguenta a aceleração da fase 4 sem a comida atravessar entre dois quadros. A zona termina em `z = -0,04`, ainda acima do `Z_SUMICO = -0,05`, então nada é descartado antes de ser conferido — há teste para isso.
- **2026-08-19** — Pontuação contada **por distância em z** (`PONTOS_POR_Z = 20`), não por tempo: no ritmo inicial dá os 10 pontos por segundo do plano e, quando a fase 4 acelerar, sobreviver ao trecho rápido passa a pagar mais.
- **2026-08-19** — O game over **congela a partida e espera Espaço/Enter**, em vez de reiniciar na hora como o plano dizia. Sem isso não dá para ver que perdeu nem qual foi a pontuação. São poucas linhas em `desenho.desenhar_game_over`, que a fase 5 leva para o `telas.py`.
- **2026-08-19** — O peso é travado nas duas pontas (`PESO_MINIMO = 30`, `PESO_GAME_OVER = 100`), então o HUD nunca mostra número fora da faixa e o fim de partida acontece com `100 / 100 kg` na tela.
- **2026-08-19** — A dificuldade cresce com o **tempo de partida**, não com a distância percorrida: a distância já acelera junto com a velocidade, então usá-la faria a rampa se realimentar e fechar antes da conta. Com o relógio, os 180 s de `DURACAO_RAMPA` são exatamente 180 s para qualquer jogador, o que é mais fácil de balancear na fase 7 e de testar (basta perguntar o valor de um instante).
- **2026-08-19** — Rampa **linear** entre a largada e o teto (`inicial + (final - inicial) * progresso`), com `progresso` travado em 1,0 daí em diante. Uma curva (progresso²) foi considerada e descartada: linear é o que se explica numa linha e já dá a diferença visível que a fase pedia.
- **2026-08-19** — Os três números que a rampa mexe viraram **pares no `config.py`** — `VELOCIDADE_INICIAL`/`VELOCIDADE_MAXIMA`, `INTERVALO_SPAWN_INICIAL`/`INTERVALO_SPAWN_MINIMO`, `CHANCE_COMIDA_RUIM_INICIAL`/`CHANCE_COMIDA_RUIM_MAXIMA`. O antigo `VELOCIDADE_JOGO` (que já tinha sido rebatizado na fase 2) virou `VELOCIDADE_INICIAL`: com dois valores por número, o nome tem de dizer qual dos dois é.
- **2026-08-19** — Quem pergunta à `dificuldade` é o **`GeradorDeComida`**, que recebe o tempo de partida em `atualizar(dt, tempo)`; a `Jogo` só repassa o cronômetro. A alternativa era a `Jogo` injetar os três valores prontos, o que engordaria a assinatura para quatro parâmetros sem tirar dependência de ninguém. Nos testes o tempo é um argumento comum: dá para congelar a largada ou o fim da rampa sem mock.
- **2026-08-19** — Simulando a partida sem janela (jogador parado, 30 sementes), a morte vem entre 47 s e 106 s, mediana de 77 s — a rampa aperta de verdade. No outro extremo, um "jogador ideal" simulado (lê a estrada inteira e troca de pista todo quadro) sobrevive 30 min sem perder: no teto de 0,45 s por spawn quase nunca as três pistas ficam bloqueadas ao mesmo tempo. Nenhum humano joga assim, mas fica anotado para a **fase 7**: se quisermos que até o jogo perfeito termine, o caminho é spawn mínimo mais curto ou soltar duas comidas de uma vez no fim da rampa. **Resolvido na fase 7**, pelos dois caminhos: a rajada de duas comidas e o spawn mínimo em 0,35 s.
- **2026-08-19** — O chão rolante passou a ser calculado a partir da **distância percorrida** em vez de `tempo * VELOCIDADE_JOGO`. É o mesmo valor enquanto a velocidade é constante, mas na fase 4 o asfalto acompanha a aceleração sozinho — e a `Jogo` não precisa guardar um cronômetro só para o desenho.
- **2026-08-19** — O jogo virou uma **máquina de estados de cinco nomes** no `main.py` (`MENU`, `JOGANDO`, `PAUSADO`, `FIM`, `SAINDO`), com `tratar_tecla(estado, partida, tecla)` devolvendo o estado seguinte. A alternativa era uma classe por tela com `atualizar`/`desenhar`: é o padrão de livro, mas para quatro telas que só desenham texto vira cerimônia. Como a função é pura em `(estado, tecla)`, a tabela inteira de controles ficou testável sem abrir janela — é o que o `testes/test_telas.py` faz.
- **2026-08-19** — Teclas por tela: o **ESC é contextual** (na partida pausa, no menu fecha o jogo, na pausa volta a jogar) e o **M volta ao menu** a partir da pausa e do game over. O ESC continua sendo a tecla de sair, como era antes da fase 5, mas só onde sair faz sentido — ninguém mais fecha o jogo sem querer no meio da corrida. Cada tela lista as próprias teclas na tela, então não é preciso decorar nada.
- **2026-08-19** — No game over, o **Espaço recomeça na hora** (mantendo o que a fase 3 já fazia) em vez de passar pelo menu: é o ritmo de endless runner, perdeu e tenta outra vez. Quem quiser o menu aperta M.
- **2026-08-19** — Os utilitários de texto do `desenho.py` (`fonte`, `com_separador`, `escrever_no_meio`) e o véu (`escurecer`) **viraram públicos**, e o `telas.py` os reaproveita. A dependência aponta numa direção só, `telas` → `desenho`, para o HUD continuar no lado que sabe de pixels sem inverter a seta.
- **2026-08-19** — O recorde mora num **JSON de uma chave** (`recorde.json`) ao lado do jogo: no script, a pasta do `main.py`; empacotado (`sys.frozen`), a pasta do `.exe` — sem isso o build `--onefile` da fase 8 gravaria numa pasta temporária e perderia o recorde a cada partida. Arquivo ausente, corrompido, com número negativo ou sem permissão de escrita vale zero e não derruba o jogo; há teste para cada um desses casos.
- **2026-08-19** — `ler` e `salvar` recebem um **`caminho` opcional**, mesmo truque do `aleatorio=None` do `GeradorDeComida`: no jogo fica em `None` (o arquivo de verdade) e nos testes recebe o `tmp_path` do pytest, sem mock e sem escrever na máquina de quem roda a suíte. Quem grava é só o `main.py`, no único instante em que a partida acaba.
- **2026-08-19** — A fonte padrão do pygame **não tem os glifos das setas**: `←` e `→` saem como quadradinhos vazios. O menu escreve "Setas ou A e D trocam de pista" — os controles continuam os mesmos, só o texto mudou. Se algum dia entrar uma fonte própria no projeto, dá para voltar às setas.
- **2026-08-19** — O menu desenha a **estrada parada atrás de um véu mais leve** (`OPACIDADE_VEU_MENU = 130`, contra os 200 da pausa e do game over): custa uma linha, já que o cenário é uma função sem estado, e o menu deixa de ser um retângulo preto com texto.

- **2026-08-19** — Os nomes dos quatro sons (`SOM_COLETA`, `SOM_IMPACTO`,
  `SOM_FIM`, `SOM_CONFIRMACAO`) moram no **`config.py`**, não no `audio.py`. A
  partida precisa dizer o que aconteceu e o áudio precisa saber o que tocar; se
  o vocabulário morasse no `audio.py`, o `jogo.py` — lógica pura — teria de
  importar pygame e numpy só para nomear um evento. O `config` já é o módulo que
  todo mundo importa e que não importa ninguém, então é o lugar natural.
- **2026-08-19** — A partida avisa por uma **lista `eventos`, esvaziada no início
  de cada `atualizar`**, e quem toca é o `main`. A alternativa era o `jogo.py`
  chamar o áudio direto, o que quebraria a regra de a lógica não conhecer pixel
  nem placa de som e obrigaria os testes a lidar com o mixer. Do jeito que ficou,
  `test_jogo.py` confere os avisos com um `assert` numa lista de strings.
- **2026-08-19** — O som de confirmação toca em **toda troca de tela**, não só ao
  começar a partida: são três linhas no `main` (`tratar_tecla` devolveu um estado
  diferente → toca) e cobre começar, pausar, despausar, voltar ao menu e
  recomeçar de uma vez.
- **2026-08-19** — Timbre **misto**: senoide na coleta e na confirmação, onda
  quadrada no impacto e no game over. Tudo em quadrada ficaria agressivo demais
  no fim da rampa, quando a comida ruim aparece a cada 0,45 s; tudo em senoide
  tiraria a punição do erro.
- **2026-08-19** — Toda nota passa por um **envelope** (sobe em 5% da duração e
  desce até zero). Sem ele a onda começa e termina cortada no meio e o
  alto-falante estala — há teste conferindo que a nota começa e acaba no silêncio.
- **2026-08-19** — O mixer é aberto com **`channels=1, allowedchanges=0`**. Sem o
  `allowedchanges=0` o Windows abre em estéreo mesmo tendo sido pedido mono, e aí
  o `make_sound` recusa o array de uma dimensão e o jogo fica mudo sem avisar —
  foi o que aconteceu no primeiro teste da fase. Com a trava o SDL aceita o
  formato pedido e converte por conta própria.
- **2026-08-19** — Sem tecla de mudo: a fase não pede e o jogo é curto. Se fizer
  falta, entra na fase 7 em poucas linhas.
- **2026-08-19** — A partida passou a soltar **duas comidas por spawn** a partir
  da metade da rampa (`COMIDAS_POR_SPAWN_INICIAL` 1 →
  `COMIDAS_POR_SPAWN_MAXIMA` 2, arredondando a mesma reta das outras três). Era
  o buraco anotado na fase 4: simulando bots que leem a estrada inteira e reagem
  em 0,20 s ou 0,35 s, **nenhum morria** em 6 minutos de jogo. Com uma comida
  por vez a conta não fecha — a janela de colisão tem 0,08 em z e o spawn mais
  apertado é de 0,35 s, então as três pistas nunca ficam bloqueadas juntas.
  Encurtar mais o intervalo não resolveria; soltar mais de uma comida resolve.
  Depois da mudança — já com o spawn mínimo em 0,35 s, que é o valor que ficou
  — os mesmos bots morrem com mediana entre 224 s e 262 s, e o jogador parado
  continua morrendo por volta dos 80 s.
- **2026-08-19** — A rajada é de **duas comidas, nunca três**: com três, todo
  mundo morria junto por volta dos 150 s, no instante em que a conta arredonda —
  morte por falta de saída, não por erro. Com duas sempre sobra pista livre, e a
  regra `COMIDAS_POR_SPAWN_MAXIMA < QTD_PISTAS` virou teste para ninguém subir
  esse número sem querer. As pistas da rajada saem de um `sample` (sem
  reposição): duas comidas na mesma pista ficariam uma escondida atrás da outra.
- **2026-08-19** — `sortear` passou a **receber a pista** em vez de sorteá-la
  por dentro, e quem sorteia as pistas é o `sortear_pistas`. Sem isso não dava
  para garantir pistas diferentes numa rajada — o sorteio por comida repetiria
  faixa de vez em quando.
- **2026-08-19** — `INTERVALO_SPAWN_MINIMO` de 0,45 s para **0,35 s**: medindo
  os mesmos bots, é o valor que fecha o último caso de jogador que sobrevive
  para sempre (de 4 em 12 para 1 em 12), sem apertar o jogador comum — a mediana
  do bot mais lento praticamente não mudou. 0,40 s foi medido e não trouxe
  diferença nenhuma.
- **2026-08-19** — O peso do HUD fica **alaranjado a partir de 80 kg**
  (`PESO_DE_ALERTA`, `COR_ALERTA`), e a mesma cor pinta o título do game over. É
  o único aviso de perigo do jogo: com o peso em número, sem barra, faltava um
  sinal periférico de que a corrida estava perto do fim.
- **2026-08-19** — `escrever_no_meio` passou a aceitar linhas de **dois ou três
  itens**: `(tamanho, texto)` usa a cor padrão e `(tamanho, texto, cor)` escolhe
  outra. Foi o jeito de dar cor ao título do menu e ao do game over sem obrigar
  as outras treze linhas das telas a repetir `config.COR_TEXTO`.
- **2026-08-19** — Sem tela de mudo e sem sprites: a fase 7 é de polimento e
  balanceamento, e o jogo é curto. Fica registrado que a arte continua sendo
  formas coloridas, como o `CLAUDE.md` prevê, trocáveis por sprite depois.
