from src.models.cart import (
    create_cart_items_table,
    insert_cart_item,
    select_cart_item_by_user_and_product,
    update_cart_item_quantity,
    select_cart_items_by_user,
    delete_cart_item
)


def add_product_to_cart(user_id, product_id, quantity):
    create_cart_items_table()

    existing_item = select_cart_item_by_user_and_product(
        user_id,
        product_id
    )

    if existing_item:
        new_quantity = existing_item["quantity"] + quantity

        update_cart_item_quantity(
            existing_item["id"],
            new_quantity
        )
    else:
        insert_cart_item(
            user_id,
            product_id,
            quantity
        )


def get_cart_by_user(user_id):
    create_cart_items_table()
    return select_cart_items_by_user(user_id)


def remove_product_from_cart(cart_item_id, user_id):
    create_cart_items_table()

    delete_cart_item(
        cart_item_id,
        user_id
    )