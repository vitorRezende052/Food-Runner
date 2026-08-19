# Plano — Food Runner

Plano de execução do jogo. **Documento vivo:** cada fase concluída é marcada aqui
(`[x]`) e as decisões que surgirem no caminho são registradas na seção "Decisões
tomadas durante a execução". As decisões travadas do projeto ficam no `CLAUDE.md`.

Status geral: **Fase 1 — perspectiva e jogador** (Fase 0 concluída: ambiente uv,
janela abrindo e pytest verde).

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
fator  = 1 / (1 + z * PROFUNDIDADE)      # 1.0 na base, ~0 no horizonte
y_tela = HORIZONTE_Y + (BASE_Y - HORIZONTE_Y) * fator
x_tela = MEIO_X + deslocamento_da_pista * fator
escala = fator                            # tamanho do objeto na tela
```

Vantagem: colisão, spawn e dificuldade são matemática pura sobre `pista` e `z`,
sem pygame no meio — dá para testar tudo com pytest. A projeção fica isolada em
`perspectiva.py` e é a única parte que conhece pixels.

---

## Estrutura de arquivos planejada

```
principal.py      # ponto de entrada: loop, eventos, troca entre menu/jogo/pausa/game over
config.py         # todas as constantes: tela, cores, pistas, perspectiva, balanceamento
perspectiva.py    # projeta (pista, z) -> (x, y, escala). Lógica pura, testável
jogador.py        # pista atual e troca de pista
comida.py         # tipos de comida, spawn e avanço em z
jogo.py           # estado da partida: peso, pontuação, dificuldade, colisões
desenho.py        # desenha cenário, pistas, jogador, comidas e HUD
telas.py          # menu inicial (com instruções), pausa e game over
audio.py          # síntese dos sons com numpy
recorde.py        # lê e grava a maior pontuação em arquivo local
testes/           # test_config.py, test_perspectiva.py, test_jogador.py, test_comida.py, test_jogo.py, test_recorde.py
```

Nada disso é definitivo: se um arquivo ficar pequeno demais ou grande demais no
caminho, ele é fundido ou dividido — e a mudança é anotada aqui.

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
| Velocidade | sobe ~2× ao longo de ~3 min |
| Intervalo entre spawns | 1,1 s no começo → 0,45 s no fim |
| Janela / FPS | 960×720, 60 FPS, movimento por delta time |

A comida boa é mais rara e devolve menos peso do que a ruim adiciona: sem erro
nenhum o jogo ainda aperta, e com o tempo termina.

---

## Fases

Cada fase deixa o jogo **rodando** (`uv run principal.py`), com os testes da
lógica alterada passando, e termina em pelo menos um commit em português.
Trabalho fase a fase: ao terminar uma, paro para você ver rodando antes da próxima.

### [x] Fase 0 — Ambiente
- `uv init`, `uv add pygame-ce`, `uv add --dev pytest`, `.gitignore` (`.venv`, `__pycache__`, `dist`, `build`, `recorde.json`).
- `config.py` com tela e cores; `principal.py` abrindo uma janela preta 960×720 que fecha no ESC/X.
- **Pronto quando:** `uv run principal.py` abre a janela e `uv run pytest` roda.
- **Feito:** pygame-ce 2.5.8 e pytest 9.1.1 no ambiente; `config.py` (janela + paleta),
  `principal.py` (loop com `relogio.tick`, saída no ESC/X) e `testes/test_config.py`.

### [ ] Fase 1 — Perspectiva e jogador
- `perspectiva.py` com a projeção descrita acima.
- `desenho.py` desenhando o horizonte, as 3 pistas convergindo e linhas de chão rolando (sensação de velocidade).
- `jogador.py`: pista central, troca com ← → e A/D, com uma interpolação curta entre pistas (movimento não teleporta).
- Testes: projeção (horizonte menor que base, pistas na ordem certa) e troca de pista (não passa das bordas).
- **Pronto quando:** dá para correr pela pista e trocar de faixa, sem obstáculos.

### [ ] Fase 2 — Comida na pista
- `comida.py`: tipos bons (maçã, brócolis, cenoura, carne grelhada) e ruins (hambúrguer, batata frita, refri, donut) como formas coloridas — verde = boa, vermelho = ruim.
- Spawn em `z = 1.0` numa pista sorteada, avanço em direção ao jogador, remoção ao passar.
- Testes: spawn respeita as pistas válidas, comida some depois de passar, proporção bom/ruim.
- **Pronto quando:** a comida vem do horizonte crescendo e atravessa o jogador sem efeito.

### [ ] Fase 3 — Colisão, peso e pontuação
- `jogo.py`: colisão (mesma pista + `z` dentro da zona do jogador), peso, pontuação por distância e bônus.
- HUD em `desenho.py`: `45 / 100 kg` e a pontuação, ambos em pt-br.
- Game over ao atingir 100 kg (por enquanto, volta ao início).
- Testes: peso sobe/desce e trava nos limites, pontuação acumula, colisão só na mesma pista.
- **Pronto quando:** o jogo tem risco e recompensa de verdade, do início ao game over.

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
- **2026-08-18** — Layout **achatado na raiz** em vez do `src/food_runner/` que o `uv init` criou: o alvo é um executável PyInstaller, não um pacote publicável, então `[project.scripts]` e `[build-system]` saíram do `pyproject.toml` e os módulos ficam na raiz (`uv run principal.py`, como o plano previa).
- **2026-08-18** — Python **3.12** (`.python-version`) em vez do 3.14 do sistema: é a versão com suporte mais rodado em pygame-ce e PyInstaller, e a fase 8 depende dos dois.
- **2026-08-18** — pytest configurado no `pyproject.toml` (`testpaths = ["testes"]`, `pythonpath = ["."]`) para os testes importarem os módulos da raiz sem gambiarra de `sys.path`.
