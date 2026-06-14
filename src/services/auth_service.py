from src.services.user_service import get_user_by_email
from flask import session


def authenticate_user(email, password):
    user = get_user_by_email(email)

    if not user:
        return None

    if user["password"] != password:
        return None

    return user



def logout_user():
    session.clear()