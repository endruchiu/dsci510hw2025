#Task 3
import math
class Shape:
    def area(self):
        raise NotImplementedError("This method should be overridden by subclass")

class Rectangle(Shape):
    def __init__(self, length= None, width= None, side = None):
        if side is not None: 
            self.length = side #square
            self.width = side
        else:
            self.length = length
            self.width = width  
    def area(self):
        return self.length * self.width

    def dimensions(self):
        if self.length == self.width:
            return{"side": self.length}
        else:
            return {"length": self.length, "width": self.width}
class Circle(Shape):
    def __init__(self,radius):
        self.radius = radius
    def area(self):
        return round(math.pi * (self.radius ** 2), 2)
    def dimensions(self):
        return {"radius": self.radius}

rectangle = Rectangle(length =5, width = 10)
print(rectangle.area())
print(rectangle.dimensions())

square = Rectangle(side = 5)
print(square.area())
print(square.dimensions())

circle = Circle(radius = 7)
print(circle.area())
print(circle.dimensions())
