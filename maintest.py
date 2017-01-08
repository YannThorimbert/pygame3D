from pygame.math import Vector2 as V2
from pygame.math import Vector3 as V3
import pygame
import pygame.gfxdraw as gfx

import thorpy
from stlreader import Object3D

#lire les normales (grace a meshlab sont juste) et regarder colinearite avec source de lumiere

obj1 = Object3D("node_ascii.stl")
obj1.move(V3(2,2,2))

obj2 = Object3D("node_ascii.stl")
obj2.move(V3(2,2,4))
for t in obj2.triangles:
    t.color = (127,127,127)
    t.ecolor = (0,0,0)

objs = [obj1, obj2]

def project(v, win_width, win_height, fov, viewer_distance):
    """ Transforms this 3D point to 2D using a perspective projection. """
    factor = fov / (viewer_distance + v.z)
    x = v.x * factor + win_width / 2
    y = -v.y * factor + win_height / 2
    return V2(x, y)

def func(event):
    objs.sort(key=lambda x:x.from_center.length(), reverse=True)
    clock.tick(50)
    screen.fill((255,255,255))
    DS = 0.2
    DA = 2
    if event.key == pygame.K_LEFT:
        obj1.move(V3(-DS,0,0))
    elif event.key == pygame.K_RIGHT:
        obj1.move(V3(DS,0,0))
    elif event.key == pygame.K_UP:
        obj1.move(V3(0,-DS,0))
    elif event.key == pygame.K_DOWN:
        obj1.move(V3(0,DS,0))
    elif event.key == pygame.K_m:
        obj1.move(V3(0,0,DS))
    elif event.key == pygame.K_l:
        obj1.move(V3(0,0,-DS))
    elif event.key == pygame.K_z:
        obj1.rotate_around_center(0,0,DA)
    elif event.key == pygame.K_u:
        obj1.rotate_around_center(0,0,-DA)
    elif event.key == pygame.K_x:
        obj1.rotate_around_center(DA,0,0)
    elif event.key == pygame.K_c:
        obj1.rotate_around_center(-DA,0,0)
    elif event.key == pygame.K_y:
        obj1.rotate_around_center(0,DA,0)
    elif event.key == pygame.K_a:
        obj1.rotate_around_center(0,-DA,0)
    for obj in objs:
        obj.refresh()
        for t in obj.triangles:
            p = []
            for v in t.vertices():
                proj = project(v, screen.get_width(), screen.get_height(), 512, 8)
                x, y = int(proj.x), int(proj.y)
                p.append((x,y))
            gfx.filled_trigon(screen, p[0][0], p[0][1], p[1][0], p[1][1], p[2][0], p[2][1], t.color)
            gfx.aatrigon(screen, p[0][0], p[0][1], p[1][0], p[1][1], p[2][0], p[2][1], t.ecolor)
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



