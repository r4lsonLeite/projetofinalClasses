from __future__ import annotations

from typing import Any

from ..database import Database, row_to_dict


class ReservasRepository:
    def __init__(self, db: Database):
        self._db = db

    def listar(self) -> list[dict[str, Any]]:
        with self._db.connect() as conn:
            rows = conn.execute("SELECT * FROM reservas ORDER BY id DESC;").fetchall()
        return [row_to_dict(r) for r in rows]

    def buscar(self, reserva_id: int) -> dict[str, Any] | None:
        with self._db.connect() as conn:
            row = conn.execute("SELECT * FROM reservas WHERE id = ?;", (reserva_id,)).fetchone()
        return row_to_dict(row) if row else None

    def inserir(self, data: dict[str, Any]) -> int:
        with self._db.connect() as conn:
            cur = conn.execute(
                """
                INSERT INTO reservas (animal_id, adotante_id, data_inicio, data_expiracao, ativo)
                VALUES (?, ?, ?, ?, ?);
                """,
                (
                    data["animal_id"],
                    data["adotante_id"],
                    data["data_inicio"],
                    data["data_expiracao"],
                    data["ativo"],
                ),
            )
            return int(cur.lastrowid)

    def atualizar_ativo(self, reserva_id: int, ativo: int) -> bool:
        with self._db.connect() as conn:
            cur = conn.execute("UPDATE reservas SET ativo = ? WHERE id = ?;", (ativo, reserva_id))
            return cur.rowcount > 0
