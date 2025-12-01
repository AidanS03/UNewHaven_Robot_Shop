from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql
from functions import get_user_from_db
# from classes import User, Product

app = Flask(__name__)
# needed for flashing messages to the template
app.secret_key = 'replace-this-with-a-secure-random-key'

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='password',
    database='robotStore',
    cursorclass=pymysql.cursors.DictCursor
)

user = None

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # if POST, get email and pw then validate
        email = request.form.get('email')
        password = request.form.get('password')
        global user
        user, pw = get_user_from_db(email, conn)
        if user and check_password_hash(pw, password):
            flash('Login successful!', 'success')
            return redirect(url_for('products'))
        else:
            flash('Invalid email or password.', 'error')
            return redirect(url_for('login'))
        
    return render_template('login.html')

@app.route('/logout')
def logout():
    # clear user variable
    flash('You have been logged out.', 'info')
    global user
    user = None
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # If POST, get form data and create account
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # check if passwords match
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('signup'))
        
        # check if user already exists
        cur = conn.cursor()
        query = "SELECT * FROM users WHERE email = %s"
        cur.execute(query, (email,))
        result = cur.fetchall()
        if not result:
            # create new user
            pw_hash = generate_password_hash(password)
            insert_query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
            cur.execute(insert_query, (full_name, email, pw_hash))
            conn.commit()
            flash('Account created. Please log in.', 'success')
            return redirect(url_for('login'))
        else:
            # user exists, flash error
            flash('A user with that email already exists.', 'error')
            return redirect(url_for('signup'))

    return render_template('signup.html')

@app.route('/products')
def products():
    
    cur = conn.cursor()
    query = "SELECT id, name, unit_price, stock, description FROM products"
    cur.execute(query)
    products = cur.fetchall()
    print(products)
    return render_template('products.html', products=products)

@app.route('/products/<int:product_id>')
def product_detail(product_id):
    cur = conn.cursor()
    query = "SELECT * FROM products WHERE id = %s"
    cur.execute(query, (product_id,))
    product = cur.fetchone()
    return render_template('product_detail.html', product=product)

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    return redirect(url_for('products'))

if __name__ == '__main__':
    app.run(debug=True)
