from rd_condominios.dominio.morador import Morador, DadosMoradorInvalidos


class MoradorServico:
    def __init__(self, repositorio, moradia_repositorio):
        self.repositorio = repositorio
        self.moradia_repositorio = moradia_repositorio

    def listar_moradores(self):
        return self.repositorio.listar()

    def listar_moradias(self):
        return self.moradia_repositorio.listar()

    def criar_morador(self, nome, nif, telefone, email, tipo, id_moradia, data_entrada):
        morador = Morador(
            id_moradores=None,
            nome=nome,
            nif=nif,
            telefone=telefone,
            email=email,
            tipo=tipo,
            id_moradia=id_moradia,
            data_entrada=data_entrada,
            data_saida=""
        )
        return self.repositorio.guardar(morador)

    def registar_saida(self, id_moradores, data_saida):
        atual = self.repositorio.obter(id_moradores)
        if atual is None:
            raise DadosMoradorInvalidos("O morador indicado não existe!")

        if not data_saida.strip():
            raise DadosMoradorInvalidos("Indique a data de saída")

        morador = Morador(
            id_moradores=atual.id_moradores,
            nome=atual.nome,
            nif=atual.nif,
            telefone=atual.telefone,
            email=atual.email,
            tipo=atual.tipo,
            id_moradia=atual.id_moradia,
            data_entrada=atual.data_entrada,
            data_saida=data_saida,
        )
        self.repositorio.registar_saida(morador)
