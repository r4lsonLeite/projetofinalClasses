from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any


@dataclass
class Reserva:
    animal_id: int
    adotante_id: int
    data_inicio: str
    data_expiracao: str
    ativo: bool = True
    id: int | None = None

    @staticmethod
    def nova(animal_id: int, adotante_id: int, dias: int = 2) -> "Reserva":
        inicio = datetime.now()
        exp = inicio + timedelta(days=dias)
        return Reserva(
            animal_id=int(animal_id),
            adotante_id=int(adotante_id),
            data_inicio=inicio.isoformat(timespec="seconds"),
            data_expiracao=exp.isoformat(timespec="seconds"),
            ativo=True,
        )

    def cadastrar(self) -> None:
        return

    def expirar(self) -> None:
        self.ativo = False

    def cancelar(self) -> None:
        self.ativo = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "animal_id": self.animal_id,
            "adotante_id": self.adotante_id,
            "data_inicio": self.data_inicio,
            "data_expiracao": self.data_expiracao,
            "ativo": int(self.ativo),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Reserva":
        return cls(
            animal_id=int(data["animal_id"]),
            adotante_id=int(data["adotante_id"]),
            data_inicio=data["data_inicio"],
            data_expiracao=data["data_expiracao"],
            ativo=bool(data.get("ativo", True)),
            id=data.get("id"),
        )
