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
        return V3(float(x),float(y),float(z))
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
        self.ecolor = self.color

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
##        self.M = max([v.length() for v in self.vertices()])

class Object3D:

    def __init__(self, filename):
        self.filename = filename
        self.lines = get_stl_lines(filename)
        self.triangles = get_triangles(self.lines)
        self.from_center = V3()

    def move(self, delta):
        for v in self.vertices():
            v += delta
        self.from_center += delta


    def rotate_around_center(self, x,y,z):
        tmp = V3(self.from_center)
        self.move(-tmp)
        for t in self.triangles:
            for v in t.vertices():
                v.rotate_x_ip(x)
                v.rotate_y_ip(y)
                v.rotate_z_ip(z)
        self.move(tmp)

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