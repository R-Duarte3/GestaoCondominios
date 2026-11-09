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
        moradias = servico.listar_moradias()
    finally:
        ligacao.close()
    return render_template("quotas/formulario.html",
                           erro=None,
                           id_moradia="",
                           ano="",
                           mes="",
                           valor="",
                           data_vencimento="",
                           moradias=moradias,
                           )


@quotas_bp.route("/", methods=["POST"])
def criar():
    id_moradia_texto = request.form.get("id_moradia", "")
    ano_texto = request.form.get("ano", "")
    mes_texto = request.form.get("mes", "")
    valor_texto = request.form.get("valor", "")
    data_vencimento = request.form.get("data_vencimento", "")

    ligacao = ligar(obter_caminho_bd())
    try:
        servico = construir_servico(ligacao)
        try:
            id_moradia = int(id_moradia_texto)
            ano = int(ano_texto)
            mes = int(mes_texto)
            valor = float(valor_texto)
        except ValueError:
            raise DadosQuotaInvalidos(
                "Preencher corretamente a moradia, o ano, o mês e o valor.")
        servico.criar_quota(id_moradia, ano, mes, valor, data_vencimento)
    except (DadosQuotaInvalidos, QuotaDuplicada) as erro:
        moradias = servico.listar_moradias()
        return render_template(
            "quotas/formulario.html",
            erro=str(erro),
            id_moradia=id_moradia_texto,
            ano=ano_texto,
            mes=mes_texto,
            valor=valor_texto,
            data_vencimento=data_vencimento,
            moradias=moradias,
        )
    finally:
        ligacao.close()

    flash("Quota registada com sucesso.")
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

    flash("Pagamento registado com sucesso.")
    return redirect(url_for("quotas.listar"))
