from src.services.cart_service import get_cart_by_user
from src.services.order_service import get_orders_by_user
from src.models.user import (
    select_user_by_id,
    update_user_profile_image,
    add_profile_image_column
)


def get_profile_cart_stats(user_id):

    cart_items = get_cart_by_user(user_id)
    orders = get_orders_by_user(user_id)

    cart_items_count = 0
    cart_total = 0

    for item in cart_items:
        cart_items_count += item["quantity"]
        cart_total += item["total_price"]

    order_count = len(orders)

    return {
        "cart_items_count": cart_items_count,
        "cart_total": cart_total,
        "order_count": order_count
    }


def get_user_profile(user_id):
    add_profile_image_column()
    return select_user_by_id(user_id)


def update_profile_image(user_id, profile_image):
    add_profile_image_column()
    update_user_profile_image(user_id, profile_image)