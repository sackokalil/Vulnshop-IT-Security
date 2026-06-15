from src.models.user import (
    create_users_table,
    insert_user,
    select_all_users,
    select_user_by_email,
    insert_user_by_admin,
    select_user_by_id,
    update_user_by_id,
    update_user_status_by_id,
    delete_user_by_id
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


def get_user_by_id(user_id):
    create_users_table()
    return select_user_by_id(user_id)


def update_user(user_id, first_name, last_name, email, role, status):
    create_users_table()

    username = first_name.lower() + "_" + last_name.lower()

    update_user_by_id(
        user_id=user_id,
        first_name=first_name,
        last_name=last_name,
        username=username,
        email=email,
        role=role,
        status=status
    )


def update_user_status(user_id, status):
    create_users_table()
    update_user_status_by_id(user_id, status)


def delete_user(user_id):
    create_users_table()
    delete_user_by_id(user_id)