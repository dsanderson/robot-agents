import utils


class Wheel():
    """A simple wheel, that adds appropriate constraints to solve for the robot position.
    Links to parts that can provide a torque and/or speed"""
    def __init__(self, reqs, radius, mass, parent):
        self.free_vars = ["torque"]
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
        return contact_points

    def get_free_forces():
        contact_points = self.get_contact_points()
        free_forces = []
        for c in contact_points:
            free_forces.append(0)
            free_forces.append(0)


    def get_config_vars():
        pass


class Linkage():
    """ """

class
