import sqlite3

conn = sqlite3.connect("instance/database.db")

conn.execute("""
INSERT INTO users (username, password)
VALUES ('admin', 'admin123')
""")

conn.commit()
conn.close()