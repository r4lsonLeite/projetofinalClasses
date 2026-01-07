from __future__ import annotations

import os
import sqlite3
from typing import Any


class SQLiteAnimalRepository:
    def __init__(self, db_file: str | None = None):
        self._db_file = db_file or _db_path()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._db_file)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def init(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS animais (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    especie TEXT NOT NULL,
                    raca TEXT NOT NULL,
                    nome TEXT NOT NULL,
                    sexo TEXT NOT NULL,
                    idade_meses INTEGER NOT NULL,
                    porte TEXT NOT NULL,
                    estado TEXT NOT NULL,
                    status TEXT NOT NULL
                );
                """
            )

    def listar(self) -> list[dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute("SELECT * FROM animais ORDER BY id DESC;").fetchall()
        return [_row_to_dict(r) for r in rows]

    def buscar_por_id(self, animal_id: int) -> dict[str, Any] | None:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM animais WHERE id = ?;", (animal_id,)).fetchone()
        return _row_to_dict(row) if row else None

    def inserir(self, data: dict[str, Any]) -> int:
        with self._connect() as conn:
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
        with self._connect() as conn:
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
        with self._connect() as conn:
            cur = conn.execute("DELETE FROM animais WHERE id = ?;", (animal_id,))
            return cur.rowcount > 0

    def alterar_status(self, animal_id: int, novo_status: str) -> bool:
        with self._connect() as conn:
            cur = conn.execute(
                "UPDATE animais SET status = ? WHERE id = ?;",
                (novo_status, animal_id),
            )
            return cur.rowcount > 0


def _db_path() -> str:
    return os.path.join(os.path.dirname(__file__), "adocao.db")


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(_db_path())
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS animais (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                especie TEXT NOT NULL,
                raca TEXT NOT NULL,
                nome TEXT NOT NULL,
                sexo TEXT NOT NULL,
                idade_meses INTEGER NOT NULL,
                porte TEXT NOT NULL,
                estado TEXT NOT NULL,
                status TEXT NOT NULL
            );
            """
        )


def _row_to_dict(row: sqlite3.Row) -> dict[str, Any]:
    return {
        "id": row["id"],
        "especie": row["especie"],
        "raca": row["raca"],
        "nome": row["nome"],
        "sexo": row["sexo"],
        "idade_meses": row["idade_meses"],
        "porte": row["porte"],
        "estado": row["estado"],
        "status": row["status"],
    }


def list_animais() -> list[dict[str, Any]]:
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM animais ORDER BY id DESC;").fetchall()
    return [_row_to_dict(r) for r in rows]


def get_animal(animal_id: int) -> dict[str, Any] | None:
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM animais WHERE id = ?;", (animal_id,)).fetchone()
    return _row_to_dict(row) if row else None


def insert_animal(data: dict[str, Any]) -> int:
    with get_connection() as conn:
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


def update_animal(animal_id: int, data: dict[str, Any]) -> bool:
    with get_connection() as conn:
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


def delete_animal(animal_id: int) -> bool:
    with get_connection() as conn:
        cur = conn.execute("DELETE FROM animais WHERE id = ?;", (animal_id,))
        return cur.rowcount > 0


def set_status(animal_id: int, novo_status: str) -> bool:
    with get_connection() as conn:
        cur = conn.execute("UPDATE animais SET status = ? WHERE id = ?;", (novo_status, animal_id))
        return cur.rowcount > 0
