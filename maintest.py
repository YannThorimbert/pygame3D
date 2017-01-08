from pygame.math import Vector2 as V2
from pygame.math import Vector3 as V3
import pygame

import thorpy
from stlreader import Object3D
from camera import Camera

obj = Object3D("cube_ascii.stl")

def func(event):
    DA = 0.01
    DP = 0.05
    space = pygame.key.get_pressed()[pygame.K_SPACE]
    #angle
    if event.key == pygame.K_z:
        if space:
            cam.angle.z += DA
        else:
            cam.angle.z -= DA
        cam.refresh_angle()
    if event.key == pygame.K_x:
        if space:
            cam.angle.x += DA
        else:
            cam.angle.x -= DA
        cam.refresh_angle()
    if event.key == pygame.K_y:
        if space:
            cam.angle.y += DA
        else:
            cam.angle.y -= DA
        cam.refresh_angle()
    #pos
    if event.key == pygame.K_LEFT:
        cam.pos.x -= DP
    if event.key == pygame.K_RIGHT:
        cam.pos.x += DP
    if event.key == pygame.K_UP:
        cam.pos.z -= DP
    if event.key == pygame.K_DOWN:
        cam.pos.z += DP
    if event.key == pygame.K_o:
        cam.pos.y -= DP
    if event.key == pygame.K_p:
        cam.pos.y += DP

    screen.fill((0,0,0))
##    cam.draw_projected_points(obj)
    cam.draw_projected_triangles(obj)
    pygame.display.flip()

reac = thorpy.Reaction(pygame.KEYDOWN,func)

app = thorpy.Application((500,500))
screen = thorpy.get_screen()
cam = Camera(screen,
             e=V3(0.,0.,2.),
             pos=V3(2.,2.,2.))

g = thorpy.Ghost.make()
g.add_reaction(reac)

m = thorpy.Menu(g)
cam.draw_projected_triangles(obj)
pygame.display.flip()
m.play()

app.quit()

