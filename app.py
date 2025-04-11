from flask import Flask, render_template, request, redirect, url_for, flash

import user_manager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

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
            # Very secure, I know...
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
        
        flash('Your account has been created', 'success')
        return redirect(url_for('login'))
    else:
        return render_template('register.html')

@app.route('/')
def home():
    try:
        # Very secure authentication
        username = request.args['username']
        password = request.args['password']

        password_valid: bool | None = user_manager.validate_password(username, password)

        # Redirect the user to the login page if any info is invalid
        if not password_valid or password_valid is None:
            flash('Incorrect username or password', 'danger')
            return redirect(url_for('login'))
    except Exception as _:
        return redirect(url_for('login'))

    return render_template('home.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
