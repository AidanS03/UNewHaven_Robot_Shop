from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql

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
        email = request.form.get('email')
        password = request.form.get('password')
        cur = conn.cursor()
        query = "SELECT * FROM users WHERE email = %s"
        cur.execute(query, (email,))
        result = cur.fetchall()
        if result and check_password_hash(result[0]['password'], password):
            global user
            user = result[0]
            # print(user['name'])
            flash('Login successful!', 'success')
            return redirect(url_for('products'))
        else:
            flash('Invalid email or password.', 'error')
            return redirect(url_for('login'))
        
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Handle signup logic here
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('signup'))
        
        cur = conn.cursor()
        query = "SELECT * FROM users WHERE email = %s"
        cur.execute(query, (email,))
        result = cur.fetchall()
        if not result:
            pw_hash = generate_password_hash(password)
            insert_query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
            cur.execute(insert_query, (full_name, email, pw_hash))
            conn.commit()
            flash('Account created. Please log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('A user with that email already exists.', 'error')
            return redirect(url_for('signup'))

    return render_template('signup.html')

@app.route('/products')
def products():
    return render_template('products.html')

if __name__ == '__main__':
    app.run(debug=True)
