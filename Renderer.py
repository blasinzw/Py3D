__author__ = 'Zander'

from pygame import gfxdraw
from Vector2 import Vector2
from Vector4 import Vector4
from Vector3 import Vector3
from Matrix4 import Matrix4
import math, pygame
import numpy as np


class Renderer:

    def __init__(self, screen, width, height, scale=1):
        self.width = width
        self.height = height
        self.screen = screen
        self.matrix = Matrix4()
        self.scale = scale
        self.wireframe = False
        self.pixels = []

    def clear(self):
        self.screen.fill((0,0,0))
        self.pixels = []

    def drawScreen(self):
        self.pixels = sorted(self.pixels, key=lambda x: x[3])
        for p in self.pixels:
            gfxdraw.pixel(self.screen, p[0], p[1], p[2])

    def putPixel(self, vector, color):
        if not vector.x < 0 and not vector.x > self.width:
            if not vector.y < 0 and not vector.y > self.height:
                self.pixels += [[int(vector.x), int(vector.y), color, vector.z]]

    def drawLine(self, point0, point1, color):
        dist = (point0 - point1).length
        if dist < 2:
            return
        middlePoint = point0 + (point1 - point0)/Vector2(2, 2)

        self.putPixel(middlePoint, color)

        self.drawLine(point0, middlePoint, color)
        self.drawLine(middlePoint, point1, color)

    def drawScanLine(self, pointA, pointB, y, sz, ez, sShade, eShade, color):
        if pointA > pointB:
            temp = pointA
            pointA = pointB
            pointB = temp

        z_slope = (ez - sz)/(pointB - pointA)

        shadingGradient = (eShade - sShade)/(pointB - pointA)

        for x in range(int(pointA), int(pointB)):
            if x > self.width:
                return
            if y > self.height:
                return

            color *= sShade
            color = self.clamp(color, 0, 255)

            self.putPixel(Vector3(x, y, sz), (color, color, color))

            sz += z_slope
            sShade += shadingGradient

    def clamp (self, value, min, max):
        if value < min:
            return min
        elif value > max:
            return max
        else:
            return value

    """a.y <= b.y <= c.y"""
    def drawTriangle(self, pointA, pointB, pointC, shades, color):
        #Uses rasterization to draw triangle
        #slopes dx/dy
        drawUpper = True

        #handles weird exceptions
        if int(pointA.y - pointC.y) != 0:
            slopeAC = (pointA.x - pointC.x)/(pointA.y - pointC.y)
            slopeACZ = (pointA.z - pointC.z)/(pointA.y - pointC.y)
            #new beta test
            shadingGradientAC = (shades[0] - shades[2])/(pointA.y - pointC.y)
        else:
            return
        if int(pointA.y - pointB.y) != 0:
            slopeAB = (pointA.x - pointB.x)/(pointA.y - pointB.y)
            slopeABZ = (pointA.z - pointB.z)/(pointA.y - pointB.y)
            #new beta code
            shadingGradientAB = (shades[0] - shades[1])/(pointA.y - pointB.y)
        else:
            drawUpper = False
            self.drawScanLine(pointA.x, pointB.x, pointA.y, pointA.z, pointB.z, shades[0], shades[0], color)

        slopeBC = (pointB.x - pointC.x)/(pointB.y - pointC.y)
        slopeBCZ = (pointB.z - pointC.z)/(pointB.y - pointC.y)

        #new beta
        shadingGradientBC = (shades[1] - shades[2])/(pointB.y - pointC.y)

        sx, ex = pointA.x, pointA.x
        sz, ez = pointA.z, pointA.z

        #new beta test
        sShade, eShade = shades[0], shades[0]

        if drawUpper:
            for y in range(int(pointA.y), int(pointB.y)):
                self.drawScanLine(sx, ex, y, sz, ez, sShade, eShade, color)
                sx += slopeAC
                ex += slopeAB
                sz += slopeACZ
                ez += slopeABZ

                sShade += shadingGradientAC
                eShade += shadingGradientAB
        else:
            ex = pointB.x
            ez = pointB.z

            eShade = shades[1]
        for y in range(int(pointB.y), int(pointC.y)):
            self.drawScanLine(sx, ex, y, sz, ez, sShade, eShade, color)
            sx += slopeAC
            ex += slopeBC
            sz += slopeACZ
            ez += slopeBCZ

            sShade += shadingGradientAC
            eShade += shadingGradientBC

    def drawBline(self, point0, point1, color):
        x0 = int(point0.x)
        y0 = int(point0.y)
        x1 = int(point1.x)
        y1 = int(point1.y)
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        if (x0 < x1):
            sx = 1
        else:
            sx = -1
        if y0 < y1:
            sy = 1
        else:
            sy = -1
        err = dx - dy

        while x0 != x1 or y0 != y1:
            self.putPixel(Vector3(x0, y0, 0), color)
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            elif e2 < dx:
                err += dx
                y0 += sy

    def project(self, vector, aspectRatio, zNear, zFar, fov_degree):
        if (aspectRatio > 1):
            sX = 1/aspectRatio
        else:
            sX = 1

        if (aspectRatio > 1):
            sY = 1
        else:
            sY = aspectRatio

        fov = 1/math.tan(math.radians(fov_degree/2))
        scaleX = fov * sX
        scaleY = fov * sY

        projectionMatrix = self.matrix.get_projection_matrix(zNear, zFar, scaleX, scaleY)
        projectedVector = Vector4(vector.x, vector.y, vector.z, 1).dot_product_with_matrix(projectionMatrix)

        return Vector3(projectedVector[0] + self.width/2, projectedVector[1]+ self.height/2, projectedVector[2])

    def render(self, camera, lights, meshes):
        polygons=[]
        for mesh in meshes:
            rotationMatrix = self.matrix.get_rotation_matrix(mesh.rotation.x, mesh.rotation.y, mesh.rotation.z)
            translationMatrix = self.matrix.get_translation_matrix(mesh.position - camera.position)
            worldMatrix = np.dot(self.matrix.get_scaling_matrix(Vector3(self.scale,self.scale,self.scale)), np.dot(rotationMatrix, translationMatrix))
            for face in mesh.faces:
                # print face[0], face[1], face[2]
                vertexA = mesh.vertices[face[0][0]]
                vertexB = mesh.vertices[face[0][1]]
                vertexC = mesh.vertices[face[0][2]]

                vertexA = vertexA.dot_product_with_matrix(worldMatrix)
                vertexB = vertexB.dot_product_with_matrix(worldMatrix)
                vertexC = vertexC.dot_product_with_matrix(worldMatrix)

                pixelA = self.project(vertexA, 800/600, 1, 1000, 70)
                pixelB = self.project(vertexB, 800/600, 1, 1000, 70)
                pixelC = self.project(vertexC, 800/600, 1, 1000, 70)

                if not self.wireframe:
                    #still in devoplment.... BETA!!!!
                    norm1 = mesh.normals[face[1][0]]
                    norm2 = mesh.normals[face[1][1]]
                    norm3 = mesh.normals[face[1][2]]

                    norm1 = norm1.dot_product_with_matrix(worldMatrix)
                    norm2 = norm2.dot_product_with_matrix(worldMatrix)
                    norm3 = norm3.dot_product_with_matrix(worldMatrix)

                    #sorts pixels
                    pixels = [pixelA, pixelB, pixelC]
                    pixels = sorted(pixels, key=lambda x: x.y)

                    color = 255

                    #gouraud shading
                    # vertices = [[vertexA, pixelA.y], [vertexB, pixelB.y], [vertexC, pixelC.y]]
                    # vertices = sorted(vertices, key=lambda x: x[1])
                    #
                    # diffuseIntensities = []
                    # for light in lights:
                    #     lightingDistanceA = light.position - vertices[0][0]
                    #     lightingDistanceB = light.position - vertices[1][0]
                    #     lightingDistanceC = light.position - vertices[2][0]
                    #
                    #     diffuseIntensities += [light.getIntensity(vertices[0][0]) * norm1.normalize().dot_product(lightingDistanceA.normalize())]
                    #     diffuseIntensities += [light.getIntensity(vertices[1][0]) * norm1.normalize().dot_product(lightingDistanceB.normalize())]
                    #     diffuseIntensities += [light.getIntensity(vertices[2][0]) * norm1.normalize().dot_product(lightingDistanceC.normalize())]
                    #
                    # self.drawTriangle(pixels[0], pixels[1], pixels[2], diffuseIntensities, color)

                    #flat shading
                    nFace = (norm1 + norm2 + norm3)/Vector3(3,3,3)
                    center = (vertexA + vertexB + vertexC)/Vector3(3,3,3)

                    diffuseIntensity = 0
                    for light in lights:
                        lightingDistance = light.position - center

                        diffuseIntensity += light.getIntensity(center) * \
                                            nFace.normalize().dot_product(lightingDistance.normalize())

                    color *= diffuseIntensity
                    color += 50
                    color = self.clamp(color, 0, 255)

                    polygons += [(self.screen, (int(color), int(color), int(color)),
                                        [[pixelA.x, pixelA.y], [pixelB.x, pixelB.y], [pixelC.x, pixelC.y]], vertexA.z)]
                else:
                    self.drawBline(pixelA, pixelB, (255,255,255))
                    self.drawBline(pixelB, pixelC, (255,255,255))
                    self.drawBline(pixelC, pixelA, (255,255,255))
        if not self.wireframe:
            polygons = sorted(polygons, key=lambda x: x[3])
            for polygon in polygons:
                pygame.draw.polygon(polygon[0], polygon[1], polygon[2])
        self.drawScreen()