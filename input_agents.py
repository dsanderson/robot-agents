from __future__ import division
from utils import sample, linspace
import numpy as np
import math

class TerrainAgent:
    def __init__(self, window_size=(1.0,1.0), res=0.001):
        self.window_size = window_size
        self.res = res

    def draw(self, plt):
        for p in self.terrain:
            plt.plot([p[0]],[p[1]], '.')

class FlatAgent(TerrainAgent):
    def set_angles(self, min_angle, max_angle):
        """Set the maximum and minimum angles of the terrain, in radians"""
        self.min_angle = min_angle
        self.max_angle = max_angle

    def create_terrain(self):
        ang = self.min_angle+sample()*(self.max_angle-self.min_angle)
        #given the angle, interpolate a series of point within the box of size window, with spacing res
        if abs(ang) == math.pi/2.0:
            p1 = (0, -self.window[1])
            p2 = (0, self.window[1])
        elif ang == 0 or abs(self.window_size[0]*math.tan(ang))<self.window_size[1]:
            p1 = (-self.window_size[0], -self.window_size[0]*math.tan(ang))
            p2 = (self.window_size[0], self.window_size[0]*math.tan(ang))
        else:
            p1 = (-self.window_size[1]/math.tan(ang), -self.window_size[0])
            p2 = (self.window_size[1]/math.tan(ang), self.window_size[0])
        self.terrain = interpolate_line(p1, p2, self.res)

class StepAgent(TerrainAgent):
    def set_step_height(self, height):
        self.step_height = height

    def create_terrain(self):
        p1 = (-self.window[0], height)
        p2 = (0, height)
        l1 = interpolate_line(p1, p2, self.res)
        p1 = (0, height)
        p2 = (0, 0)
        l2 = interpolate_line(p1, p2, self.res)
        p1 = (0, 0)
        p2 = (self.window[0], 0)
        l3 = interpolate_line(p1, p2, self.res)
        self.terrain = l1+l2+l3

class NoiseAgent:
    pass

def interpolate_line(p1, p2, spacing):
    npts = 1+int(math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)/spacing)
    xs = np.linspace(p1[0], p2[0], npts)
    ys = np.linspace(p1[1], p2[1], npts)
    out = zip(xs,ys)
    return out
