from rd_condominios.dominio.moradia import Moradia, DadosMoradiaInvalidos


class MoradiaServico:
    def __init__(self, repositorio):
        self.repositorio = repositorio

    def listar_moradias(self):
        return self.repositorio.listar()

    def criar_moradia(self, identificacao, andar, tipologia, observacoes):
        moradia = Moradia(
            id_moradia=None,
            identificacao=identificacao,
            andar=andar,
            tipologia=tipologia,
            observacoes=observacoes,
        )
        return self.repositorio.guardar(moradia)

    def obter_moradia(self, id_moradia):
        moradia = self.repositorio.obter(id_moradia)
        if moradia is None:
            raise DadosMoradiaInvalidos("A moradia indicada não existe!")
        return moradia

    def editar_moradia(self, id_moradia, identificacao, andar, tipologia, observacoes):
        self.obter_moradia(id_moradia)
        moradia = Moradia(
            id_moradia=id_moradia,
            identificacao=identificacao,
            andar=andar,
            tipologia=tipologia,
            observacoes=observacoes,
        )
        self.repositorio.atualizar(moradia)

    def apagar_moradia(self, id_moradia):
        self.obter_moradia(id_moradia)
        self.repositorio.apagar(id_moradia)
