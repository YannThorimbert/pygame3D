from pygame.math import Vector2 as V2
from pygame.math import Vector3 as V3
import pygame
import pygame.gfxdraw as gfx
from math import cos, sin

colors = [(255,0,0),(0,255,0),(0,0,255),(255,255,255)]

class Camera:

    def __init__(self, screen, e, pos):
        self.screen = screen
        self.e = e
        self.pos = pos
        self.angle = V3()
        self.cx = cos(self.angle.x)
        self.cy = cos(self.angle.y)
        self.cz = cos(self.angle.z)
        self.sx = sin(self.angle.x)
        self.sy = sin(self.angle.y)
        self.sz = sin(self.angle.z)

    def set_angle(self, x,y,z):
        self.angle = V3(x,y,z)
        self.refresh_angle()

    def refresh_angle(self):
        self.cx = cos(self.angle.x)
        self.cy = cos(self.angle.y)
        self.cz = cos(self.angle.z)
        self.sx = sin(self.angle.x)
        self.sy = sin(self.angle.y)
        self.sz = sin(self.angle.z)

    def project(self, point):
        x,y,z = point - self.pos
        A = self.sz*y + self.cz*x #-> x
        B = self.cz*y - self.sz*x #-> y
        D = self.cy*z + self.sy*A #-> z
        #
        dx = self.cy*A - self.sy*z #->x
        dy = self.sx*D + self.cx*B #->y
        dz = self.cx*D - self.sx*B #->z
        #
        C = (self.e.z/dz)
        bx = dx*C - self.e.x
        by = dy*C - self.e.y
        return V2(bx,by)

    def get_projected_points(self, obj):
        points = []
        for t in obj.triangles:
            points += [self.project(t.v1),
                        self.project(t.v2),
                        self.project(t.v3)]
        return points

    def draw_projected_points(self, obj, k=100):
        for x,y in self.get_projected_points(obj):
            x = int(k*x)
            y = int(k*y)
            gfx.pixel(self.screen, x, y, (255,255,255))

    def draw_projected_triangles(self, obj, k=100):
        i = 0
        triangle = [None, None, None]
        n = 0
        for x,y in self.get_projected_points(obj):
            x = int(k*x)
            y = int(k*y)
            triangle[i] = (x,y)
            if i == 2:
                x1,y1 = triangle[0]
                x2,y2 = triangle[1]
                x3,y3 = triangle[2]
                color = colors[n%len(colors)]
                gfx.aatrigon(self.screen, x1, y1, x2, y2, x3, y3, color)
                i = 0
                n += 1
            else:
                i += 1
