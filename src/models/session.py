from src.database.db import get_db_connection


def create_user_sessions_table():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            session_token TEXT NOT NULL,
            ip_address TEXT,
            user_agent TEXT,
            login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            logout_time TIMESTAMP,
            status TEXT DEFAULT 'Active',
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()


def insert_user_session(user_id, session_token, ip_address, user_agent):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO user_sessions (
            user_id,
            session_token,
            ip_address,
            user_agent,
            status
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        user_id,
        session_token,
        ip_address,
        user_agent,
        "Active"
    ))

    conn.commit()
    conn.close()


def select_all_user_sessions():
    conn = get_db_connection()

    sessions = conn.execute("""
        SELECT 
            user_sessions.id,
            user_sessions.session_token,
            user_sessions.ip_address,
            user_sessions.user_agent,
            user_sessions.login_time,
            user_sessions.logout_time,
            user_sessions.status,
            users.username,
            users.email,
            users.role
        FROM user_sessions
        JOIN users ON user_sessions.user_id = users.id
        ORDER BY user_sessions.id DESC
    """).fetchall()

    conn.close()
    return sessions


def close_user_session(session_token):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE user_sessions
        SET status = 'Inactive',
            logout_time = CURRENT_TIMESTAMP
        WHERE session_token = ?
    """, (session_token,))

    conn.commit()
    conn.close()