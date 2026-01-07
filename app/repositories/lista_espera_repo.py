from __future__ import annotations

from typing import Any

from ..database import Database, row_to_dict


class ListaEsperaRepository:
    def __init__(self, db: Database):
        self._db = db

    def listar(self, animal_id: int | None = None) -> list[dict[str, Any]]:
        with self._db.connect() as conn:
            if animal_id is None:
                rows = conn.execute("SELECT * FROM lista_espera ORDER BY prioridade DESC, id ASC;").fetchall()
            else:
                rows = conn.execute(
                    "SELECT * FROM lista_espera WHERE animal_id = ? ORDER BY prioridade DESC, id ASC;",
                    (animal_id,),
                ).fetchall()
        return [row_to_dict(r) for r in rows]

    def inserir(self, data: dict[str, Any]) -> int:
        with self._db.connect() as conn:
            cur = conn.execute(
                """
                INSERT INTO lista_espera (animal_id, adotante_id, prioridade)
                VALUES (?, ?, ?);
                """,
                (data["animal_id"], data["adotante_id"], data["prioridade"]),
            )
            return int(cur.lastrowid)

    def remover(self, item_id: int) -> bool:
        with self._db.connect() as conn:
            cur = conn.execute("DELETE FROM lista_espera WHERE id = ?;", (item_id,))
            return cur.rowcount > 0
