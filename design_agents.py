import utils, random


class Wheel():
    """A simple wheel, that adds appropriate constraints to solve for the robot position.
    Links to parts that can provide a torque and/or speed"""
    def __init__(self, radius, mass, parent=None, terrain=None):
        self.parent = parent
        self.radius = radius
        self.mass = mass
        if terrain==None:
            self.terrain = parent.terrain
        else:
            self.terrain = terrain
        self.name = random.random()

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def get_contact_points(self, slop = 0.0001):
        contact_points = []
        for p in self.terrain:
            if utils.dist(p, (self.x, self.y)) <= self.radius+slop and utils.dist(p, (self.x, self.y)) >= self.radius-slop:
                contact_points.append(p)
        self.contact_points = contact_points
        return self.contact_points

    def get_free_forces():
        contact_points = self.get_contact_points()
        self.free_forces = []
        for c in contact_points:
            self.free_forces.append(0) #radial force
            self.free_forces.append(0) #angular force
        return self.free_forces

    def set_free_forces(self, forces):
        for i, f in enumerate(forces):
            self.free_forces[i] = f

    def get_transmitted_force(self):
        net_external_torque = 0
        net_external_force_x = 0
        net_external_force_y = -self.mass*9.8
        for i, c in enumerate(self.contact_points):
            ang = math.atan2(c[1]-self.y, c[0]-self.x)
            #TODO check right hand rule
            net_external_torque += math.sin(ang)*self.free_forces[2*i]*self.radius
            net_external_torque += math.cos(ang)*self.free_forces[2*i+1]*self.radius
            net_external_force_x += self.free_forces[2*i]
            net_external_force_y += self.free_forces[2*i+1]
        transmitted_force = [-net_external_force_x, -net_external_force_y, -net_external_torque]
        return transmitted_force

    def get_net_forces(self):
        """we assume each body is static, so we can set the net force to zero and calculate the corresponding internal forces"""
        return [0,0,0]

    def get_config_vars(self):
        if self.parent==None:
            return ["x","y"]
        else:
            return []

    def set_config_vars(self, vars):
        self.set_position(vars[0], vars[1])

    def score_config(self):
        score = 0
        for p in self.terrain:
            d = utils.dist(p, (self.x, self.y))
            if d<self.radius:
                score+=self.radius-d
        return score

    def get_children(self):
        return []

class Motor():
    def __init__(self, mass, max_torque, parent=None, child=None, terrain=None):
        self.mass = mass
        self.parent = parent
        self.child = child
        self.max_torque = max_torque
        if terrain==None:
            self.terrain = parent.terrain
        else:
            self.terrain = terrain
        self.name = random.random()

    def get_config_vars(self):
        return []

    def get_transmitted_force(self):
        x, y, torque = *self.child.get_transmitted_force()
        y = y-self.mass*9.8
        if abs(torque)>abs(self.max_torque):
            out_torque = self.signum(torque)*self.max_torque
        else:
            out_torque = torque
        transmitted_force = [-x, -y, -out_torque]
        return transmitted_force

    def get_net_force(self):
        tf = self.get_transmitted_force()
        ef = self.child.get_transmitted_force()
        forces = [sum(x) for x in zip(tf, ef)]
        return forces

    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.child.set_position(x,y)

    def get_children(self):
        return [self.child]

class Linkage():
    """Class to generate and solve forces for linkages"""
    #TODO: how do we handle linkage loops, ensuring the ends meet up? add a check/cost function:soln, ass a pin object
    def __init__(self, length, mass, child, parent=None, is_root=False, terrain=None):
        self.length = length
        self.mass = mass
        self.child = child
        self.parent = parent
        self.is_root = is_root
        self.angle = 0
        if terrain==None:
            self.terrain = parent.terrain
        else:
            self.terrain = terrain
        self.name = random.random()

    def get_child_xy(self):
        x = self.x+self.length*math.cos(self.angle)
        y = self.y+self.length*math.sin(self.angle)
        return x, y

    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.child.set_position(*self.get_child_xy())
        if self.is_root:
            self.parent.set_position(x, y)

    def get_config_vars(self):
        if self.is_root==True:
            return ["x","y","angle"]
        else:
            return ["angle"]

    def set_config_vars(self, vars):
        if self.is_root == True:
            self.angle = vars[2]
            self.set_position(vars[0], vars[1])
        else:
            self.angle = vars[0]
            self.child.set_position(*self.get_child_xy())

    def get_net_force(self):
        if not self.is_root:
            return [0,0,0]
        else:
            tf = self.get_transmitted_force()
            pf = self.parent.get_transmitted_force()
            return [sum(z) for z in zip(tf, pf)]

    def get_transmitted_force(self):
        x, y, torque = *self.child.get_transmitted_force()
        net_torque = torque+math.sin(self.ang+math.pi)*x*self.length
        net_torque += math.cos(self.ang+math.pi)*y*self.length
        net_y = y-self.mass*9.8
        net_torque += math.cos(self.ang+math.pi)*-self.mass*9.8*self.length*0.66
        transmitted_force = [-x, -net_y, -net_torque]
        return transmitted_force

    def get_children(self):
        if not self.is_root:
            return [self.child]
        else:
            return [self.child, self.parent]

class Pin():
    def __init__(self, parent1, parent2, terrain=None):
        self.parent1 = parent1
        self.parent2 = parent2
        if terrain==None:
            self.terrain = parent.terrain
        else:
            self.terrain = terrain
        self.name = random.random()

    def get_config_vars(self):
        return []

    def get_transmitted_force(self, name):
        if name == self.parent1.name:
            return [self.free_forces[0], self.free_forces[1], 0]
        return [-self.free_forces[0], -self.free_forces[1], 0]

    def get_free_forces(self):
        return ["x","y"]

    def set_free_forces(self, forces):
        self.free_forces = forces

    def get_net_force(self):
        return [0,0,0]

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def score_config(self):
        score = abs(utils.dist((self.parent1.x,self.parent1.y), (self.parent2.x,self.parent2.y)))
        return score

    def get_children(self):
        return []
