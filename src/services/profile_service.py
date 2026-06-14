from src.services.cart_service import get_cart_by_user


def get_profile_cart_stats(user_id):
    cart_items = get_cart_by_user(user_id)

    cart_items_count = 0
    cart_total = 0

    for item in cart_items:
        cart_items_count += item["quantity"]
        cart_total += item["total_price"]

    return {
        "cart_items_count": cart_items_count,
        "cart_total": cart_total
    }