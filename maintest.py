from pygame.math import Vector2 as V2
from pygame.math import Vector3 as V3
import pygame
import pygame.gfxdraw as gfx

import thorpy
##from stlreader import Object3D
from core3d import Object3D
from light import Light
from camera import Camera

#comparer perfs core3d vs stlreader quand l'ordi ira mieux ==> un CHOUILLA mieux
#rotation : fonctions a part pour x, y et z. Faire sur papier (revient au cas 2D)
#camera.move, camera.rotate ==> agit sur objs

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

##cube = Object3D("cube_ascii.stl"); cube.refresh_normals()
cube = Object3D("cube2.stl")
cube.move(V3(0,0,4))
for t in cube.triangles:
    t.color = V3(70,70,255)
    t.ecolor = t.color

from core3d import ManualObject3D, Triangle
a = 4
t1 = ManualObject3D([Triangle(a*V3(-1,0,0), a*V3(1,0,0), a*V3(0,1,0),
                                        color=V3(50,50,255)),
                        Triangle(a*V3(1,0,0), a*V3(-1,0,0), a*V3(0,-1,0),
                                        color=V3(50,50,255))])
t1.refresh_normals()
t1.move(V3(0,0,5))


##obj1.scale(0.2)

active_obj = obj1
objs = [obj1]

##objs = [cube]
##active_obj = cube

##active_obj = t1
##objs = [t1]

##fighter = Object3D("meshes/chasseur_biplace.stl")
fighter = Object3D("meshes/THM15.stl")
for t in fighter.triangles:
    t.color = V3(70,70,255)
    t.ecolor = t.color
fighter.move(V3(0,0,5))

##active_obj = fighter
##objs = [fighter]

def func(event):
    global light_pos
    objs.sort(key=lambda x:x.from_center.length(), reverse=True)
    screen.fill((255,255,255))
    DS = 0.2
    DA = 2
    print(pygame.event.event_name(event.type))
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
        active_obj.rotate_around_center_z(DA)
    elif event.key == pygame.K_u:
        active_obj.rotate_around_center_z(-DA)
    elif event.key == pygame.K_x:
        active_obj.rotate_around_center_x(DA)
    elif event.key == pygame.K_c:
        active_obj.rotate_around_center_x(-DA)
    elif event.key == pygame.K_y:
        active_obj.rotate_around_center_y(DA)
    elif event.key == pygame.K_a:
        active_obj.rotate_around_center_y(-DA)
    elif event.key == pygame.K_SPACE:
##        cam.move(V3(1,0,1), objs)
        cam.rotate("y",1,objs)
    for obj in objs: #pas boucler sur objs mais sur tous les triangles de la scen!!! ==> objet scene, le concept de obj est la que pour user transfos ?
        obj.refresh()
        i = 0
        for t in obj.triangles:
            if t.c.z > 0: #c denotes the center coordinate
                p = []
                for v in t.vertices():
                    x,y = cam.project(v)
                    p.append((int(x),int(y)))
                color = light.get_color(t)
##                print(color)
##                color = t.color
##                print(p)
                gfx.filled_trigon(screen, p[0][0], p[0][1], p[1][0], p[1][1], p[2][0], p[2][1], color)
                gfx.aatrigon(screen, p[0][0], p[0][1], p[1][0], p[1][1], p[2][0], p[2][1], color)
            i+=1
    pygame.display.flip()

##thorpy.application.SHOW_FPS = True

reac = thorpy.Reaction(pygame.KEYDOWN,func)
##reac = thorpy.Reaction(thorpy.THORPY_EVENT,func,{"id":thorpy.constants.EVENT_TIME})

app = thorpy.Application((800,600))
screen = thorpy.get_screen()

cam = Camera(screen, fov=512, d=2)

g = thorpy.Ghost.make()
g.add_reaction(reac)

m = thorpy.Menu(g,fps=100)
m.play()

app.quit()



