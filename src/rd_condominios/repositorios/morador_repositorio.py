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
                moradias.identificacao AS moradia_identificacao
            FROM moradores
            JOIN moradias ON moradores.id_moradia = moradias.id_moradia
            ORDER BY moradores.nome, moradores.id_moradores
        """).fetchall()
        return linhas

    def guardar(self, morador):
        try:
            with self.ligacao:
                cursor = self.ligacao.execute(
                    """
                    INSERT INTO moradores
                        (nome, nif, telefone, email, tipo, id_moradia)
                    VALUES (?, ?, ?, ?, ?, ?)
                """,
                    (morador.nome,
                     morador.nif,
                     morador.telefone,
                     morador.email,
                     morador.tipo,
                     morador.id_moradia,
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
        )
