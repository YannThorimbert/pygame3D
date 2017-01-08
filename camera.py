
class Camera:

    def __init__(self, screen, fov, d):
        self.screen = screen
        self.w = screen.get_width()/2.
        self.h = screen.get_height()/2.
        self.fov = fov
        self.d = d

    def project(self, v): #perspective projection
        factor = self.fov / (self.d + v.z)
        x = v.x * factor + self.w
        y = -v.y * factor + self.h
        return x, y