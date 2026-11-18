import pytest

from rd_condominios.dominio.morador import Morador, DadosMoradorInvalidos, NifDuplicado
from rd_condominios.dominio.moradia import MoradiaEmUso
from rd_condominios.repositorios.morador_repositorio import MoradorRepositorio
from rd_condominios.repositorios.moradia_repositorio import MoradiaRepositorio
from rd_condominios.servicos.morador_servico import MoradorServico
from rd_condominios.servicos.moradia_servico import MoradiaServico


def criar_servico(ligacao):
    return MoradorServico(MoradorRepositorio(ligacao), MoradiaRepositorio(ligacao))


def criar_moradia(ligacao, identificacao="1.º Esq"):
    servico = MoradiaServico(MoradiaRepositorio(ligacao))
    return servico.criar_moradia(identificacao, "1", "T2", "")


def criar_morador(servico, id_moradia, nome="Ana Teste", nif="123456789"):
    return servico.criar_morador(nome, nif, "", "", "proprietario", id_moradia, "2026-01-01")

# Validacao obrigatoria___________________________________________
# DOMINIO__________________________________________________________


def test_morador_sem_nome():
    with pytest.raises(DadosMoradorInvalidos):
        Morador(None, "", "123456789", "", "",
                "proprietario", 1, "2026-01-01", "")


def test_nif_com_menos_de_9_algarismos():
    with pytest.raises(DadosMoradorInvalidos):
        Morador(None, "Ana Teste", "12345678", "", "",
                "proprietario", 1, "2026-01-01", "")


def test_nif_com_letras():
    with pytest.raises(DadosMoradorInvalidos):
        Morador(None, "Ana Teste", "12345678A", "", "",
                "proprietario", 1, "2026-01-01", "")


def test_morador_sem_data_de_entrada():
    with pytest.raises(DadosMoradorInvalidos):
        Morador(None, "Ana Teste", "123456789",
                "", "", "proprietario", 1, "", "")


def test_saida_antes_da_entrada():
    with pytest.raises(DadosMoradorInvalidos):
        Morador(None, "Ana Teste", "123456789", "", "",
                "proprietario", 1, "2026-05-01", "2026-04-01")


# REGRA NIF DUPLICADO__________________________________________________________

def test_criar_morador_valido(ligacao):
    moradia = criar_moradia(ligacao)
    servico = criar_servico(ligacao)
    morador = criar_morador(servico, moradia.id_moradia)
    assert morador.id_moradores is not None
    assert len(servico.listar_moradores()) == 1


def test_nif_duplicado(ligacao):
    moradia = criar_moradia(ligacao)
    servico = criar_servico(ligacao)
    criar_morador(servico, moradia.id_moradia)
    with pytest.raises(NifDuplicado):
        criar_morador(servico, moradia.id_moradia, nome="Bruno Teste")
    assert len(servico.listar_moradores()) == 1


# MORADIA INEXISTENTE__________________________________________________________

def test_morador_com_moradia_inexistente(ligacao):
    servico = criar_servico(ligacao)
    with pytest.raises(DadosMoradorInvalidos):
        criar_morador(servico, 999)


# TESTAR SAIDA__________________________________________________________

def test_registar_saida(ligacao):
    moradia = criar_moradia(ligacao)
    servico = criar_servico(ligacao)
    morador = criar_morador(servico, moradia.id_moradia)
    servico.registar_saida(morador.id_moradores, "2026-06-01")
    assert servico.obter_morador(
        morador.id_moradores).data_saida == "2026-06-01"


def test_registar_saida_antes_da_entrada(ligacao):
    moradia = criar_moradia(ligacao)
    servico = criar_servico(ligacao)
    morador = criar_morador(servico, moradia.id_moradia)
    with pytest.raises(DadosMoradorInvalidos):
        servico.registar_saida(morador.id_moradores, "2025-12-01")


# MORADIA COM MORADORES NAO APAGA__________________________________________________________

def test_nao_apaga_moradia_com_moradores(ligacao):
    moradia = criar_moradia(ligacao)
    criar_morador(criar_servico(ligacao), moradia.id_moradia)
    servico_moradia = MoradiaServico(MoradiaRepositorio(ligacao))
    with pytest.raises(MoradiaEmUso):
        servico_moradia.apagar_moradia(moradia.id_moradia)
