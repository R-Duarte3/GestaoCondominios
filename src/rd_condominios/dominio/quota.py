from dataclasses import dataclass
from datetime import date


class DadosQuotaInvalidos(ValueError):
    pass


class QuotaDuplicada(Exception):
    pass


@dataclass(frozen=True)
class Quota:
    id_quotas: int | None
    id_moradia: int
    ano: int
    mes: int
    valor: float
    data_vencimento: str
    data_pagamento: str

    def __post_init__(self):
        data_vencimento = self.data_vencimento.strip()
        data_pagamento = self.data_pagamento.strip()

        if self.mes < 1 or self.mes > 12:
            raise DadosQuotaInvalidos("O mês deve estar entre 1 e 12!")

        if self.ano < 2000 or self.ano > 2100:
            raise DadosQuotaInvalidos("O ano indicado não é válido!")

        if self.valor <= 0:
            raise DadosQuotaInvalidos("O valor da quota deve ser positivo!")

        if not data_vencimento:
            raise DadosQuotaInvalidos("A data de vencimento é obrigatória!")

        object.__setattr__(self, "data_vencimento", data_vencimento)
        object.__setattr__(self, "data_pagamento", data_pagamento)

    def estado(self):
        if self.data_pagamento:
            return "Pago"

        if self.data_vencimento < date.today().isoformat():
            return "Em atraso"
        return "Pendente"
