from src.database.db import get_db_connection


def create_categories_table():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT
        )
    """)

    conn.commit()
    conn.close()


def insert_category(name, description):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO categories (name, description)
        VALUES (?, ?)
    """, (name, description))

    conn.commit()
    conn.close()


def select_all_categories():
    conn = get_db_connection()

    categories = conn.execute("""
        SELECT id, name, description
        FROM categories
        ORDER BY id DESC
    """).fetchall()

    conn.close()
    return categories


def select_category_by_name(name):
    conn = get_db_connection()

    category = conn.execute("""
        SELECT id, name, description
        FROM categories
        WHERE name = ?
    """, (name,)).fetchone()

    conn.close()
    return category



def select_category_by_id(category_id):
    conn = get_db_connection()

    category = conn.execute("""
        SELECT id, name, description
        FROM categories
        WHERE id = ?
    """, (category_id,)).fetchone()

    conn.close()
    return category


def update_category(category_id, name, description):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE categories
        SET name = ?,
            description = ?
        WHERE id = ?
    """, (name, description, category_id))

    conn.commit()
    conn.close()


def delete_category_by_id(category_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM categories
        WHERE id = ?
    """, (category_id,))

    conn.commit()
    conn.close()