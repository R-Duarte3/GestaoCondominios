from rd_condominios.dominio.morador import Morador


class MoradorServico:
    def __init__(self, repositorio, moradia_repositorio):
        self.repositorio = repositorio
        self.moradia_repositorio = moradia_repositorio

    def listar_moradores(self):
        return self.repositorio.listar()

    def listar_moradias(self):
        return self.moradia_repositorio.listar()

    def criar_morador(self, nome, nif, telefone, email, tipo, id_moradia):
        morador = Morador(
            id_moradores=None,
            nome=nome,
            nif=nif,
            telefone=telefone,
            email=email,
            tipo=tipo,
            id_moradia=id_moradia,
        )
        return self.repositorio.guardar(morador)
