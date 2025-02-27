#Task 1
class Vehicle:
    def __init__(self, vehicle_id:str, make:str, model: str, year: int):
        self.vehicle_id = vehicle_id
        self.make = make
        self.model = model
        self.year = year
    def __str__(self):    #added another quote for the string to make it quoted for output
        return f"Vehicle(vehicle_id='{self.vehicle_id}', make = '{self.make}', year = {self.year})" 
    def __repr__(self):  #developer- friendly output for reader
        return self.__str__()

car = Vehicle("VIN123", "Toyota", "Camry", 2020)
print(car)
