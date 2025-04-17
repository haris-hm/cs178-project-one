from flask import Flask, render_template, request, redirect, url_for, flash
from functools import wraps
from typing import Any

import cs178_project_one.user_manager as user_manager
import cs178_project_one.product_manager as product_manager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Very secure authentication method
def authenticate(func):
    """
    Decorator to authenticate the user before accessing a route.
    If the user is not logged in, it redirects them to the login page.
    
    :param func: The Flask route to decorate.
    :return: The decorated route function.
    """
    @wraps(func)
    def auth_user(*args, **kwargs):
        try:
            username = request.args['username']
            password = request.args['password']

            password_valid: bool | None = user_manager.validate_password(username, password)

            # Redirect the user to the login page if any info is invalid
            if not password_valid or password_valid is None:
                flash('Incorrect username or password', 'danger')
                return redirect(url_for('login'))
        except Exception as _:
            return redirect(url_for('login'))
        
        return func(*args, **kwargs)
    return auth_user

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handles user login requests. For POST requests, it authenticates the username and password. 
    For GET requests, it renders the login page.

    :return: Redirects to the home page if login is successful, otherwise renders the login page.  
    """

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        password_valid: bool | None = user_manager.validate_password(username, password)

        # Display errors for incorrect usernames/passwords
        if password_valid is None:
            flash('Please create an account.', 'warning')
            return redirect(url_for('login'))
        elif not password_valid:
            flash('Incorrect username or password', 'danger')
            return redirect(url_for('login'))
        else:
            # Again, definitely very secure...
            return redirect(url_for('home', username=username, password=password))
    else:
        return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handles user registration requests. 
    
    For POST requests, it validates the username is not already in use, 
    then registers the account in the database. For GET requests, it renders
    the register page.

    :return: Redirects to the login page if registration is successful, otherwise,
    it renders the register page.
    """

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        create_account_response: tuple[bool, str] = user_manager.create_account(username, password)

        # If the username/password don't match, or the username is taken, display an error
        if not create_account_response[0]:
            flash(create_account_response[1], 'warning') 
            return redirect(url_for('register'))
        
        flash('Your account has been created. You can now log in.', 'success')
        return redirect(url_for('login'))
    else:
        return render_template('register.html')

@app.route('/cart', methods=['GET', 'POST'])
@authenticate
def cart():
    """
    Handles the main cart page, as well as adding items to the cart.

    For POST requests, it puts the item the user wants into their cart.
    For GET requests, it renders the cart page.

    :return: Redirects to the home page so the user can add more items if they want
    after they add one, otherwise, it renders the cart page.
    """

    username = request.args.get('username')
    if request.method == 'POST':
        product_id = request.form['product_id']
        product_name = request.form['product_name']
        product_price = request.form['product_price']

        product_manager.edit_cart(username, product_id, product_name, product_price)
        
        # Customized user feedback after adding an item to the cart
        if product_name[-1].lower() == 's':
            flash(f'{product_name} have been added to your cart! Feel free to keep shopping, or head to your cart now!', 'success')
        else:
            flash(f'{product_name} has been added to your cart! Feel free to keep shopping, or head to your cart now!', 'success')
        
        return redirect(url_for('home', username=username, password=request.args.get('password'), category=request.args.get('category')))
    else:
        cart: dict[str, dict[Any]] = product_manager.get_cart(username)
        return render_template('cart.html', cart=cart)
    
@app.route('/cart/update-quantity', methods=['POST'])
@authenticate
def update_quantity():
    """
    Handles update quantity requests. If the user adds or removes a product by clicking the 
    plus or minus button, it updates the quantity accordingly. If the user clicks the trash
    can, it deletes all of that product from their cart.

    :return: Redirect to the cart page, now updated.
    """

    username = request.args.get('username')
    delete = request.args.get('delete')
    product_id = request.args.get('product_id')
    quantity = request.args.get('quantity')

    if int(delete) or int(quantity) <= 0:
        product_manager.delete_cart_item(username, product_id)
    else:
        product_manager.update_quantity(username, product_id, quantity)

    return redirect(url_for('cart', username=username, password=request.args.get('password')))

@app.route('/cart/clear', methods=['POST'])
@authenticate
def clear_cart():
    """
    Clears the user's cart of all items.

    :return: Redirect to the updated cart page.
    """

    username = request.args.get('username')
    product_manager.clear_cart(username)
    return redirect(url_for('cart', username=username, password=request.args.get('password')))
    
@app.route('/')
@authenticate
def home(): 
    """
    Handles requests to the home page with products filtered based on the 
    user's category URL argument. Requires the user to be logged in.

    :return: Redirect to the home page, with items filtered how the user wants.
    """

    category: str | None = request.args.get('category')

    if category is None:
        return redirect(url_for('home', username=request.args.get('username'), password=request.args.get('password'), category='All'))

    categories: tuple[tuple[str]] = product_manager.get_all_categories()
    products: tuple[tuple[str | float | int]] = product_manager.get_products(category)

    return render_template('home.html', categories=categories, products=products)

def serve():
    app.run(host='0.0.0.0', port=8080, debug=True)

if __name__ == '__main__':
    serve()
