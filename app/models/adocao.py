from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any


@dataclass
class Adocao:
    animal_id: int
    adotante_id: int
    data: str
    taxa: float
    status: str = "aberta"  # aberta/finalizada/cancelada
    id: int | None = None

    def cadastrar(self) -> None:
        return

    def finalizar(self) -> None:
        if self.status == "cancelada":
            raise ValueError("Adoção cancelada não pode ser finalizada")
        self.status = "finalizada"

    def cancelar(self) -> None:
        if self.status == "finalizada":
            raise ValueError("Adoção finalizada não pode ser cancelada")
        self.status = "cancelada"

    def gerar_contrato(self, adotante_nome: str, animal_nome: str) -> str:
        dt = self.data or date.today().isoformat()
        return (
            f"CONTRATO DE ADOÇÃO\n"
            f"Data: {dt}\n"
            f"Adotante: {adotante_nome}\n"
            f"Animal: {animal_nome}\n"
            f"Taxa: R$ {self.taxa:.2f}\n"
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "animal_id": self.animal_id,
            "adotante_id": self.adotante_id,
            "data": self.data,
            "taxa": float(self.taxa),
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Adocao":
        return cls(
            animal_id=int(data["animal_id"]),
            adotante_id=int(data["adotante_id"]),
            data=str(data.get("data", date.today().isoformat())),
            taxa=float(data.get("taxa", 0.0)),
            status=str(data.get("status", "aberta")),
            id=data.get("id"),
        )
