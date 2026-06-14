from src.models.user import (
    create_users_table,
    insert_user,
    select_all_users,
    select_user_by_email,
    insert_user_by_admin
)


def create_user(first_name, last_name, email, password):
    create_users_table()

    username = first_name.lower() + "_" + last_name.lower()

    insert_user(
        first_name=first_name,
        last_name=last_name,
        username=username,
        email=email,
        password=password
    )


def get_all_users():
    create_users_table()
    return select_all_users()


def get_user_by_email(email):
    create_users_table()
    return select_user_by_email(email)


def create_user_by_admin(first_name, last_name, email, password, role, status):
    create_users_table()

    username = first_name.lower() + "_" + last_name.lower()

    insert_user_by_admin(
        first_name=first_name,
        last_name=last_name,
        username=username,
        email=email,
        password=password,
        role=role,
        status=status
    )