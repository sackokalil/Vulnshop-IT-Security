from src.models.order import (
    create_orders_table,
    create_order_items_table,
    insert_order,
    insert_order_item,
    select_orders_by_user,
    select_all_orders,
    select_order_by_id,
    select_order_items_by_order_id,
    update_order_status,
    delete_order_items_by_order_id,
    delete_order_by_id
)

from src.services.cart_service import get_cart_by_user
from src.models.cart import delete_all_cart_items_by_user
from src.services.product_service import get_product_by_id


def create_tables_for_orders():
    create_orders_table()
    create_order_items_table()


def create_order_from_cart(user_id):
    create_tables_for_orders()

    cart_items = get_cart_by_user(user_id)

    if not cart_items:
        return None

    total_price = 0

    for item in cart_items:
        total_price += item["total_price"]

    order_id = insert_order(
        user_id=user_id,
        total_price=total_price,
        status="Pending"
    )

    for item in cart_items:
        insert_order_item(
            order_id=order_id,
            product_id=item["product_id"],
            quantity=item["quantity"],
            price=item["price"]
        )

    delete_all_cart_items_by_user(user_id)

    return order_id




def create_order_from_admin(user_id, status, product_ids, quantities):
    create_tables_for_orders()

    total_price = 0
    order_items = []

    for product_id, quantity in zip(product_ids, quantities):
        if not product_id:
            continue

        product = get_product_by_id(int(product_id))
        quantity = int(quantity)

        price = product["price"]
        total_price += price * quantity

        order_items.append({
            "product_id": int(product_id),
            "quantity": quantity,
            "price": price
        })

    if not order_items:
        return None

    order_id = insert_order(
        user_id=int(user_id),
        total_price=total_price,
        status=status
    )

    for item in order_items:
        insert_order_item(
            order_id=order_id,
            product_id=item["product_id"],
            quantity=item["quantity"],
            price=item["price"]
        )

    return order_id




def get_orders_by_user(user_id):
    create_tables_for_orders()
    return select_orders_by_user(user_id)


def get_all_orders():
    create_tables_for_orders()
    return select_all_orders()


def get_order_details(order_id):
    create_tables_for_orders()

    order = select_order_by_id(order_id)
    items = select_order_items_by_order_id(order_id)

    return order, items


def change_order_status(order_id, status):
    create_tables_for_orders()
    update_order_status(order_id, status)


def remove_order(order_id):
    create_tables_for_orders()

    delete_order_items_by_order_id(order_id)
    delete_order_by_id(order_id)