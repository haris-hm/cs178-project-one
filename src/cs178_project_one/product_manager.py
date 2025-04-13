import cs178_project_one.db_utils as db_utils
import boto3

from boto3.dynamodb.conditions import Key
from decimal import Decimal
from typing import Any

TABLE_NAME = 'ShoppingCart'

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
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
            SELECT description, name, price, ID
            FROM Inventory, Category
            WHERE Inventory.categoryID = Category.categoryID
            """
        )
    else:
        return db_utils.run_query(
            f"""
            SELECT description, name, price, ID
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

def edit_cart(username: str, product_id: str, product_name: str, product_price: float):
    response = table.query(
        KeyConditionExpression=Key('username').eq(username)
    )

    # If the cart doesn't already exist, create the cart
    if len(response['Items']) == 0:
        create_cart(username, product_id, product_name, product_price)
        return
    
    current_items: dict[str, dict[Any]] = response['Items'][0]['cart_items']
    
    # If the product is already in the user's cart, update the quantity
    if product_id in current_items.keys():
        table.update_item(
            Key={'username': username},
            UpdateExpression='SET cart_items.#pid.quantity = :val',
            ExpressionAttributeNames={
                '#pid': product_id
            },
            ExpressionAttributeValues={
                ':val': current_items[product_id]['quantity'] + 1
            }
        )
        return

    # If the cart exists, add a new item into the cart_items list
    new_item_info = {
        'description': product_name,
        'price': Decimal(product_price),
        'quantity': 1
    }   

    table.update_item(
        Key={'username': username},
        UpdateExpression='SET cart_items.#pid = :product_info',
        ExpressionAttributeNames={
            '#pid': product_id
        },
        ExpressionAttributeValues={
            ':product_info': new_item_info
        }
    )
    

def create_cart(username: str, product_id: str, product_name: str, product_price: float):
    new_cart: dict[str, str | dict[str, dict[Any]]] = {
        'username': username,
        'cart_items': {
            product_id: {
                'description': product_name,
                'price': Decimal(product_price),
                'quantity': 1
            }
        }
    }

    table.put_item(Item=new_cart)

def get_cart(username: str) -> dict[str, dict[Any]]:
    response = table.query(
        KeyConditionExpression=Key('username').eq(username)
    )

    if len(response['Items']) == 0:
        return {}
    
    return response['Items'][0]['cart_items']

def delete_cart_item(username: str, product_id: str):
    print('DELETE')
    pass

def update_quantity(username: str, product_id: str, new_quantity: str):
    print('UPDATE')
    pass
