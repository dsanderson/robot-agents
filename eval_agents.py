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

    def score_loop():
        config_score = sum([d.score_config() for d in walk_design(design)])
        if config_score>1:
            return config_score
        # run force agent
        
