from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql
from functions import get_user_from_db, get_all_products, delete_product_by_id, get_product_by_id
from classes import ShoppingCart

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

cart = ShoppingCart()

def get_current_user():
    user_info = session.get('user')
    if not user_info:
        return None
    # Lazy import to avoid circular issues
    from classes import User
    u = User(user_info.get('username'), user_info.get('email'), user_info.get('id'))
    # propagate id to the User object so routes/templates use correct user
    if 'id' in user_info and user_info['id'] is not None:
        try:
            u.id = int(user_info['id'])
        except Exception:
            pass
    # The classes.User sets is_admin based on username; ensure it matches stored flag if present
    if 'is_admin' in user_info:
        u.is_admin = user_info['is_admin']
    return u

# Make get_current_user available in all templates
@app.context_processor
def inject_user():
    return {
        'get_current_user': get_current_user,
        'current_user': get_current_user()
    }

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
        user_obj, pw = get_user_from_db(email, conn)
        if user_obj and check_password_hash(pw, password):
            # store minimal user info in the session
            session['user'] = {
                'id': getattr(user_obj, 'id', None),
                'username': user_obj.username,
                'email': user_obj.email,
                'is_admin': getattr(user_obj, 'is_admin', False)
            }
            flash('Login successful!', 'success')
            return redirect(url_for('products'))
        else:
            flash('Invalid email or password.', 'error')
            return redirect(url_for('login'))
        
    return render_template('login.html')

@app.route('/logout')
def logout():
    # clear session user
    flash('You have been logged out.', 'info')
    session.pop('user', None)
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
    user = get_current_user()
    if user and getattr(user, 'is_admin', False):
        return redirect(url_for('admin_products'))
    products = get_all_products(conn)
    products = [p for p in products if getattr(p, 'is_active', True)]
    return render_template('products.html', products=products)

@app.route('/products/<int:product_id>', methods=['GET', 'POST'])
def product_detail(product_id):
    product = get_product_by_id(product_id, conn)
    print(product.description)
    if request.method == 'POST':
        # Add selected product to cart then redirect to cart view
        quantity = request.form.get('quantity', default=1, type=int)
        print(product, quantity)
        cart.add_item(product, quantity)
        return redirect(url_for('view_cart'))
    return render_template('product_detail.html', product=product)

# -----------------------------------------------------------------------------
# Shopping Cart Routes
@app.route('/cart')
def view_cart():
    # Simple cart view; adding happens in product_detail POST
    return render_template('cart.html', cart=cart)

@app.route('/cart/update_item/<int:product_id>', methods=['POST'])
def update_cart_item(product_id):
    quantity = request.form.get('quantity', default=1, type=int)
    cart.update_item(product_id, quantity)
    return redirect(url_for('view_cart'))

@app.route('/cart/remove_item/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    cart.remove_item(product_id)
    return redirect(url_for('view_cart'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    user = get_current_user()
    if not user:
        flash('Please log in to complete checkout.', 'error')
        return redirect(url_for('login'))

    # Ensure there are items in the cart
    if not cart.items:
        flash('Your cart is empty.', 'info')
        return redirect(url_for('view_cart'))

    try:
        cur = conn.cursor()
        # Insert order
        total = cart.get_cart_total()
        insert_order = "INSERT INTO orders (user_id, status, total) VALUES (%s, %s, %s)"
        cur.execute(insert_order, (getattr(user, 'id', None) or 1, 'pending', total))
        conn.commit()

        # Get the new order id
        order_id = cur.lastrowid

        # Insert order items
        insert_item = (
            "INSERT INTO order_items (order_id, product_id, quantity, unit_price, subtotal) "
            "VALUES (%s, %s, %s, %s, %s)"
        )
        for item, qty in zip(cart.items, cart.quantities):
            subtotal = float(item.unit_price) * int(qty)
            cur.execute(insert_item, (order_id, item.id, int(qty), float(item.unit_price), subtotal))
        conn.commit()

        # Decrease stock 
        try:
            for item, qty in zip(cart.items, cart.quantities):
                cur.execute("UPDATE products SET stock = stock - %s WHERE id = %s", (int(qty), item.id))
            conn.commit()
        except Exception:
            conn.rollback()

        # Clear the cart after successful checkout
        cart.items.clear()
        cart.quantities.clear()

        flash('Order placed successfully!', 'success')
        return redirect(url_for('products'))
    except Exception as e:
        conn.rollback()
        flash(f'Checkout failed: {str(e)}', 'error')
        return redirect(url_for('view_cart'))

@app.route('/orders/<int:user_id>')
def orders(user_id):
    user = get_current_user()
    if not user:
        flash('Please log in to view your orders.', 'error')
        return redirect(url_for('login'))
    effective_user_id = getattr(user, 'id', None) or user_id
    if effective_user_id != user_id:
        return redirect(url_for('orders', user_id=effective_user_id))

    cur = conn.cursor()
    # Fetch orders for user, newest first
    cur.execute(
        "SELECT id, status, total, created_at FROM orders WHERE user_id = %s ORDER BY created_at DESC",
        (user_id,)
    )
    orders = cur.fetchall()

    order_ids = [row['id'] for row in orders]
    items_by_order = {}
    if order_ids:
        # Fetch items for these orders
        format_strings = ','.join(['%s'] * len(order_ids))
        cur.execute(
            f"""
            SELECT oi.order_id, oi.product_id, oi.quantity, oi.unit_price, oi.subtotal,
                   p.name
            FROM order_items oi
            JOIN products p ON p.id = oi.product_id
            WHERE oi.order_id IN ({format_strings})
            ORDER BY oi.order_id ASC
            """,
            tuple(order_ids)
        )
        for row in cur.fetchall():
            items_by_order.setdefault(row['order_id'], []).append(row)

    return render_template('orders.html', orders=orders, items_by_order=items_by_order)

# -----------------------------------------------------------------------------
# Admin Routes
@app.route('/admin/products')
def admin_products():
    user = get_current_user()
    if not user or not getattr(user, 'is_admin', False):
        flash('Access denied. Admins only.', 'error')
        return redirect(url_for('login'))
    prods = get_all_products(conn)
    return render_template('admin_products.html', products=prods)

# Users
@app.route('/admin/users', methods=['GET'])
def admin_users():
    user = get_current_user()
    if not user or not getattr(user, 'is_admin', False):
        flash('Access denied. Admins only.', 'error')
        return redirect(url_for('login'))

    q = request.args.get('q', '').strip()
    cur = conn.cursor()
    if q:
        cur.execute(
            """
            SELECT id, name, email, created_at, is_active
            FROM users
            WHERE name LIKE %s OR email LIKE %s OR CAST(id AS CHAR) = %s
            ORDER BY created_at DESC
            """,
            (f"%{q}%", f"%{q}%", q)
        )
    else:
        cur.execute("SELECT id, name, email, created_at, is_active FROM users ORDER BY created_at DESC")
    users = cur.fetchall()
    return render_template('admin_users.html', users=users, q=q)

@app.route('/admin/users/add', methods=['GET', 'POST'])
def admin_add_user():
    user = get_current_user()
    if not user or not getattr(user, 'is_admin', False):
        flash('Access denied. Admins only.', 'error')
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        is_active = int(request.form.get('is_active', 1))
        pw_hash = generate_password_hash(password)
        cur = conn.cursor()
        cur.execute("INSERT INTO users (name, email, password, is_active) VALUES (%s, %s, %s, %s)", (name, email, pw_hash, is_active))
        conn.commit()
        flash('User added.', 'success')
        return redirect(url_for('admin_users'))
    return render_template('admin_edit_user.html', user=None)

@app.route('/admin/users/<int:user_id>', methods=['GET', 'POST'])
def admin_edit_user(user_id):
    user = get_current_user()
    if not user or not getattr(user, 'is_admin', False):
        flash('Access denied. Admins only.', 'error')
        return redirect(url_for('login'))
    cur = conn.cursor()
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        is_active = int(request.form.get('is_active', 1))
        password = request.form.get('password')
        if password:
            pw_hash = generate_password_hash(password)
            cur.execute("UPDATE users SET name=%s, email=%s, password=%s, is_active=%s WHERE id=%s", (name, email, pw_hash, is_active, user_id))
        else:
            cur.execute("UPDATE users SET name=%s, email=%s, is_active=%s WHERE id=%s", (name, email, is_active, user_id))
        conn.commit()
        flash('User updated.', 'success')
        return redirect(url_for('admin_users'))
    cur.execute("SELECT id, name, email, created_at, is_active FROM users WHERE id=%s", (user_id,))
    u = cur.fetchone()
    return render_template('admin_edit_user.html', user=u)

@app.route('/admin/users/delete/<int:user_id>', methods=['POST'])
def admin_delete_user(user_id):
    user = get_current_user()
    if not user or not getattr(user, 'is_admin', False):
        flash('Access denied. Admins only.', 'error')
        return redirect(url_for('login'))
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id=%s", (user_id,))
    conn.commit()
    flash('User deleted.', 'success')
    return redirect(url_for('admin_users'))

# Orders
@app.route('/admin/orders', methods=['GET'])
def admin_orders():
    user = get_current_user()
    if not user or not getattr(user, 'is_admin', False):
        flash('Access denied. Admins only.', 'error')
        return redirect(url_for('login'))
    q = request.args.get('q', '').strip()
    cur = conn.cursor()
    if q:
        cur.execute(
            """
            SELECT o.id, o.user_id, u.name, u.email, o.status, o.total, o.created_at
            FROM orders o
            JOIN users u ON u.id = o.user_id
            WHERE u.name LIKE %s OR u.email LIKE %s OR CAST(o.user_id AS CHAR) = %s
            ORDER BY o.created_at DESC
            """,
            (f"%{q}%", f"%{q}%", q)
        )
    else:
        cur.execute(
            "SELECT o.id, o.user_id, u.name, u.email, o.status, o.total, o.created_at FROM orders o JOIN users u ON u.id=o.user_id ORDER BY o.created_at DESC"
        )
    orders = cur.fetchall()
    return render_template('admin_orders.html', orders=orders, q=q)

@app.route('/admin/orders/<int:order_id>', methods=['GET', 'POST'])
def admin_order_detail(order_id):
    user = get_current_user()
    if not user or not getattr(user, 'is_admin', False):
        flash('Access denied. Admins only.', 'error')
        return redirect(url_for('login'))
    cur = conn.cursor()
    if request.method == 'POST':
        status = request.form.get('status')
        total = request.form.get('total')
        cur.execute("UPDATE orders SET status=%s, total=%s WHERE id=%s", (status, total, order_id))
        conn.commit()
        flash('Order updated.', 'success')
        return redirect(url_for('admin_order_detail', order_id=order_id))
    # fetch order
    cur.execute("SELECT o.id, o.user_id, u.name, u.email, o.status, o.total, o.created_at FROM orders o JOIN users u ON u.id=o.user_id WHERE o.id=%s", (order_id,))
    order = cur.fetchone()
    # fetch items
    cur.execute(
        """
        SELECT oi.id, oi.product_id, p.name, oi.quantity, oi.unit_price, oi.subtotal
        FROM order_items oi
        JOIN products p ON p.id=oi.product_id
        WHERE oi.order_id=%s
        ORDER BY oi.id ASC
        """,
        (order_id,)
    )
    items = cur.fetchall()
    return render_template('admin_order_detail.html', order=order, items=items)

@app.route('/admin/orders/<int:order_id>/items/add', methods=['POST'])
def admin_order_item_add(order_id):
    user = get_current_user()
    if not user or not getattr(user, 'is_admin', False):
        flash('Access denied. Admins only.', 'error')
        return redirect(url_for('login'))
    cur = conn.cursor()
    product_id = int(request.form.get('product_id'))
    quantity = int(request.form.get('quantity'))
    # get price
    cur.execute("SELECT unit_price FROM products WHERE id=%s", (product_id,))
    row = cur.fetchone()
    unit_price = float(row['unit_price']) if row else 0.0
    subtotal = unit_price * quantity
    cur.execute("INSERT INTO order_items (order_id, product_id, quantity, unit_price, subtotal) VALUES (%s, %s, %s, %s, %s)", (order_id, product_id, quantity, unit_price, subtotal))
    conn.commit()
    flash('Item added.', 'success')
    return redirect(url_for('admin_order_detail', order_id=order_id))

@app.route('/admin/orders/items/<int:item_id>/update', methods=['POST'])
def admin_order_item_update(item_id):
    user = get_current_user()
    if not user or not getattr(user, 'is_admin', False):
        flash('Access denied. Admins only.', 'error')
        return redirect(url_for('login'))
    cur = conn.cursor()
    quantity = int(request.form.get('quantity'))
    unit_price = float(request.form.get('unit_price'))
    subtotal = unit_price * quantity
    cur.execute("UPDATE order_items SET quantity=%s, unit_price=%s, subtotal=%s WHERE id=%s", (quantity, unit_price, subtotal, item_id))
    conn.commit()
    flash('Item updated.', 'success')
    # need order_id to redirect; fetch
    cur.execute("SELECT order_id FROM order_items WHERE id=%s", (item_id,))
    row = cur.fetchone()
    return redirect(url_for('admin_order_detail', order_id=row['order_id']))

@app.route('/admin/orders/items/<int:item_id>/delete', methods=['POST'])
def admin_order_item_delete(item_id):
    user = get_current_user()
    if not user or not getattr(user, 'is_admin', False):
        flash('Access denied. Admins only.', 'error')
        return redirect(url_for('login'))
    cur = conn.cursor()
    cur.execute("SELECT order_id FROM order_items WHERE id=%s", (item_id,))
    row = cur.fetchone()
    cur.execute("DELETE FROM order_items WHERE id=%s", (item_id,))
    conn.commit()
    flash('Item deleted.', 'success')
    return redirect(url_for('admin_order_detail', order_id=row['order_id']))

@app.route('/admin/orders/delete/<int:order_id>', methods=['POST'])
def admin_order_delete(order_id):
    user = get_current_user()
    if not user or not getattr(user, 'is_admin', False):
        flash('Access denied. Admins only.', 'error')
        return redirect(url_for('login'))
    cur = conn.cursor()
    cur.execute("DELETE FROM orders WHERE id=%s", (order_id,))
    conn.commit()
    flash('Order deleted.', 'success')
    return redirect(url_for('admin_orders'))

@app.route('/admin/products/add', methods=['GET', 'POST'])
def admin_add_product():
    user = get_current_user()
    if not user or not getattr(user, 'is_admin', False):
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
    user = get_current_user()
    if not user or not getattr(user, 'is_admin', False):
        flash('Access denied. Admins only.', 'error')
        return redirect(url_for('login'))
    delete_product_by_id(product_id, conn)
    flash(f'Product {product_id}, deleted successfully.', 'success')
    return redirect(url_for('admin_products'))

@app.route('/admin/products/<int:product_id>', methods=['GET', 'POST'])
def admin_edit_product(product_id):
    user = get_current_user()
    if not user or not getattr(user, 'is_admin', False):
        flash('Access denied. Admins only.', 'error')
        return redirect(url_for('login'))
    prod = get_product_by_id(product_id, conn)
    
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        unit_price = request.form.get('unit_price')
        stock = request.form.get('stock')
        description = request.form.get('description')

        # Update product in database
        cur = conn.cursor()
        update_query = "UPDATE products SET name=%s, unit_price=%s, stock=%s, description=%s WHERE id=%s"
        cur.execute(update_query, (name, unit_price, stock, description, product_id))
        conn.commit()
        flash(f'Product {name} updated successfully.', 'success')
        return redirect(url_for('admin_products'))
    return render_template('admin_edit_product.html', product=prod)

if __name__ == '__main__':
    app.run(debug=True)
