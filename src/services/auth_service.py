from src.database.db import get_db_connection

def vulnerable_login(username, password):
    conn = get_db_connection()

    query = f"""
        SELECT * FROM users
        WHERE username = '{username}'
        AND password = '{password}'
    """

    print("Executed SQL Query:")
    print(query)

    user = conn.execute(query).fetchone()

    print("RESULT:")
    print(user)

    conn.close()

    return user, query