from flask import Flask, render_template, request, redirect, url_for, flash
from functools import wraps

import cs178_project_one.user_manager as user_manager
import cs178_project_one.product_manager as product_manager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Very secure authentication method
def authenticate(func):
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
    if request.method == 'POST':
        pass
    else:
        return render_template('cart.html')
    
@app.route('/')
@authenticate
def home(): 
    category: str = request.args.get('category')

    categories: tuple[tuple[str]] = product_manager.get_all_categories()
    products: tuple[tuple[str | float | int]] = product_manager.get_products(category)

    return render_template('home.html', categories=categories, products=products)

def serve():
    app.run(host='0.0.0.0', port=8080, debug=True)

if __name__ == '__main__':
    serve()
