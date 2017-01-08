class Light:

    def __init__(self, pos, m, M):
        self.pos = pos
        self.m = m
        self.M = M

    def get_color_factor(self, t):
        line = t.c - self.pos
        angle = t.n.angle_to(line)
        return angle/180.

    def set_light(self, c, f):
        """Modify color c to reflect light exposition f."""
        if f > 0.5:
            f = (f-0.5)/0.5
            return f*self.M + (1.-f)*c
        else:
            f = f/0.5
            return f*c + (1.-f)*self.m

    def get_color(self, t):
        f = self.get_color_factor(t)
        return self.set_light(t.color, f)