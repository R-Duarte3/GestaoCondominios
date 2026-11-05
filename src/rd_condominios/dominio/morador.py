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

    def __post_init__(self):
        nome = self.nome.strip()
        nif = self.nif.strip()
        telefone = self.telefone.strip()
        email = self.email.strip()
        tipo = self.tipo.strip()

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

        object.__setattr__(self, "nome", nome)
        object.__setattr__(self, "nif", nif)
        object.__setattr__(self, "telefone", telefone)
        object.__setattr__(self, "email", email)
        object.__setattr__(self, "tipo", tipo)
