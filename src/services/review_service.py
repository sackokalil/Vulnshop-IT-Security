from src.models.review import (
    create_reviews_table,
    insert_review,
    select_reviews_by_product_id,
    select_review_stats_by_product_id
)


def create_review(product_id, user_id, reviewer_name, rating, comment):
    create_reviews_table()

    insert_review(
        product_id=product_id,
        user_id=user_id,
        reviewer_name=reviewer_name,
        rating=rating,
        comment=comment
    )


def get_reviews_by_product_id(product_id):
    create_reviews_table()
    return select_reviews_by_product_id(product_id)



def get_review_stats_by_product_id(product_id):
    create_reviews_table()

    stats = select_review_stats_by_product_id(product_id)

    return {
        "review_count": stats["review_count"],
        "average_rating": round(stats["average_rating"] or 0)
    }


def get_review_stats_for_products(products):
    product_stats = {}

    for product in products:
        product_stats[product["id"]] = get_review_stats_by_product_id(product["id"])

    return product_stats