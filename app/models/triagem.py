from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class Triagem:
    animal_id: int
    adotante_id: int
    pontuacao: int = 0
    elegivel: bool = False
    observacoes: str = ""
    id: int | None = None

    def cadastrar(self) -> None:
        return

    def validar_politicas(self, moradia: str, criancas: bool) -> bool:
        moradia = str(moradia).strip().lower()
        if moradia not in {"casa", "apto"}:
            return False
        # política mínima: sempre valida, mas deixa gancho
        _ = criancas
        return True

    def calcular_compatibilidade(self, area_util: float, experiencia: str, outros_animais: bool) -> int:
        score = 0
        if float(area_util) >= 30:
            score += 40
        if str(experiencia).strip():
            score += 30
        if outros_animais:
            score += 10
        return score

    def avaliar(self, adotante: dict[str, Any]) -> None:
        ok = self.validar_politicas(adotante.get("moradia"), bool(adotante.get("criancas")))
        if not ok:
            self.pontuacao = 0
            self.elegivel = False
            self.observacoes = "Reprovado nas políticas"
            return

        score = self.calcular_compatibilidade(
            adotante.get("area_util", 0),
            adotante.get("experiencia", ""),
            bool(adotante.get("outros_animais")),
        )
        self.pontuacao = int(score)
        self.elegivel = self.pontuacao >= 50
        self.observacoes = "Elegível" if self.elegivel else "Pontuação insuficiente"

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "animal_id": self.animal_id,
            "adotante_id": self.adotante_id,
            "pontuacao": self.pontuacao,
            "elegivel": int(self.elegivel),
            "observacoes": self.observacoes,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Triagem":
        return cls(
            animal_id=int(data["animal_id"]),
            adotante_id=int(data["adotante_id"]),
            pontuacao=int(data.get("pontuacao", 0)),
            elegivel=bool(data.get("elegivel", False)),
            observacoes=str(data.get("observacoes", "")),
            id=data.get("id"),
        )
