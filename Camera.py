__author__ = 'Zander'
from Vector3 import Vector3

class Camera:

    def __init__(self):
        self.position = Vector3(0,0,0)
        self.target = Vector3(0,0,0)