import numbers
import math

class Complex:

    def __init__(self, x = 0, y = 0):
        if not isinstance(x, (numbers.Number, numbers.Real)):
            raise ValueError
        if not isinstance(y, (numbers.Number, numbers.Real)):
            raise ValueError
        self.x = x
        self.y = y

    def __add__(self, other):
        if not isinstance(other, Complex):
            other = Complex(other)
        return Complex(self.x + other.x, self.y + other.y)

    def __radd__(self, other):
        return Complex.__add__(self, other)

    def __sub__(self, other):
        if not isinstance(other, Complex):
            other = Complex(other)
        return Complex(self.x - other.x, self.y - other.y)

    def __rsub__(self, other):
        if not isinstance(other, Complex):
            other = Complex(other)
        return Complex.__sub__(other, self)

    def __mul__(self, other):
        if not isinstance(other, Complex):
            other = Complex(other)
        x1, y1, x2, y2 = self.x, self.y, other.x, other.y
        return Complex(x1 * x2 - y1 * y2, x1 * y2 + y1 * x2)

    def __rmul__(self, other):
        return Complex.__mul__(self, other)

    def __truediv__(self, other):
        if not isinstance(other, Complex):
            other = Complex(other)
        x1, y1, x2, y2 = self.x, self.y, other.x, other.y
        return Complex((x1 * x2 + y1 * y2) / (x2 ** 2 + y2 ** 2), (y1 * x2 - x1 * y2) / (x2 ** 2 + y2 ** 2))

    def __rtruediv__(self, other):
        if not isinstance(other, Complex):
            other = Complex(other)
        return Complex.__truediv__(other, self)

    def __iadd__(self, other):
        self = Complex.__add__(self, other)
        return self

    def __isub__(self, other):
        self = Complex.__sub__(self, other)
        return self

    def __imul__(self, other):
        self = Complex.__mul__(self, other)
        return self

    def __itruediv__(self, other):
        self = Complex.__truediv__(self, other)
        return self

    def __pow__(self, other):
        if not isinstance(other, numbers.Number):
            other = numbers.Number(other)

        if other == 0:
            return Complex(1, 0)
        
        result = Complex(1, 0)
        if other > 0:
            while other:
                if other & 1:
                    result *= self
                self *= self
                other >>= 1
        else:
            other = -other
            while other:
                if other & 1:
                    result /= self
                self *= self
                other >>= 1
        return result

    def __abs__(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def __str__(self):
        return "{}+{}i".format(self.x, self.y)

    __repr__ = __str__
