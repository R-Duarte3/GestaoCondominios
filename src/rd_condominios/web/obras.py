from flask import Blueprint, render_template, request, redirect, url_for, flash

from rd_condominios.base_dados import ligar
from rd_condominios.config import obter_caminho_bd
from rd_condominios.dominio.obra import DadosObraInvalidos
from rd_condominios.repositorios.obra_repositorio import ObraRepositorio
from rd_condominios.servicos.obra_servico import ObraServico

obras_bp = Blueprint("obras", __name__, url_prefix="/obras")

NOMES_ESTADOS = {
    "pendente": "Pendente",
    "em_curso": "Em curso",
    "concluida": "Concluída",
}


def construir_servico(ligacao):
    repositorio = ObraRepositorio(ligacao)
    return ObraServico(repositorio)


def converter_valor(texto, mensagem_erro):
    texto = texto.strip()
    if not texto:
        return None
    try:
        return float(texto)
    except ValueError:
        raise DadosObraInvalidos(mensagem_erro)


@obras_bp.route("/")
def listar():
    ligacao = ligar(obter_caminho_bd())
    try:
        servico = construir_servico(ligacao)
        obras = servico.listar_obras()
        estados = servico.listar_estados()
    finally:
        ligacao.close()
    return render_template("obras/lista.html",
                           obras=obras,
                           estados=estados,
                           nomes_estados=NOMES_ESTADOS,
                           erro=None)


@obras_bp.route("/nova")
def formulario():
    return render_template("obras/formulario.html",
                           erro=None,
                           descricao="",
                           data_pedido="",
                           orcamento="",
                           )


@obras_bp.route("/", methods=["POST"])
def criar():
    descricao = request.form.get("descricao", "")
    data_pedido = request.form.get("data_pedido", "")
    orcamento_texto = request.form.get("orcamento", "")

    ligacao = ligar(obter_caminho_bd())
    try:
        servico = construir_servico(ligacao)
        orcamento = converter_valor(
            orcamento_texto, "O orçamento indicado não é válido!")
        servico.criar_obra(descricao, data_pedido, orcamento)
    except DadosObraInvalidos as erro:
        return render_template(
            "obras/formulario.html",
            erro=str(erro),
            descricao=descricao,
            data_pedido=data_pedido,
            orcamento=orcamento_texto,
        )
    finally:
        ligacao.close()

    flash("Obra registada com sucesso!")
    return redirect(url_for("obras.listar"))


@obras_bp.route("/estado/<int:id_obras>", methods=["POST"])
def atualizar_estado(id_obras):
    estado = request.form.get("estado", "")
    data_conclusao = request.form.get("data_conclusao", "")
    custo_texto = request.form.get("custo_final", "")

    ligacao = ligar(obter_caminho_bd())
    try:
        servico = construir_servico(ligacao)
        custo_final = converter_valor(
            custo_texto, "O custo final indicado não é válido!")
        servico.atualizar_estado(id_obras, estado, data_conclusao, custo_final)
    except DadosObraInvalidos as erro:
        obras = servico.listar_obras()
        estados = servico.listar_estados()
        return render_template("obras/lista.html",
                               obras=obras,
                               estados=estados,
                               nomes_estados=NOMES_ESTADOS,
                               erro=str(erro))
    finally:
        ligacao.close()

    flash("Estado da obra atualizado com sucesso!")
    return redirect(url_for("obras.listar"))
