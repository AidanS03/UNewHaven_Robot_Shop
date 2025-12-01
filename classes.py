import pymysql
from flask import url_for


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
    def __init__(self, product_id, name, unit_price, stock, desc):
        self.id = product_id
        self.name = name
        self.unit_price = unit_price
        self.stock = stock
        self.description = ""
        self.image_path = f"{self.name}.jpg"

    def is_in_stock(self):
        return self.stock > 0
    
    def get_product_info(self):
        return {
            'product_id': self.id,
            'name': self.name,
            'unit_price': self.unit_price,
            'stock': self.stock,
            'description': self.description
        }
        
class CartItem:
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity

    def get_total_price(self):
        return self.product.price * self.quantity
    
class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_item(self, product, quantity):
        self.items.append(CartItem(product, quantity))

    def get_cart_total(self):
        return sum(item.get_total_price() for item in self.items)
