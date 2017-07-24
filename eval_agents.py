import utils
from utils import walk_design
import math

class ForceAgent():
    """An agent that will consume a design, and calculate the forces on that body"""
    def __init__(self):
        pass

    def evaluate(self, design, reqs):
        #initialize by getting all the free variables for forces
        #TODO deal with packing/unpacking nested lists
        inputs = [d.get_free_forces() for d in walk_design(design)]
        #Optimize, driving total to zero

    def calc_forces_and_torques(self, design, free_forces):
        #set the free forces in the design
        for i, d in enumerate(walk_design(design)):
            d.set_free_forces(free_forces[i])
        net_force_x = sum([d.get_net_force_x() for d in walk_design(design)])
        net_force_y = sum([d.get_net_force_y() for d in walk_design(design)])
        net_torque = sum([d.get_net_torque() for d in walk_design(design)])
        return net_force_x, net_force_y, net_torque

class PositionAgent():
    """Find a configuration that works"""
    def __init__(self):
        pass

    def evaluate(self, design, reqs, threshold = 1.0):
        inputs = [d.get_config_vars() for d in walk_design(design)]

    def score_loop():
        config_score = sum([d.score_config() for d in walk_design(design)])
        if config_score>1:
            return config_score
        # run force agent
        
