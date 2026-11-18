import pytest

from rd_condominios.dominio.quota import Quota, DadosQuotaInvalidos, QuotaDuplicada
from rd_condominios.repositorios.quota_repositorio import QuotaRepositorio
from rd_condominios.repositorios.moradia_repositorio import MoradiaRepositorio
from rd_condominios.servicos.quota_servico import QuotaServico
from rd_condominios.servicos.moradia_servico import MoradiaServico


def criar_servico(ligacao):
    return QuotaServico(QuotaRepositorio(ligacao),
                        MoradiaRepositorio(ligacao))


def criar_moradia(ligacao, identificacao="1.º Esq"):
    servico = MoradiaServico(MoradiaRepositorio(ligacao))
    return servico.criar_moradia(identificacao, "1", "T2", "")


def criar_quota(servico, id_moradia, mes=1):
    return servico.criar_quota(id_moradia, 2026, mes, 50.0, "2026-01-31")

# Validacao obrigatoria___________________________________________
# DOMINIO__________________________________________________________


def test_mes_zero():
    with pytest.raises(DadosQuotaInvalidos):
        Quota(None, 1, 2026, 0, 50.0, "2026-01-31", "")


def test_mes_treze():
    with pytest.raises(DadosQuotaInvalidos):
        Quota(None, 1, 2026, 13, 50.0, "2026-01-31", "")


def test_valor_zero():
    with pytest.raises(DadosQuotaInvalidos):
        Quota(None, 1, 2026, 1, 0, "2026-01-31", "")


def test_valor_negativo():
    with pytest.raises(DadosQuotaInvalidos):
        Quota(None, 1, 2026, 1, -10.0, "2026-01-31", "")


def test_quota_sem_data_de_vencimento():
    with pytest.raises(DadosQuotaInvalidos):
        Quota(None, 1, 2026, 1, 50.0, "", "")

# ESTADO CALCULADO__________________________________________________________


def test_estado_pago():
    quota = Quota(None, 1, 2026, 1, 50.0, "2000-01-31", "2000-01-15")
    assert quota.estado() == "Pago"


def test_estado_em_atraso():
    quota = Quota(None, 1, 2000, 1, 50.0, "2000-01-31", "")
    assert quota.estado() == "Em atraso"


def test_estado_pendente():
    quota = Quota(None, 1, 2099, 1, 50.0, "2099-12-31", "")
    assert quota.estado() == "Pendente"

# DUPLICACAO__________________________________________________________


def test_criar_quota_valida(ligacao):
    moradia = criar_moradia(ligacao)
    servico = criar_servico(ligacao)
    quota = criar_quota(servico, moradia.id_moradia)
    assert quota.id_quotas is not None
    assert len(servico.listar_quotas()) == 1


def test_quota_duplicada(ligacao):
    moradia = criar_moradia(ligacao)
    servico = criar_servico(ligacao)
    criar_quota(servico, moradia.id_moradia)
    with pytest.raises(QuotaDuplicada):
        criar_quota(servico, moradia.id_moradia)
    assert len(servico.listar_quotas()) == 1


# PAGAMENTO E ESTADO__________________________________________________________

def test_registar_pagamento(ligacao):
    moradia = criar_moradia(ligacao)
    servico = criar_servico(ligacao)
    quota = criar_quota(servico, moradia.id_moradia)
    servico.registar_pagamento(quota.id_quotas, "2026-01-20")
    assert servico.obter_quota(quota.id_quotas).estado() == "Pago"


# EDITAR E APAGAR__________________________________________________________

def test_editar_quota_que_nao_existe(ligacao):
    moradia = criar_moradia(ligacao)
    servico = criar_servico(ligacao)
    with pytest.raises(DadosQuotaInvalidos):
        servico.editar_quota(999, moradia.id_moradia, 2026, 1, 50.0,
                             "2026-01-31", "")
