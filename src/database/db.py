import sqlite3
from src.config.config import Config


def init_db():
    conn = sqlite3.connect(Config.DATABASE)

    with open("src/database/schema.sql") as f:
        conn.executescript(f.read())
    conn.close()


def get_db_connection():
    conn = sqlite3.connect(Config.DATABASE)
    return conn