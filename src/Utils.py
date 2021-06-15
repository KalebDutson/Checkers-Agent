from math import sqrt, pow

class Point:    

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, other):
        return sqrt(pow(self.x - other.x, 2) + pow(self.y - other.y, 2))

    def length(self):
        return sqrt(self.x ** 2 + self.y ** 2)

    def __str__(self):
        return "(%s, %s)" % (self.x, self.y)

    def __eq__(self, other):
        if other == None:
            return False
        elif isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        else:
            return False

    def __ne__(self, other):
        if other == None:
            return True
        elif isinstance(other, Point):
            return self.x != other.x or self.y != other.y
        else:
            return True

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    # divide all points by divisor
    def divide(self, divisor):
        return Point(self.x // divisor, self.y // divisor)