from __future__ import annotations

from typing import Any

from ..database import Database


class RelatoriosRepository:
    def __init__(self, db: Database):
        self._db = db

    def mais_adotados_por_especie(self, inicio: str, fim: str) -> list[dict[str, Any]]:
        with self._db.connect() as conn:
            rows = conn.execute(
                """
                SELECT a.especie as especie, COUNT(*) as total
                FROM adocoes ad
                JOIN animais a ON a.id = ad.animal_id
                WHERE ad.data >= ? AND ad.data <= ? AND ad.status = 'finalizada'
                GROUP BY a.especie
                ORDER BY total DESC;
                """,
                (inicio, fim),
            ).fetchall()
        return [dict(r) for r in rows]

    def devolucoes_por_motivo(self, inicio: str, fim: str) -> list[dict[str, Any]]:
        with self._db.connect() as conn:
            rows = conn.execute(
                """
                SELECT motivo, COUNT(*) as total
                FROM devolucoes
                WHERE data >= ? AND data <= ?
                GROUP BY motivo
                ORDER BY total DESC;
                """,
                (inicio, fim),
            ).fetchall()
        return [dict(r) for r in rows]

    def total_adocoes(self, inicio: str, fim: str) -> int:
        with self._db.connect() as conn:
            row = conn.execute(
                "SELECT COUNT(*) as total FROM adocoes WHERE data >= ? AND data <= ? AND status = 'finalizada';",
                (inicio, fim),
            ).fetchone()
        return int(row["total"]) if row else 0
