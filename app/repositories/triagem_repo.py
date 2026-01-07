from __future__ import annotations

from typing import Any

from ..database import Database, row_to_dict


class TriagemRepository:
    def __init__(self, db: Database):
        self._db = db

    def listar(self) -> list[dict[str, Any]]:
        with self._db.connect() as conn:
            rows = conn.execute("SELECT * FROM triagens ORDER BY id DESC;").fetchall()
        return [row_to_dict(r) for r in rows]

    def buscar(self, triagem_id: int) -> dict[str, Any] | None:
        with self._db.connect() as conn:
            row = conn.execute("SELECT * FROM triagens WHERE id = ?;", (triagem_id,)).fetchone()
        return row_to_dict(row) if row else None

    def inserir(self, data: dict[str, Any]) -> int:
        with self._db.connect() as conn:
            cur = conn.execute(
                """
                INSERT INTO triagens (animal_id, adotante_id, pontuacao, elegivel, observacoes)
                VALUES (?, ?, ?, ?, ?);
                """,
                (
                    data["animal_id"],
                    data["adotante_id"],
                    data["pontuacao"],
                    data["elegivel"],
                    data["observacoes"],
                ),
            )
            return int(cur.lastrowid)
