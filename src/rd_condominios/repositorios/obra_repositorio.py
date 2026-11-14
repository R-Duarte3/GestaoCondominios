from rd_condominios.dominio.obra import Obra


class ObraRepositorio:
    def __init__(self, ligacao):
        self.ligacao = ligacao

    def _converter(self, linha):
        return Obra(
            id_obras=linha["id_obras"],
            descricao=linha["descricao"],
            data_pedido=linha["data_pedido"],
            data_conclusao=linha["data_conclusao"] or "",
            estado=linha["estado"],
            orcamento=linha["orcamento"],
            custo_final=linha["custo_final"],
        )

    def listar(self):
        linhas = self.ligacao.execute("""
                SELECT id_obras, descricao, data_pedido, data_conclusao, estado, orcamento, custo_final
                FROM obras
                ORDER BY data_pedido DESC, id_obras DESC
        """).fetchall()
        return [self._converter(linha) for linha in linhas]

    def obter(self, id_obras):
        linha = self.ligacao.execute(
            """
            SELECT id_obras, descricao, data_pedido, data_conclusao, estado, orcamento, custo_final
            FROM obras
            WHERE id_obras =?
            """, (id_obras,),
        ).fetchone()
        if linha is None:
            return None
        return self._converter(linha)

    def guardar(self, obra):
        with self.ligacao:
            cursor = self.ligacao.execute(
                """
                INSERT INTO obras
                    (descricao, data_pedido, data_conclusao, estado, orcamento, custo_final)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    obra.descricao,
                    obra.data_pedido,
                    obra.data_conclusao or None,
                    obra.estado,
                    obra.orcamento,
                    obra.custo_final,
                ),
            )
            novo_id = cursor.lastrowid
        return Obra(
            id_obras=novo_id,
            descricao=obra.descricao,
            data_pedido=obra.data_pedido,
            data_conclusao=obra.data_conclusao,
            estado=obra.estado,
            orcamento=obra.orcamento,
            custo_final=obra.custo_final,
        )

    def atualizar_estado(self, obra):
        with self.ligacao:
            self.ligacao.execute(
                """
                UPDATE obras
                SET estado = ?, data_conclusao = ?, custo_final = ?
                WHERE id_obras = ?
                """,
                (
                    obra.estado,
                    obra.data_conclusao or None,
                    obra.custo_final,
                    obra.id_obras
                ),
            )
