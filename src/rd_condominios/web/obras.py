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


def texto_ou_vazio(valor):
    if valor is None:
        return ""
    return valor


def dados_em_branco():
    return {
        "descricao": "",
        "data_pedido": "",
        "data_conclusao": "",
        "estado": "pendente",
        "orcamento": "",
        "custo_final": "",
    }


def ler_formulario():
    return {
        "descricao": request.form.get("descricao", ""),
        "data_pedido": request.form.get("data_pedido", ""),
        "data_conclusao": request.form.get("data_conclusao", ""),
        "estado": request.form.get("estado", "pendente"),
        "orcamento": request.form.get("orcamento", ""),
        "custo_final": request.form.get("custo_final", ""),
    }


def apresentar_formulario(servico, dados, titulo, acao, erro=None,
                          mostrar_estado=False):
    return render_template(
        "obras/formulario.html",
        titulo=titulo,
        acao=acao,
        erro=erro,
        mostrar_estado=mostrar_estado,
        descricao=dados["descricao"],
        data_pedido=dados["data_pedido"],
        data_conclusao=dados["data_conclusao"],
        estado=dados["estado"],
        orcamento=dados["orcamento"],
        custo_final=dados["custo_final"],
        estados=servico.listar_estados(),
        nomes_estados=NOMES_ESTADOS,
    )


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
    ligacao = ligar(obter_caminho_bd())
    try:
        servico = construir_servico(ligacao)
        return apresentar_formulario(
            servico,
            dados_em_branco(),
            "Registar obra",
            url_for("obras.criar"),
        )
    finally:
        ligacao.close()


@obras_bp.route("/", methods=["POST"])
def criar():
    dados = ler_formulario()

    ligacao = ligar(obter_caminho_bd())
    try:
        servico = construir_servico(ligacao)
        try:
            orcamento = converter_valor(
                dados["orcamento"], "O orçamento indicado não é válido!")
            servico.criar_obra(dados["descricao"], dados["data_pedido"],
                               orcamento)
        except DadosObraInvalidos as erro:
            return apresentar_formulario(
                servico,
                dados,
                "Registar obra",
                url_for("obras.criar"),
                erro=str(erro),
            )
    finally:
        ligacao.close()

    flash("Obra registada com sucesso!")
    return redirect(url_for("obras.listar"))


@obras_bp.route("/<int:id_obras>/editar")
def formulario_editar(id_obras):
    ligacao = ligar(obter_caminho_bd())
    try:
        servico = construir_servico(ligacao)
        obra = servico.obter_obra(id_obras)
        if obra is None:
            flash("A obra indicada não existe!", "erro")
            return redirect(url_for("obras.listar"))
        dados = {
            "descricao": obra.descricao,
            "data_pedido": obra.data_pedido,
            "data_conclusao": obra.data_conclusao,
            "estado": obra.estado,
            "orcamento": texto_ou_vazio(obra.orcamento),
            "custo_final": texto_ou_vazio(obra.custo_final),
        }
        return apresentar_formulario(
            servico,
            dados,
            "Editar obra",
            url_for("obras.editar", id_obras=id_obras),
            mostrar_estado=True,
        )
    finally:
        ligacao.close()


@obras_bp.route("/<int:id_obras>/editar", methods=["POST"])
def editar(id_obras):
    dados = ler_formulario()

    ligacao = ligar(obter_caminho_bd())
    try:
        servico = construir_servico(ligacao)
        try:
            orcamento = converter_valor(
                dados["orcamento"], "O orçamento indicado não é válido!")
            custo_final = converter_valor(
                dados["custo_final"], "O custo final indicado não é válido!")
            servico.editar_obra(id_obras, dados["descricao"],
                                dados["data_pedido"], dados["data_conclusao"],
                                dados["estado"], orcamento, custo_final)
        except DadosObraInvalidos as erro:
            return apresentar_formulario(
                servico,
                dados,
                "Editar obra",
                url_for("obras.editar", id_obras=id_obras),
                erro=str(erro),
                mostrar_estado=True,
            )
    finally:
        ligacao.close()

    flash("Obra atualizada com sucesso!")
    return redirect(url_for("obras.listar"))


@obras_bp.route("/<int:id_obras>/apagar", methods=["POST"])
def apagar(id_obras):
    ligacao = ligar(obter_caminho_bd())
    try:
        servico = construir_servico(ligacao)
        try:
            servico.apagar_obra(id_obras)
        except DadosObraInvalidos as erro:
            flash(str(erro), "erro")
            return redirect(url_for("obras.listar"))
    finally:
        ligacao.close()

    flash("Obra apagada com sucesso!")
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
