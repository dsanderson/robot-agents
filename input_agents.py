from utils import sample, linspace

class FlatAgent:
    def __init__(self, window_size=(1.0,1.0), res=0.001):
        self.window_size = window_size

    def set_angles(self, min_angle, max_angle):
        """Set the maximum and minimum angles of the terrain, in radians"""
        self.min_angle = min_angle
        self.max_angle = max_angle

    def get_example(self):
        ang = self.min_angle+sample()*(self.max_angle-self.min_angle)
        #given the angle, interpolate a series of point within the box of size window, with spacing res
        x_res = abs(math.cos(ang))
        y_res = abs(math.sin(ang))
        x_min = max(-abs(1.0/math.sin(ang)), -1.0) if ang != 0 else -1.0
        x_max = min(abs(1.0/math.sin(ang)), 1.0) if ang != 0 else 1.0
        y_min = max(-abs(1.0/math.cos(ang)), -1.0) if ang != 0 else -1.0
        y_max = min(abs(1.0/math.cos(ang)), 1.0) if ang != 0 else 1.0
        

class StepAgent:


class NoiseAgent:
