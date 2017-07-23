import random, math

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
