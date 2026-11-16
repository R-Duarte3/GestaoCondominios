from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import date

from rd_condominios.base_dados import ligar
from rd_condominios.config import obter_caminho_bd
from rd_condominios.dominio.quota import DadosQuotaInvalidos, QuotaDuplicada
from rd_condominios.repositorios.quota_repositorio import QuotaRepositorio
from rd_condominios.repositorios.moradia_repositorio import MoradiaRepositorio
from rd_condominios.servicos.quota_servico import QuotaServico

quotas_bp = Blueprint("quotas", __name__, url_prefix="/quotas")


def construir_servico(ligacao):
    repositorio = QuotaRepositorio(ligacao)
    moradia_repositorio = MoradiaRepositorio(ligacao)
    return QuotaServico(repositorio, moradia_repositorio)


def dados_em_branco():
    return {
        "id_moradia": "",
        "ano": "",
        "mes": "",
        "valor": "",
        "data_vencimento": "",
        "data_pagamento": "",
    }


def ler_formulario():
    return {
        "id_moradia": request.form.get("id_moradia", ""),
        "ano": request.form.get("ano", ""),
        "mes": request.form.get("mes", ""),
        "valor": request.form.get("valor", ""),
        "data_vencimento": request.form.get("data_vencimento", ""),
        "data_pagamento": request.form.get("data_pagamento", ""),
    }


def converter_numeros(dados):
    try:
        id_moradia = int(dados["id_moradia"])
        ano = int(dados["ano"])
        mes = int(dados["mes"])
        valor = float(dados["valor"])
    except ValueError:
        raise DadosQuotaInvalidos(
            "Preencher corretamente os dados.")
    return id_moradia, ano, mes, valor


def apresentar_formulario(servico, dados, titulo, acao, erro=None, mostrar_pagamento=False):
    moradias = servico.listar_moradias()
    return render_template(
        "quotas/formulario.html",
        titulo=titulo,
        acao=acao,
        erro=erro,
        mostrar_pagamento=mostrar_pagamento,
        moradias=moradias,
        **dados,
    )


@quotas_bp.route("/")
def listar():
    ligacao = ligar(obter_caminho_bd())
    try:
        servico = construir_servico(ligacao)
        quotas = servico.listar_quotas()
    finally:
        ligacao.close()
    return render_template("quotas/lista.html", quotas=quotas, hoje=date.today().isoformat())


@quotas_bp.route("/nova")
def formulario():
    ligacao = ligar(obter_caminho_bd())
    try:
        servico = construir_servico(ligacao)
        return apresentar_formulario(
            servico,
            dados_em_branco(),
            "Registar quota",
            url_for("quotas.criar"),
        )
    finally:
        ligacao.close()


@quotas_bp.route("/", methods=["POST"])
def criar():
    dados = ler_formulario()

    ligacao = ligar(obter_caminho_bd())
    try:
        servico = construir_servico(ligacao)
        try:
            id_moradia, ano, mes, valor = converter_numeros(dados)
            servico.criar_quota(id_moradia, ano, mes, valor,
                                dados["data_vencimento"])
        except (DadosQuotaInvalidos, QuotaDuplicada) as erro:
            return apresentar_formulario(
                servico,
                dados,
                "Registar quota",
                url_for("quotas.criar"),
                erro=str(erro),
            )
    finally:
        ligacao.close()

    flash("Quota registada com sucesso.")
    return redirect(url_for("quotas.listar"))


@quotas_bp.route("/<int:id_quotas>/editar")
def formulario_editar(id_quotas):
    ligacao = ligar(obter_caminho_bd())
    try:
        servico = construir_servico(ligacao)
        quota = servico.obter_quota(id_quotas)
        if quota is None:
            flash("A quota indicada não existe!", "erro")
            return redirect(url_for("quotas.listar"))
        dados = {
            "id_moradia": str(quota.id_moradia),
            "ano": quota.ano,
            "mes": str(quota.mes),
            "valor": quota.valor,
            "data_vencimento": quota.data_vencimento,
            "data_pagamento": quota.data_pagamento,
        }
        return apresentar_formulario(
            servico,
            dados,
            "Editar quota",
            url_for("quotas.editar", id_quotas=id_quotas),
            mostrar_pagamento=True,
        )
    finally:
        ligacao.close()


@quotas_bp.route("/<int:id_quotas>/editar", methods=["POST"])
def editar(id_quotas):
    dados = ler_formulario()

    ligacao = ligar(obter_caminho_bd())
    try:
        servico = construir_servico(ligacao)
        try:
            id_moradia, ano, mes, valor = converter_numeros(dados)
            servico.editar_quota(id_quotas, id_moradia, ano, mes, valor,
                                 dados["data_vencimento"], dados["data_pagamento"])
        except (DadosQuotaInvalidos, QuotaDuplicada) as erro:
            return apresentar_formulario(
                servico,
                dados,
                "Editar quota",
                url_for("quotas.editar", id_quotas=id_quotas),
                erro=str(erro),
                mostrar_pagamento=True,
            )
    finally:
        ligacao.close()

    flash("Quota atualizada com sucesso!")
    return redirect(url_for("quotas.listar"))


@quotas_bp.route("/<int:id_quotas>/apagar", methods=["POST"])
def apagar(id_quotas):
    ligacao = ligar(obter_caminho_bd())
    try:
        servico = construir_servico(ligacao)
        try:
            servico.apagar_quota(id_quotas)
        except DadosQuotaInvalidos as erro:
            flash(str(erro), "erro")
            return redirect(url_for("quotas.listar"))
    finally:
        ligacao.close()

    flash("Quota apagada com sucesso!")
    return redirect(url_for("quotas.listar"))


@quotas_bp.route("/pagar/<int:id_quotas>", methods=["POST"])
def pagar(id_quotas):
    data_pagamento = request.form.get("data_pagamento", "")

    ligacao = ligar(obter_caminho_bd())
    try:
        servico = construir_servico(ligacao)
        servico.registar_pagamento(id_quotas, data_pagamento)
    finally:
        ligacao.close()

    flash("Pagamento registado com sucesso!")
    return redirect(url_for("quotas.listar"))
