import utils
from utils import walk_design
import math, random
import scipy.optimize
import numpy as np

class ForceAgent():
    """An agent that will consume a design, and calculate the forces on that body"""
    def __init__(self):
        pass

    def evaluate(self, design, reqs):
        #initialize by getting all the free variables for forces
        #TODO deal with packing/unpacking nested lists
        inputs = [d.get_free_forces() for d in walk_design(design)]
        #Optimize, driving total to zero

    def get_free_forces(self, design):
        self.free_forces = [d.get_free_forces() for d in walk_design(design)]
        return self.free_forces

    def calc_forces_and_torques(self, design, free_forces):
        #set the free forces in the design
        for i, d in enumerate(walk_design(design)):
            d.set_free_forces(free_forces[i])
        forces = [d.get_net_force() for d in walk_design(design)]
        net_force_x = sum([f[0] for f in forces])
        net_force_y = sum([f[1] for f in forces])
        net_torque = sum([f[2] for f in forces])
        return net_force_x, net_force_y, net_torque

    def unpack_forces(self):
        out = []
        for force in self.free_forces:
            out = out + [0.0 for c in force]
        return out

    def pack_forces(self, vals):
        f = []
        i = 0
        for c in self.free_forces:
            f.append(vals[i:i+len(c)])
            i = i+len(c)
        return f

    def score(self, x, Design):
        vals = self.pack_forces(x)
        score = sum([abs(v) for v in self.calc_forces_and_torques(Design, vals)])
        return score

    def solve_forces(self, Design):
        self.get_free_forces(Design)
        x0 = self.unpack_forces()
        res = scipy.optimize.minimize(self.score, x0, args = (Design))
        if not res.success:
            x1 = [random.random() for x in x0]
            res = scipy.optimize.minimize(self.score, x1, args = (Design))
        return res.x, res.success, res.fun


class ConfigAgent():
    """Find a configuration that works"""
    def __init__(self):
        pass

    def evaluate(self, design, reqs, threshold = 1.0):
        inputs = [d.get_config_vars() for d in walk_design(design)]

    def get_config_vars(self, design):
        self.configs = [d.get_config_vars() for d in walk_design(design)]
        return self.configs

    def unpack_configs(self):
        out = []
        for config in self.configs:
            out = out + [0.0 for c in config]
        return out

    def pack_configs(self, vals):
        conf = []
        i = 0
        for c in self.configs:
            conf.append(vals[i:i+len(c)])
            i = i+len(c)
        return conf

    def set_configs(self, design, configs):
        for i, d in enumerate(walk_design(design)):
            d.set_config_vars(configs[i])

    def score(self, x, Design, tol=0.001):
        confs = self.pack_configs()
        self.set_configs(Design, confs)
        config_score = sum([d.score_config() for d in walk_design(Design)])
        if config_score>0.1:
            return config_score
        else:
            FA = ForceAgent()
            sol, success, val = FA.solve_forces(Design)
            return np.tanh([abs(val)])[0]*0.09+config_score*0.1

    def solve_config(self, Design):
        #TODO Prevent negative tangential forecs at wheels, fix gravity
        self.get_config_vars(Design)
        x0 = self.unpack_configs()
        res = scipy.optimize.minimize(self.score, x0, args = (Design))
        return res.x, res.success, res.fun

class StatusAgent():
    def __init__(self):
        pass

    def pprint(self, Design):
        for d in utils.walk_design(Design):
            print "{}: {}".format(d.__class__.__name__, d.name)
            print "Net Forces:\t{}\t{}\t{}".format(*d.get_net_force())
            print "Transmitted Forces:\t{}\t{}\t{}".format(*d.get_transmitted_force())
            print ""
