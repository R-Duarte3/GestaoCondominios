from rd_condominios.dominio.despesa import Despesa, CATEGORIAS, DadosDespesaInvalidos


class DespesaServico:
    def __init__(self, repositorio, moradia_repositorio):
        self.repositorio = repositorio
        self.moradia_repositorio = moradia_repositorio

    def listar_despesas(self):
        numero = self.moradia_repositorio.contar()
        resultado = []
        for despesa in self.repositorio.listar():
            resultado.append((despesa, despesa.parte_por_moradia(numero)))
        return resultado

    def numero_moradias(self):
        return self.moradia_repositorio.contar()

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

    def obter_despesa(self, id_despesas):
        return self.repositorio.obter(id_despesas)

    def editar_despesa(self, id_despesas, descricao, categoria, valor, data, fornecedor):
        if self.repositorio.obter(id_despesas) is None:
            raise DadosDespesaInvalidos("A despesa indicada não existe!")
        despesa = Despesa(
            id_despesas=id_despesas,
            descricao=descricao,
            categoria=categoria,
            valor=valor,
            data=data,
            fornecedor=fornecedor,
        )
        self.repositorio.atualizar(despesa)

    def apagar_despesa(self, id_despesas):
        if self.repositorio.obter(id_despesas) is None:
            raise DadosDespesaInvalidos("A despesa indicada não existe!")
        self.repositorio.apagar(id_despesas)
