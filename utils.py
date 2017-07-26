import random, math
import matplotlib.pyplot as plt


def sample():
    return random.random()

def dist(p1,p2):
    return math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)

def signum(num):
    if num>=0:
        return 1
    else:
        return -1

def walk_design(design):
    """walk down the .children of a design, returning each, as a generator"""
    des = []
    for d in design.get_children():
        des = des+walk_design(d)
    des.append(design)
    return des

def draw_design(design, terrain):
    f, p = plt.subplots(1, 1)
    p.hold(True)
    terrain.draw(p)
    for d in walk_design(design):
        d.draw(p)
    plt.axis('equal')
    plt.show()
