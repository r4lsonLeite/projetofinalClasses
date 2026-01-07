from __future__ import annotations

from typing import Any

from ..models.reserva import Reserva
from ..repositories.reservas_repo import ReservasRepository
from ..repositories.animais_repo import AnimaisRepository


class ReservasService:
    def __init__(self, repo: ReservasRepository, animais_repo: AnimaisRepository):
        self._repo = repo
        self._animais = animais_repo

    def listar(self) -> list[dict[str, Any]]:
        return self._repo.listar()

    def criar(self, animal_id: int, adotante_id: int, dias: int = 2) -> dict[str, Any]:
        animal = self._animais.buscar(animal_id)
        if not animal:
            raise ValueError("animal não encontrado")
        reserva = Reserva.nova(animal_id, adotante_id, dias=dias)
        reserva_id = self._repo.inserir(reserva.to_dict())
        return self._repo.buscar(reserva_id) or {"id": reserva_id}

    def expirar(self, reserva_id: int) -> dict[str, Any] | None:
        ok = self._repo.atualizar_ativo(reserva_id, 0)
        return self._repo.buscar(reserva_id) if ok else None

    def cancelar(self, reserva_id: int) -> dict[str, Any] | None:
        ok = self._repo.atualizar_ativo(reserva_id, 0)
        return self._repo.buscar(reserva_id) if ok else None
