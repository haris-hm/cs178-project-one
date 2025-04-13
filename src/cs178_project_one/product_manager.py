import cs178_project_one.db_utils as db_utils
import boto3

from boto3.dynamodb.conditions import Key
from decimal import Decimal
from typing import Any

TABLE_NAME = 'ShoppingCart'

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table(TABLE_NAME)

def get_all_categories() -> tuple[tuple[str]]:
    """
    Returns all the categories in the database. The first category is 'All', which is used to display all products.
    :return: A tuple of tuples, where each inner tuple contains the name of a category.
    """

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
    """
    Returns all the products in the inventory. If a category is specified, it returns only the products in that category.
    If no category is specified, it returns all products.

    :param category_name: The name of the category to filter by. If None, all products are returned.
    :return: A tuple of tuples, where each inner tuple contains the description, name, price, and ID of a product.
    """

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

def edit_cart(username: str, product_id: str, product_name: str, product_price: float) -> None:
    """
    Adds a product to the user's cart. If the cart doesn't exist, it creates a new cart. If the product is already in the cart,
    it updates the quantity of the product in the cart.

    :param username: The username of the user.
    :param product_id: The ID of the product to add to the cart.
    :param product_name: The name of the product to add to the cart.
    :param product_price: The price of the product to add to the cart.
    """

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
        update_quantity(username, product_id, current_items[product_id]['quantity'] + 1)
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
    

def create_cart(username: str, product_id: str, product_name: str, product_price: float) -> None:
    """
    Creates a new cart for the user with the specified product.

    :param username: The username of the user.
    :param product_id: The ID of the product to add to the cart.
    :param product_name: The name of the product to add to the cart.
    :param product_price: The price of the product to add to the cart.
    """

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
    """
    Returns the cart items for the specified user. If the cart doesn't exist, it returns an empty dictionary.

    :param username: The username of the user.
    :return: A dictionary of cart items, where the keys are product IDs and the values are dictionaries containing
             the product name, price, and quantity.
    """

    response = table.query(
        KeyConditionExpression=Key('username').eq(username)
    )

    if len(response['Items']) == 0:
        return {}
    
    return response['Items'][0]['cart_items']

def delete_cart_item(username: str, product_id: str) -> None:
    """
    Deletes a product from the user's cart. If the cart is empty after deletion, it clears the cart.

    :param username: The username of the user.
    :param product_id: The ID of the product to delete from the cart.
    """

    table.update_item(
        Key={'username': username},
        UpdateExpression='REMOVE cart_items.#pid',
        ExpressionAttributeNames={
            '#pid': product_id
        }
    )

    response = table.query(
        KeyConditionExpression=Key('username').eq(username)
    )
    current_items: dict[str, dict[Any]] = response['Items'][0]['cart_items']

    if len(current_items.keys()) == 0:
        clear_cart(username)

def update_quantity(username: str, product_id: str, new_quantity: str) -> None:
    """
    Updates the quantity of a product in the user's cart.

    :param username: The username of the user.
    :param product_id: The ID of the product to update.
    :param new_quantity: The new quantity of the product.
    """

    table.update_item(
        Key={'username': username},
        UpdateExpression='SET cart_items.#pid.quantity = :val',
        ExpressionAttributeNames={
            '#pid': product_id
        },
        ExpressionAttributeValues={
            ':val': Decimal(new_quantity)
        }
    )

def clear_cart(username: str) -> None:
    """
    Clears the user's cart by deleting the cart item from the database.
    
    :param username: The username of the user.
    """

    table.delete_item(
        Key={'username': username}
    )
