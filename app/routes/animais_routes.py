from __future__ import annotations

from flask import Blueprint, current_app

from ._helpers import err, get_json, ok
from ..repositories.animais_repo import AnimaisRepository
from ..repositories.eventos_repo import EventosRepository
from ..services.animais_service import AnimaisService


animais_bp = Blueprint("animais", __name__)


def _service() -> AnimaisService:
    db = current_app.config["DB"]
    return AnimaisService(AnimaisRepository(db), EventosRepository(db))


@animais_bp.get("/animais")
def listar_animais():
    return ok(_service().listar())


@animais_bp.get("/animais/<int:animal_id>")
def buscar_animal(animal_id: int):
    animal = _service().buscar(animal_id)
    if not animal:
        return err("animal não encontrado", 404)
    return ok(animal)


@animais_bp.post("/animais")
def criar_animal():
    try:
        animal = _service().criar(get_json())
        return ok(animal, 201)
    except ValueError as e:
        return err(str(e), 400)
    except (KeyError, TypeError) as e:
        return err(f"json inválido: {e}", 400)
    except Exception as e:
        return err(str(e), 500)


@animais_bp.put("/animais/<int:animal_id>")
def atualizar_animal(animal_id: int):
    try:
        animal = _service().atualizar(animal_id, get_json())
        if not animal:
            return err("animal não encontrado", 404)
        return ok(animal)
    except ValueError as e:
        return err(str(e), 400)
    except (KeyError, TypeError) as e:
        return err(f"json inválido: {e}", 400)
    except Exception as e:
        return err(str(e), 500)


@animais_bp.delete("/animais/<int:animal_id>")
def remover_animal(animal_id: int):
    ok_remove = _service().remover(animal_id)
    if not ok_remove:
        return err("animal não encontrado", 404)
    return ok({"id": animal_id})


@animais_bp.post("/animais/<int:animal_id>/adotar")
def adotar_animal(animal_id: int):
    try:
        animal = _service().adotar(animal_id)
        if not animal:
            return err("animal não encontrado", 404)
        return ok(animal)
    except ValueError as e:
        return err(str(e), 400)
    except Exception as e:
        return err(str(e), 500)
