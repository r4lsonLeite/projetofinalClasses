from __future__ import annotations

from flask import Blueprint, current_app

from ._helpers import err, get_json, ok
from ..repositories.devolucoes_repo import DevolucoesRepository
from ..repositories.animais_repo import AnimaisRepository
from ..services.devolucoes_service import DevolucoesService


devolucoes_bp = Blueprint("devolucoes", __name__)


def _service() -> DevolucoesService:
    db = current_app.config["DB"]
    return DevolucoesService(DevolucoesRepository(db), AnimaisRepository(db))


@devolucoes_bp.get("/devolucoes")
def listar_devolucoes():
    return ok(_service().listar())


@devolucoes_bp.post("/devolucoes")
def criar_devolucao():
    try:
        devolucao = _service().criar(get_json())
        return ok(devolucao, 201)
    except ValueError as e:
        return err(str(e), 400)
    except (KeyError, TypeError) as e:
        return err(f"json inválido: {e}", 400)
    except Exception as e:
        return err(str(e), 500)


@devolucoes_bp.post("/devolucoes/<int:devolucao_id>/reavaliacao")
def reavaliacao(devolucao_id: int):
    devolucao = _service().reavaliacao(devolucao_id)
    if not devolucao:
        return err("devolução não encontrada", 404)
    return ok(devolucao)
