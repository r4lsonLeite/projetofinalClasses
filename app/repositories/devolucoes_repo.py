from __future__ import annotations

from typing import Any

from ..database import Database, row_to_dict


class DevolucoesRepository:
    def __init__(self, db: Database):
        self._db = db

    def listar(self) -> list[dict[str, Any]]:
        with self._db.connect() as conn:
            rows = conn.execute("SELECT * FROM devolucoes ORDER BY id DESC;").fetchall()
        return [row_to_dict(r) for r in rows]

    def buscar(self, devolucao_id: int) -> dict[str, Any] | None:
        with self._db.connect() as conn:
            row = conn.execute("SELECT * FROM devolucoes WHERE id = ?;", (devolucao_id,)).fetchone()
        return row_to_dict(row) if row else None

    def inserir(self, data: dict[str, Any]) -> int:
        with self._db.connect() as conn:
            cur = conn.execute(
                """
                INSERT INTO devolucoes (animal_id, data, motivo, status)
                VALUES (?, ?, ?, ?);
                """,
                (data["animal_id"], data["data"], data["motivo"], data["status"]),
            )
            return int(cur.lastrowid)

    def atualizar_status(self, devolucao_id: int, status: str) -> bool:
        with self._db.connect() as conn:
            cur = conn.execute("UPDATE devolucoes SET status = ? WHERE id = ?;", (status, devolucao_id))
            return cur.rowcount > 0
