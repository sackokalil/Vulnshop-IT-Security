from src.models.dashboard import (
    count_users,
    count_products,
    count_orders
)


def get_dashboard_stats():
    return {
        "users_count": count_users(),
        "products_count": count_products(),
        "orders_count": count_orders(),
        "security_challenges": "10/10"
    }