from rd_condominios.dominio.moradia import Moradia


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
