from __future__ import annotations

import os
import sqlite3
from typing import Any, Iterable


class Database:
    def __init__(self, db_file: str | None = None):
        self._db_file = db_file or os.path.join(os.path.dirname(__file__), "..", "adocao.db")
        self._db_file = os.path.abspath(self._db_file)

    @property
    def path(self) -> str:
        return self._db_file

    def connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._db_file)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def _table_columns(self, conn: sqlite3.Connection, table: str) -> set[str]:
        cols = conn.execute(f"PRAGMA table_info({table});").fetchall()
        return {row["name"] for row in cols}

    def _ensure_columns(self, conn: sqlite3.Connection, table: str, columns: Iterable[tuple[str, str]]):
        existing = self._table_columns(conn, table)
        for col_name, col_def in columns:
            if col_name not in existing:
                conn.execute(f"ALTER TABLE {table} ADD COLUMN {col_name} {col_def};")

    def init_db(self) -> None:
        with self.connect() as conn:
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
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT (datetime('now'))
                );
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    idade INTEGER NOT NULL,
                    moradia TEXT NOT NULL,
                    area_util REAL NOT NULL,
                    experiencia TEXT NOT NULL,
                    criancas INTEGER NOT NULL,
                    outros_animais INTEGER NOT NULL,
                    created_at TEXT NOT NULL DEFAULT (datetime('now'))
                );
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS eventos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    animal_id INTEGER NOT NULL,
                    status TEXT NOT NULL,
                    descricao TEXT NOT NULL,
                    data TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT (datetime('now')),
                    FOREIGN KEY(animal_id) REFERENCES animais(id) ON DELETE CASCADE
                );
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS triagens (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    animal_id INTEGER NOT NULL,
                    adotante_id INTEGER NOT NULL,
                    pontuacao INTEGER NOT NULL,
                    elegivel INTEGER NOT NULL,
                    observacoes TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT (datetime('now')),
                    FOREIGN KEY(animal_id) REFERENCES animais(id) ON DELETE CASCADE,
                    FOREIGN KEY(adotante_id) REFERENCES usuarios(id) ON DELETE CASCADE
                );
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS reservas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    animal_id INTEGER NOT NULL,
                    adotante_id INTEGER NOT NULL,
                    data_inicio TEXT NOT NULL,
                    data_expiracao TEXT NOT NULL,
                    ativo INTEGER NOT NULL,
                    created_at TEXT NOT NULL DEFAULT (datetime('now')),
                    FOREIGN KEY(animal_id) REFERENCES animais(id) ON DELETE CASCADE,
                    FOREIGN KEY(adotante_id) REFERENCES usuarios(id) ON DELETE CASCADE
                );
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS adocoes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    animal_id INTEGER NOT NULL,
                    adotante_id INTEGER NOT NULL,
                    data TEXT NOT NULL,
                    taxa REAL NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT (datetime('now')),
                    FOREIGN KEY(animal_id) REFERENCES animais(id) ON DELETE CASCADE,
                    FOREIGN KEY(adotante_id) REFERENCES usuarios(id) ON DELETE CASCADE
                );
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS lista_espera (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    animal_id INTEGER NOT NULL,
                    adotante_id INTEGER NOT NULL,
                    prioridade INTEGER NOT NULL,
                    created_at TEXT NOT NULL DEFAULT (datetime('now')),
                    FOREIGN KEY(animal_id) REFERENCES animais(id) ON DELETE CASCADE,
                    FOREIGN KEY(adotante_id) REFERENCES usuarios(id) ON DELETE CASCADE
                );
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS devolucoes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    animal_id INTEGER NOT NULL,
                    data TEXT NOT NULL,
                    motivo TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT (datetime('now')),
                    FOREIGN KEY(animal_id) REFERENCES animais(id) ON DELETE CASCADE
                );
                """
            )

            # migrações leves para bases já criadas antes
            self._ensure_columns(conn, "animais", [("created_at", "TEXT NOT NULL DEFAULT (datetime('now'))")])
            self._ensure_columns(conn, "usuarios", [("created_at", "TEXT NOT NULL DEFAULT (datetime('now'))")])
            self._ensure_columns(conn, "eventos", [("created_at", "TEXT NOT NULL DEFAULT (datetime('now'))")])
            self._ensure_columns(conn, "triagens", [("created_at", "TEXT NOT NULL DEFAULT (datetime('now'))")])
            self._ensure_columns(conn, "reservas", [("created_at", "TEXT NOT NULL DEFAULT (datetime('now'))")])
            self._ensure_columns(conn, "adocoes", [("created_at", "TEXT NOT NULL DEFAULT (datetime('now'))")])
            self._ensure_columns(conn, "lista_espera", [("created_at", "TEXT NOT NULL DEFAULT (datetime('now'))")])
            self._ensure_columns(conn, "devolucoes", [("created_at", "TEXT NOT NULL DEFAULT (datetime('now'))")])


def row_to_dict(row: sqlite3.Row) -> dict[str, Any]:
    return dict(row)
