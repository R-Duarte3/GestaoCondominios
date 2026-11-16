import sqlite3

from rd_condominios.dominio.morador import Morador, NifDuplicado, DadosMoradorInvalidos


class MoradorRepositorio:
    def __init__(self, ligacao):
        self.ligacao = ligacao

    def listar(self):
        linhas = self.ligacao.execute("""
            SELECT
                moradores.id_moradores,
                moradores.nome,
                moradores.nif,
                moradores.telefone,
                moradores.email,
                moradores.tipo,
                moradores.id_moradia,
                moradores.data_entrada,
                moradores.data_saida,
                moradias.identificacao AS moradia_identificacao
            FROM moradores
            JOIN moradias ON moradores.id_moradia = moradias.id_moradia
            ORDER BY (moradores.data_saida IS NOT NULL),
                    moradores.nome, moradores.id_moradores
        """).fetchall()
        return linhas

    def obter(self, id_moradores):
        linha = self.ligacao.execute(
            """
            SELECT id_moradores, nome, nif, telefone, email, tipo,
                   id_moradia, data_entrada, data_saida
            FROM moradores
            WHERE id_moradores = ?
            """,
            (id_moradores,),
        ).fetchone()
        if linha is None:
            return None
        return Morador(
            id_moradores=linha["id_moradores"],
            nome=linha["nome"],
            nif=linha["nif"],
            telefone=linha["telefone"] or "",
            email=linha["email"] or "",
            tipo=linha["tipo"],
            id_moradia=linha["id_moradia"],
            data_entrada=linha["data_entrada"],
            data_saida=linha["data_saida"] or "",
        )

    def guardar(self, morador):
        try:
            with self.ligacao:
                cursor = self.ligacao.execute(
                    """
                    INSERT INTO moradores
                        (nome, nif, telefone, email, tipo, id_moradia, data_entrada, data_saida)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (morador.nome,
                     morador.nif,
                     morador.telefone,
                     morador.email,
                     morador.tipo,
                     morador.id_moradia,
                     morador.data_entrada,
                     morador.data_saida or None,
                     ),
                )
            novo_id = cursor.lastrowid
        except sqlite3.IntegrityError as erro:
            if erro.sqlite_errorcode == sqlite3.SQLITE_CONSTRAINT_UNIQUE:
                raise NifDuplicado("Já existe um morador com este NIF.")
            if erro.sqlite_errorcode == sqlite3.SQLITE_CONSTRAINT_FOREIGNKEY:
                raise DadosMoradorInvalidos("A moradia escolhida não existe.")
            raise

        return Morador(
            id_moradores=novo_id,
            nome=morador.nome,
            nif=morador.nif,
            telefone=morador.telefone,
            email=morador.email,
            tipo=morador.tipo,
            id_moradia=morador.id_moradia,
            data_entrada=morador.data_entrada,
            data_saida=morador.data_saida,
        )

    def registar_saida(self, morador):
        with self.ligacao:
            self.ligacao.execute(
                """
                UPDATE moradores
                SET data_saida = ?
                WHERE id_moradores = ?
                """,
                (morador.data_saida or None, morador.id_moradores),
            )

    def atualizar(self, morador):
        try:
            with self.ligacao:
                self.ligacao.execute(
                    """
                    UPDATE moradores
                    SET nome = ?, nif = ?, telefone = ?, email = ?,
                        tipo = ?, id_moradia =?,
                        data_entrada = ?, data_saida = ?
                    WHERE id_moradores = ?
                    """,
                    (
                        morador.nome,
                        morador.nif,
                        morador.telefone,
                        morador.email,
                        morador.tipo,
                        morador.id_moradia,
                        morador.data_entrada,
                        morador.data_saida or None,
                        morador.id_moradores),
                )
        except sqlite3.IntegrityError as erro:
            if erro.sqlite_errorcode == sqlite3.SQLITE_CONSTRAINT_UNIQUE:
                raise NifDuplicado("Já existe um morador com este NIF!")
            if erro.sqlite_errorcode == sqlite3.SQLITE_CONSTRAINT_FOREIGNKEY:
                raise DadosMoradorInvalidos("A moradia escolhida não existe!")
            raise

    def apagar(self, id_moradores):
        with self.ligacao:
            self.ligacao.execute(
                "DELETE FROM moradores WHERE id_moradores = ?",
                (id_moradores,),
            )
