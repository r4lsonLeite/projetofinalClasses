from __future__ import annotations

from typing import Any

from ..repositories.relatorios_repo import RelatoriosRepository


class RelatoriosService:
    def __init__(self, repo: RelatoriosRepository):
        self._repo = repo

    def gerar(self, tipo: str, inicio: str, fim: str) -> dict[str, Any]:
        tipo = str(tipo).strip().lower()

        if tipo == "mais adotados":
            return {"tipo": tipo, "data": self._repo.mais_adotados_por_especie(inicio, fim)}
        if tipo == "devolucoes motivo":
            return {"tipo": tipo, "data": self._repo.devolucoes_por_motivo(inicio, fim)}
        if tipo == "taxa de adocao":
            return {"tipo": tipo, "total_adocoes": self._repo.total_adocoes(inicio, fim)}

        raise ValueError("tipo de relatório inválido")
