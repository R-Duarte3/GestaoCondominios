from flask import Blueprint, render_template, request, redirect, url_for, flash

from rd_condominios.base_dados import ligar
from rd_condominios.config import obter_caminho_bd
from rd_condominios.dominio.despesa import DadosDespesaInvalidos
from rd_condominios.repositorios.despesa_repositorio import DespesaRepositorio
from rd_condominios.servicos.despesa_servico import DespesaServico
from rd_condominios.repositorios.moradia_repositorio import MoradiaRepositorio

despesas_bp = Blueprint("despesas", __name__, url_prefix="/despesas")

NOMES_CATEGORIAS = {
    "limpeza": "Limpeza",
    "seguro": "Seguro",
    "agua": "Água",
    "eletricidade": "Eletricidade",
    "outras": "Outras",
}


def construir_servico(ligacao):
    repositorio = DespesaRepositorio(ligacao)
    moradia_repositorio = MoradiaRepositorio(ligacao)
    return DespesaServico(repositorio, moradia_repositorio)


def dados_em_branco():
    return {
        "descricao": "",
        "categoria": "",
        "valor": "",
        "data": "",
        "fornecedor": "",
    }


def ler_formulario():
    return {
        "descricao": request.form.get("descricao", ""),
        "categoria": request.form.get("categoria", ""),
        "valor": request.form.get("valor", ""),
        "data": request.form.get("data", ""),
        "fornecedor": request.form.get("fornecedor", ""),
    }


def converter_valor(dados):
    try:
        return float(dados["valor"])
    except ValueError:
        raise DadosDespesaInvalidos("O valor indicado não é válido!")


def apresentar_formulario(servico, dados, titulo, acao, erro=None):
    return render_template(
        "despesas/formulario.html",
        titulo=titulo,
        acao=acao,
        erro=erro,
        descricao=dados["descricao"],
        categoria=dados["categoria"],
        valor=dados["valor"],
        data=dados["data"],
        fornecedor=dados["fornecedor"],
        categorias=servico.listar_categorias(),
        nomes_categorias=NOMES_CATEGORIAS,
    )


@despesas_bp.route("/")
def listar():
    ligacao = ligar(obter_caminho_bd())
    try:
        servico = construir_servico(ligacao)
        despesas = servico.listar_despesas()
        numero_moradias = servico.numero_moradias()
    finally:
        ligacao.close()
    return render_template("despesas/lista.html",
                           despesas=despesas,
                           numero_moradias=numero_moradias,
                           nomes_categorias=NOMES_CATEGORIAS)


@despesas_bp.route("/nova")
def formulario():
    ligacao = ligar(obter_caminho_bd())
    try:
        servico = construir_servico(ligacao)
        return apresentar_formulario(
            servico,
            dados_em_branco(),
            "Registar despesa",
            url_for("despesas.criar"),
        )
    finally:
        ligacao.close()


@despesas_bp.route("/", methods=["POST"])
def criar():
    dados = ler_formulario()

    ligacao = ligar(obter_caminho_bd())
    try:
        servico = construir_servico(ligacao)
        try:
            valor = converter_valor(dados)
            servico.criar_despesa(
                dados["descricao"], dados["categoria"], valor, dados["data"], dados["fornecedor"])
        except DadosDespesaInvalidos as erro:
            return apresentar_formulario(
                servico,
                dados,
                "Registar despesa",
                url_for("despesa.criar"),
                erro=str(erro),
            )
    finally:
        ligacao.close()

    flash("Despesa registada com sucesso!")
    return redirect(url_for("despesas.listar"))


@despesas_bp.route("/<int:id_despesas>/editar")
def formulario_editar(id_despesas):
    ligacao = ligar(obter_caminho_bd())
    try:
        servico = construir_servico(ligacao)
        despesa = servico.obter_despesa(id_despesas)
        if despesa is None:
            flash("A despesa indicada não existe!", "erro")
            return redirect(url_for("despesas.listar"))
        dados = {
            "descricao": despesa.descricao,
            "categoria": despesa.categoria,
            "valor": despesa.valor,
            "data": despesa.data,
            "fornecedor": despesa.fornecedor,
        }
        return apresentar_formulario(
            servico,
            dados,
            "Editar despesa",
            url_for("despesas.editar", id_despesas=id_despesas),
        )
    finally:
        ligacao.close()


@despesas_bp.route("/<int:id_despesas>/editar", methods=["POST"])
def editar(id_despesas):
    dados = ler_formulario()

    ligacao = ligar(obter_caminho_bd())
    try:
        servico = construir_servico(ligacao)
        try:
            valor = converter_valor(dados)
            servico.editar_despesa(id_despesas, dados["descricao"],
                                   dados["categoria"], valor, dados["data"],
                                   dados["fornecedor"])
        except DadosDespesaInvalidos as erro:
            return apresentar_formulario(
                servico,
                dados,
                "Editar despesa",
                url_for("despesas.editar", id_despesas=id_despesas),
                erro=str(erro),
            )
    finally:
        ligacao.close()

    flash("Despesa atualizada com sucesso!")
    return redirect(url_for("despesas.listar"))


@despesas_bp.route("/<int:id_despesas>/apagar", methods=["POST"])
def apagar(id_despesas):
    ligacao = ligar(obter_caminho_bd())
    try:
        servico = construir_servico(ligacao)
        try:
            servico.apagar_despesa(id_despesas)
        except DadosDespesaInvalidos as erro:
            flash(str(erro), "erro")
            return redirect(url_for("despesas.listar"))
    finally:
        ligacao.close()

    flash("Despesa apagada com sucesso!")
    return redirect(url_for("despesas.listar"))
