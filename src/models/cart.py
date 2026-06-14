from src.database.db import get_db_connection


def create_cart_items_table():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cart_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 1,

            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    """)

    conn.commit()
    conn.close()


def insert_cart_item(user_id, product_id, quantity):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO cart_items (user_id, product_id, quantity)
        VALUES (?, ?, ?)
    """, (user_id, product_id, quantity))

    conn.commit()
    conn.close()


def select_cart_item_by_user_and_product(user_id, product_id):
    conn = get_db_connection()

    cart_item = conn.execute("""
        SELECT id, user_id, product_id, quantity
        FROM cart_items
        WHERE user_id = ? AND product_id = ?
    """, (user_id, product_id)).fetchone()

    conn.close()
    return cart_item


def update_cart_item_quantity(cart_item_id, quantity):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE cart_items
        SET quantity = ?
        WHERE id = ?
    """, (quantity, cart_item_id))

    conn.commit()
    conn.close()


def select_cart_items_by_user(user_id):
    conn = get_db_connection()

    cart_items = conn.execute("""
        SELECT 
            cart_items.id,
            cart_items.user_id,
            cart_items.product_id,
            cart_items.quantity,
            products.name,
            products.price,
            products.image_url,
            products.category,
            cart_items.quantity * products.price AS total_price
        FROM cart_items
        JOIN products ON cart_items.product_id = products.id
        WHERE cart_items.user_id = ?
    """, (user_id,)).fetchall()

    conn.close()
    return cart_items


def delete_cart_item(cart_item_id, user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM cart_items
        WHERE id = ? AND user_id = ?
    """, (cart_item_id, user_id))

    conn.commit()
    conn.close()

def delete_all_cart_items_by_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM cart_items
        WHERE user_id = ?
    """, (user_id,))

    conn.commit()
    conn.close()