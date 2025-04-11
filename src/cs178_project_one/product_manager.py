import cs178_project_one.db_utils as db_utils
import boto3

TABLE_NAME = "ShoppingCart"

dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
table = dynamodb.Table(TABLE_NAME)

def get_all_categories() -> tuple[tuple[str]]:
    categories: tuple[tuple[str]] = db_utils.run_query(
        """
        SELECT name
        FROM Category
        """
    )
    
    categories_list = list(categories)
    categories_list.insert(0, ('All',))
    categories = tuple(categories_list)

    return categories

def get_products(category_name: str | None) -> tuple[tuple[str | float | int]]:
    if category_name == 'All':
        return db_utils.run_query(
            """
            SELECT description, name, price
            FROM Inventory, Category
            WHERE Inventory.categoryID = Category.categoryID
            """
        )
    else:
        return db_utils.run_query(
            f"""
            SELECT description, name, price
            FROM Inventory, Category
            WHERE Inventory.categoryID = Category.categoryID AND name = '{category_name}'
            """
        )

def get_products_from_category(category_id: int) -> tuple[tuple[str | float | int]]:
    return db_utils.run_query(
        """
        SELECT description, name, price
        FROM Inventory, Category
        WHERE Inventory.categoryID = Category.categoryID
        """
    )

def create_cart_entry():
    pass

def edit_cart_entry():
    pass
