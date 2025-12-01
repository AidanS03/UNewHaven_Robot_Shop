from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql
from functions import get_user_from_db, get_all_products, delete_product_by_id, get_product_by_id
# from classes import User, Product

# *****************************************************************************
# Initializations
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

# *****************************************************************************
# Routes
@app.route('/')
def home():
    return redirect(url_for('logout'))

# -----------------------------------------------------------------------------
# Basic User Authentication Routes
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
            if user.is_admin:
                return redirect(url_for('admin_products'))
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

# -----------------------------------------------------------------------------
# Product and Shopping Routes, main user pages
@app.route('/products')
def products(): 
    
    cur = conn.cursor()
    query = "SELECT id, name, unit_price, stock, description FROM products"
    cur.execute(query)
    products = cur.fetchall()
    return render_template('products.html', products=products)

@app.route('/products/<int:product_id>')
def product_detail(product_id):
    product = get_product_by_id(product_id, conn)
    print(product)
    return render_template('product_detail.html', product=product)

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    return redirect(url_for('products'))

# -----------------------------------------------------------------------------
# Admin Routes
@app.route('/admin/products')
def admin_products():
    global user
    if not user or not user.is_admin:
        flash('Access denied. Admins only.', 'error')
        return redirect(url_for('login'))
    prods = get_all_products(conn)
    return render_template('admin_products.html', products=prods)

@app.route('/admin/products/add', methods=['GET', 'POST'])
def admin_add_product():
    global user
    if not user or not user.is_admin:
        flash('Access denied. Admins only.', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        unit_price = request.form.get('unit_price')
        stock = request.form.get('stock')
        description = request.form.get('description')

        # Insert new product into database
        cur = conn.cursor()
        insert_query = "INSERT INTO products (name, unit_price, stock, description) VALUES (%s, %s, %s, %s)"
        cur.execute(insert_query, (name, unit_price, stock, description))
        conn.commit()
        flash(f'Product {name} added successfully.', 'success')
        return redirect(url_for('admin_products'))
    return render_template('admin_add_product.html')

@app.route('/admin/products/delete/<int:product_id>', methods=['POST'])
def admin_delete_product(product_id):
    global user
    if not user or not user.is_admin:
        flash('Access denied. Admins only.', 'error')
        return redirect(url_for('login'))
    delete_product_by_id(product_id, conn)
    flash(f'Product {product_id}, deleted successfully.', 'success')
    return redirect(url_for('admin_products'))

@app.route('/admin/products/<int:product_id>', methods=['GET', 'POST'])
def admin_edit_product(product_id):
    global user
    if not user or not user.is_admin:
        flash('Access denied. Admins only.', 'error')
        return redirect(url_for('login'))
    prod = get_product_by_id(product_id, conn)
    return render_template('admin_edit_product.html', product=prod)

if __name__ == '__main__':
    app.run(debug=True)
