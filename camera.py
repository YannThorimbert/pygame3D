
class Camera:

    def __init__(self, screen, fov, d):
        self.screen = screen
        self.w = screen.get_width()/2.
        self.h = screen.get_height()/2.
        self.fov = fov
        self.d = d

    def project(self, v): #perspective projection
        denom = self.d + v.z
##        print(denom)
        if denom < 1:
            denom = 1
##            print("uh")
        factor = self.fov / denom
        x = v.x * factor + self.w
        y = -v.y * factor + self.h
##        print("     after",x,y)
        return x, y

    def move(self, delta, objs):
        delta *= -1.
        for o in objs:
            o.move(delta)

    def rotate(self, axis, angle, objs):
        angle *= -1.
        func = "rotate_"+axis
        for o in objs:
            getattr(o,func)(angle)