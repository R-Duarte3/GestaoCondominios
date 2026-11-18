import pytest

from rd_condominios.dominio.obra import Obra, DadosObraInvalidos
from rd_condominios.repositorios.obra_repositorio import ObraRepositorio
from rd_condominios.servicos.obra_servico import ObraServico


def criar_servico(ligacao):
    return ObraServico(ObraRepositorio(ligacao))


def criar_obra(servico):
    return servico.criar_obra("Pintura do hall", "2026-03-01", 500.0)

# Validacao obrigatoria___________________________________________
# DOMINIO__________________________________________________________


def test_obra_sem_descricao():
    with pytest.raises(DadosObraInvalidos):
        Obra(None, "", "2026-03-01", "", "pendente", None, None)


def test_obra_sem_data_de_pedido():
    with pytest.raises(DadosObraInvalidos):
        Obra(None, "Pintura", "", "", "pendente", None, None)


def test_estado_invalido():
    with pytest.raises(DadosObraInvalidos):
        Obra(None, "Pintura", "2026-03-01", "", "cancelada", None, None)


def test_concluida_sem_data_de_conclusao():
    with pytest.raises(DadosObraInvalidos):
        Obra(None, "Pintura", "2026-03-01", "", "concluida", None, None)


def test_nao_concluida_com_data_de_conclusao():
    with pytest.raises(DadosObraInvalidos):
        Obra(None, "Pintura", "2026-03-01", "2026-03-10", "em_curso",
             None, None)


def test_obra_concluida_valida():
    obra = Obra(None, "Pintura", "2026-03-01", "2026-03-10", "concluida",
                500.0, 480.0)
    assert obra.estado == "concluida"

# SERVICO__________________________________________________________


def test_criar_obra_sem_orcamento(ligacao):
    servico = criar_servico(ligacao)
    obra = servico.criar_obra("Pintura do hall", "2026-03-01", None)
    assert servico.obter_obra(obra.id_obras).orcamento is None


def test_atualizar_estado_concluida_sem_data(ligacao):
    servico = criar_servico(ligacao)
    obra = criar_obra(servico)
    with pytest.raises(DadosObraInvalidos):
        servico.atualizar_estado(obra.id_obras, "concluida", "", None)
    assert servico.obter_obra(obra.id_obras).estado == "pendente"


def test_editar_concluida_sem_data(ligacao):
    servico = criar_servico(ligacao)
    obra = criar_obra(servico)
    with pytest.raises(DadosObraInvalidos):
        servico.editar_obra(obra.id_obras, "Pintura do hall", "2026-03-01",
                            "", "concluida", 500.0, None)


def test_apagar_obra(ligacao):
    servico = criar_servico(ligacao)
    obra = criar_obra(servico)
    servico.apagar_obra(obra.id_obras)
    assert servico.listar_obras() == []
