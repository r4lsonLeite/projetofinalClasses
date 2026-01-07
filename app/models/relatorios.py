from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Relatorios:
    data_inicio: str
    data_fim: str
    tipo: str

    def gerar_relatorio(self) -> dict:
        # a geração real depende do repositório (consultas SQL)
        return {
            "data_inicio": self.data_inicio,
            "data_fim": self.data_fim,
            "tipo": self.tipo,
        }
