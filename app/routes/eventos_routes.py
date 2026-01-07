from __future__ import annotations

from flask import Blueprint, current_app, request

from ._helpers import err, get_json, ok
from ..repositories.eventos_repo import EventosRepository
from ..services.eventos_service import EventosService


eventos_bp = Blueprint("eventos", __name__)


def _service() -> EventosService:
    db = current_app.config["DB"]
    return EventosService(EventosRepository(db))


@eventos_bp.get("/eventos")
def listar_eventos():
    animal_id = request.args.get("animal_id")
    return ok(_service().listar(animal_id=int(animal_id) if animal_id else None))


@eventos_bp.post("/eventos")
def criar_evento():
    try:
        evento = _service().criar(get_json())
        return ok(evento, 201)
    except ValueError as e:
        return err(str(e), 400)
    except (KeyError, TypeError) as e:
        return err(f"json inválido: {e}", 400)
    except Exception as e:
        return err(str(e), 500)


@eventos_bp.put("/eventos/<int:evento_id>")
def atualizar_evento(evento_id: int):
    try:
        evento = _service().atualizar(evento_id, get_json())
        if not evento:
            return err("evento não encontrado", 404)
        return ok(evento)
    except ValueError as e:
        return err(str(e), 400)
    except (KeyError, TypeError) as e:
        return err(f"json inválido: {e}", 400)
    except Exception as e:
        return err(str(e), 500)


@eventos_bp.delete("/eventos/<int:evento_id>")
def remover_evento(evento_id: int):
    ok_remove = _service().remover(evento_id)
    if not ok_remove:
        return err("evento não encontrado", 404)
    return ok({"id": evento_id})
