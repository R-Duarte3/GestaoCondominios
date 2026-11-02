from dataclasses import dataclass


class DadosMoradiaInvalidos(ValueError):
    pass


class IdentificacaoDuplicada(Exception):
    pass


@dataclass(frozen=True)
class Moradia:
    id_moradia: int | None
    identificacao: str
    andar: str
    tipologia: str
    observacoes: str

    def __post_init__(self):
        identificacao = self.identificacao.strip()
        andar = self.andar.strip()
        tipologia = self.tipologia.strip()
        observacoes = self.observacoes.strip()

        if not identificacao:
            raise DadosMoradiaInvalidos(
                "A identificação da moradia não pode estar vazia.")

        if len(identificacao) > 100:
            raise DadosMoradiaInvalidos(
                "A identificação da moradia não pode ter mais de 100 caracteres.")

        object.__setattr__(self, "identificacao", identificacao)
        object.__setattr__(self, "andar", andar)
        object.__setattr__(self, "tipologia", tipologia)
        object.__setattr__(self, "observacoes", observacoes)
