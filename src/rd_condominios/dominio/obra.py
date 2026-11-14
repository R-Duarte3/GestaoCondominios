from dataclasses import dataclass

ESTADOS = ("pendente", "em_curso", "concluida")


class DadosObraInvalidos(ValueError):
    pass


@dataclass(frozen=True)
class Obra:
    id_obras: int | None
    descricao: str
    data_pedido: str
    data_conclusao: str
    estado: str
    orcamento: float | None
    custo_final: float | None

    def __post_init__(self):
        descricao = self.descricao.strip()
        data_pedido = self.data_pedido.strip()
        data_conclusao = self.data_conclusao.strip()
        estado = self.estado.strip()

        if not descricao:
            raise DadosObraInvalidos(
                "A descrição da obra não pode estar vazia!")

        if len(descricao) > 200:
            raise DadosObraInvalidos(
                "A descrição não pode ter mais de 200 caracteres!")

        if not data_pedido:
            raise DadosObraInvalidos("A data de pedido é obrigatória!")

        if estado not in ESTADOS:
            raise DadosObraInvalidos("O estado escolhido não é válido!")

        if estado == "concluida" and not data_conclusao:
            raise DadosObraInvalidos(
                "Uma obra concluída tem de ter data de conclusão")

        if estado != "concluida" and data_conclusao:
            raise DadosObraInvalidos(
                "Só uma obra concluída pode ter data de conclusão")

        if data_conclusao and data_conclusao < data_pedido:
            raise DadosObraInvalidos(
                "A data de conclusão não pode ser anterior á data do pedido!")

        if self.orcamento is not None and self.orcamento < 0:
            raise DadosObraInvalidos("O orçamento não pode ser negativo!")

        if self.custo_final is not None and self.custo_final < 0:
            raise DadosObraInvalidos("o custo final não pode ser negativo!")

        object.__setattr__(self, "descricao", descricao)
        object.__setattr__(self, "data_pedido", data_pedido)
        object.__setattr__(self, "data_conclusao", data_conclusao)
        object.__setattr__(self, "estado", estado)
