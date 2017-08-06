import math, os
import numpy as np

def wheel_step_points_gen(width, height, radius, max_torque, mass):
    """return points in the form (x, y, Fx_center, Fy_center, Torque, valid?)
    assumes all the bodies are static, """

def wheel_flat_points_gen(radius, max_torque, mass, max_strength=10, mu=0.5, density=50):
    """return points in the form (x, y, Fx_center, Fy_center, Torque, valid?)
    assumes all the bodies are static, """
    #return points that are on the floor
    pts = []
    weight = mass*-9.8
    y = radius
    for x in np.linspace(0, 1, density):
        for Fy_center in np.linspace(max_strength, weight, density):
            Fn = -1*(Fy_center+weight)
            max_Fr = Fn*mu
            for Torque in np.linspace(-max_torque,  max_torque, density):
                Fx_center = -Torque*radius
                if abs(Fx_center)<abs(max_Fr):
                    pts.append((x, y, Fx_center, Fy_center, Torque, 1))
        pts.append((x, y+0.01, 0, weight, 0, 1))
        pts.append((x, y-0.01, 0, 0, 0, 0))
    return pts


def bar(length, mass, x_range, y_range, max_strength=10, density=5):
    """returns points in the form (x, y, angle, Fx_1, Fy_1, T1, Fx_2, Fy_2, T2, valid?)"""
    Fg = mass*-9.8
    for x in np.linspace(0, x_range, density):
        for y in np.linspace(0, y_range, density):
            for ang in np.linspace(0, 2*math.pi, density):
                for Fx_1 in np.linspace(-max_strength, max_strength, density):
                    for Fy_1 in np.linspace(-max_strength, max_strength, density):
                        for T_1 in np.linspace(-max_strength, max_strength, density):
                            Fx_2 = T_1*length*math.sin(ang)-Fx_1
                            Fy_2 = -Fy_1-Fg-T_1*length*math.cos(ang)
                            T_2 = Fx_1*length*math.sin(ang+math.pi)-Fy_1*length*math.cos(ang+math.pi)-Fy_1*length*math.cos(ang+math.pi)/2.0-T_1
                            #TODO Save results in list
                for Fx_2 in np.linspace(-max_strength, max_strength, density):
                    for Fy_2 in np.linspace(-max_strength, max_strength, density):
                        for T_2 in np.linspace(-max_strength, max_strength, density):
                            #TODO ensure the RHS has the correct referrants and signs
                            Fx_1 = T_1*length*math.sin(ang)-Fx_1
                            Fy_1 = -Fy_1-Fg-T_1*length*math.cos(ang)
                            T_1 = Fx_1*length*math.sin(ang+math.pi)-Fy_1*length*math.cos(ang+math.pi)-Fy_1*length*math.cos(ang+math.pi)/2.0-T_1
