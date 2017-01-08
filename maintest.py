from pygame.math import Vector2 as V2
from pygame.math import Vector3 as V3
import pygame
import pygame.gfxdraw as gfx

import thorpy
from stlreader import Object3D
import core3d

obj = Object3D("cube_ascii.stl")
obj.move(2,2,2)

def func(event):
    global angleX,angleY,angleZ
    clock.tick(50)
    screen.fill((0,0,0))
    if event.key == pygame.K_x:
        obj.move(0,0,0.1)
        angleX, angleY, angleZ = 0,0,0
    else:
        angleX, angleY, angleZ = 1,1,1
    i = 0
    obj.refresh()
    screen.fill((0,0,0))
    for t in obj.triangles:
        p = []
        for v in t.vertices():
            # Rotate the point around X axis, then around Y axis, and finally around Z axis.
##            r = v.rotateX(angleX).rotateY(angleY).rotateZ(angleZ)
            r = v.rotate_x(angleX).rotate_y(angleY).rotate_z(angleZ)
            v.x, v.y, v.z = r.x, r.y, r.z
            # Transform the point from 3D to 2D
            proj = v.project(screen.get_width(), screen.get_height(), 256, 4)
            x, y = int(proj.x), int(proj.y)
            p.append((x,y))
        gfx.filled_trigon(screen, p[0][0], p[0][1], p[1][0], p[1][1], p[2][0], p[2][1], t.color)
        gfx.aatrigon(screen, p[0][0], p[0][1], p[1][0], p[1][1], p[2][0], p[2][1], t.color)
        i += 1
    pygame.display.flip()

reac = thorpy.Reaction(pygame.KEYDOWN,func)
clock = pygame.time.Clock()


app = thorpy.Application((800,600))
screen = thorpy.get_screen()

g = thorpy.Ghost.make()
g.add_reaction(reac)

m = thorpy.Menu(g)
m.play()

app.quit()



