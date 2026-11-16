from rd_condominios.dominio.despesa import Despesa


class DespesaRepositorio:
    def __init__(self, ligacao):
        self.ligacao = ligacao

    def listar(self):
        linhas = self.ligacao.execute("""
            SELECT id_despesas, descricao, categoria, valor, data, fornecedor
            FROM despesas
            ORDER BY data DESC, id_despesas DESC
        """).fetchall()

        return [
            Despesa(
                id_despesas=linha["id_despesas"],
                descricao=linha["descricao"],
                categoria=linha["categoria"],
                valor=linha["valor"],
                data=linha["data"],
                fornecedor=linha["fornecedor"] or "",
            )
            for linha in linhas
        ]

    def guardar(self, despesa):
        with self.ligacao:
            cursor = self.ligacao.execute(
                """
                INSERT INTO despesas (descricao, categoria, valor, data, fornecedor)
                VALUES (?, ?, ?, ?, ?)
                """,
                (despesa.descricao,
                 despesa.categoria,
                 despesa.valor,
                 despesa.data,
                 despesa.fornecedor or None,
                 ),
            )
            novo_id = cursor.lastrowid

        return Despesa(
            id_despesas=novo_id,
            descricao=despesa.descricao,
            categoria=despesa.categoria,
            valor=despesa.valor,
            data=despesa.data,
            fornecedor=despesa.fornecedor,
        )

    def obter(self, id_despesas):
        linha = self.ligacao.execute(
            """
            SELECT id_despesas, descricao, categoria, valor, data, fornecedor
            FROM despesas
            WHERE id_despesas = ?
            """,
            (id_despesas,),
        ).fetchone()
        if linha is None:
            return None
        return Despesa(
            id_despesas=linha["id_despesas"],
            descricao=linha["descricao"],
            categoria=linha["categoria"],
            valor=linha["valor"],
            data=linha["data"],
            fornecedor=linha["fornecedor"] or "",
        )

    def atualizar(self, despesa):
        with self.ligacao:
            self.ligacao.execute(
                """
                UPDATE despesas
                SET descricao = ?,
                    categoria = ?,
                    valor = ?,
                    data = ?,
                    fornecedor = ?
                where id_despesas = ?
                """,
                (
                    despesa.descricao,
                    despesa.categoria,
                    despesa.valor,
                    despesa.data,
                    despesa.fornecedor or None,
                    despesa.id_despesas
                ),
            )

    def apagar(self, id_despesas):
        with self.ligacao:
            self.ligacao.execute(
                "DELETE FROM despesas WHERE id_despesas = ?", (id_despesas,),
            )
