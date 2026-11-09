from rd_condominios.dominio.despesa import Despesa, CATEGORIAS


class DespesaServico:
    def __init__(self, repositorio):
        self.repositorio = repositorio

    def listar_despesas(self):
        return self.repositorio.listar()

    def listar_categorias(self):
        return CATEGORIAS

    def criar_despesa(self, descricao, categoria, valor, data, fornecedor):
        despesa = Despesa(
            id_despesas=None,
            descricao=descricao,
            categoria=categoria,
            valor=valor,
            data=data,
            fornecedor=fornecedor,
        )
        return self.repositorio.guardar(despesa)
