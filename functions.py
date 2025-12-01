from classes import User

def get_user_from_db(email, conn):
    cur = conn.cursor()
    query = "SELECT * FROM users WHERE email = %s"
    cur.execute(query, (email,))
    result = cur.fetchone()
    if result:
        return (User(result['name'], result['email']), result['password'])
    return None