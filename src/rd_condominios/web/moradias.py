from flask import Blueprint, render_template, request, redirect, url_for, flash
from rd_condominios.base_dados import ligar
from rd_condominios.config import obter_caminho_bd
from rd_condominios.dominio.moradia import DadosMoradiaInvalidos, IdentificacaoDuplicada
from rd_condominios.repositorios.moradia_repositorio import MoradiaRepositorio
from rd_condominios.servicos.moradia_servico import MoradiaServico

moradias_bp = Blueprint("moradias", __name__, url_prefix="/moradias")


def construir_servico(ligacao):
    repositorio = MoradiaRepositorio(ligacao)
    return MoradiaServico(repositorio)


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
    return render_template("moradias/formulario.html",
                           erro=None,
                           identificacao="",
                           andar="",
                           tipologia="",
                           observacoes="",
                           )


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
        return render_template(
            "moradias/formulario.html",
            erro=str(erro),
            identificacao=identificacao,
            andar=andar,
            tipologia=tipologia,
            observacoes=observacoes,
        )
    finally:
        ligacao.close()

    flash("Moradia registada com sucesso!")
    return redirect(url_for("moradias.listar"))
