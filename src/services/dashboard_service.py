
from src.models.dashboard import (
    count_users,
    count_products,
    count_orders
)

from src.services.security_event_service import (
    get_recent_security_events,
    get_security_event_stats
)


def get_dashboard_stats():

    security_event_rows = get_security_event_stats()

    chart_labels = []
    chart_values = []

    for row in security_event_rows:
        chart_labels.append(row["event_type"])
        chart_values.append(row["total"])

    return {
        "users_count": count_users(),
        "products_count": count_products(),
        "orders_count": count_orders(),
        "security_challenges": "9/9",
        "recent_security_events": get_recent_security_events(10),

        "security_chart_labels": chart_labels,
        "security_chart_values": chart_values
    }