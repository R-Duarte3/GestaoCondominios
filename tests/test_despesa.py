import pytest

from rd_condominios.dominio.despesa import Despesa, DadosDespesaInvalidos
from rd_condominios.repositorios.despesa_repositorio import DespesaRepositorio
from rd_condominios.repositorios.moradia_repositorio import MoradiaRepositorio
from rd_condominios.servicos.despesa_servico import DespesaServico
from rd_condominios.servicos.moradia_servico import MoradiaServico


def criar_servico(ligacao):
    return DespesaServico(DespesaRepositorio(ligacao),
                          MoradiaRepositorio(ligacao))


def criar_moradias(ligacao, quantas):
    servico = MoradiaServico(MoradiaRepositorio(ligacao))
    for numero in range(quantas):
        servico.criar_moradia("Moradia " + str(numero + 1), "", "", "")


def criar_despesa(servico, valor=310.0):
    return servico.criar_despesa("Limpeza das escadas", "limpeza", valor,
                                 "2026-01-10", "")

# Validacao obrigatoria___________________________________________
# DOMINIO__________________________________________________________


def test_despesa_sem_descricao():
    with pytest.raises(DadosDespesaInvalidos):
        Despesa(None, "", "limpeza", 10.0, "2026-01-10", "")


def test_descricao_so_com_espacos():
    with pytest.raises(DadosDespesaInvalidos):
        Despesa(None, "     ", "limpeza", 10.0, "2026-01-10", "")


def test_valor_zero():
    with pytest.raises(DadosDespesaInvalidos):
        Despesa(None, "Teste", "limpeza", 0, "2026-01-10", "")


def test_valor_negativo():
    with pytest.raises(DadosDespesaInvalidos):
        Despesa(None, "Teste", "limpeza", -5.0, "2026-01-10", "")


# PARTE POR MORADIA (DOMINIO)__________________________________________________________


def test_parte_por_moradia_divisao_exata():
    despesa = Despesa(None, "Teste", "limpeza", 300.0, "2026-01-10", "")
    assert despesa.parte_por_moradia(3) == 100.0


def test_parte_por_moradia_arredonda_ao_centimo():
    despesa = Despesa(None, "Teste", "limpeza", 310.0, "2026-01-10", "")
    assert despesa.parte_por_moradia(3) == 103.33


def test_parte_por_moradia_sem_moradias():
    despesa = Despesa(None, "Teste", "limpeza", 310.0, "2026-01-10", "")
    assert despesa.parte_por_moradia(0) is None

# SERVICO__________________________________________________________


def test_criar_despesa_valida(ligacao):
    servico = criar_servico(ligacao)
    despesa = criar_despesa(servico)
    assert despesa.id_despesas is not None


def test_listar_despesas_sem_moradias(ligacao):
    servico = criar_servico(ligacao)
    criar_despesa(servico)
    despesa, parte = servico.listar_despesas()[0]
    assert parte is None


def test_editar_com_valor_invalido(ligacao):
    servico = criar_servico(ligacao)
    despesa = criar_despesa(servico)
    with pytest.raises(DadosDespesaInvalidos):
        servico.editar_despesa(despesa.id_despesas, "Limpeza das escadas",
                               "limpeza", 0, "2026-01-10", "")


def test_apagar_despesa(ligacao):
    servico = criar_servico(ligacao)
    despesa = criar_despesa(servico)
    servico.apagar_despesa(despesa.id_despesas)
    assert servico.listar_despesas() == []
