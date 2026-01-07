from __future__ import annotations

from typing import Any

from ..database import Database, row_to_dict


class AnimaisRepository:
    def __init__(self, db: Database):
        self._db = db

    def listar(self) -> list[dict[str, Any]]:
        with self._db.connect() as conn:
            rows = conn.execute("SELECT * FROM animais ORDER BY id DESC;").fetchall()
        return [row_to_dict(r) for r in rows]

    def buscar(self, animal_id: int) -> dict[str, Any] | None:
        with self._db.connect() as conn:
            row = conn.execute("SELECT * FROM animais WHERE id = ?;", (animal_id,)).fetchone()
        return row_to_dict(row) if row else None

    def inserir(self, data: dict[str, Any]) -> int:
        with self._db.connect() as conn:
            cur = conn.execute(
                """
                INSERT INTO animais (especie, raca, nome, sexo, idade_meses, porte, estado, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?);
                """,
                (
                    data["especie"],
                    data["raca"],
                    data["nome"],
                    data["sexo"],
                    data["idade_meses"],
                    data["porte"],
                    data["estado"],
                    data["status"],
                ),
            )
            return int(cur.lastrowid)

    def atualizar(self, animal_id: int, data: dict[str, Any]) -> bool:
        with self._db.connect() as conn:
            cur = conn.execute(
                """
                UPDATE animais
                SET especie = ?, raca = ?, nome = ?, sexo = ?, idade_meses = ?, porte = ?, estado = ?, status = ?
                WHERE id = ?;
                """,
                (
                    data["especie"],
                    data["raca"],
                    data["nome"],
                    data["sexo"],
                    data["idade_meses"],
                    data["porte"],
                    data["estado"],
                    data["status"],
                    animal_id,
                ),
            )
            return cur.rowcount > 0

    def remover(self, animal_id: int) -> bool:
        with self._db.connect() as conn:
            cur = conn.execute("DELETE FROM animais WHERE id = ?;", (animal_id,))
            return cur.rowcount > 0

    def alterar_status(self, animal_id: int, status: str) -> bool:
        with self._db.connect() as conn:
            cur = conn.execute("UPDATE animais SET status = ? WHERE id = ?;", (status, animal_id))
            return cur.rowcount > 0
