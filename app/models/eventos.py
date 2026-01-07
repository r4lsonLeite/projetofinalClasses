from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any


@dataclass
class Evento:
    STATUS_VALIDOS = {"entrada", "vacina", "adoção", "devolução"}

    animal_id: int
    status: str
    descricao: str
    data: str
    id: int | None = None

    def __post_init__(self) -> None:
        self.status = str(self.status).strip().lower()
        if self.status not in self.STATUS_VALIDOS:
            raise ValueError("status de evento inválido: entrada, vacina, adoção, devolução")
        self.descricao = str(self.descricao).strip()
        if not self.descricao:
            raise ValueError("descricao não pode ser vazia")
        self.data = str(self.data).strip()
        if not self.data:
            self.data = date.today().isoformat()

    def mudanca_de_status(self, novo_status: str) -> None:
        novo_status = str(novo_status).strip().lower()
        if novo_status not in self.STATUS_VALIDOS:
            raise ValueError("status de evento inválido")
        self.status = novo_status

    def cadastrar(self) -> None:
        return

    def editar(self, novo_status: str, nova_descricao: str, nova_data: str) -> None:
        self.mudanca_de_status(novo_status)
        self.descricao = str(nova_descricao).strip()
        self.data = str(nova_data).strip()

    def remover(self) -> None:
        return

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "animal_id": self.animal_id,
            "status": self.status,
            "descricao": self.descricao,
            "data": self.data,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Evento":
        return cls(
            animal_id=int(data["animal_id"]),
            status=data["status"],
            descricao=data["descricao"],
            data=data.get("data", ""),
            id=data.get("id"),
        )
