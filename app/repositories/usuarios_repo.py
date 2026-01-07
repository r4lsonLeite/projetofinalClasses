from __future__ import annotations

from typing import Any

from ..database import Database, row_to_dict


class UsuariosRepository:
    def __init__(self, db: Database):
        self._db = db

    def listar(self) -> list[dict[str, Any]]:
        with self._db.connect() as conn:
            rows = conn.execute("SELECT * FROM usuarios ORDER BY id DESC;").fetchall()
        return [row_to_dict(r) for r in rows]

    def buscar(self, usuario_id: int) -> dict[str, Any] | None:
        with self._db.connect() as conn:
            row = conn.execute("SELECT * FROM usuarios WHERE id = ?;", (usuario_id,)).fetchone()
        return row_to_dict(row) if row else None

    def inserir(self, data: dict[str, Any]) -> int:
        with self._db.connect() as conn:
            cur = conn.execute(
                """
                INSERT INTO usuarios (nome, idade, moradia, area_util, experiencia, criancas, outros_animais)
                VALUES (?, ?, ?, ?, ?, ?, ?);
                """,
                (
                    data["nome"],
                    data["idade"],
                    data["moradia"],
                    data["area_util"],
                    data["experiencia"],
                    data["criancas"],
                    data["outros_animais"],
                ),
            )
            return int(cur.lastrowid)

    def atualizar(self, usuario_id: int, data: dict[str, Any]) -> bool:
        with self._db.connect() as conn:
            cur = conn.execute(
                """
                UPDATE usuarios
                SET nome = ?, idade = ?, moradia = ?, area_util = ?, experiencia = ?, criancas = ?, outros_animais = ?
                WHERE id = ?;
                """,
                (
                    data["nome"],
                    data["idade"],
                    data["moradia"],
                    data["area_util"],
                    data["experiencia"],
                    data["criancas"],
                    data["outros_animais"],
                    usuario_id,
                ),
            )
            return cur.rowcount > 0

    def remover(self, usuario_id: int) -> bool:
        with self._db.connect() as conn:
            cur = conn.execute("DELETE FROM usuarios WHERE id = ?;", (usuario_id,))
            return cur.rowcount > 0
