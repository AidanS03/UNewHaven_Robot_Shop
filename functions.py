from classes import User, Product

def get_user_from_db(email, conn):
    cur = conn.cursor()
    query = "SELECT * FROM users WHERE email = %s"
    cur.execute(query, (email,))
    result = cur.fetchone()
    if result:
        return (User(result['name'], result['email']), result['password'])
    return None

def get_all_products(conn):
    cur = conn.cursor()
    query = "SELECT * FROM products"
    cur.execute(query)
    products = [Product(product['id'], product['name'], product['unit_price'], product['stock'], product['description']) for product in cur.fetchall()]
    return products

def get_product_by_id(product_id, conn):
    cur = conn.cursor()
    query = "SELECT * FROM products WHERE id = %s"
    cur.execute(query, (product_id,))
    product = cur.fetchone()
    if product:
        return Product(product['id'], product['name'], product['unit_price'], product['stock'], product['description'])
    return None

def delete_product_by_id(product_id, conn):
    cur = conn.cursor()
    query = "DELETE FROM products WHERE id = %s"
    cur.execute(query, (product_id,))
    conn.commit()