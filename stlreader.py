from pygame.math import Vector2 as V2
from pygame.math import Vector3 as V3
import math
import random

def get_stl_lines(filename):
    f = open(filename, "r")
    lines = f.readlines()
    f.close()
    return [line.replace("\n","") for line in lines]

def get_vertex(line):
    if "vertex" in line:
        line = line.split(" ")
        x, y, z = line[-3],line[-2],line[-1]
        return Point3D(float(x),float(y),float(z))
    return False

def get_triangles(lines):
    triangles = []
    k = 0
    vertices = [None, None, None]
    for line in lines:
        v = get_vertex(line)
        if v:
            vertices[k] = v
            k += 1
        if k == 3:
            triangles.append(Triangle(vertices[0],vertices[1],vertices[2]))
            k = 0
    assert k == 0
    return triangles

class Point3D(V3):

    def rotateX(self, angle):
        """ Rotates the point around the X axis by the given angle in degrees. """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        y = self.y * cosa - self.z * sina
        z = self.y * sina + self.z * cosa
        return Point3D(self.x, y, z)

    def rotateY(self, angle):
        """ Rotates the point around the Y axis by the given angle in degrees. """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        z = self.z * cosa - self.x * sina
        x = self.z * sina + self.x * cosa
        return Point3D(x, self.y, z)

    def rotateZ(self, angle):
        """ Rotates the point around the Z axis by the given angle in degrees. """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        x = self.x * cosa - self.y * sina
        y = self.x * sina + self.y * cosa
        return Point3D(x, y, self.z)

    def project(self, win_width, win_height, fov, viewer_distance):
        """ Transforms this 3D point to 2D using a perspective projection. """
        factor = fov / (viewer_distance + self.z)
        x = self.x * factor + win_width / 2
        y = -self.y * factor + win_height / 2
        return Point3D(x, y, 1)



#les triangles font des references a des points, qui eux subissent les transfos!
#sinon, les triangles contiennent les indices des points (repartis dans 3 listes), et traitement avec numpy

class Triangle:

    def __init__(self, v1, v2, v3, color=None):
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        self.n = self.compute_normal()
        self.c = None
        self.color = color
        if color is None:
            self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))

    def compute_normal(self):
        e1 = self.v2 - self.v1
        e2 = self.v3 - self.v1
##        e3 = self.p3 - self.p2
        n1 = e1.cross(e2)
##        n2 = e1.cross(e3)
##        n3 = e2.cross(e3)
        #n1,n2,n3 yield the same result
        return n1

    def refresh_normal(self):
        self.n = self.compute_normal()

    def vertices(self):
        yield self.v1
        yield self.v2
        yield self.v3

    def refresh_center(self):
        self.c = (self.v1 + self.v2 + self.v3)/3. #3 is not necessary (error to all)
        self.d = self.c.length() #could use length_squared

class Object3D:

    def __init__(self, filename):
        self.filename = filename
        self.lines = get_stl_lines(filename)
        self.triangles = get_triangles(self.lines)

    def move(self, dx,dy,dz):
        for v in self.vertices():
            v.x += dx
            v.y += dy
            v.z += dz

    def scale(self, factor):
        for t in self.triangles:
            t.v1 *= factor
            t.v2 *= factor
            t.v3 *= factor
            t.refresh_normal()

    def vertices(self):
        for t in self.triangles:
            yield t.v1
            yield t.v2
            yield t.v3

    def refresh(self):
        for t in self.triangles:
            t.refresh_center()
        self.triangles.sort(key=lambda x:x.d, reverse=True)



#dabord voir comment exporte de wings3d