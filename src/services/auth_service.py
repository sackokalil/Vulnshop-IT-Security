from flask import session
from src.database.db import get_db_connection


def authenticate_user(email, password):
    """
    VULNERABLE LOGIN FUNCTION - SQL Injection Lab

    This function is intentionally vulnerable.
    User input is directly inserted into the SQL query.
    """

    conn = get_db_connection()

    query = (
        "SELECT id, first_name, last_name, username, email, password, role, status, created_at "
        "FROM users "
        f"WHERE email = '{email}' AND password = '{password}'"
    )
    #result : SELECT ... FROM users WHERE email = '' OR role='Admin' AND status='Active' -- ' AND password = 'anything'

    print("SQL QUERY:")
    print(query)

    user = conn.execute(query).fetchone()

    if user:
        print("USER FOUND:")
        print(dict(user))
    else:
        print("NO USER FOUND")

    conn.close()

    return user


def logout_user():
    session.clear()