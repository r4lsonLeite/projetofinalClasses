from __future__ import annotations

from flask import Blueprint, current_app

from ._helpers import err, get_json, ok
from ..repositories.usuarios_repo import UsuariosRepository
from ..services.usuarios_service import UsuariosService


usuarios_bp = Blueprint("usuarios", __name__)


def _service() -> UsuariosService:
    db = current_app.config["DB"]
    return UsuariosService(UsuariosRepository(db))


@usuarios_bp.get("/usuarios")
def listar_usuarios():
    return ok(_service().listar())


@usuarios_bp.get("/usuarios/<int:usuario_id>")
def buscar_usuario(usuario_id: int):
    usuario = _service().buscar(usuario_id)
    if not usuario:
        return err("usuario não encontrado", 404)
    return ok(usuario)


@usuarios_bp.post("/usuarios")
def criar_usuario():
    try:
        usuario = _service().criar(get_json())
        return ok(usuario, 201)
    except ValueError as e:
        return err(str(e), 400)
    except (KeyError, TypeError) as e:
        return err(f"json inválido: {e}", 400)
    except Exception as e:
        return err(str(e), 500)


@usuarios_bp.put("/usuarios/<int:usuario_id>")
def atualizar_usuario(usuario_id: int):
    try:
        usuario = _service().atualizar(usuario_id, get_json())
        if not usuario:
            return err("usuario não encontrado", 404)
        return ok(usuario)
    except ValueError as e:
        return err(str(e), 400)
    except (KeyError, TypeError) as e:
        return err(f"json inválido: {e}", 400)
    except Exception as e:
        return err(str(e), 500)


@usuarios_bp.delete("/usuarios/<int:usuario_id>")
def remover_usuario(usuario_id: int):
    ok_remove = _service().remover(usuario_id)
    if not ok_remove:
        return err("usuario não encontrado", 404)
    return ok({"id": usuario_id})
