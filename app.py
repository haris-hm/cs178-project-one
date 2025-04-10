from flask import Flask
from flask import render_template
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)

@app.route('/login')
def account():
    return render_template('login.html')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
