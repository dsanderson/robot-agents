import points_approach, RBM
import numpy as np
import tqdm
import sklearn.model_selection
import random
import math, time, copy
import matplotlib.pyplot as plt

def tester(rbm, points):
    dists = []
    print "Evaluating points at {}".format(time.ctime())
    pout = rbm.update(points)
    print "Finished evaluating at {}".format(time.ctime())
    #print p, pout, len(pout[0])
    for i, p in enumerate(list(points)):
        dists.append(distance(p, list(pout[i])))
    return dists

def distance(a, b):
    d = 0
    for i in range(0, len(a)):
        d = d+(a[i]-b[i])**2
    d = math.sqrt(d)
    return d

def get_norm_funcs(points):
    maxes = [max([p[i] for p in points]) for i in range(0, len(points[0]))]
    mins = [min([p[i] for p in points]) for i in range(0, len(points[0]))]
    print maxes, mins
    ranges = [p[0]-p[1] for p in zip(maxes, mins)]
    def norm(pt):
        normed = [(p-mins[i])/float(ranges[i]) for i, p in enumerate(pt)]
        return tuple(normed)
    def unnorm(pt):
        unnormed = [(p*float(ranges[i]))+mins[i] for i, p in enumerate(pt)]
        return tuple(unnormed)
    return norm, unnorm

def cart_echo(bar_rbm, wheel_rbm, bar_norm, bar_unnorm, wheel_norm, wheel_unnorm, n=10):
    """bar=(x, y, angle, x1, y1, x2, y2, Fx_1, Fy_1, T1, Fx_2, Fy_2, T2)
    wheel=(x, y, Fx_center, Fy_center, Torque)"""
    x = 0.5
    xi = 0
    random.seed(10)
    bar = [random.random() for _ in range(0,13)]
    bar = bar_unnorm(bar)
    wheel_1 = [random.random() for _ in range(0,5)]
    wheel_1 = wheel_unnorm(wheel_1)
    wheel_2 = [random.random() for _ in range(0,5)]
    wheel_2 = wheel_unnorm(wheel_2)
    for i in xrange(n):
        #manually set the appropriate values
        bar = list(bar)
        wheel_1 = list(wheel_1)
        wheel_2 = list(wheel_2)
        #print bar, wheel_1, wheel_2

        bar[xi] = x

        w1x = (bar[3]+wheel_1[0])/2.0
        bar[3] = w1x
        wheel_1[0] = w1x

        w1y = (bar[4]+wheel_1[1])/2.0
        bar[4] = w1y
        wheel_1[1] = w1y

        w2x = (bar[5]+wheel_2[0])/2.0
        bar[5] = w2x
        wheel_2[0] = w2x

        w2y = (bar[6]+wheel_2[1])/2.0
        bar[6] = w2y
        wheel_2[1] = w2y

        w1fx, w1fy, w1t = ((bar[7]-wheel_1[2])/2.0, (bar[8]-wheel_1[3])/2.0, (bar[9]-wheel_1[4])/2.0)
        bar[7] = w1fx
        bar[8] = w1fy
        bar[9] = w1t
        wheel_1[2] = -w1fx
        wheel_1[3] = -w1fy
        wheel_1[4] = -w1t

        w2fx, w2fy, w2t = ((bar[10]-wheel_2[2])/2.0, (bar[11]-wheel_2[3])/2.0, (bar[12]-wheel_2[4])/2.0)
        bar[10] = w2fx
        bar[11] = w2fy
        bar[12] = w2t
        wheel_2[2] = -w2fx
        wheel_2[3] = -w2fy
        wheel_2[4] = -w2t

        bar = bar_unnorm(bar_rbm.update(np.array(bar_norm(bar)).reshape(1,-1))[0])
        wheel_1 = wheel_unnorm(wheel_rbm.update(np.array(wheel_norm(wheel_1)).reshape(1,-1))[0])
        wheel_2 = wheel_unnorm(wheel_rbm.update(np.array(wheel_norm(wheel_2)).reshape(1,-1))[0])

    return bar, wheel_1, wheel_2

def tri_cart_echo(bar_rbm, bar_2_rbm, wheel_rbm, bar_norm, bar_unnorm, bar_2_norm, bar_2_unnorm, wheel_norm, wheel_unnorm, n=10):
    """bar=(x, y, angle, x1, y1, x2, y2, Fx_1, Fy_1, T1, Fx_2, Fy_2, T2)
    wheel=(x, y, Fx_center, Fy_center, Torque)"""
    x = 0.5
    xi = 0
    random.seed(10)
    bar = [random.random() for _ in range(0,13)]
    bar = bar_unnorm(bar)
    bar1 = [random.random() for _ in range(0,13)]
    bar1 = bar_2_unnorm(bar1)
    bar2 = [random.random() for _ in range(0,13)]
    bar2 = bar_2_unnorm(bar2)
    bar3 = [random.random() for _ in range(0,13)]
    bar3 = bar_2_unnorm(bar3)
    wheel_1 = [random.random() for _ in range(0,5)]
    wheel_1 = wheel_unnorm(wheel_1)
    wheel_2 = [random.random() for _ in range(0,5)]
    wheel_2 = wheel_unnorm(wheel_2)
    wheel_3 = [random.random() for _ in range(0,5)]
    wheel_3 = wheel_unnorm(wheel_3)
    wheel_4 = [random.random() for _ in range(0,5)]
    wheel_4 = wheel_unnorm(wheel_4)
    for i in xrange(n):
        #manually set the appropriate values
        bar = list(bar)
        bar1 = list(bar1)
        bar2 = list(bar2)
        bar3 = list(bar3)
        wheel_1 = list(wheel_1)
        wheel_2 = list(wheel_2)
        wheel_4 = list(wheel_3)
        wheel_3 = list(wheel_4)

        bar[xi] = x

        w1x = (bar[3]+wheel_1[0])/2.0
        bar[3] = w1x
        wheel_1[0] = w1x
        w1y = (bar[4]+wheel_1[1])/2.0
        bar[4] = w1y
        wheel_1[1] = w1y

        w1fx, w1fy, w1t = ((bar[7]-wheel_1[2])/2.0, (bar[8]-wheel_1[3])/2.0, (bar[9]-wheel_1[4])/2.0)
        bar[7] = w1fx
        bar[8] = w1fy
        bar[9] = w1t
        wheel_1[2] = -w1fx
        wheel_1[3] = -w1fy
        wheel_1[4] = -w1t

        bx, by = ((bar[5]+bar1[3]+bar2[3]+bar3[3])/4.0, (bar[6]+bar1[4]+bar2[4]+bar3[4])/4.0)
        bar[5] = bx
        bar[6] = by
        bar1[3] = bx
        bar1[4] = by
        bar2[3] = bx
        bar2[4] = by
        bar3[3] = bx
        bar3[4] = by

        bang = (bar1[2]+bar2[2]-(2*math.pi/3.0)+bar3[2]-(4*math.pi/3.0))/3.0
        bar1[2] = bang
        bar2[2] = bang+(2*math.pi/3.0)
        bar3[2] = bang+(4*math.pi/3.0)

        bfxe, bfye, bte = (bar[10]+bar1[7]+bar2[7]+bar3[7])/4.0, (bar[11]+bar1[8]+bar2[8]+bar3[8])/4.0, (bar[12]+bar1[9]+bar2[9]+bar3[9])/4.0
        bar[10] = bar[10]+bfxe
        bar[11] = bar[11]+bfye
        bar[12] = bar[12]+bte
        bar1[7] = bar1[7]-bfxe
        bar1[8] = bar1[8]-bfye
        bar1[9] = bar1[9]-bte
        bar2[7] = bar2[7]-bfxe
        bar2[8] = bar2[8]-bfye
        bar2[9] = bar2[9]-bte
        bar3[7] = bar3[7]-bfxe
        bar3[8] = bar3[8]-bfye
        bar3[9] = bar3[9]-bte

        w1x = (bar1[5]+wheel_2[0])/2.0
        bar1[5] = w1x
        wheel_2[0] = w1x
        w1y = (bar1[6]+wheel_2[1])/2.0
        bar1[6] = w1y
        wheel_2[1] = w1y

        w2fx, w2fy, w2t = ((bar1[10]+wheel_2[2])/2.0, (bar1[11]+wheel_2[3])/2.0, (bar1[12]+wheel_2[4])/2.0)
        bar1[10] = w2fx
        bar1[11] = w2fy
        bar1[12] = w2t
        wheel_2[2] = -w2fx
        wheel_2[3] = -w2fy
        wheel_2[4] = -w2t

        w1x = (bar2[5]+wheel_3[0])/2.0
        bar2[5] = w1x
        wheel_3[0] = w1x
        w1y = (bar2[6]+wheel_3[1])/2.0
        bar2[6] = w1y
        wheel_3[1] = w1y

        w2fx, w2fy, w2t = ((bar2[10]+wheel_3[2])/2.0, (bar2[11]+wheel_3[3])/2.0, (bar2[12]+wheel_3[4])/2.0)
        bar2[10] = w2fx
        bar2[11] = w2fy
        bar2[12] = w2t
        wheel_3[2] = -w2fx
        wheel_3[3] = -w2fy
        wheel_3[4] = -w2t

        w1x = (bar3[5]+wheel_4[0])/2.0
        bar3[5] = w1x
        wheel_4[0] = w1x
        w1y = (bar3[6]+wheel_4[1])/2.0
        bar3[6] = w1y
        wheel_4[1] = w1y

        w2fx, w2fy, w2t = ((bar3[10]+wheel_4[2])/2.0, (bar3[11]+wheel_4[3])/2.0, (bar3[12]+wheel_4[4])/2.0)
        bar3[10] = w2fx
        bar3[11] = w2fy
        bar3[12] = w2t
        wheel_4[2] = -w2fx
        wheel_4[3] = -w2fy
        wheel_4[4] = -w2t

        bar = bar_unnorm(bar_rbm.update(np.array(bar_norm(bar)).reshape(1,-1))[0])
        bar1 = bar_2_unnorm(bar_2_rbm.update(np.array(bar_2_norm(bar1)).reshape(1,-1))[0])
        bar2 = bar_2_unnorm(bar_2_rbm.update(np.array(bar_2_norm(bar2)).reshape(1,-1))[0])
        bar3 = bar_2_unnorm(bar_2_rbm.update(np.array(bar_2_norm(bar3)).reshape(1,-1))[0])
        wheel_1 = wheel_unnorm(wheel_rbm.update(np.array(wheel_norm(wheel_1)).reshape(1,-1))[0])
        wheel_2 = wheel_unnorm(wheel_rbm.update(np.array(wheel_norm(wheel_2)).reshape(1,-1))[0])
        wheel_3 = wheel_unnorm(wheel_rbm.update(np.array(wheel_norm(wheel_3)).reshape(1,-1))[0])
        wheel_4 = wheel_unnorm(wheel_rbm.update(np.array(wheel_norm(wheel_4)).reshape(1,-1))[0])

    return bar, wheel_1, wheel_2

if __name__ == '__main__':
    wheel_pts = points_approach.wheel_flat_points_gen(0.1, 1.0, 0.1)
    wheel_pts = [p[:-1] for p in wheel_pts]
    wheel_norm, wheel_unnorm = get_norm_funcs(wheel_pts)
    wheel_pts = [wheel_norm(p) for p in wheel_pts]
    wheel_pts = np.array(wheel_pts)
    print "Training on {} points".format(len(wheel_pts))
    random.shuffle(wheel_pts)
    print "Training wheels begins at {}".format(time.ctime())
    wheel_rbm = RBM.RBM(len(wheel_pts[0]), 1024, visible_unit_type='gauss', verbose=0)
    wheel_rbm.fit(wheel_pts)
    print "Training wheels ends at {}".format(time.ctime())

    bar_pts = points_approach.bar(0.2,0.1,1.0,1.0)
    bar_pts = [p[:-1] for p in bar_pts]
    bar_norm, bar_unnorm = get_norm_funcs(bar_pts) #TODO make sure norms line up between bar and wheels
    bar_pts = [bar_norm(p) for p in bar_pts]
    bar_pts = np.array(bar_pts)
    print "Training on {} points".format(len(bar_pts))
    random.shuffle(bar_pts)
    print "Training bars begins at {}".format(time.ctime())
    bar_rbm = RBM.RBM(len(bar_pts[0]), 1024, visible_unit_type='gauss', verbose=0)
    bar_rbm.fit(bar_pts)
    print "Training bars ends at {}".format(time.ctime())

    print "Calculating cart configurations at {}".format(time.ctime())
    bar_res, wheel_1_res, wheel_2_res = cart_echo(bar_rbm, wheel_rbm, bar_norm, bar_unnorm, wheel_norm, wheel_unnorm)
    print "Finished cart configurations at {}".format(time.ctime())

    bar2_pts = points_approach.bar(0.1,0.1,1.0,1.0)
    bar2_pts = [p[:-1] for p in bar2_pts]
    bar2_norm, bar2_unnorm = get_norm_funcs(bar2_pts) #TODO make sure norms line up between bar and wheels
    bar2_pts = [bar2_norm(p) for p in bar2_pts]
    bar2_pts = np.array(bar2_pts)
    print "Training on {} points".format(len(bar2_pts))
    random.shuffle(bar2_pts)
    print "Training bars begins at {}".format(time.ctime())
    bar2_rbm = RBM.RBM(len(bar2_pts[0]), 1024, visible_unit_type='gauss', verbose=0)
    bar2_rbm.fit(bar2_pts)
    print "Training bars ends at {}".format(time.ctime())
    print "Calculating tri-cart configurations at {}".format(time.ctime())
    res = tri_cart_echo(bar_rbm, bar2_rbm, wheel_rbm, bar_norm, bar_unnorm, bar2_norm, bar2_unnorm, wheel_norm, wheel_unnorm)
    print "Finished tri-cart configurations at {}".format(time.ctime())

    print "Evaluating at {}".format(time.ctime())
    dists = tester(bar_rbm, bar_pts)
    plt.figure()
    plt.hist(dists, bins=50)
    plt.title("Bar_dists")

    dists = tester(wheel_rbm, wheel_pts)
    plt.figure()
    plt.hist(dists, bins=50)
    plt.title("wheel_dists")

    plt.show()
