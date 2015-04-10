__author__ = 'Zander'
import math
import numpy as np

class Vector3:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.length = math.sqrt(x**2 + y**2 + z**2)

    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        return Vector3(self.x * other.x, self.y * other.y, self.z * other.z)

    def __div__(self, other):
        return Vector3(self.x / other.x, self.y / other.y, self.z / other.z)

    def normalize(self):
        self.x /= self.length
        self.y /= self.length
        self.z /= self.length

        self.length = math.sqrt(self.x**2 + self.y**2 + self.z**2)

        return self

    def getAngle(self, other):
        return math.acos(self.dot_product(other)/(self.length * other.length))

    def dot_product(self, other):
        return (self.x * other.x) + (self.y * other.y) + (self.z + other.z)

    def dot_product_with_matrix(self, other):
        matrix = np.dot(np.matrix([self.x, self.y, self.z, 1]), other)
        matrix = matrix.getA()
        return Vector3(matrix[0][0], matrix[0][1], matrix[0][2])

    def cross_product(self, other):
        crossX = self.y * other.z - (self.z * other.z)
        crossY = self.z * other.x - (self.x * other.z)
        crossZ = self.x * other.y - (self.y * other.x)

        return Vector3(crossX, crossY, crossZ)

    def rotate(self, theta, axis):
        theta = math.radians(theta)
        if axis == "x":
            rotY = self.y * math.cos(theta) - self.z*math.sin(theta)
            rotZ = self.y * math.sin(theta) + self.z*math.cos(theta)
            rotX = self.x
        if axis == "y":
            rotZ = self.z * math.cos(theta) - self.x*math.sin(theta)
            rotX = self.z * math.sin(theta) + self.x*math.cos(theta)
            rotY = self.y
        if axis == "z":
            rotX = self.x * math.cos(theta) - self.y*math.sin(theta)
            rotY = self.x * math.sin(theta) + self.y*math.cos(theta)
            rotZ = self.z

        return Vector3(rotX, rotY, rotZ)