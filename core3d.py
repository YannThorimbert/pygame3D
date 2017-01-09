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
        return V3(float(x),float(y),float(z)), "v"
    elif "normal" in line:
        line = line.split(" ")
        x, y, z = line[-3],line[-2],line[-1]
        return V3(float(x),float(y),float(z)), "n"
    return False

def get_triangles(lines):
    triangles = []
    k = 0
    vertices = [None, None, None]
    normal = None
    for line in lines:
        v = get_vertex(line)
        if v:
            if v[1] == "v":
                vertices[k] = v[0]
                k += 1
            elif v[1] == "n":
                normal = v[0]
        if k == 3:
            t = Triangle(vertices[0],vertices[1],vertices[2])
            t.n = normal
            triangles.append(t)
            assert t.n is not None
            k = 0
    assert k == 0
    return triangles

#les triangles font des references a des points, qui eux subissent les transfos!

class Triangle:

    def __init__(self, v1, v2, v3, color=None):
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        self.n = None
        self.c = None
        self.color = color
        if color is None:
            self.color = V3(random.randint(0,255),random.randint(0,255),random.randint(0,255))
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

##    def rotate(self, x,y,z):
##        for v in [self.v1, self.v2, self.v3]:
##            v.rotate_x_ip(x)
##            v.rotate_y_ip(y)
##            v.rotate_z_ip(z)
####        self.refresh_normal()
##        #or add self.n to the for loop above


class Object3D:

    def __init__(self, filename):
        self.filename = filename
        self.lines = get_stl_lines(filename)
        self.triangles = get_triangles(self.lines)
        self.from_center = V3()
        vset = self.get_vertices_set()
        self.vertices = {val:V3(val) for val in vset}
        self.compactize()

    def compactize(self):
        for t in self.triangles:
            t.v1 = self.vertices[tuple(t.v1)]
            t.v2 = self.vertices[tuple(t.v2)]
            t.v3 = self.vertices[tuple(t.v3)]

    def move(self, delta):
        for v in self.vertices.values():
            v += delta
        self.from_center += delta

    def rotate_x(self, angle, refresh=True):
        for v in self.vertices.values():
            v.rotate_x_ip(angle)
        if refresh:
            self.refresh_normals()

    def rotate_around_center_x(self, angle, refresh=True):
        tmp = V3(self.from_center)
        self.move(-tmp)
        self.rotate_x(angle, refresh)
        self.move(tmp)

    def rotate_y(self, angle, refresh=True):
        for v in self.vertices.values():
            v.rotate_y_ip(angle)
        if refresh:
            self.refresh_normals()

    def rotate_around_center_y(self, angle, refresh=True):
        tmp = V3(self.from_center)
        self.move(-tmp)
        self.rotate_y(angle, refresh)
        self.move(tmp)

    def rotate_z(self, angle, refresh=True):
        for v in self.vertices.values():
            v.rotate_z_ip(angle)
        if refresh:
            self.refresh_normals()

    def rotate_around_center_z(self, angle, refresh=True):
        tmp = V3(self.from_center)
        self.move(-tmp)
        self.rotate_z(angle, refresh)
        self.move(tmp)

##    def rotate_around_center(self, x,y,z):
##        tmp = V3(self.from_center)
##        self.move(-tmp)
##        for v in self.vertices.values():
##            v.rotate_x_ip(x)
##            v.rotate_y_ip(y)
##            v.rotate_z_ip(z)
##        self.move(tmp)
##        self.refresh_normals()

    def refresh_normals(self):
        for t in self.triangles:
            t.refresh_normal()

    def scale(self, factor): #account for this for rotations!
        for v in self.vertices.values():
            v *= factor
        self.refresh_normals()

    def refresh(self):
        for t in self.triangles:
            t.refresh_center()
        self.triangles.sort(key=lambda x:x.d, reverse=True)

    def get_vertices_set(self):
        vset = set()
        for t in self.triangles:
            for v in[t.v1,t.v2,t.v3]:
                vset.add(tuple(v))
        return vset

class ManualObject3D(Object3D):

    def __init__(self, triangles):
        self.triangles = triangles
        self.from_center = V3()
        vset = self.get_vertices_set()
        self.vertices = {val:V3(val) for val in vset}
        self.compactize()
