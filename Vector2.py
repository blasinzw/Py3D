__author__ = 'Zander'
import math


class Vector2:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.length = math.sqrt(x**2 + y**2)

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Vector2(self.x * other.x, self.y * other.y)

    def __div__(self, other):
        return Vector2(self.x / other.x, self.y / other.y)

    def normalize(self):
        self.x /= self.length
        self.y /= self.length

        return self

    def dot_product(self, other):
        return (self.x * other.x) + (self.y * other.y)

    def rotate(self, theta):
        theta = math.radians(theta)

        rotX = self.x * math.cos(theta) - self.y * math.sin(theta)
        rotY = self.x * math.sin(theta) + self.y * math.cos(theta)

        return Vector2(rotX, rotY)
