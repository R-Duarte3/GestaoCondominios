from rd_condominios.dominio.quota import Quota


class QuotaServico:
    def __init__(self, repositorio, moradia_repositorio):
        self.repositorio = repositorio
        self.moradia_repositorio = moradia_repositorio

    def listar_quotas(self):
        return self.repositorio.listar()

    def listar_moradias(self):
        return self.moradia_repositorio.listar()

    def criar_quota(self, id_moradia, ano, mes, valor, data_vencimento):
        quota = Quota(
            id_quotas=None,
            id_moradia=id_moradia,
            ano=ano,
            mes=mes,
            valor=valor,
            data_vencimento=data_vencimento,
            data_pagamento="",
        )
        return self.repositorio.guardar(quota)

    def registar_pagamento(self, id_quotas, data_pagamento):
        self.repositorio.registar_pagamento(id_quotas, data_pagamento)
