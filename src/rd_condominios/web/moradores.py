from flask import Blueprint, render_template, request, redirect, url_for, flash

from rd_condominios.base_dados import ligar
from rd_condominios.config import obter_caminho_bd
from rd_condominios.dominio.morador import DadosMoradorInvalidos, NifDuplicado
from rd_condominios.repositorios.morador_repositorio import MoradorRepositorio
from rd_condominios.repositorios.moradia_repositorio import MoradiaRepositorio
from rd_condominios.servicos.morador_servico import MoradorServico

moradores_bp = Blueprint('moradores', __name__, url_prefix="/moradores")


def construir_servico(ligacao):
    repositorio = MoradorRepositorio(ligacao)
    moradia_repositorio = MoradiaRepositorio(ligacao)
    return MoradorServico(repositorio, moradia_repositorio)


@moradores_bp.route("/")
def listar():
    ligacao = ligar(obter_caminho_bd())
    try:
        servico = construir_servico(ligacao)
        moradores = servico.listar_moradores()
    finally:
        ligacao.close()
    return render_template("moradores/lista.html", moradores=moradores)


@moradores_bp.route("/novo")
def formulario():
    ligacao = ligar(obter_caminho_bd())
    try:
        servico = construir_servico(ligacao)
        moradias = servico.listar_moradias()
    finally:
        ligacao.close()
    return render_template("moradores/formulario.html",
                           erro=None,
                           nome="",
                           nif="",
                           telefone="",
                           email="",
                           tipo="",
                           id_moradia="",
                           moradias=moradias
                           )


@moradores_bp.route("/", methods=["POST"])
def criar():
    nome = request.form.get("nome", "")
    nif = request.form.get("nif", "")
    telefone = request.form.get("telefone", "")
    email = request.form.get("email", "")
    tipo = request.form.get("tipo", "")
    id_moradia_texto = request.form.get("id_moradia", "")

    ligacao = ligar(obter_caminho_bd())
    try:
        servico = construir_servico(ligacao)
        try:
            id_moradia = int(id_moradia_texto)
        except ValueError:
            raise DadosMoradorInvalidos("Tem de escolher uma moradia.")
        servico.criar_morador(nome, nif, telefone, email, tipo, id_moradia)
    except (DadosMoradorInvalidos, NifDuplicado) as erro:
        moradias = servico.listar_moradias()
        return render_template("moradores/formulario.html",
                               erro=str(erro),
                               nome=nome,
                               nif=nif,
                               telefone=telefone,
                               email=email,
                               tipo=tipo,
                               id_moradia=id_moradia_texto,
                               moradias=moradias
                               )
    finally:
        ligacao.close()

    flash("Morador registado com sucesso!")
    return redirect(url_for("moradores.listar"))
