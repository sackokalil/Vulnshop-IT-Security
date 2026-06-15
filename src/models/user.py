from src.database.db import get_db_connection


def create_users_table():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            username TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'User',
            status TEXT DEFAULT 'Active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def insert_user(first_name, last_name, username, email, password):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users (first_name, last_name, username, email, password)
        VALUES (?, ?, ?, ?, ?)
    """, (first_name, last_name, username, email, password))

    conn.commit()
    conn.close()


def select_all_users():
    conn = get_db_connection()

    users = conn.execute("""
        SELECT id, first_name, last_name, username, email, role, status, created_at
        FROM users
        ORDER BY id DESC
    """).fetchall()

    conn.close()
    return users


def select_user_by_email(email):
    conn = get_db_connection()

    user = conn.execute("""
        SELECT id, first_name, last_name, username, email, password, role, status, created_at
        FROM users
        WHERE email = ?
    """, (email,)).fetchone()

    conn.close()
    return user


def insert_user_by_admin(first_name, last_name, username, email, password, role, status):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users (
            first_name,
            last_name,
            username,
            email,
            password,
            role,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        first_name,
        last_name,
        username,
        email,
        password,
        role,
        status
    ))

    conn.commit()
    conn.close()


def select_user_by_id(user_id):
    conn = get_db_connection()

    user = conn.execute("""
        SELECT id, first_name, last_name, username, email, role, status, created_at
        FROM users
        WHERE id = ?
    """, (user_id,)).fetchone()

    conn.close()
    return user


def update_user_by_id(user_id, first_name, last_name, username, email, role, status):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET first_name = ?,
            last_name = ?,
            username = ?,
            email = ?,
            role = ?,
            status = ?
        WHERE id = ?
    """, (
        first_name,
        last_name,
        username,
        email,
        role,
        status,
        user_id
    ))

    conn.commit()
    conn.close()


def update_user_status_by_id(user_id, status):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET status = ?
        WHERE id = ?
    """, (status, user_id))

    conn.commit()
    conn.close()


def delete_user_by_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM users
        WHERE id = ?
    """, (user_id,))

    conn.commit()
    conn.close()