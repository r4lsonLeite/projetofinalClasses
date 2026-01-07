from __future__ import annotations

from flask import Blueprint, current_app, request

from ._helpers import err, ok
from ..repositories.relatorios_repo import RelatoriosRepository
from ..services.relatorios_service import RelatoriosService


relatorios_bp = Blueprint("relatorios", __name__)


def _service() -> RelatoriosService:
    db = current_app.config["DB"]
    return RelatoriosService(RelatoriosRepository(db))


@relatorios_bp.get("/relatorios")
def gerar_relatorio():
    tipo = request.args.get("tipo", "")
    inicio = request.args.get("inicio", "0000-01-01")
    fim = request.args.get("fim", "9999-12-31")

    try:
        return ok(_service().gerar(tipo, inicio, fim))
    except ValueError as e:
        return err(str(e), 400)
    except Exception as e:
        return err(str(e), 500)
