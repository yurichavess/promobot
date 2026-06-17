import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "promobot.sqlite3"


def conectar():
    return sqlite3.connect(DB_PATH)


def criar_tabelas():
    with conectar() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS produtos_enviados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chave TEXT NOT NULL UNIQUE,
                titulo TEXT NOT NULL,
                enviado_em DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def obter_chave_produto(produto):
    return produto.get("asin") or produto["link"]


def ja_foi_enviado(produto):
    chave = obter_chave_produto(produto)

    with conectar() as conn:
        resultado = conn.execute(
            "SELECT 1 FROM produtos_enviados WHERE chave = ?",
            (chave,),
        ).fetchone()

    return resultado is not None


def marcar_como_enviado(produto):
    chave = obter_chave_produto(produto)

    with conectar() as conn:
        conn.execute(
            """
            INSERT OR IGNORE INTO produtos_enviados (chave, titulo)
            VALUES (?, ?)
            """,
            (chave, produto["titulo"]),
        )
