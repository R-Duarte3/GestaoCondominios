import sqlite3
from rd_condominios.dominio.moradia import Moradia, IdentificacaoDuplicada


class MoradiaRepositorio:
    def __init__(self, ligacao):
        self.ligacao = ligacao

    def listar(self):
        linhas = self.ligacao.execute("""
            SELECT id_moradia, identificacao, andar, tipologia, observacoes
            FROM moradias
            ORDER BY identificacao, id_moradia
        """).fetchall()

        return [
            Moradia(
                id_moradia=linha["id_moradia"],
                identificacao=linha["identificacao"],
                andar=linha["andar"] or "",
                tipologia=linha["tipologia"] or "",
                observacoes=linha["observacoes"] or "",
            )
            for linha in linhas
        ]

    def guardar(self, moradia):
        try:
            with self.ligacao:
                cursor = self.ligacao.execute(
                    """
                    INSERT INTO moradias (identificacao, andar, tipologia, observacoes)
                    VALUES (?, ?, ?, ?)
                    """,
                    (moradia.identificacao,
                     moradia.andar,
                     moradia.tipologia,
                     moradia.observacoes,
                     ),
                )
                novo_id = cursor.lastrowid
        except sqlite3.IntegrityError:
            raise IdentificacaoDuplicada(
                "Já existe uma moradia com esta identificação.")

        return Moradia(
            id_moradia=novo_id,
            identificacao=moradia.identificacao,
            andar=moradia.andar,
            tipologia=moradia.tipologia,
            observacoes=moradia.observacoes,
        )
