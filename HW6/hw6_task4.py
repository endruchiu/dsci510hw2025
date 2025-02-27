#Task 4
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

class Shopper:
    def __init__(self, name, shopper_id):
        self.name = name
        self.shopper_id = shopper_id
        self.cart = {} #empty dictionary product as object
    def add_item(self, product, quantity):
        if quantity < 0:
            print("No nonnegative integer") #non negative
            return
        if product in self.cart:
            self.cart[product] = self.cart[product] + quantity # increase by quantity
        else:
            self.cart[product] = quantity
    def remove_item(self, product, quantity):
        if product not in self.cart:
            print("no execution")
            return
        if self.cart[product] <= quantity:
            del self.cart[product]
        else:
            self.cart[product] -= quantity
    def cart_total(self):
        total = sum(product.price * quantity for product, quantity in self.cart.items())
        return round(total, 2)

    def __str__(self):
        cart_items = ", ".join([f"{product.name} x{quantity}" for product, quantity in self.cart.items()])
        return f"Shopper({self.name}, ID: {self.shopper_id}, Cart: [{cart_items}], Total: ${self.cart_total()})"

class PremiumShopper(Shopper):
    def __init__(self, name, shopper_id):
        super().__init__(name, shopper_id)  #inherit the calss
    def cart_total(self):
        total = super().cart_total()
        if total >= 50:
            return round(total * 0.965, 2)
        return total

RTX_4090 = Product("1", "RTX_4090", 1999.99, 10)
Call_of_Duty = Product("2", "Call_of_Duty", 70, 100)
#Calculate my total
shopper = Shopper("Andrew", "007")
shopper.add_item(RTX_4090, 1)
shopper.add_item(Call_of_Duty,1)
print(shopper)
#Removing one of my items
shopper = Shopper("Andrew", "007")
shopper.add_item(RTX_4090, 1)
shopper.add_item(Call_of_Duty,1)

shopper.remove_item(Call_of_Duty, 1)

print(shopper)
#Premium shopper privillege
shopper = PremiumShopper("Andrew", "007")
shopper.add_item(RTX_4090, 1)
shopper.add_item(Call_of_Duty,1)
print(shopper)  #4.5 percent off
