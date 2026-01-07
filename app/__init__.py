from __future__ import annotations

from flask import Flask

from .database import Database
from .routes.animais_routes import animais_bp
from .routes.usuarios_routes import usuarios_bp
from .routes.eventos_routes import eventos_bp
from .routes.triagem_routes import triagem_bp
from .routes.reservas_routes import reservas_bp
from .routes.adocoes_routes import adocoes_bp
from .routes.devolucoes_routes import devolucoes_bp
from .routes.relatorios_routes import relatorios_bp


def create_app() -> Flask:
    app = Flask(__name__)

    db = Database()
    db.init_db()

    app.config["DB"] = db

    app.register_blueprint(animais_bp)
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(eventos_bp)
    app.register_blueprint(triagem_bp)
    app.register_blueprint(reservas_bp)
    app.register_blueprint(adocoes_bp)
    app.register_blueprint(devolucoes_bp)
    app.register_blueprint(relatorios_bp)

    return app
