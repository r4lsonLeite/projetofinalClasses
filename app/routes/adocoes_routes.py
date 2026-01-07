from __future__ import annotations

from flask import Blueprint, current_app

from ._helpers import err, get_json, ok
from ..repositories.adocoes_repo import AdocoesRepository
from ..repositories.animais_repo import AnimaisRepository
from ..repositories.usuarios_repo import UsuariosRepository
from ..services.adocoes_service import AdocoesService


adocoes_bp = Blueprint("adocoes", __name__)


def _service() -> AdocoesService:
    db = current_app.config["DB"]
    return AdocoesService(AdocoesRepository(db), AnimaisRepository(db), UsuariosRepository(db))


@adocoes_bp.get("/adocoes")
def listar_adocoes():
    return ok(_service().listar())


@adocoes_bp.post("/adocoes")
def criar_adocao():
    try:
        adocao = _service().criar(get_json())
        return ok(adocao, 201)
    except ValueError as e:
        return err(str(e), 400)
    except (KeyError, TypeError) as e:
        return err(f"json inválido: {e}", 400)
    except Exception as e:
        return err(str(e), 500)


@adocoes_bp.post("/adocoes/<int:adocao_id>/finalizar")
def finalizar_adocao(adocao_id: int):
    try:
        adocao = _service().finalizar(adocao_id)
        if not adocao:
            return err("adoção não encontrada", 404)
        return ok(adocao)
    except ValueError as e:
        return err(str(e), 400)
    except Exception as e:
        return err(str(e), 500)


@adocoes_bp.post("/adocoes/<int:adocao_id>/cancelar")
def cancelar_adocao(adocao_id: int):
    try:
        adocao = _service().cancelar(adocao_id)
        if not adocao:
            return err("adoção não encontrada", 404)
        return ok(adocao)
    except ValueError as e:
        return err(str(e), 400)
    except Exception as e:
        return err(str(e), 500)


@adocoes_bp.get("/adocoes/<int:adocao_id>/contrato")
def contrato_adocao(adocao_id: int):
    contrato = _service().contrato(adocao_id)
    if not contrato:
        return err("adoção não encontrada", 404)
    return ok({"contrato": contrato})
