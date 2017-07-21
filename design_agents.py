import utils


class Wheel():
    """A simple wheel, that adds appropriate constraints to solve for the robot position.
    Links to parts that can provide a torque and/or speed"""
    def __init__(self, reqs, radius, mass, parent):
        self.parent = parent
        self.radius = radius
        self.terrain = parent.terrain

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

    def convert_free_forces():


    def set_free_forces(self, forces):
        for i, f in enumerate(forces):
            self.free_forces[i] = f

    def get_net_force_x(self):
        forces = self.convert_free_forces()

    def get_net_force_y(self):
        pass

    def get_net_torque(self):
        pass

    def get_config_vars():
        return []


class Linkage():
    """ """

class
