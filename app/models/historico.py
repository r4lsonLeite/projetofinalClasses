from __future__ import annotations

from typing import Any


class HistoricoEventos:
    def __init__(self, animal_id: int):
        self.animal_id = int(animal_id)

    def adicionar(self) -> None:
        # Persistência é via repositório de eventos
        return

    def remover(self) -> None:
        return

    def listar(self, eventos: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return [e for e in eventos if int(e.get("animal_id")) == self.animal_id]
