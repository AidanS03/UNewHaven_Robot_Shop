from classes import User, Product

def get_user_from_db(email, conn):
    cur = conn.cursor()
    query = "SELECT * FROM users WHERE email = %s"
    cur.execute(query, (email,))
    result = cur.fetchone()
    if result:
        user = User(result['name'], result['email'], result.get('id'))
        # propagate DB id and is_admin flag if present
        if 'id' in result:
            try:
                user.id = int(result['id'])
            except Exception:
                pass
        if 'is_admin' in result:
            user.is_admin = bool(result['is_admin'])
        return (user, result.get('password'))
    return (None, None)

def get_all_products(conn):
    cur = conn.cursor()
    query = "SELECT * FROM products"
    cur.execute(query)
    products = [Product(product['id'], product['name'], product['unit_price'], product['stock'], product['description'], product['is_active']) for product in cur.fetchall()]
    return products

def get_product_by_id(product_id, conn):
    cur = conn.cursor()
    query = "SELECT * FROM products WHERE id = %s"
    cur.execute(query, (product_id,))
    product = cur.fetchone()
    if product:
        return Product(product['id'], product['name'], product['unit_price'], product['stock'], product['description'], product['is_active'])
    return None

def delete_product_by_id(product_id, conn):
    cur = conn.cursor()
    query = "DELETE FROM products WHERE id = %s"
    cur.execute(query, (product_id,))
    conn.commit()