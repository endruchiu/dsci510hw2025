#Task 1 OOP - Vehicle Inheritance
class Vehicle:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year
    def __str__(self):
        return f"{self.year} {self.make} {self.model}"
class Bike(Vehicle):
    def __init__(self, make, model, year, bike_type):
        super().__init__(make,model,year) #parent class
        self.bike_type = bike_type # subclass attribute
    def __str__(self):
        original_str = super().__str__() #parent class gonna use it on all sub class
        return f"{original_str}, {self.bike_type} type"
class Car(Vehicle):
    def __init__(self, make, model, year, is_electric = False):
        super().__init__(make, model, year)
        self.is_electric = is_electric
    def __str__(self):
        original_str = super().__str__()
        if self.is_electric:
            return f"{original_str}, Electric"
        else:
            return f"{original_str}, Non-Electric"
    def driving_range(self, energy):
        miles_per_battery_percent = 4
        miles_per_gallon = 30
        if self.is_electric:
            return miles_per_battery_percent * energy
        else:
            return miles_per_gallon * energy

#electric car
my_car = Car("tesla", "model s", 2020, True)
print(my_car)
print("electric car driving range:", my_car.driving_range(50))
#car
my_non_electric_car = Car("Ford", "Mustang", 1965)
print(my_non_electric_car)
print("Non-Electric Car Driving Range:", my_non_electric_car.driving_range(10))
#bike
my_bike = Bike("Trek", "Domane", 2019, "road")
print(my_bike)
