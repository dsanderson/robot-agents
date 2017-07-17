from utils import sample

class MinSpeedAgent:
    def __init__(self):
        pass

    def set_speed(self,x,y):
        self.x = x
        self.y = y

    def evaluate(self, desc):
        return desc["results"]["min_speed"]["x"] > self.x and desc["results"]["min_speed"]["y"] > self.y    
