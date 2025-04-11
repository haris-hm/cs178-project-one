import cs178_project_one.db_utils as db_utils
import boto3

def get_products() -> tuple[tuple[str | float | int]]:
    return db_utils.run_query(
        """
        SELECT description, name, price
        FROM Inventory, Category
        WHERE Inventory.categoryID = Category.categoryID
        """
    )
