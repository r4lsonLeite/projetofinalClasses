from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class ListaEspera:
    animal_id: int
    adotante_id: int
    prioridade: int = 0
    id: int | None = None

    def adicionar(self) -> None:
        return

    def remover(self) -> None:
        return

    def proximo(self, fila: list[dict[str, Any]]) -> dict[str, Any] | None:
        candidatos = [f for f in fila if int(f.get("animal_id")) == self.animal_id]
        if not candidatos:
            return None
        candidatos.sort(key=lambda x: (-int(x.get("prioridade", 0)), str(x.get("created_at", ""))))
        return candidatos[0]

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "animal_id": self.animal_id,
            "adotante_id": self.adotante_id,
            "prioridade": int(self.prioridade),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ListaEspera":
        return cls(
            animal_id=int(data["animal_id"]),
            adotante_id=int(data["adotante_id"]),
            prioridade=int(data.get("prioridade", 0)),
            id=data.get("id"),
        )
