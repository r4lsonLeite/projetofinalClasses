from __future__ import annotations

from typing import Any

from ..database import Database, row_to_dict


class AdocoesRepository:
    def __init__(self, db: Database):
        self._db = db

    def listar(self) -> list[dict[str, Any]]:
        with self._db.connect() as conn:
            rows = conn.execute("SELECT * FROM adocoes ORDER BY id DESC;").fetchall()
        return [row_to_dict(r) for r in rows]

    def buscar(self, adocao_id: int) -> dict[str, Any] | None:
        with self._db.connect() as conn:
            row = conn.execute("SELECT * FROM adocoes WHERE id = ?;", (adocao_id,)).fetchone()
        return row_to_dict(row) if row else None

    def inserir(self, data: dict[str, Any]) -> int:
        with self._db.connect() as conn:
            cur = conn.execute(
                """
                INSERT INTO adocoes (animal_id, adotante_id, data, taxa, status)
                VALUES (?, ?, ?, ?, ?);
                """,
                (data["animal_id"], data["adotante_id"], data["data"], data["taxa"], data["status"]),
            )
            return int(cur.lastrowid)

    def atualizar_status(self, adocao_id: int, status: str) -> bool:
        with self._db.connect() as conn:
            cur = conn.execute("UPDATE adocoes SET status = ? WHERE id = ?;", (status, adocao_id))
            return cur.rowcount > 0
