import pymysql
from flask import url_for


class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email
        self.id = 1
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
    def __init__(self, product_id, name, unit_price, stock, desc, is_active=False):
        self.id = product_id
        self.name = name
        self.unit_price = unit_price
        self.stock = stock
        self.description = desc
        self.is_active = is_active
        self.image_path = f"{self.name}.jpg"

    def is_in_stock(self):
        return self.stock > 0
    
    def get_product_info(self):
        return {
            'product_id': self.id,
            'name': self.name,
            'unit_price': self.unit_price,
            'stock': self.stock,
            'description': self.description,
            'is_active': self.is_active
        }

class ShoppingCart:
    def __init__(self):
        self.items = []
        self.quantities = []
        self.tax_rate = 0.0635  # 6.35% sales tax

    def add_item(self, product, quantity):
        for item in self.items:
            if item.id == product.id:
                index = self.items.index(item)
                self.quantities[index] += quantity
                return
        self.items.append(product)
        self.quantities.append(quantity)

    def get_cart_subtotal(self):
        return float(sum(item.unit_price * qty for item, qty in zip(self.items, self.quantities)))

    def get_cart_total(self):
        subtotal = self.get_cart_subtotal()
        tax = subtotal * self.tax_rate
        return subtotal + tax
    
    def get_cart_tax(self):
        subtotal = self.get_cart_subtotal()
        return subtotal * self.tax_rate
    
    def get_item_total(self, product_id):
        for item in self.items:
            if item.id == product_id:
                index = self.items.index(item)
                return item.unit_price * self.quantities[index]
        return 0
    
    def get_item_quantity(self, product_id):
        for item in self.items:
            if item.id == product_id:
                index = self.items.index(item)
                return self.quantities[index]
        return 0

    def update_item(self, product_id, new_quantity):
        for item in self.items:
            if item.id == product_id:
                index = self.items.index(item)
                self.quantities[index] = new_quantity
                break

    def remove_item(self, product_id):
        for item in self.items:
            if item.id == product_id:
                index = self.items.index(item)
                self.items.pop(index)
                self.quantities.pop(index)
                break
