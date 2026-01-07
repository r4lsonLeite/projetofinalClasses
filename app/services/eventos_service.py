from __future__ import annotations

from typing import Any

from ..models.eventos import Evento
from ..repositories.eventos_repo import EventosRepository


class EventosService:
    def __init__(self, repo: EventosRepository):
        self._repo = repo

    def listar(self, animal_id: int | None = None) -> list[dict[str, Any]]:
        return self._repo.listar(animal_id=animal_id)

    def buscar(self, evento_id: int) -> dict[str, Any] | None:
        return self._repo.buscar(evento_id)

    def criar(self, payload: dict[str, Any]) -> dict[str, Any]:
        evento = Evento.from_dict(payload)
        evento.cadastrar()
        evento_id = self._repo.inserir(evento.to_dict())
        return self._repo.buscar(evento_id) or {"id": evento_id}

    def atualizar(self, evento_id: int, payload: dict[str, Any]) -> dict[str, Any] | None:
        payload = dict(payload)
        payload["id"] = evento_id
        evento = Evento.from_dict(payload)
        ok = self._repo.atualizar(evento_id, evento.to_dict())
        return self._repo.buscar(evento_id) if ok else None

    def remover(self, evento_id: int) -> bool:
        return self._repo.remover(evento_id)
