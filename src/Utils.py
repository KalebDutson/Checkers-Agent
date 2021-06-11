from math import sqrt, pow

class Point:    

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __init__(self):
        self.__init__(0,0)

    def distance(self, other):
        return sqrt(pow(self.x - other.x, 2) + pow(self.y - other.y, 2))

    def length(self):
        return sqrt(self.x ** 2 + self.y ** 2)

    def __str__(self):
        return "(%s, %s)" % (self.x, self.y)