from __future__ import annotations

from typing import Any

from ..models.animais import Animais
from ..repositories.animais_repo import AnimaisRepository
from ..repositories.eventos_repo import EventosRepository


class AnimaisService:
    def __init__(self, animais_repo: AnimaisRepository, eventos_repo: EventosRepository):
        self._animais = animais_repo
        self._eventos = eventos_repo

    def listar(self) -> list[dict[str, Any]]:
        return self._animais.listar()

    def buscar(self, animal_id: int) -> dict[str, Any] | None:
        return self._animais.buscar(animal_id)

    def criar(self, payload: dict[str, Any]) -> dict[str, Any]:
        animal = Animais.from_dict(payload)
        animal.cadastrar()
        animal_id = self._animais.inserir(animal.to_dict())
        # evento de entrada
        self._eventos.inserir(
            {
                "animal_id": animal_id,
                "status": "entrada",
                "descricao": "Entrada do animal no sistema",
                "data": payload.get("data", ""),
            }
        )
        return self._animais.buscar(animal_id) or {"id": animal_id}

    def atualizar(self, animal_id: int, payload: dict[str, Any]) -> dict[str, Any] | None:
        payload = dict(payload)
        payload["id"] = animal_id
        animal = Animais.from_dict(payload)
        ok = self._animais.atualizar(animal_id, animal.to_dict())
        return self._animais.buscar(animal_id) if ok else None

    def remover(self, animal_id: int) -> bool:
        return self._animais.remover(animal_id)

    def adotar(self, animal_id: int) -> dict[str, Any] | None:
        data = self._animais.buscar(animal_id)
        if not data:
            return None
        animal = Animais.from_dict(data)
        animal.adotar()
        self._animais.alterar_status(animal_id, animal.status)
        self._eventos.inserir(
            {
                "animal_id": animal_id,
                "status": "adoção",
                "descricao": "Animal adotado",
                "data": "",
            }
        )
        return self._animais.buscar(animal_id)
