from src.models.session import (
    create_user_sessions_table,
    insert_user_session,
    select_all_user_sessions,
    close_user_session
)


def create_session(user_id, session_token, ip_address, user_agent):
    create_user_sessions_table()

    insert_user_session(
        user_id=user_id,
        session_token=session_token,
        ip_address=ip_address,
        user_agent=user_agent
    )


def get_all_sessions():
    create_user_sessions_table()
    return select_all_user_sessions()


def end_session(session_token):
    create_user_sessions_table()
    close_user_session(session_token)