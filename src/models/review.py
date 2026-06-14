from src.database.db import get_db_connection


def create_reviews_table():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            user_id INTEGER,
            reviewer_name TEXT NOT NULL,
            rating INTEGER NOT NULL,
            comment TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (product_id) REFERENCES products(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()


def insert_review(product_id, user_id, reviewer_name, rating, comment):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO reviews (product_id, user_id, reviewer_name, rating, comment)
        VALUES (?, ?, ?, ?, ?)
    """, (product_id, user_id, reviewer_name, rating, comment))

    conn.commit()
    conn.close()


def select_reviews_by_product_id(product_id):
    conn = get_db_connection()

    reviews = conn.execute("""
        SELECT id, product_id, user_id, reviewer_name, rating, comment, created_at
        FROM reviews
        WHERE product_id = ?
        ORDER BY id DESC
    """, (product_id,)).fetchall()

    conn.close()
    return reviews



def select_review_stats_by_product_id(product_id):
    conn = get_db_connection()

    stats = conn.execute("""
        SELECT
            COUNT(*) AS review_count,
            AVG(rating) AS average_rating
        FROM reviews
        WHERE product_id = ?
    """, (product_id,)).fetchone()

    conn.close()
    return stats