from flask import Flask, redirect, url_for

from rd_condominios.base_dados import inicializar
from rd_condominios.config import obter_caminho_bd
from rd_condominios.web.moradias import moradias_bp
from rd_condominios.web.moradores import moradores_bp
from rd_condominios.web.quotas import quotas_bp
from rd_condominios.web.despesas import despesas_bp


def criar_app():
    app = Flask(__name__)
    app.secret_key = "rd-condominios-chave-desenvolvimento"

    inicializar(obter_caminho_bd())

    app.register_blueprint(moradias_bp)
    app.register_blueprint(moradores_bp)
    app.register_blueprint(quotas_bp)
    app.register_blueprint(despesas_bp)

    @app.route("/")
    def inicio():
        return redirect(url_for("moradias.listar"))

    return app


app = criar_app()

if __name__ == "__main__":
    app.run(debug=True)
