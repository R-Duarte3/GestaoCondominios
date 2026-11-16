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


def dados_em_branco():
    return {
        "nome": "",
        "nif": "",
        "telefone": "",
        "email": "",
        "tipo": "",
        "id_moradia": "",
        "data_entrada": "",
        "data_saida": "",
    }


def ler_formulario():
    dados = {}
    for campo in dados_em_branco():
        dados[campo] = request.form.get(campo, "")
    return dados


def converter_moradia(texto):
    try:
        return int(texto)
    except ValueError:
        raise DadosMoradorInvalidos("Tem de escolher uma moradia!")


def apresentar_formulario(servico, titulo, acao, erro, dados, mostrar_saida):
    return render_template(
        "moradores/formulario.html",
        titulo=titulo,
        acao=acao,
        erro=erro,
        mostrar_saida=mostrar_saida,
        moradias=servico.listar_moradias(),
        **dados,
    )


@moradores_bp.route("/")
def listar():
    ligacao = ligar(obter_caminho_bd())
    try:
        servico = construir_servico(ligacao)
        moradores = servico.listar_moradores()
    finally:
        ligacao.close()
    return render_template("moradores/lista.html", moradores=moradores, erro=None)


@moradores_bp.route("/novo")
def formulario():
    ligacao = ligar(obter_caminho_bd())
    try:
        servico = construir_servico(ligacao)
        return apresentar_formulario(
            servico, "Registar morador", url_for("moradores.criar"),
            None, dados_em_branco(), False)
    finally:
        ligacao.close()


@moradores_bp.route("/", methods=["POST"])
def criar():
    dados = ler_formulario()

    ligacao = ligar(obter_caminho_bd())
    try:
        servico = construir_servico(ligacao)
        servico.criar_morador(
            dados["nome"], dados["nif"], dados["telefone"], dados["email"], dados["tipo"], converter_moradia(dados["id_moradia"]), dados["data_entrada"])
    except (DadosMoradorInvalidos, NifDuplicado) as erro:
        return apresentar_formulario(
            servico, "Registar morador", url_for("moradores.criar"), str(erro), dados, False)
    finally:
        ligacao.close()

    flash("Morador registado com sucesso!")
    return redirect(url_for("moradores.listar"))


@moradores_bp.route("/<int:id_moradores>/editar")
def formulario_editar(id_moradores):
    ligacao = ligar(obter_caminho_bd())
    try:
        servico = construir_servico(ligacao)
        morador = servico.obter_morador(id_moradores)
        dados = {
            "nome": morador.nome,
            "nif": morador.nif,
            "telefone": morador.telefone,
            "email": morador.email,
            "tipo": morador.tipo,
            "id_moradia": str(morador.id_moradia),
            "data_entrada": morador.data_entrada,
            "data_saida": morador.data_saida,
        }
        return apresentar_formulario(
            servico, "Editar morador",
            url_for("moradores.editar", id_moradores=id_moradores),
            None, dados, True)
    except DadosMoradorInvalidos as erro:
        flash(str(erro), "erro")
        return redirect(url_for("moradores.listar"))
    finally:
        ligacao.close()


@moradores_bp.route("/<int:id_moradores>/editar", methods=["POST"])
def editar(id_moradores):
    dados = ler_formulario()

    ligacao = ligar(obter_caminho_bd())
    try:
        servico = construir_servico(ligacao)
        servico.editar_morador(
            id_moradores, dados["nome"], dados["nif"], dados["telefone"],
            dados["email"], dados["tipo"],
            converter_moradia(dados["id_moradia"]),
            dados["data_entrada"], dados["data_saida"])
    except (DadosMoradorInvalidos, NifDuplicado) as erro:
        return apresentar_formulario(
            servico, "Editar morador",
            url_for("moradores.editar", id_moradores=id_moradores),
            str(erro), dados, True)
    finally:
        ligacao.close()

    flash("Morador atualizado com sucesso!")
    return redirect(url_for("moradores.listar"))


@moradores_bp.route("/<int:id_moradores>/apagar", methods=["POST"])
def apagar(id_moradores):
    ligacao = ligar(obter_caminho_bd())
    try:
        servico = construir_servico(ligacao)
        servico.apagar_morador(id_moradores)
    except DadosMoradorInvalidos as erro:
        flash(str(erro), "erro")
        return redirect(url_for("moradores.listar"))
    finally:
        ligacao.close()

    flash("Morador apagado com sucesso!")
    return redirect(url_for("moradores.listar"))


@moradores_bp.route("/saida/<int:id_moradores>", methods=["POST"])
def registar_saida(id_moradores):
    data_saida = request.form.get("data_saida", "")

    ligacao = ligar(obter_caminho_bd())
    try:
        servico = construir_servico(ligacao)
        servico.registar_saida(id_moradores, data_saida)
    except DadosMoradorInvalidos as erro:
        moradores = servico.listar_moradores()
        return render_template("moradores/lista.html",
                               moradores=moradores,
                               erro=str(erro))
    finally:
        ligacao.close()

    flash("Saída do morador registada com sucesso!")
    return redirect(url_for("moradores.listar"))
