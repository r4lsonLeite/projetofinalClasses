from __future__ import annotations

from typing import Any

from ..database import Database, row_to_dict


class EventosRepository:
    def __init__(self, db: Database):
        self._db = db

    def listar(self, animal_id: int | None = None) -> list[dict[str, Any]]:
        with self._db.connect() as conn:
            if animal_id is None:
                rows = conn.execute("SELECT * FROM eventos ORDER BY id DESC;").fetchall()
            else:
                rows = conn.execute(
                    "SELECT * FROM eventos WHERE animal_id = ? ORDER BY id DESC;",
                    (animal_id,),
                ).fetchall()
        return [row_to_dict(r) for r in rows]

    def buscar(self, evento_id: int) -> dict[str, Any] | None:
        with self._db.connect() as conn:
            row = conn.execute("SELECT * FROM eventos WHERE id = ?;", (evento_id,)).fetchone()
        return row_to_dict(row) if row else None

    def inserir(self, data: dict[str, Any]) -> int:
        with self._db.connect() as conn:
            cur = conn.execute(
                """
                INSERT INTO eventos (animal_id, status, descricao, data)
                VALUES (?, ?, ?, ?);
                """,
                (data["animal_id"], data["status"], data["descricao"], data["data"]),
            )
            return int(cur.lastrowid)

    def atualizar(self, evento_id: int, data: dict[str, Any]) -> bool:
        with self._db.connect() as conn:
            cur = conn.execute(
                """
                UPDATE eventos
                SET status = ?, descricao = ?, data = ?
                WHERE id = ?;
                """,
                (data["status"], data["descricao"], data["data"], evento_id),
            )
            return cur.rowcount > 0

    def remover(self, evento_id: int) -> bool:
        with self._db.connect() as conn:
            cur = conn.execute("DELETE FROM eventos WHERE id = ?;", (evento_id,))
            return cur.rowcount > 0
