from src.models.security_event import (
    create_security_events_table,
    insert_security_event,
    select_recent_security_events
)


def create_security_event(event_type, severity, description, user_id=None, endpoint=None, ip_address=None, user_agent=None):
    create_security_events_table()

    insert_security_event(
        event_type=event_type,
        severity=severity,
        description=description,
        user_id=user_id,
        endpoint=endpoint,
        ip_address=ip_address,
        user_agent=user_agent
    )


def get_recent_security_events(limit=10):
    create_security_events_table()
    return select_recent_security_events(limit)