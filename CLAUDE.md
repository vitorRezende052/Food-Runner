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
- Peso mostrado como número (`45 / 100 kg`) — sem barra nem ícone; perto do limite o número fica alaranjado, que é o único aviso de perigo do jogo.
- Comida boa reduz peso E dá pontos.
- Arte: cartoon desenhado em código (verde = boa, vermelho = ruim) — ver **Direção Visual** abaixo, que substituiu as formas coloridas simples do protótipo.
- Áudio: sons sintéticos gerados por código (numpy), sem arquivos externos — jogo autocontido.
- Tela de menu inicial (com instruções de controle) e tela de game over com a pontuação final.
- Pausa com ESC/P durante a partida.
- Recorde (maior pontuação) salvo em arquivo local, exibido no menu e no game over.

## Direção Visual
Redefinição visual do jogo (fases 8 a 12 do `PLAN.md`; as fases 8 a 10 — a
fundação, a animação do corredor e as comidas — já estão no ar). Substitui a
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

### Escolhas já feitas (fases 8 a 10)
Valem para as fases seguintes, para o visual não brigar consigo mesmo:
- **Dia claro:** o céu vai do azul suave no topo ao branco-azulado no horizonte.
- **Rua de cidade:** calçada dos dois lados do asfalto e grama além dela — é
  nesse terreno que os prédios da fase 11 sobem.
- **O corredor** é um atleta cartoon de costas: camiseta coral, shorts azul,
  tênis claros e cabelo escuro, montado em peças separadas para a animação.
- **A comida fica na cor de verdade e o tipo vai para a auréola.** Comida real
  tem cor própria, e a maçã, que é saudável, é vermelha. Em vez de mentir na cor
  do alimento, cada comida ganhou atrás um disco translúcido verde (boa) ou
  vermelho (ruim): no horizonte, onde ela tem menos de dez pixels e só a cor
  dominante se lê, é a auréola que avisa; de perto ela vira moldura e o desenho
  do alimento fala por si. `COR_COMIDA_BOA` e `COR_COMIDA_RUIM` são as cores
  dessa auréola.
- **O que se move é puxado pela distância percorrida**, nunca por um cronômetro
  próprio: as linhas do asfalto já eram assim e a passada do corredor entrou no
  mesmo esquema na fase 9. Sai de graça a sincronia com a rampa de dificuldade
  (a corrida acelera, tudo acelera junto) e o congelamento na pausa. Os postes,
  as árvores e o parallax da fase 11 seguem a mesma receita.

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

`[x]` = já existe. Todos os módulos previstos existem desde a fase 6, mais o `personagem.py` e o `desenho_comida.py`, que as fases 8 e 10 separaram do `desenho.py` (o status por fase fica no `PLAN.md`).

```
[x] main.py        # loop principal e troca de telas (ponto de entrada)
[x] config.py      # valores centralizados: cores, tamanhos, balanceamento, velocidades
[x] perspectiva.py # projeta (pista, profundidade z) -> (x, y, escala) na tela
[x] jogador.py     # personagem, troca de pista e inclinacao
[x] desenho.py     # cenário, pistas, HUD e utilitários de texto
[x] desenho_comida.py # os oito alimentos e a auréola que diz o tipo deles
[x] personagem.py  # o corredor visto de costas, montado em peças e animado
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
- Testes automatizados com pytest para a lógica pura (peso, pontuação, spawn, balanceamento); não testar a camada gráfica. Conta que não toca pixel vale teste mesmo morando num módulo gráfico — é o caso da `desenho.misturar_cores` e das constantes da paleta.

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
