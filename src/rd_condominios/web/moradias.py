from flask import Blueprint, render_template, request, redirect, url_for, flash
from rd_condominios.base_dados import ligar
from rd_condominios.config import obter_caminho_bd
from rd_condominios.dominio.moradia import DadosMoradiaInvalidos, IdentificacaoDuplicada, MoradiaEmUso
from rd_condominios.repositorios.moradia_repositorio import MoradiaRepositorio
from rd_condominios.servicos.moradia_servico import MoradiaServico

moradias_bp = Blueprint("moradias", __name__, url_prefix="/moradias")


def construir_servico(ligacao):
    repositorio = MoradiaRepositorio(ligacao)
    return MoradiaServico(repositorio)


def apresentar_formulario(titulo, acao, erro, identificacao, andar, tipologia, observacoes):
    return render_template(
        "moradias/formulario.html",
        titulo=titulo,
        acao=acao,
        erro=erro,
        identificacao=identificacao,
        andar=andar,
        tipologia=tipologia,
        observacoes=observacoes,
    )


@moradias_bp.route("/")
def listar():
    ligacao = ligar(obter_caminho_bd())
    try:
        servico = construir_servico(ligacao)
        moradias = servico.listar_moradias()
    finally:
        ligacao.close()
    return render_template("moradias/lista.html", moradias=moradias)


@moradias_bp.route("/nova")
def formulario():
    return apresentar_formulario("Registar moradia", url_for("moradias.criar"), None, "", "", "", "")


@moradias_bp.route("/", methods=["POST"])
def criar():
    identificacao = request.form.get("identificacao", "")
    andar = request.form.get("andar", "")
    tipologia = request.form.get("tipologia", "")
    observacoes = request.form.get("observacoes", "")

    ligacao = ligar(obter_caminho_bd())
    try:
        servico = construir_servico(ligacao)
        servico.criar_moradia(identificacao, andar, tipologia, observacoes)
    except (DadosMoradiaInvalidos, IdentificacaoDuplicada) as erro:
        return apresentar_formulario("Registar moradia", url_for("moradias.criar"), str(erro), identificacao, andar, tipologia, observacoes)
    finally:
        ligacao.close()

    flash("Moradia registada com sucesso!")
    return redirect(url_for("moradias.listar"))


@moradias_bp.route("/<int:id_moradia>/editar")
def formulario_editar(id_moradia):
    ligacao = ligar(obter_caminho_bd())
    try:
        servico = construir_servico(ligacao)
        moradia = servico.obter_moradia(id_moradia)
    except DadosMoradiaInvalidos as erro:
        flash(str(erro), "erro")
        return redirect(url_for("moradias.listar"))
    finally:
        ligacao.close()

    return apresentar_formulario(
        "Editar moradia",
        url_for("moradias.editar", id_moradia=id_moradia),
        None,
        moradia.identificacao, moradia.andar,
        moradia.tipologia, moradia.observacoes)


@moradias_bp.route("/<int:id_moradia>/editar", methods=["POST"])
def editar(id_moradia):
    identificacao = request.form.get("identificacao", "")
    andar = request.form.get("andar", "")
    tipologia = request.form.get("tipologia", "")
    observacoes = request.form.get("observacoes", "")

    ligacao = ligar(obter_caminho_bd())
    try:
        servico = construir_servico(ligacao)
        servico.editar_moradia(id_moradia, identificacao,
                               andar, tipologia, observacoes)
    except (DadosMoradiaInvalidos, IdentificacaoDuplicada) as erro:
        return apresentar_formulario(
            "Editar moradia",
            url_for("moradias.editar", id_moradia=id_moradia),
            str(erro), identificacao, andar, tipologia, observacoes)
    finally:
        ligacao.close()

    flash("Moradia atualizada com sucesso!")
    return redirect(url_for("moradias.listar"))


@moradias_bp.route("/<int:id_moradia>/apagar", methods=["POST"])
def apagar(id_moradia):
    ligacao = ligar(obter_caminho_bd())
    try:
        servico = construir_servico(ligacao)
        servico.apagar_moradia(id_moradia)
    except (DadosMoradiaInvalidos, MoradiaEmUso) as erro:
        flash(str(erro), "erro")
        return redirect(url_for("moradias.listar"))
    finally:
        ligacao.close()

    flash("Moradia apagada com sucesso!")
    return redirect(url_for("moradias.listar"))
