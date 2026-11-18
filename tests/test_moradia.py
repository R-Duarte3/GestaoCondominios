import pytest

from rd_condominios.dominio.moradia import Moradia, DadosMoradiaInvalidos, IdentificacaoDuplicada
from rd_condominios.repositorios.moradia_repositorio import MoradiaRepositorio
from rd_condominios.servicos.moradia_servico import MoradiaServico


def criar_servico(ligacao):
    return MoradiaServico(MoradiaRepositorio(ligacao))

# Validacao obrigatoria___________________________________________
# DOMINIO__________________________________________________________


def test_moradia_sem_identificacao():
    with pytest.raises(DadosMoradiaInvalidos):
        Moradia(None, "", "", "", "")


def test_moradia_so_com_espacos():
    with pytest.raises(DadosMoradiaInvalidos):
        Moradia(None, "    ", "", "", "")


def test_identificacao_com_mais_100_caracteres():
    with pytest.raises(DadosMoradiaInvalidos):
        Moradia(None, "A" * 101, "", "", "")


def test_espacos_nas_pontas_removidos():
    moradia = Moradia(None, " 1ºESQ ", "", "", "")
    assert moradia.identificacao == "1ºESQ"

# SERVICO__________________________________________________________


def test_servico_nao_cria_moradia_sem_identificacao(ligacao):
    servico = criar_servico(ligacao)
    with pytest.raises(DadosMoradiaInvalidos):
        servico.criar_moradia("", "1", "T2", "")
    assert servico.listar_moradias() == []

# REGRAS DE DUPLICACAO__________________________________________________________


def test_criar_moradia_valida(ligacao):
    servico = criar_servico(ligacao)
    moradia = servico.criar_moradia("1.º Esq", "1", "T2", "")
    assert moradia.id_moradia is not None
    assert len(servico.listar_moradias()) == 1


def test_editar_sem_mudar_a_identificacao(ligacao):
    servico = criar_servico(ligacao)
    moradia = servico.criar_moradia("1.º Esq", "1", "T2", "")
    servico.editar_moradia(moradia.id_moradia, "1.º Esq", "1", "T3", "")
    editada = servico.obter_moradia(moradia.id_moradia)
    assert editada.tipologia == "T3"
