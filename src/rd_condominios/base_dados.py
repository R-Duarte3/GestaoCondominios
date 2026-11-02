import sqlite3


def ligar(caminho):
    caminho.parent.mkdir(parents=True, exist_ok=True)

    ligacao = sqlite3.connect(caminho)
    ligacao.row_factory = sqlite3.Row
    ligacao.execute("PRAGMA foreign_keys = ON")
    return ligacao


def inicializar(caminho):
    ligacao = ligar(caminho)
    try:
        with ligacao:
            ligacao.executescript("""
                CREATE TABLE IF NOT EXISTS moradias (
                    id_moradia     INTEGER PRIMARY KEY,
                    identificacao  VARCHAR(100) NOT NULL UNIQUE,
                    andar          VARCHAR(50),
                    tipologia      VARCHAR(20),
                    observacoes    TEXT
                );
            """)

    finally:
        ligacao.close()
