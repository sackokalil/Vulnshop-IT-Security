from src.database.db import get_db_connection


def count_users():
    conn = get_db_connection()

    total = conn.execute("""
        SELECT COUNT(*) AS total
        FROM users
    """).fetchone()

    conn.close()
    return total["total"]


def count_products():
    conn = get_db_connection()

    total = conn.execute("""
        SELECT COUNT(*) AS total
        FROM products
    """).fetchone()

    conn.close()
    return total["total"]


def count_orders():
    conn = get_db_connection()

    total = conn.execute("""
        SELECT COUNT(*) AS total
        FROM orders
    """).fetchone()

    conn.close()
    return total["total"]