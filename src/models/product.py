from src.database.db import get_db_connection


def create_products_table():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            category TEXT,
            image_url TEXT
        )
    """)

    conn.commit()
    conn.close()


def insert_product(name, description, price, category, image_url):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO products (name, description, price, category, image_url)
        VALUES (?, ?, ?, ?, ?)
    """, (name, description, price, category, image_url))

    conn.commit()
    conn.close()


def select_all_products():
    conn = get_db_connection()

    products = conn.execute("""
        SELECT id, name, description, price, category, image_url
        FROM products
    """).fetchall()

    conn.close()
    return products


def select_product_by_id(product_id):
    conn = get_db_connection()

    product = conn.execute("""
        SELECT id, name, description, price, category, image_url
        FROM products
        WHERE id = ?
    """, (product_id,)).fetchone()

    conn.close()
    return product


def update_product(product_id, name, description, price, category, image_url):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE products
        SET name = ?,
            description = ?,
            price = ?,
            category = ?,
            image_url = ?
        WHERE id = ?
    """, (name, description, price, category, image_url, product_id))

    conn.commit()
    conn.close()


def delete_product_by_id(product_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM products
        WHERE id = ?
    """, (product_id,))

    conn.commit()
    conn.close()




def search_products_by_keyword(keyword):
    conn = get_db_connection()

    products = conn.execute("""
        SELECT id, name, description, price, category, image_url
        FROM products
        WHERE name LIKE ?
           OR description LIKE ?
           OR category LIKE ?
        ORDER BY id DESC
    """, (
        f"%{keyword}%",
        f"%{keyword}%",
        f"%{keyword}%"
    )).fetchall()

    conn.close()
    return products