# Plano — Food Runner

Plano de execução do jogo. **Documento vivo:** cada fase concluída é marcada aqui
(`[x]`) e as decisões que surgirem no caminho são registradas na seção "Decisões
tomadas durante a execução". As decisões travadas do projeto ficam no `CLAUDE.md`.

Status geral: **Fase 4 — dificuldade progressiva** (Fases 0 a 3 concluídas: ambiente
uv, estrada em perspectiva rolando, jogador trocando de pista, comida vindo do
horizonte e a partida completa — peso, pontuação, HUD e game over —, com pytest
verde).

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

`[x]` = já existe no repositório; o resto entra nas fases seguintes.

```
[x] main.py        # ponto de entrada: loop, eventos, troca entre menu/jogo/pausa/game over
[x] config.py      # todas as constantes: tela, cores, pistas, perspectiva, balanceamento
[x] perspectiva.py # projeta (pista, z) -> (x, y, escala). Lógica pura, testável
[x] jogador.py     # pista atual e troca de pista
[x] desenho.py     # desenha cenário, pistas, jogador, comidas e HUD
[x] testes/        # test_config, test_perspectiva, test_jogador, test_comida, test_jogo
[x] comida.py      # tipos de comida, spawn e avanço em z
[x] jogo.py        # estado da partida: peso, pontuação, dificuldade, colisões
[ ] telas.py       # menu inicial (com instruções), pausa e game over
[ ] audio.py       # síntese dos sons com numpy
[ ] recorde.py     # lê e grava a maior pontuação em arquivo local
```

Até aqui a estrutura real bateu com a planejada, sem fusões nem divisões — o
único desvio foi o ponto de entrada, que virou `main.py`. O aviso de game over da
fase 3 nasceu dentro do `desenho.py`; na fase 5 ele se muda para o `telas.py`,
junto do menu e da pausa. Nada disso é definitivo: se um arquivo ficar pequeno
demais ou grande demais no caminho, ele é fundido ou dividido — e a mudança é
anotada aqui.

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
| Intervalo entre spawns | 1,1 s no começo → 0,45 s no fim |
| Tamanho da comida | 90 px de lado ao chegar no jogador |
| Janela / FPS | 960×720, 60 FPS, movimento por delta time |

A comida boa é mais rara e devolve menos peso do que a ruim adiciona: sem erro
nenhum o jogo ainda aperta, e com o tempo termina.

Do que já está valendo no `config.py`: velocidade, intervalo de spawn, chance de
comida ruim e tamanho da comida (todos ainda no valor inicial, sem a progressão
da fase 4), além dos números de peso e pontuação que a fase 3 trouxe. A
pontuação por distância virou `PONTOS_POR_Z = 20`, que no ritmo inicial de
0,5 z/s dá exatamente os 10 pontos por segundo da tabela.

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

### [ ] Fase 4 — Dificuldade progressiva
- Velocidade, frequência de spawn e chance de comida ruim crescendo com o tempo de partida.
- Testes: os três valores crescem de forma monotônica e param nos tetos definidos.
- **Pronto quando:** uma partida longa fica visivelmente mais difícil e termina sozinha.

### [ ] Fase 5 — Telas, pausa e recorde
- `telas.py`: menu inicial com título, instruções curtas (controles + regra do peso) e recorde; tela de game over com pontuação final e recorde; overlay de pausa (ESC/P).
- `recorde.py`: grava a maior pontuação num arquivo local ao lado do jogo.
- Testes: recorde só sobe, arquivo ausente/corrompido não quebra o jogo.
- **Pronto quando:** dá para abrir, jogar, pausar, perder e recomeçar sem sair do jogo.

### [ ] Fase 6 — Áudio sintetizado
- `audio.py` com numpy: som de coleta (boa), impacto (ruim), game over e confirmação do menu. Sem arquivos externos.
- Falha de áudio (máquina sem dispositivo) não pode derrubar o jogo.
- **Pronto quando:** cada evento tem seu som e o jogo continua rodando mesmo sem placa de som.

### [ ] Fase 7 — Polimento e balanceamento
- Jogar, ajustar os números do `config.py`, revisar nomes e comentários, garantir a suíte de testes verde.
- Atualizar o `README.md` (o que é, como rodar, como jogar, como testar).

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
- **2026-08-19** — As linhas de chão são calculadas a partir do tempo de jogo (`_profundidades_das_linhas`), sem estado guardado: o cenário não precisa de objeto próprio.
- **2026-08-19** — Colisão por **zona em torno do jogador**: acerta quem estiver na mesma pista com `abs(z) <= ZONA_COLISAO = 0,04`. Foi preferida a "cruzou o plano do jogador" porque não deixa a comida já ultrapassada continuar valendo se o jogador entrar na pista dela depois, e porque a janela de 0,08 em z aguenta a aceleração da fase 4 sem a comida atravessar entre dois quadros. A zona termina em `z = -0,04`, ainda acima do `Z_SUMICO = -0,05`, então nada é descartado antes de ser conferido — há teste para isso.
- **2026-08-19** — Pontuação contada **por distância em z** (`PONTOS_POR_Z = 20`), não por tempo: no ritmo inicial dá os 10 pontos por segundo do plano e, quando a fase 4 acelerar, sobreviver ao trecho rápido passa a pagar mais.
- **2026-08-19** — O game over **congela a partida e espera Espaço/Enter**, em vez de reiniciar na hora como o plano dizia. Sem isso não dá para ver que perdeu nem qual foi a pontuação. São poucas linhas em `desenho.desenhar_game_over`, que a fase 5 leva para o `telas.py`.
- **2026-08-19** — O peso é travado nas duas pontas (`PESO_MINIMO = 30`, `PESO_GAME_OVER = 100`), então o HUD nunca mostra número fora da faixa e o fim de partida acontece com `100 / 100 kg` na tela.
- **2026-08-19** — O chão rolante passou a ser calculado a partir da **distância percorrida** em vez de `tempo * VELOCIDADE_JOGO`. É o mesmo valor enquanto a velocidade é constante, mas na fase 4 o asfalto acompanha a aceleração sozinho — e a `Jogo` não precisa guardar um cronômetro só para o desenho.
