from __future__ import annotations

from flask import Blueprint, current_app

from ._helpers import err, get_json, ok
from ..repositories.triagem_repo import TriagemRepository
from ..repositories.usuarios_repo import UsuariosRepository
from ..services.triagem_service import TriagemService


triagem_bp = Blueprint("triagem", __name__)


def _service() -> TriagemService:
    db = current_app.config["DB"]
    return TriagemService(TriagemRepository(db), UsuariosRepository(db))


@triagem_bp.get("/triagens")
def listar_triagens():
    return ok(_service().listar())


@triagem_bp.post("/triagens")
def criar_triagem_avaliando():
    try:
        triagem = _service().criar_avaliando(get_json())
        return ok(triagem, 201)
    except ValueError as e:
        return err(str(e), 400)
    except (KeyError, TypeError) as e:
        return err(f"json inválido: {e}", 400)
    except Exception as e:
        return err(str(e), 500)
