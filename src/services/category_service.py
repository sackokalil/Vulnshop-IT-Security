from src.models.category import (
    create_categories_table,
    insert_category,
    select_all_categories,
    select_category_by_name,
    select_category_by_id,
    update_category,
    delete_category_by_id
)

def create_category(name, description):
    create_categories_table()

    insert_category(
        name=name,
        description=description
    )


def get_all_categories():
    create_categories_table()
    return select_all_categories()


def get_category_by_name(name):
    create_categories_table()
    return select_category_by_name(name)


def get_category_by_id(category_id):
    create_categories_table()
    return select_category_by_id(category_id)


def edit_category(category_id, name, description):
    create_categories_table()

    update_category(
        category_id=category_id,
        name=name,
        description=description
    )


def remove_category(category_id):
    create_categories_table()
    delete_category_by_id(category_id)