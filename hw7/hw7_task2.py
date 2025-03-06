#Task 2
class ComplexNumber:
    def __init__(self, real, imaginary):
        self.real = real
        self.imag = imaginary
    def __add__(self, other):
        return ComplexNumber(self.real + other.real, self.imag + other.imag)  #(a + c) + (b+d)i 
    def __mul__(self, other):
        real_part = self.real * other.real - self.imag * other.imag #ac-bd
        imag_part = self.real * other.imag + self.imag * other.real #(ad + bc)i
        return ComplexNumber(real_part, imag_part)
    def __str__(self):
        return f"Complex number with real part {self.real} and imaginary part {self.imag}"

a = ComplexNumber(2, 3) #2+ 3 i
b = ComplexNumber(1, 7) #1 + 7i
c = a + b
d = a * b 
print(c) #3 + 10i
print(d)
