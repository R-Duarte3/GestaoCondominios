from flask import Flask, redirect, url_for

from rd_condominios.base_dados import inicializar
from rd_condominios.config import obter_caminho_bd
from rd_condominios.web.moradias import moradias_bp
from rd_condominios.web.moradores import moradores_bp


def criar_app():
    app = Flask(__name__)
    app.secret_key = "rd-condominios-chave-desenvolvimento"
    # é uma chave que o Flask usa para proteger a sessão do utilizador (onde as mensagens flash ficam guardadas temporariamente)

    inicializar(obter_caminho_bd())

    app.register_blueprint(moradias_bp)
    app.register_blueprint(moradores_bp)

    @app.route("/")
    def inicio():
        return redirect(url_for("moradias.listar"))

    return app


app = criar_app()

if __name__ == "__main__":
    app.run(debug=True)
