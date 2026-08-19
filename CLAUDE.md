# CLAUDE.md — Food Runner

Contexto do projeto. Respeite as decisões abaixo; se precisar contrariar alguma, confirme antes.

## O que é
Endless runner (estilo Subway Surfers) com temática de alimentação saudável. Trabalho acadêmico individual. Metade da nota é o processo (código limpo, organização e entregas incrementais), então simplicidade e clareza valem tanto quanto o jogo funcionar. O código deve ser autoral e explicável pelo autor.

## Regras do jogo
- Personagem corre sozinho por 3 pistas fixas; o jogador troca de pista (← → e A/D) para desviar de comida ruim e coletar comida boa.
- Comida ruim (ultraprocessados: hambúrguer, batata frita, refri, donut) → aumenta o peso.
- Comida boa (frutas, verduras, carne grelhada) → diminui o peso e dá bônus de pontos.
- Peso no máximo (100 kg) → game over.
- Pontuação = distância percorrida + bônus das comidas boas.
- Dificuldade aumenta ao longo da partida (velocidade e frequência de comida ruim crescentes).
- Balanceamento: comida boa é mais rara e reduz menos peso do que a ruim adiciona — o jogo endurece com o tempo e eventualmente termina.

## Decisões travadas (não mudar sem confirmar)
- Desktop / executável (sem navegador).
- Perspectiva **pseudo-3D**: as 3 pistas convergem para um horizonte, o jogador fica fixo na base e a comida nasce pequena no fundo e cresce ao se aproximar.
- Peso mostrado como número (`45 / 100 kg`) — sem barra nem ícone.
- Comida boa reduz peso E dá pontos.
- Arte: formas coloridas simples (verde = boa, vermelho = ruim), fácil de trocar por sprites depois.
- Áudio: sons sintéticos gerados por código (numpy), sem arquivos externos — jogo autocontido.
- Tela de menu inicial (com instruções de controle) e tela de game over com a pontuação final.
- Pausa com ESC/P durante a partida.
- Recorde (maior pontuação) salvo em arquivo local, exibido no menu e no game over.

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

`[x]` = já existe; o resto entra nas fases seguintes (o status por fase fica no `PLAN.md`).

```
[x] main.py        # loop principal e troca de telas (ponto de entrada)
[x] config.py      # valores centralizados: cores, tamanhos, balanceamento, velocidades
[x] perspectiva.py # projeta (pista, profundidade z) -> (x, y, escala) na tela
[x] jogador.py     # personagem e troca de pista
[x] desenho.py     # cenário, pistas, jogador, comidas e HUD
[x] testes/        # testes pytest da lógica pura
[x] comida.py      # spawn e tipos de comida
[x] jogo.py        # estado da partida, colisões, pontuação, peso, dificuldade
[ ] telas.py       # menu inicial, pausa e game over
[ ] audio.py       # síntese dos sons com numpy
[ ] recorde.py     # lê e grava a maior pontuação
```

## Convenções
- Modular: arquivos pequenos, uma responsabilidade cada.
- **Tudo em pt-br:** nomes de variáveis, funções, classes e arquivos; comentários e docstrings; e todo o texto visível no jogo (menu, HUD, game over, mensagens). Nomes de arquivo sem acentos e sem cedilha. Única exceção: o ponto de entrada é `main.py`, convenção universal de projetos Python — não renomear.
- **Acentos só no que o jogador lê:** dentro do código (nomes, comentários e docstrings) escrevemos sem acento e sem cedilha, como já está em `config.py` e `perspectiva.py`; o texto que aparece na tela vai acentuado normalmente.
- Sem números mágicos: cores, tamanhos e balanceamento centralizados num módulo de configuração (não espalhados pelo código).
- Commits pequenos, descritivos, **em português**, no modo imperativo (ex.: `adiciona troca de pista`).
- Testes automatizados com pytest para a lógica pura (peso, pontuação, spawn, balanceamento); não testar a camada gráfica.

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
O `PLAN.md` é o documento vivo do projeto: fases, estrutura de arquivos, balanceamento e decisões tomadas no caminho. **Mantenha-o atualizado** — marque a fase concluída, registre desvios do plano e anote decisões novas ali. Se uma decisão travada desta página mudar (com minha confirmação), atualize esta página também.

@PLAN.md
