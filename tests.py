import input_agents
import design_agents
import eval_agents
import math

def test_flat_agent():
    A = input_agents.FlatAgent(-math.radians(20), math.radians(20))
    assert(A.create_terrain()!=A.create_terrain())

def build_cart():
    Design = design_agents.Linkage(0.25, 0.1,
        design_agents.Wheel(0.01, 0.1),
        design_agents.Wheel(0.01, 0.1),
        True,
        [(0,0)])
    Design.child.parent = Design
    Design.parent.parent = Design
    return Design

if __name__ == '__main__':
    test_flat_agent()
    c = build_cart()
