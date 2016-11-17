
class Celsius:
    
    def __init__(self):
        self.celsius = 0

    def __get__(self, instance, owner): #fahrenh -> cels
        return (5 / 9) * (instance.fahrenheit - 32)

    def __set__(self, instance, value): #fahrenh <- cels
        instance.fahrenheit = (9 / 5) * value + 32

class Temperature:
    celsius = Celsius()

    def __init__(self, value = 0):
        self.fahrenheit = value


