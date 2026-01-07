from __future__ import annotations

from typing import Any

from ..models.usuario import Usuario
from ..repositories.usuarios_repo import UsuariosRepository


class UsuariosService:
    def __init__(self, repo: UsuariosRepository):
        self._repo = repo

    def listar(self) -> list[dict[str, Any]]:
        return self._repo.listar()

    def buscar(self, usuario_id: int) -> dict[str, Any] | None:
        return self._repo.buscar(usuario_id)

    def criar(self, payload: dict[str, Any]) -> dict[str, Any]:
        usuario = Usuario.from_dict(payload)
        usuario.cadastrar()
        usuario_id = self._repo.inserir(usuario.to_dict())
        return self._repo.buscar(usuario_id) or {"id": usuario_id}

    def atualizar(self, usuario_id: int, payload: dict[str, Any]) -> dict[str, Any] | None:
        payload = dict(payload)
        payload["id"] = usuario_id
        usuario = Usuario.from_dict(payload)
        ok = self._repo.atualizar(usuario_id, usuario.to_dict())
        return self._repo.buscar(usuario_id) if ok else None

    def remover(self, usuario_id: int) -> bool:
        return self._repo.remover(usuario_id)
