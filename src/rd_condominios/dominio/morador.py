from dataclasses import dataclass


class DadosMoradorInvalidos(ValueError):
    pass


class NifDuplicado(Exception):
    pass


@dataclass(frozen=True)
class Morador:
    id_moradores: int | None
    nome: str
    nif: str
    telefone: str
    email: str
    tipo: str
    id_moradia: int
    data_entrada: str
    data_saida: str

    def __post_init__(self):
        nome = self.nome.strip()
        nif = self.nif.strip()
        telefone = self.telefone.strip()
        email = self.email.strip()
        tipo = self.tipo.strip()
        data_entrada = self.data_entrada.strip()
        data_saida = self.data_saida.strip()

        if not nome:
            raise DadosMoradorInvalidos(
                "O nome não pode estar vazio.")

        if len(nome) > 100:
            raise DadosMoradorInvalidos(
                "O nome não pode ter mais de 100 caracteres.")

        if not nif:
            raise DadosMoradorInvalidos(
                "O NIF não pode estar vazio.")

        if len(nif) != 9 or not nif.isdigit():
            raise DadosMoradorInvalidos(
                "O NIF deve ter 9 algarismos.")

        if tipo not in ("proprietario", "inquilino"):
            raise DadosMoradorInvalidos(
                "O tipo deve ser 'Proprietário' ou 'Inquilino'.")

        if not data_entrada:
            raise DadosMoradorInvalidos(
                "A data de entrada é obrigatória!")

        if data_saida and data_saida < data_entrada:
            raise DadosMoradorInvalidos(
                "A data de saída não pode ser anterior à data de entrada!")

        object.__setattr__(self, "nome", nome)
        object.__setattr__(self, "nif", nif)
        object.__setattr__(self, "telefone", telefone)
        object.__setattr__(self, "email", email)
        object.__setattr__(self, "tipo", tipo)
        object.__setattr__(self, "data_entrada", data_entrada)
        object.__setattr__(self, "data_saida", data_saida)
