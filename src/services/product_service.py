from src.database.db import get_db_connection


def get_all_products():

    conn = get_db_connection()

    conn.row_factory = lambda cursor, row: {
        "id": row[0],
        "name": row[1],
        "description": row[2],
        "price": row[3],
        "category": row[4],
        "image_url": row[5]
    }

    products = conn.execute(
        "SELECT * FROM products"
    ).fetchall()

    conn.close()

    return products


def get_product_by_id(product_id):

    conn = get_db_connection()

    conn.row_factory = lambda cursor, row: {
        "id": row[0],
        "name": row[1],
        "description": row[2],
        "price": row[3],
        "category": row[4],
        "image_url": row[5]
    }

    product = conn.execute(
        "SELECT * FROM products WHERE id = ?",
        (product_id,)
    ).fetchone()

    conn.close()

    return product