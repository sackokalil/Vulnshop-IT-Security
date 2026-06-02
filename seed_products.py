import sqlite3

conn = sqlite3.connect("instance/database.db")

cursor = conn.cursor()

products = [

(
    "Wireless Headphones",
    "Premium wireless headphones",
    149.99,
    "Electronics",
    "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=700"
),

(
    "Smart Watch",
    "Fitness smartwatch",
    299.00,
    "Electronics",
    "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=700"
),

(
    "Backpack",
    "Urban backpack",
    79.99,
    "Accessories",
    "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=700"
),

(
    "Running Shoes",
    "Professional running shoes",
    129.00,
    "Sports",
    "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=700"
)

]

cursor.executemany(
    """
    INSERT INTO products
    (name, description, price, category, image_url)
    VALUES (?, ?, ?, ?, ?)
    """,
    products
)

conn.commit()
conn.close()

print("Products inserted.")