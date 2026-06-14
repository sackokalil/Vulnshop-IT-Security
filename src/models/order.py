from src.database.db import get_db_connection


def create_orders_table():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            total_price REAL NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()


def create_order_items_table():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,

            FOREIGN KEY (order_id) REFERENCES orders(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    """)

    conn.commit()
    conn.close()


def insert_order(user_id, total_price, status="Pending"):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO orders (user_id, total_price, status)
        VALUES (?, ?, ?)
    """, (user_id, total_price, status))

    order_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return order_id


def insert_order_item(order_id, product_id, quantity, price):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO order_items (order_id, product_id, quantity, price)
        VALUES (?, ?, ?, ?)
    """, (order_id, product_id, quantity, price))

    conn.commit()
    conn.close()


def select_orders_by_user(user_id):
    conn = get_db_connection()

    orders = conn.execute("""
        SELECT id, user_id, total_price, status, created_at
        FROM orders
        WHERE user_id = ?
        ORDER BY created_at DESC
    """, (user_id,)).fetchall()

    conn.close()
    return orders


def select_all_orders():
    conn = get_db_connection()

    orders = conn.execute("""
        SELECT 
            orders.id,
            orders.user_id,
            orders.total_price,
            orders.status,
            orders.created_at,
            users.username,
            users.email
        FROM orders
        JOIN users ON orders.user_id = users.id
        ORDER BY orders.created_at DESC
    """).fetchall()

    conn.close()
    return orders


def select_order_by_id(order_id):
    conn = get_db_connection()

    order = conn.execute("""
        SELECT
            orders.id,
            orders.user_id,
            orders.total_price,
            orders.status,
            orders.created_at,
            users.username,
            users.email
        FROM orders
        JOIN users ON orders.user_id = users.id
        WHERE orders.id = ?
    """, (order_id,)).fetchone()

    conn.close()
    return order


def select_order_items_by_order_id(order_id):
    conn = get_db_connection()

    items = conn.execute("""
        SELECT
            order_items.id,
            order_items.order_id,
            order_items.product_id,
            order_items.quantity,
            order_items.price,
            products.name AS product_name,
            products.image_url,
            order_items.quantity * order_items.price AS total_price
        FROM order_items
        JOIN products ON order_items.product_id = products.id
        WHERE order_items.order_id = ?
    """, (order_id,)).fetchall()

    conn.close()
    return items


def update_order_status(order_id, status):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE orders
        SET status = ?
        WHERE id = ?
    """, (status, order_id))

    conn.commit()
    conn.close()



def delete_order_items_by_order_id(order_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM order_items
        WHERE order_id = ?
    """, (order_id,))

    conn.commit()
    conn.close()


def delete_order_by_id(order_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM orders
        WHERE id = ?
    """, (order_id,))

    conn.commit()
    conn.close()