#Task 3
class Product: #class
    def __init__(self, product_code, name, price, quantity_available):
        self.product_code = product_code
        self.name = name
        self.price = price
        self.quantity_available = quantity_available

    def update_price(self, updated_price):
        self.price = updated_price
    def add_stock(self, quantity):
        self.quantity_available = self.quantity_available + quantity #right side calculates the quantity and stores into the left side
    def sell_product(self, quantity):
        if quantity > 0 and self.quantity_available >= quantity:
            self.quantity_available = self.quantity_available - quantity
        else:
            print("Unable to perform any sale")
    def __str__(self):
        return f"Product(product_code = {self.product_code}, name = {self.name}, price = {self.price}, quantity_available = {self.quantity_available})"
    def __repr__(self):
        return self.__str__()

#instance

product = Product("12345", "Coffee Mug", 12.99, 100)
print(product)
