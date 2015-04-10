__author__ = 'Zander'

class Light ():

    def __init__(self, position, intensity):
        self.position = position
        self.intensity = intensity

    #other is a Vector3
    def getIntensity(self, other):
        return self.intensity / (other - self.position).length