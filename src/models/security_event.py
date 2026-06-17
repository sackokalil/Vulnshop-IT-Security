from src.database.db import get_db_connection


def create_security_events_table():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS security_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT NOT NULL,
            severity TEXT NOT NULL,
            description TEXT NOT NULL,
            user_id INTEGER,
            endpoint TEXT,
            ip_address TEXT,
            user_agent TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()


def insert_security_event(event_type, severity, description, user_id, endpoint, ip_address, user_agent):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO security_events (
            event_type,
            severity,
            description,
            user_id,
            endpoint,
            ip_address,
            user_agent
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        event_type,
        severity,
        description,
        user_id,
        endpoint,
        ip_address,
        user_agent
    ))

    conn.commit()
    conn.close()


def select_recent_security_events(limit=10):
    conn = get_db_connection()

    events = conn.execute("""
        SELECT
            security_events.id,
            security_events.event_type,
            security_events.severity,
            security_events.description,
            security_events.endpoint,
            security_events.ip_address,
            security_events.created_at,
            users.username
        FROM security_events
        LEFT JOIN users ON security_events.user_id = users.id
        ORDER BY security_events.id DESC
        LIMIT ?
    """, (limit,)).fetchall()

    conn.close()
    return events