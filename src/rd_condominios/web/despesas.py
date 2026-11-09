from flask import Blueprint, render_template, request, redirect, url_for, flash

from rd_condominios.base_dados import ligar
from rd_condominios.config import obter_caminho_bd
from rd_condominios.dominio.despesa import DadosDespesaInvalidos
from rd_condominios.repositorios.despesa_repositorio import DespesaRepositorio
from rd_condominios.servicos.despesa_servico import DespesaServico

despesas_bp = Blueprint("despesas", __name__, url_prefix="/despesas")

NOMES_CATEGORIAS = {
    "limpeza": "Limpeza",
    "seguro": "Seguro",
    "agua": "Água",
    "eletricidade": "Eletricidade",
    "obra": "Obra",
    "outras": "Outras",
}


def construir_servico(ligacao):
    repositorio = DespesaRepositorio(ligacao)
    return DespesaServico(repositorio)


@despesas_bp.route("/")
def listar():
    ligacao = ligar(obter_caminho_bd())
    try:
        servico = construir_servico(ligacao)
        despesas = servico.listar_despesas()
    finally:
        ligacao.close()
    return render_template("despesas/lista.html",
                           despesas=despesas,
                           nomes_categorias=NOMES_CATEGORIAS)


@despesas_bp.route("/nova")
def formulario():
    ligacao = ligar(obter_caminho_bd())
    try:
        servico = construir_servico(ligacao)
        categorias = servico.listar_categorias()
    finally:
        ligacao.close()
    return render_template("despesas/formulario.html",
                           erro=None,
                           descricao="",
                           categoria="",
                           valor="",
                           data="",
                           fornecedor="",
                           categorias=categorias,
                           nomes_categorias=NOMES_CATEGORIAS,
                           )


@despesas_bp.route("/", methods=["POST"])
def criar():
    descricao = request.form.get("descricao", "")
    categoria = request.form.get("categoria", "")
    valor_texto = request.form.get("valor", "")
    data = request.form.get("data", "")
    fornecedor = request.form.get("fornecedor", "")

    ligacao = ligar(obter_caminho_bd())
    try:
        servico = construir_servico(ligacao)
        try:
            valor = float(valor_texto)
        except ValueError:
            raise DadosDespesaInvalidos("O valor indicado não é válido!")
        servico.criar_despesa(descricao, categoria, valor, data, fornecedor)
    except DadosDespesaInvalidos as erro:
        categorias = servico.listar_categorias()
        return render_template(
            "despesas/formulario.html",
            erro=str(erro),
            descricao=descricao,
            categoria=categoria,
            valor=valor_texto,
            data=data,
            fornecedor=fornecedor,
            categorias=categorias,
            nomes_categorias=NOMES_CATEGORIAS,
        )
    finally:
        ligacao.close()

    flash("Despesa registada com sucesso!")
    return redirect(url_for("despesas.listar"))
