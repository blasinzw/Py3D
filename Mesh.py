__author__ = 'Zander'
from Vector3 import Vector3

class Mesh:

    def __init__(self, name, filename, position=Vector3(0,0,0), rotation=Vector3(0,0,0), scale=1):
        self.name = name
        self.vertices = self.loadOBJ(filename, "vertices")
        self.normals = self.loadOBJ(filename, "normals")
        self.faces = self.loadOBJ(filename, "faces")
        self.rotation = rotation
        self.position = position
        self.scaleVertices(scale)

    def scaleVertices(self, scale):
        for i in range(len(self.vertices)):
            self.vertices[i] = self.vertices[i] * Vector3(scale, scale, scale)

    #loads .obj files
    def loadOBJ(self, filename, option=True):
        if option == "vertices":
            verts = []
        elif option == "normals":
            norms = []
        else:
            facesOut = []
        # normsOut = []
        for line in open(filename, "r"):
            vals = line.split()
            if vals[0] == "v" and option != "faces" and option != "normals":
                v = map(float, vals[1:4])
                vector = Vector3(v[0],v[1],v[2])
                verts.append(vector)
            elif vals[0] == "vn" and option != "vertices" and option != "faces":
                n = map(float, vals[1:4])
                normal = Vector3(n[0], n[1], n[2])
                norms.append(normal)
            elif vals[0] == "f" and option != "vertices" and option != "normals":
                face = []
                norm = []
                for f in vals[1:]:
                    w = f.split("/")
                    face.append(int(w[0]) - 1)
                    norm.append(int(w[2]) - 1)
                facesOut.append([[face[0], face[1], face[2]], [norm[0], norm[1], norm[2]]])

        # return vertsOut, normsOut
        if option == "vertices":
            return verts
        elif option == "normals":
            return norms
        else:
            return facesOut