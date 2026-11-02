import os
from pathlib import Path


def obter_caminho_bd():
    valor = os.getenv("RD_CONDOMINIOS_BD", "data/condominio.db")
    return Path(valor)
