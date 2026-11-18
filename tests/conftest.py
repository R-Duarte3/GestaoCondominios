import pytest

from rd_condominios.base_dados import inicializar, ligar


@pytest.fixture
def ligacao(tmp_path):
    caminho = tmp_path / "teste.db"
    inicializar(caminho)
    ligacao = ligar(caminho)
    yield ligacao
    ligacao.close()
