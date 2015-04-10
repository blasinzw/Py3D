__author__ = 'Zander'

import numpy as np
import math

class Matrix4:

    def __init__(self):
        pass

    #all functions take a Vector3 for second parameter

    def get_translation_matrix(self, v):
        matrix = np.array([[1,0,0,0],
                          [0,1,0,0],
                          [0,0,1,0],
                          [v.x,v.y,1,1]])
        #temporary something is wrong!!!!

        return matrix

    def get_scaling_matrix(self, v):
        matrix = np.array([[v.x,0,0,0],
                          [0,v.y,0,0],
                          [0,0,v.z,0],
                          [0,0,0,1]])

        return matrix

    """
    Args:
        axis: is a string of either "x", "y", or "z"
        theta: angle in degrees to rotate
    """
    def get_rotation_matrix(self, thetaX, thetaY, thetaZ):
        thetaX = math.radians(thetaX)
        thetaY = math.radians(thetaY)
        thetaZ = math.radians(thetaZ)

        matrixA = np.array([[1,0,0,0],
                          [0,math.cos(thetaX),-math.sin(thetaX),0],
                          [0,math.sin(thetaX),math.cos(thetaX),0],
                          [0,0,0,1]])

        matrixB = np.array([[math.cos(thetaY),0,math.sin(thetaY),0],
                          [0,1,0,0],
                          [-math.sin(thetaY),0,math.cos(thetaY),0],
                          [0,0,0,1]])

        matrixC = np.array([[math.cos(thetaZ),-math.sin(thetaZ),0,0],
                          [math.sin(thetaZ),math.cos(thetaZ),0,0],
                          [0,0,1,0],
                          [0,0,0,1]])
        matrix = np.dot(np.dot(matrixA, matrixB), matrixC)
        return matrix

    def get_projection_matrix(self, zNear, zFar, scaleX, scaleY):
        matrix = np.array([[scaleX,0,0,0],
                          [0,scaleY,0,0],
                          [0,0,(zFar)/(zFar - zNear),-(zFar + zNear)/(zFar-zNear)],
                          [0,0,1,0]])

        return matrix