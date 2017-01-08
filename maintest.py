from pygame.math import Vector2 as V2
from pygame.math import Vector3 as V3
import pygame
import pygame.gfxdraw as gfx

import thorpy
##from stlreader import Object3D
from core3d import Object3D
from light import Light
from camera import Camera

#comparer perfs core3d vs stlreader quand l'ordi ira mieux

light_pos = V3(1,0,0)
light_m = V3(20,20,20)
light_M = V3(230,230,230)
light = Light(light_pos, light_m, light_M)


obj1 = Object3D("node_ascii.stl")
obj1.move(V3(0,0,2))
for t in obj1.triangles:
    t.color = V3(70,70,255)
    t.ecolor = t.color

obj2 = Object3D("node_ascii.stl")
obj2.move(V3(0,0,5))

##cube = Object3D("cube_ascii.stl")
cube = Object3D("cube2.stl")
##cube.scale(1.)
for t in cube.triangles:
    t.color = V3(70,70,255)
    t.ecolor = t.color

##obj1.scale(0.2)

active_obj = obj1
objs = [obj1, obj2]


##objs = [cube]
##active_obj = cube


def func(event):
    global light_pos
    objs.sort(key=lambda x:x.from_center.length(), reverse=True)
    clock.tick(50)
    screen.fill((255,255,255))
    DS = 0.2
    DA = 2
    if event.key == pygame.K_LEFT:
        active_obj.move(V3(-DS,0,0))
    elif event.key == pygame.K_RIGHT:
        active_obj.move(V3(DS,0,0))
    elif event.key == pygame.K_DOWN:
        active_obj.move(V3(0,-DS,0))
    elif event.key == pygame.K_UP:
        active_obj.move(V3(0,DS,0))
    elif event.key == pygame.K_m:
        active_obj.move(V3(0,0,DS))
    elif event.key == pygame.K_l:
        active_obj.move(V3(0,0,-DS))
    elif event.key == pygame.K_z:
        active_obj.rotate_around_center(0,0,DA)
    elif event.key == pygame.K_u:
        active_obj.rotate_around_center(0,0,-DA)
    elif event.key == pygame.K_x:
        active_obj.rotate_around_center(DA,0,0)
    elif event.key == pygame.K_c:
        active_obj.rotate_around_center(-DA,0,0)
    elif event.key == pygame.K_y:
        active_obj.rotate_around_center(0,DA,0)
    elif event.key == pygame.K_a:
        active_obj.rotate_around_center(0,-DA,0)
    for obj in objs:
        obj.refresh()
        i = 0
        for t in obj.triangles:
            if t.c.z > 1:
                p = []
                for v in t.vertices():
                    x,y = cam.project(v)
                    p.append((int(x),int(y)))
                color = light.get_color(t)
##                print(color)
##                color = t.color
                gfx.filled_trigon(screen, p[0][0], p[0][1], p[1][0], p[1][1], p[2][0], p[2][1], color)
    ##            gfx.aatrigon(screen, p[0][0], p[0][1], p[1][0], p[1][1], p[2][0], p[2][1], t.ecolor)
            i+=1
    pygame.display.flip()

reac = thorpy.Reaction(pygame.KEYDOWN,func)
clock = pygame.time.Clock()


app = thorpy.Application((800,600))
screen = thorpy.get_screen()

cam = Camera(screen, fov=512, d=8)

g = thorpy.Ghost.make()
g.add_reaction(reac)

m = thorpy.Menu(g)
m.play()

app.quit()



