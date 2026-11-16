from rd_condominios.dominio.obra import Obra, DadosObraInvalidos, ESTADOS


class ObraServico:
    def __init__(self, repositorio):
        self.repositorio = repositorio

    def listar_obras(self):
        return self.repositorio.listar()

    def listar_estados(self):
        return ESTADOS

    def criar_obra(self, descricao, data_pedido, orcamento):
        obra = Obra(
            id_obras=None,
            descricao=descricao,
            data_pedido=data_pedido,
            data_conclusao="",
            estado="pendente",
            orcamento=orcamento,
            custo_final=None,
        )
        return self.repositorio.guardar(obra)

    def atualizar_estado(self, id_obras, estado, data_conclusao, custo_final):
        atual = self.repositorio.obter(id_obras)
        if atual is None:
            raise DadosObraInvalidos("A obra indicada não existe!")

        # com os novos dados cria a obra
        obra = Obra(
            id_obras=atual.id_obras,
            descricao=atual.descricao,
            data_pedido=atual.data_pedido,
            data_conclusao=data_conclusao,
            estado=estado,
            orcamento=atual.orcamento,
            custo_final=custo_final,
        )
        self.repositorio.atualizar_estado(obra)

    def obter_obra(self, id_obras):
        return self.repositorio.obter(id_obras)

    def editar_obra(self, id_obras, descricao, data_pedido, data_conclusao, estado, orcamento, custo_final):
        if self.repositorio.obter(id_obras) is None:
            raise DadosObraInvalidos("A obra indicada não existe!")
        obra = Obra(
            id_obras=id_obras,
            descricao=descricao,
            data_pedido=data_pedido,
            data_conclusao=data_conclusao,
            estado=estado,
            orcamento=orcamento,
            custo_final=custo_final,
        )
        self.repositorio.atualizar(obra)

    def apagar_obra(self, id_obras):
        if self.repositorio.obter(id_obras) is None:
            raise DadosObraInvalidos("A obra indicada não existe!")
        self.repositorio.apagar(id_obras)
