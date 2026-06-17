from src.models.dashboard import (
    count_users,
    count_products,
    count_orders
)

from src.services.security_event_service import get_recent_security_events


def get_dashboard_stats():
    return {
        "users_count": count_users(),
        "products_count": count_products(),
        "orders_count": count_orders(),
        "security_challenges": "10/10",
        "recent_security_events": get_recent_security_events(10)
    }