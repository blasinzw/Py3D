#test B
__author__ = 'Zander'

import pygame, sys, time

from Camera import Camera
from Vector2 import Vector2
from Vector3 import Vector3
from Mesh import Mesh
from Renderer import Renderer
from Light import Light

# pygame stuff
SCREEN_SIZE = [800, 600]
pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE))

#renderer
renderer = Renderer(screen, SCREEN_SIZE[0], SCREEN_SIZE[1], 1)
renderer.wireframe = False

#rotation speed
rotSpeed = 5

#lighting
lights = []
light1 = Light(Vector3(0, 100, -100), 100)
lights += [light1]

#camera
camera = Camera()
camera.position = Vector3(0, 0, 860)

#mesh
mesh = Mesh("test", "models/monkey.obj", Vector3(0, 200, 0), Vector3(180, 200, 0), 10)

print "faces: "+str(len(mesh.faces))
print "vertices: "+str(len(mesh.vertices))
print "normals: " + str(len(mesh.normals))

meshes = []
meshes += [mesh]

angleX, angleY, angleZ = 0, 0, 0

#code for timer
start = time.time()

while True:
    #input loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                angleY = rotSpeed
            if event.key == pygame.K_s:
                angleY = -rotSpeed
            if event.key == pygame.K_a:
                angleX = -rotSpeed
            if event.key == pygame.K_d:
                angleX = rotSpeed
            if event.key == pygame.K_e:
                angleZ = rotSpeed
            if event.key == pygame.K_q:
                angleZ = -rotSpeed
            if event.key == pygame.K_UP:
                camera.position.y += rotSpeed
            if event.key == pygame.K_DOWN:
                camera.position.y += -rotSpeed
            if event.key == pygame.K_LEFT:
                camera.position.x += -rotSpeed
            if event.key == pygame.K_RIGHT:
                camera.position.x += rotSpeed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                angleY = 0
            if event.key == pygame.K_s:
                angleY = 0
            if event.key == pygame.K_a:
                angleX = 0
            if event.key == pygame.K_d:
                angleX = 0
            if event.key == pygame.K_e:
                angleZ = 0
            if event.key == pygame.K_q:
                angleZ = 0

    #renders all the meshes
    #rotates all points
    for mesh in meshes:
        mesh.rotation.x += angleX
        mesh.rotation.y += angleY
        mesh.rotation.z += angleZ

    renderer.clear()
    renderer.render(camera, lights, meshes)

    pygame.display.flip()

    #prints fps
    # print 1.0/(time.time() - start)
    start = time.time()
