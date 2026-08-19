"""Guarda a maior pontuacao ja feita, num arquivo ao lado do jogo.

O arquivo e um JSON de uma chave so. Se ele nao existir, estiver corrompido ou
nao puder ser escrito, o jogo segue normalmente com o recorde valendo zero: um
placar perdido nunca pode derrubar a partida.
"""

import json
import sys
from pathlib import Path

NOME_DO_ARQUIVO = "recorde.json"
CHAVE = "recorde"


def caminho_padrao():
    """Onde o recorde mora: ao lado do executavel, ou do codigo enquanto e script."""
    if getattr(sys, "frozen", False):  # empacotado pelo PyInstaller (fase 8)
        pasta = Path(sys.executable).parent
    else:
        pasta = Path(__file__).parent
    return pasta / NOME_DO_ARQUIVO


def ler(caminho=None):
    """Le a maior pontuacao gravada. Arquivo ausente ou estragado vale zero."""
    caminho = Path(caminho or caminho_padrao())
    try:
        dados = json.loads(caminho.read_text(encoding="utf-8"))
        return max(int(dados[CHAVE]), 0)
    except (OSError, ValueError, TypeError, KeyError):
        return 0


def salvar(pontuacao, caminho=None):
    """Grava a pontuacao se ela for a maior ate agora e devolve o recorde vigente."""
    caminho = Path(caminho or caminho_padrao())
    recorde = ler(caminho)
    if pontuacao <= recorde:
        return recorde
    try:
        caminho.write_text(json.dumps({CHAVE: pontuacao}), encoding="utf-8")
    except OSError:
        return recorde  # sem permissao de escrita: o jogo continua sem recorde novo
    return pontuacao
