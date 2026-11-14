import sqlite3
from rd_condominios.dominio.moradia import Moradia, IdentificacaoDuplicada, MoradiaEmUso


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

    def contar(self):
        linha = self.ligacao.execute(
            "SELECT COUNT(*) AS total FROM moradias"
        ).fetchone()
        return linha["total"]

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

    def obter(self, id_moradia):
        linha = self.ligacao.execute(
            """
            SELECT id_moradia, identificacao, andar, tipologia, observacoes
            FROM moradias
            WHERE id_moradia = ?
            """,
            (id_moradia,),
        ).fetchone()
        if linha is None:
            return None
        return Moradia(
            id_moradia=linha["id_moradia"],
            identificacao=linha["identificacao"],
            andar=linha["andar"] or "",
            tipologia=linha["tipologia"] or "",
            observacoes=linha["observacoes"] or "",
        )

    def atualizar(self, moradia):
        try:
            with self.ligacao:
                self.ligacao.execute(
                    """
                    UPDATE moradias
                    SET identificacao = ?, andar = ?,
                        tipologia = ?, observacoes = ?
                    WHERE id_moradia = ?
                    """,
                    (
                        moradia.identificacao,
                        moradia.andar,
                        moradia.tipologia,
                        moradia.observacoes,
                        moradia.id_moradia
                    ),
                )
        except sqlite3.IntegrityError as erro:
            if erro.sqlite_errorcode == sqlite3.SQLITE_CONSTRAINT_UNIQUE:
                raise IdentificacaoDuplicada(
                    "Já existe uma moradia com esta identificação!")
            raise

    def apagar(self, id_moradia):
        try:
            with self.ligacao:
                self.ligacao.execute(
                    "DELETE FROM moradias WHERE id_moradia = ?",
                    (id_moradia,),
                )
        except sqlite3.IntegrityError as erro:
            if erro.sqlite_errorcode == sqlite3.SQLITE_CONSTRAINT_FOREIGNKEY:
                raise MoradiaEmUso(
                    "Nao pode apagar esta moradia, porque tem moradores ou quotas associados!")
            raise
