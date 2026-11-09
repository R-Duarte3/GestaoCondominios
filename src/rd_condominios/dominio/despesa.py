from dataclasses import dataclass

CATEGORIAS = ("limpeza", "seguro", "agua", "eletricidade", "obra", "outras")


class DadosDespesaInvalidos(ValueError):
    pass


@dataclass(frozen=True)
class Despesa:
    id_despesas: int | None
    descricao: str
    categoria: str
    valor: float
    data: str
    fornecedor: str

    def __post_init__(self):
        descricao = self.descricao.strip()
        categoria = self.categoria.strip()
        data = self.data.strip()
        fornecedor = self.fornecedor.strip()

        if not descricao:
            raise DadosDespesaInvalidos(
                "A descrição da despesa não pode estar vazia!")

        if len(descricao) > 200:
            raise DadosDespesaInvalidos(
                "A descrição da despesa não pode ter mais de 200 caracteres!")

        if categoria not in CATEGORIAS:
            raise DadosDespesaInvalidos("A categoria escolhida não é válida!")

        if self.valor <= 0:
            raise DadosDespesaInvalidos(
                "O valor da despesa deve ser positivo!")

        if not data:
            raise DadosDespesaInvalidos("A data da despesa é obrigatória!")

        if len(self.fornecedor) > 100:
            raise DadosDespesaInvalidos(
                "O nome do fornecedor não pode ter mais de 100 caracteres!")

        object.__setattr__(self, "descricao", descricao)
        object.__setattr__(self, "categoria", categoria)
        object.__setattr__(self, "data", data)
        object.__setattr__(self, "fornecedor", fornecedor)
