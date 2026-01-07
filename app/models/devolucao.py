from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any


@dataclass
class Devolucao:
    animal_id: int
    data: str
    motivo: str
    status: str = "aberta"  # aberta/reavaliacao/finalizada
    id: int | None = None

    def cadastrar(self) -> None:
        return

    def reavaliacao(self, novo_status: str = "reavaliacao") -> None:
        self.status = str(novo_status).strip().lower()

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "animal_id": self.animal_id,
            "data": self.data,
            "motivo": self.motivo,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Devolucao":
        return cls(
            animal_id=int(data["animal_id"]),
            data=str(data.get("data", date.today().isoformat())),
            motivo=str(data.get("motivo", "")),
            status=str(data.get("status", "aberta")),
            id=data.get("id"),
        )
