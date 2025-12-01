import pymysql


class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email
        if self.username == 'admin':
            self.is_admin = True
        else:
            self.is_admin = False

    def get_profile(self):
        return {
            'username': self.username,
            'email': self.email,
            'is_admin': self.is_admin
        }
        
class Product:
    def __init__(self, product_id, name, price, stock):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock
        self.description = ""
        self.image_path = f"images/{self.product_id}.jpg"

    def is_in_stock(self):
        return self.stock > 0
    
    def get_product_info(self):
        return {
            'product_id': self.product_id,
            'name': self.name,
            'price': self.price,
            'stock': self.stock,
            'description': self.description
        }
        
