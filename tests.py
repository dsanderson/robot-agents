import input_agents
import design_agents
import eval_agents
import utils
import math

def test_flat_agent():
    A = input_agents.FlatAgent()
    A.set_angles(math.radians(20), math.radians(20))
    ct = A.create_terrain()
    print len(ct), ct[0], ct[-1]
    return A, ct

def build_cart(terrain = [(0,0)]):
    Design = design_agents.Linkage(0.25, 0.1,
        None,
        True,
        terrain)
    w1 = design_agents.Wheel(0.08, 0.1, Design)
    w2 = design_agents.Wheel(0.08, 0.1, Design)
    Design.set_child(w1)
    Design.parent = w2
    return Design

def test_config(Design):
    CA = eval_agents.ConfigAgent()
    cv = CA.get_config_vars(Design)
    print cv
    vals = CA.unpack_configs()
    print vals
    cvals = CA.pack_configs(vals)
    print cvals
    CA.set_configs(Design, cvals)

def test_force_eval(Design):
    #print utils.walk_design(Design)
    FA = eval_agents.ForceAgent()
    print FA.get_free_forces(Design)
    forces = FA.unpack_forces()
    input_forces = FA.pack_forces(forces)
    print FA.calc_forces_and_torques(Design, input_forces)
    print FA.solve_forces(Design)

def test_draw(Design, Terrain):
    utils.draw_design(Design, Terrain)

def test_solvers(Design):
    pass


if __name__ == '__main__':
    A, ct = test_flat_agent()
    c = build_cart(ct)
    test_config(c)
    c.set_config_vars([0.0,0.08,math.radians(20)])
    #test_force_eval(c)
    test_draw(c, A)
