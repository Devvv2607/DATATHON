from __future__ import annotations

import uuid
import time
import os
import sqlite3
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class StoredContext:
    context_id: str
    filename: str
    text: str
    created_at: float


class SqliteDocumentContextStore:
    def __init__(self, db_path: str) -> None:
        self._db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._db_path)
        conn.execute("PRAGMA journal_mode=WAL")
        return conn

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS document_context (
                    context_id TEXT PRIMARY KEY,
                    filename TEXT NOT NULL,
                    text TEXT NOT NULL,
                    created_at REAL NOT NULL
                )
                """
            )

    def put(self, *, filename: str, text: str) -> StoredContext:
        context_id = uuid.uuid4().hex
        created_at = time.time()
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO document_context (context_id, filename, text, created_at) VALUES (?, ?, ?, ?)",
                (context_id, filename, text, created_at),
            )
        return StoredContext(
            context_id=context_id,
            filename=filename,
            text=text,
            created_at=created_at,
        )

    def get(self, context_id: str) -> Optional[StoredContext]:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT context_id, filename, text, created_at FROM document_context WHERE context_id = ?",
                (context_id,),
            ).fetchone()

        if not row:
            return None

        return StoredContext(
            context_id=row[0],
            filename=row[1],
            text=row[2],
            created_at=float(row[3]),
        )

    def delete(self, context_id: str) -> None:
        with self._connect() as conn:
            conn.execute(
                "DELETE FROM document_context WHERE context_id = ?",
                (context_id,),
            )


_global_store: Optional[SqliteDocumentContextStore] = None


def get_document_context_store() -> SqliteDocumentContextStore:
    global _global_store
    if _global_store is None:
        db_path = os.path.join(os.getcwd(), "document_context", "document_context.db")
        _global_store = SqliteDocumentContextStore(db_path=db_path)
    return _global_store
