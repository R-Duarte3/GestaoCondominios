import sqlite3

from rd_condominios.dominio.quota import Quota, QuotaDuplicada, DadosQuotaInvalidos


class QuotaRepositorio:
    def __init__(self, ligacao):
        self.ligacao = ligacao

    def listar(self):
        linhas = self.ligacao.execute("""
            SELECT
                quotas.id_quotas,
                quotas.id_moradia,
                quotas.ano,
                quotas.mes,
                quotas.valor,
                quotas.data_vencimento,
                quotas.data_pagamento,
                moradias.identificacao AS moradia_identificacao
            FROM quotas
            JOIN moradias ON quotas.id_moradia = moradias.id_moradia
            ORDER BY quotas.ano DESC, quotas.mes DESC, moradias.identificacao 
        """).fetchall()
        return linhas

    def guardar(self, quota):
        try:
            with self.ligacao:
                cursor = self.ligacao.execute(
                    """
                    INSERT INTO quotas
                        (id_moradia, ano, mes, valor, data_vencimento, data_pagamento)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (quota.id_moradia,
                     quota.ano,
                     quota.mes,
                     quota.valor,
                     quota.data_vencimento,
                     quota.data_pagamento or None,
                     ),
                )
                novo_id = cursor.lastrowid
        except sqlite3.IntegrityError as erro:
            if erro.sqlite_errorcode == sqlite3.SQLITE_CONSTRAINT_UNIQUE:
                raise QuotaDuplicada(
                    "Já existe uma quota para esta moradia nes mes e ano")
            if erro.sqlite_errorcode == sqlite3.SQLITE_CONSTRAINT_FOREIGNKEY:
                raise QuotaDuplicada("A moradia escolhida nao existe")
            raise
        return Quota(
            id_quotas=novo_id,
            id_moradia=quota.id_moradia,
            ano=quota.ano,
            mes=quota.mes,
            valor=quota.valor,
            data_vencimento=quota.data_vencimento,
            data_pagamento=quota.data_pagamento,
        )

    def registar_pagamento(self, id_quotas, data_pagamento):
        with self.ligacao:
            self.ligacao.execute(
                """
                UPDATE quotas
                SET data_pagamento = ?
                WHERE id_quotas = ?
                """,
                (data_pagamento, id_quotas),
            )

    def obter(self, id_quotas):
        linha = self.ligacao.execute(
            """
            SELECT id_quotas, id_moradia, ano, mes, valor,
                   data_vencimento, data_pagamento
            FROM quotas
            WHERE id_quotas = ?
            """,
            (id_quotas,),
        ).fetchone()
        if linha is None:
            return None
        return Quota(
            id_quotas=linha["id_quotas"],
            id_moradia=linha["id_moradia"],
            ano=linha["ano"],
            mes=linha["mes"],
            valor=linha["valor"],
            data_vencimento=linha["data_vencimento"],
            data_pagamento=linha["data_pagamento"] or "",
        )

    def atualizar(self, quota):
        try:
            with self.ligacao:
                self.ligacao.execute(
                    """
                    UPDATE quotas
                    SET id_moradia = ?,
                        ano = ?,
                        mes = ?,
                        valor = ?,
                        data_vencimento = ?,
                        data_pagamento = ?
                    WHERE id_quotas = ?
                    """,
                    (quota.id_moradia,
                     quota.ano,
                     quota.mes,
                     quota.valor,
                     quota.data_vencimento,
                     quota.data_pagamento or None,
                     quota.id_quotas),
                )
        except sqlite3.IntegrityError as erro:
            if erro.sqlite_errorcode == sqlite3.SQLITE_CONSTRAINT_UNIQUE:
                raise QuotaDuplicada(
                    "Já existe uma quota para esta moradia neste mês e ano!")
            if erro.sqlite_errorcode == sqlite3.SQLITE_CONSTRAINT_FOREIGNKEY:
                raise DadosQuotaInvalidos("A moradia escolhida não existe!")
            raise

    def apagar(self, id_quotas):
        with self.ligacao:
            self.ligacao.execute(
                "DELETE FROM quotas WHERE id_quotas = ?",
                (id_quotas,),
            )
