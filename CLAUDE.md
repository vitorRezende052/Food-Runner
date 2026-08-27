# CLAUDE.md — Food Runner

Contexto do projeto. Respeite as decisões abaixo; se precisar contrariar alguma, confirme antes.

## O que é
Endless runner (estilo Subway Surfers) com temática de alimentação saudável. Trabalho acadêmico individual. Metade da nota é o processo (código limpo, organização e entregas incrementais), então simplicidade e clareza valem tanto quanto o jogo funcionar. O código deve ser autoral e explicável pelo autor.

## Regras do jogo
- Personagem corre sozinho por 3 pistas fixas; o jogador troca de pista (← → e A/D) para desviar de comida ruim e coletar comida boa.
- Comida ruim (ultraprocessados: hambúrguer, batata frita, refri, donut) → aumenta o peso.
- Comida boa (frutas e verduras: maçã, brócolis, cenoura, uva) → diminui o peso e dá bônus de pontos.
- Peso no máximo (100 kg) → game over.
- Pontuação = distância percorrida + bônus das comidas boas.
- Dificuldade aumenta ao longo da partida: velocidade, frequência de spawn e chance de comida ruim crescentes e, da metade da rampa em diante, duas comidas por spawn em pistas diferentes (nunca as três — sempre sobra por onde escapar).
- Balanceamento: comida boa é mais rara e reduz menos peso do que a ruim adiciona — o jogo endurece com o tempo e eventualmente termina.

## Decisões travadas (não mudar sem confirmar)
- Desktop / executável (sem navegador).
- Perspectiva **pseudo-3D**: as 3 pistas convergem para um horizonte, o jogador fica fixo na base e a comida nasce pequena no fundo e cresce ao se aproximar.
- Peso mostrado como número (`45 / 100 kg`) — sem barra nem ícone; perto do limite o número fica alaranjado, que é o único aviso de perigo do jogo. Desde a fase 12 ele e a pontuação ficam sobre uma cápsula translúcida de pontas redondas, que dá fundo ao texto sem virar barra nem ícone.
- Comida boa reduz peso E dá pontos.
- Arte: cartoon desenhado em código (auréola verde = boa, auréola vermelha = ruim) — ver **Direção Visual** abaixo, que substituiu as formas coloridas simples do protótipo.
- Áudio: sons sintéticos gerados por código (numpy), sem arquivos externos — jogo autocontido.
- Tela de menu inicial (com instruções de controle) e tela de game over com a pontuação final.
- Pausa com ESC/P durante a partida.
- Recorde (maior pontuação) salvo em arquivo local, exibido no menu e no game over.

## Direção Visual
Redefinição visual do jogo (fases 8 a 12 do `PLAN.md`, todas no ar: a fundação,
a animação do corredor, as comidas, a rua da cidade e o juice). Substitui a
decisão travada "Arte: formas coloridas simples" — o "fácil de trocar por
sprites depois" é agora.

- **Estilo: cartoon colorido e vibrante** — formas lisas, cantos arredondados e
  sombreamento suave (nada de gradientes complexos, texturas ou pixel art).
  Escolhido por dois motivos: combina com a estrada em perspectiva que já existe
  e renderiza bem no Pygame, que desenha primitivas com anti-aliasing sem
  esforço.
- **Tudo desenhado em código** — sem `assets/`, sem imagens externas, sem
  arquivos de sprite. Cada elemento é montado com primitivas do pygame a partir
  da pista e do `z`, o que dá controle total sobre a perspectiva (a mesma escala
  que já vale para a comida vale para prédios, postes e para o personagem) e
  mantém o jogo autocontido, como já acontece com o áudio.
- **Perspectiva / visto de trás (estilo Subway Surfers):** o personagem é visto
  **de costas**, correndo para o fundo da tela. Os elementos de cenário nas
  laterais respeitam a mesma perspectiva da estrada: nascem pequenos no
  horizonte e crescem conforme se aproximam da câmera.
- **Paleta harmônica e levemente dessaturada** — nada de cores puras como
  `(255, 0, 0)` ou `(0, 255, 0)`. As cores ficam centralizadas no módulo de
  configuração, como todas as outras constantes, e o par verde = boa /
  vermelho = ruim continua valendo, só que em tons mais macios — desde a fase
  10 ele mora na **auréola** atrás da comida, e não na cor do alimento (ver
  abaixo).
- **Fonte e anti-aliasing:** manter a tipografia que já está no HUD e nas telas —
  a fonte padrão do pygame (`pygame.font.Font(None, tamanho)`), desenhada com
  anti-aliasing e, desde a fase 8, com um sombreado escuro atrás para o texto
  ficar legível tanto sobre o céu claro quanto sobre o véu das telas.

### Escolhas já feitas (fases 8 a 11)
Valem para as fases seguintes, para o visual não brigar consigo mesmo:
- **Dia claro:** o céu vai do azul suave no topo ao branco-azulado no horizonte.
- **Rua de cidade:** calçada dos dois lados do asfalto e grama além dela — é
  nesse terreno que os prédios da fase 11 subiram.
- **O corredor** é um atleta cartoon de costas: camiseta coral, shorts azul,
  tênis claros e cabelo escuro, montado em peças separadas para a animação.
- **A comida fica na cor de verdade e o tipo vai para a auréola.** Comida real
  tem cor própria. Em vez de mentir na cor do alimento, cada comida ganhou atrás
  uma auréola: um **disco verde** se ela for boa, **vermelho** se for ruim. No
  horizonte, onde o alimento tem uma dúzia de pixels e só a cor dominante se lê,
  é a auréola que avisa; de perto ela vira moldura e o desenho
  do alimento fala por si. `COR_COMIDA_BOA` e `COR_COMIDA_RUIM` são as cores
  dessa auréola, e as `*_BORDA`, as do anel que a recorta.
- **A forma é a mesma para os dois tipos; só a cor muda.** A auréola é sempre um
  disco — em 27/08/2026 a estrela espetada da comida ruim virou círculo, a
  pedido, para os dois marcadores ficarem irmãos. O custo é o aviso passar a
  depender só do tom, sem a redundância de silhueta que ajudava quem não
  distingue verde de vermelho; a cor da auréola ficou sendo o único canal.
- **A auréola é a única coisa com piso em pixels.** Todo o resto do jogo
  encolhe junto com a perspectiva; o anel da auréola (`AUREOLA_BORDA_MINIMA`) e o
  tamanho da comida (`TAMANHO_COMIDA_MINIMO`) não, porque só como fração eles
  arredondariam para zero justamente no fundo da estrada, que é onde o jogador
  ainda tem tempo de trocar de pista. É uma exceção consciente à regra das
  frações, e vale só para o aviso.
- **O que se move é puxado pela distância percorrida**, nunca por um cronômetro
  próprio: as linhas do asfalto já eram assim, a passada do corredor entrou no
  mesmo esquema na fase 9 e a rua inteira, na fase 11. Sai de graça a sincronia
  com a rampa de dificuldade (a corrida acelera, tudo acelera junto) e o
  congelamento na pausa. **A única exceção é o `efeitos.py`** — ver abaixo.
- **O juice conta o próprio tempo, e só ele.** A regra acima vale para cenário;
  um flash de 0,35 s é um evento, e tem de acabar mesmo depois de a corrida ter
  parado, que é o que acontece no game over. Por isso o `efeitos.py` é o único
  módulo que anda em segundos. A pausa continua congelando tudo porque o `main`
  só atualiza os efeitos enquanto o jogo está em `JOGANDO` ou em `FIM`.

### O juice (fase 12)
O feedback de cada ação, todo num `efeitos.py`:
- **Nada de canal novo de informação.** A `Efeitos.reagir` lê a mesma lista
  `partida.eventos` de que o `main` já tirava os sons desde a fase 6: comida boa
  vira fagulhas verdes nos ombros do corredor, ultraprocessado vira véu vermelho
  mais tranco na tela. O `jogo.py` não ganhou uma linha e continua sem saber o
  que é um pixel.
- **O tranco é uma volta que se fecha, não um sorteio.** O ângulo do desvio corre
  com o que já passou do tremor e o raio encolhe com o que falta — sem `random`
  e sem um segundo cronômetro, o que deixa a conta testável de ponta a ponta.
- **A tela treme sem nenhum outro módulo saber.** O `main` monta o quadro numa
  `Surface` e a joga na tela deslocada; nenhuma função de desenho mudou de
  assinatura por causa disso. O preço é um blit de tela cheia por quadro
  (a mediana passou de 6,1 ms para 7,2 ms).
- **O fade é só fade in.** A troca de tela acontece na hora e a tela nova nasce
  escura e clareia. Escurecer-trocar-clarear obrigaria o `main` a guardar um
  estado pendente e a ignorar teclas durante a cortina, e a pausa é justamente o
  que não pode demorar a responder.
- **O véu é um só.** O escuro do menu, o vermelho do impacto e a cortina saem
  todos do `desenho.veu(tela, cor, opacidade)`.

### A rua da cidade (fase 11)
As laterais deixaram de ser grama vazia. Valem para o que vier:
- **A rua é uma fila plantada, e é a corrida que passa por ela.** Cada elemento
  (prédio, poste, árvore, faixa de pedestres) tem um lugar fixo na rua e um
  **índice inteiro que nunca se repete**: `z = (indice + deslocamento) *
  espacamento - distancia`. É o contrário das linhas do asfalto da fase 1, que
  são vagas recicladas — e essa diferença é o ponto, porque um índice que só
  cresce serve de **identidade permanente**.
- **Nada é sorteado e nada é guardado.** Altura, cor e janelas acesas saem do
  índice pela `cidade.variacao(indice, chave)`, que multiplica índice e chave por
  irracionais diferentes. Sem `random`, sem estado entre quadros: o mesmo quadro
  desenhado duas vezes sai idêntico, e a cidade congela na pausa sozinha.
- **Um prédio é uma caixa de duas paredes** — a lateral (virada para a rua, mais
  escura) e a fachada (virada para a câmera). Cada parede é descrita pelos seus
  **dois pés**, cada um uma `(pista, z)`, e a interpolação entre eles é o que a
  faz convergir para o horizonte. Uma função só desenha as duas.
- **A altura do prédio é um número inteiro de andares.** A grade de janelas fecha
  certinho em qualquer altura, e a janela mede sempre o mesmo em pixels a uma
  dada distância — foi isso que deu um limiar honesto (`PREDIO_JANELA_MINIMA`)
  para o prédio distante ficar liso em vez de sujo.
- **Desenho custa, e a fase 11 chegou perto do teto.** A primeira versão gastava
  11 ms de um orçamento de 16,7 ms por quadro. Sempre que a rua crescer: não
  desenhe o que já saiu da tela, não desenhe detalhe menor que uns poucos pixels
  e projete uma vez por coluna em vez de uma vez por peça. A conferência é uma
  partida inteira rodando sem janela, medindo a mediana e o percentil 99.

## Stack
- Python + pygame-ce.
- **uv para tudo** — nunca `pip`/`python` direto.
- numpy só para sintetizar áudio.
- PyInstaller (dev) para gerar o executável no final.
- pytest (dev) para os testes automatizados.
- Não adicionar outras dependências sem confirmar.

## Comandos
`uv` 0.12.5 instalado via winget (18/08/2026). Se `uv` não for encontrado no shell, abra um terminal novo — o instalador alterou o PATH.

- Rodar: `uv run main.py`
- Adicionar dependência: `uv add <pacote>` — dev: `uv add --dev <pacote>`
- Sincronizar ambiente: `uv sync`
- Rodar testes: `uv run pytest`
- Build (confirmar flags): `uv run pyinstaller --onefile --windowed main.py`
- Conferir o desenho sem abrir janela: num script à parte, `SDL_VIDEODRIVER=dummy` + desenhar num `pygame.Surface` + `pygame.image.save` — bom para checar a perspectiva rápido, sem ficar abrindo o jogo.

## Estrutura
Você decide a arquitetura. O mapa abaixo é o que o `PLAN.md` prevê: ajuste, junte, divida ou renomeie o que fizer mais sentido conforme o jogo cresce, anotando a mudança no `PLAN.md`. O que vale mesmo são as Convenções e o "Como trabalhar" desta página.

`[x]` = já existe. Todos os módulos previstos existem desde a fase 6, mais o `personagem.py`, o `desenho_comida.py`, o `cidade.py` e o `efeitos.py`, que as fases 8, 10, 11 e 12 separaram do `desenho.py` (o status por fase fica no `PLAN.md`).

```
[x] main.py        # loop principal e troca de telas (ponto de entrada)
[x] config.py      # valores centralizados: cores, tamanhos, balanceamento, velocidades
[x] perspectiva.py # projeta (pista, profundidade z) -> (x, y, escala) na tela
[x] jogador.py     # personagem, troca de pista e inclinacao
[x] desenho.py     # cenário, pistas, HUD e utilitários de texto
[x] desenho_comida.py # os oito alimentos e a auréola que diz o tipo deles
[x] personagem.py  # o corredor visto de costas, montado em peças e animado
[x] cidade.py      # a rua: prédios, postes, árvores e faixa de pedestres
[x] efeitos.py     # o juice: fagulhas, flash, tranco da tela e a cortina
[x] testes/        # testes pytest da lógica pura
[x] comida.py      # spawn e tipos de comida
[x] jogo.py        # estado da partida, colisões, pontuação, peso, dificuldade
[x] dificuldade.py # rampa de velocidade, spawn e chance de comida ruim
[x] telas.py       # menu inicial, pausa e game over
[x] audio.py       # síntese dos sons com numpy
[x] recorde.py     # lê e grava a maior pontuação
```

## Convenções
- Modular: arquivos pequenos, uma responsabilidade cada.
- **Tudo em pt-br:** nomes de variáveis, funções, classes e arquivos; comentários e docstrings; e todo o texto visível no jogo (menu, HUD, game over, mensagens). Nomes de arquivo sem acentos e sem cedilha. Única exceção: o ponto de entrada é `main.py`, convenção universal de projetos Python — não renomear.
- **Acentos só no que o jogador lê:** dentro do código (nomes, comentários e docstrings) escrevemos sem acento e sem cedilha, como já está em `config.py` e `perspectiva.py`; o texto que aparece na tela vai acentuado normalmente.
- Sem números mágicos: cores, tamanhos e balanceamento centralizados num módulo de configuração (não espalhados pelo código).
- Commits pequenos, descritivos, **em português**, no modo imperativo (ex.: `adiciona troca de pista`).
- Testes automatizados com pytest para a lógica pura (peso, pontuação, spawn, balanceamento); não testar a camada gráfica. Conta que não toca pixel vale teste mesmo morando num módulo gráfico — é o caso da `desenho.misturar_cores`, das constantes da paleta, das contas da rua no `cidade.py` (`posicoes`, `variacao` e as faixas da grade de janelas) e de todo o `efeitos.py` fora do desenho (o decaimento, a vida da fagulha e o tranco).

## Git
- **Você roda os comandos git neste repositório** (`add`, `commit`, `status`, `log`) sem precisar pedir permissão a cada vez.
- **Commit ao fim de cada etapa**, não no fim do projeto: cada fase concluída do `PLAN.md` vira pelo menos um commit, com o jogo rodando e os testes passando.
- Nunca commite com o jogo quebrado ou com teste vermelho.
- `push` e qualquer operação que reescreva histórico (`reset --hard`, `rebase`, `--force`): só se eu pedir.

## Como trabalhar
- **Solução mais simples que resolve.** Sem design patterns, camadas ou abstrações "para o futuro". Se algo está ficando "genérico/flexível/escalável" para um requisito que ainda não existe, é over-engineering — simplifique.
- **YAGNI:** implemente só o que a tarefa pede.
- **Incremental:** cada mudança deixa o jogo rodando; passos pequenos, com testes cobrindo a lógica alterada.
- **Não reescreva o que já funciona** sem motivo. Clareza acima de esperteza.
- **Arquitetura é sua.** Organize os arquivos como achar melhor, sem precisar pedir permissão — só avise o que mudou. Reorganizações grandes no meio do caminho, aí sim, combine antes.
- **Pergunte antes de decisões grandes:** adicionar dependência ou alterar qualquer decisão travada.

## Plano
O `PLAN.md` é o documento vivo do projeto: fases, estrutura de arquivos e balanceamento. **Mantenha-o atualizado** — marque a fase concluída e registre no bloco dela os desvios do plano. Se uma decisão travada desta página mudar (com minha confirmação), atualize esta página também.

@PLAN.md
