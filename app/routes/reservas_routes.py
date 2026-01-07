from __future__ import annotations

from flask import Blueprint, current_app

from ._helpers import err, get_json, ok
from ..repositories.reservas_repo import ReservasRepository
from ..repositories.animais_repo import AnimaisRepository
from ..services.reservas_service import ReservasService


reservas_bp = Blueprint("reservas", __name__)


def _service() -> ReservasService:
    db = current_app.config["DB"]
    return ReservasService(ReservasRepository(db), AnimaisRepository(db))


@reservas_bp.get("/reservas")
def listar_reservas():
    return ok(_service().listar())


@reservas_bp.post("/reservas")
def criar_reserva():
    try:
        payload = get_json()
        reserva = _service().criar(
            animal_id=int(payload["animal_id"]),
            adotante_id=int(payload["adotante_id"]),
            dias=int(payload.get("dias", 2)),
        )
        return ok(reserva, 201)
    except ValueError as e:
        return err(str(e), 400)
    except (KeyError, TypeError) as e:
        return err(f"json inválido: {e}", 400)
    except Exception as e:
        return err(str(e), 500)


@reservas_bp.post("/reservas/<int:reserva_id>/expirar")
def expirar_reserva(reserva_id: int):
    reserva = _service().expirar(reserva_id)
    if not reserva:
        return err("reserva não encontrada", 404)
    return ok(reserva)


@reservas_bp.post("/reservas/<int:reserva_id>/cancelar")
def cancelar_reserva(reserva_id: int):
    reserva = _service().cancelar(reserva_id)
    if not reserva:
        return err("reserva não encontrada", 404)
    return ok(reserva)
