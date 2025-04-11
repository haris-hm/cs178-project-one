import db_utils
import boto3

def get_products() -> tuple[tuple[str | float | int]]:
    return db_utils.run_query(
        """
        SELECT * FROM Inventory
        """
    )
