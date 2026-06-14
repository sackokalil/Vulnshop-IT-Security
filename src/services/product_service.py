from src.models.product import (
    create_products_table,
    insert_product,
    select_all_products,
    select_product_by_id,
    update_product,
    delete_product_by_id
)


def create_product(name, description, price, category, image_url):
    create_products_table()

    insert_product(
        name=name,
        description=description,
        price=price,
        category=category,
        image_url=image_url
    )


def get_all_products():
    create_products_table()
    return select_all_products()


def get_product_by_id(product_id):
    create_products_table()
    return select_product_by_id(product_id)



def edit_product(product_id, name, description, price, category, image_url):
    create_products_table()

    update_product(
        product_id=product_id,
        name=name,
        description=description,
        price=price,
        category=category,
        image_url=image_url
    )


def remove_product(product_id):
    create_products_table()
    delete_product_by_id(product_id)