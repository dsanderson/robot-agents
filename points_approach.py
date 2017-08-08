import math, os
import numpy as np
import itertools
import tqdm
import sklearn.model_selection
import sklearn.ensemble
import sklearn.metrics
import sklearn.svm
import sklearn.neighbors
import time

def wheel_step_points_gen(width, height, radius, max_torque, mass):
    """return points in the form (x, y, Fx_center, Fy_center, Torque, valid?)
    assumes all the bodies are static, """
    pass

def wheel_flat_points_gen(radius, max_torque, mass, max_strength=10, mu=0.5, density=50, slop=0.01):
    """return points in the form (x, y, Fx_center, Fy_center, Torque, valid?)
    assumes all the bodies are static, """
    #return points that are on the floor
    pts = []
    weight = mass*-9.8
    y = radius
    for x in np.linspace(0, 1, density):
        for Fy_center in np.linspace(max_strength, weight, density):
            Fn = -1*(Fy_center+weight)
            max_Fr = Fn*mu
            for Torque in np.linspace(-max_torque,  max_torque, density):
                Fx_center = -Torque*radius
                if abs(Fx_center)<abs(max_Fr):
                    pts.append((x, y, Fx_center, Fy_center, Torque, 1))
                    pts.append((x, y, Fx_center+0.01, Fy_center, Torque, 0))
                    pts.append((x, y, Fx_center-0.01, Fy_center, Torque, 0))
                    pts.append((x, y, Fx_center, Fy_center+0.01, Torque, 0))
                    pts.append((x, y, Fx_center, Fy_center-0.01, Torque, 0))
        pts.append((x, y+0.01, 0, weight, 0, 1))
        pts.append((x, y+0.01, 0, weight-0.01, 0, 0))
        pts.append((x, y+0.01, 0, weight+0.01, 0, 0))
        pts.append((x, y+0.01, -0.01, weight, 0, 0))
        pts.append((x, y+0.01, 0.01, weight, 0, 0))
        pts.append((x, y+0.01, 0, weight, -0.01, 0))
        pts.append((x, y+0.01, 0, weight, 0.01, 0))
        pts.append((x, y-0.01, 0, 0, 0, 0))
    return pts


def bar(length, mass, x_range, y_range, max_strength=10, density=5):
    """returns points in the form (x, y, angle, x1, y1, x2, y2, Fx_1, Fy_1, T1, Fx_2, Fy_2, T2, valid?)"""
    Fg = mass*-9.8
    pts = []
    for x in tqdm.tqdm(np.linspace(0, x_range, density)):
        for y in np.linspace(0, y_range, density):
            for ang in np.linspace(0, 2*math.pi, density):
                x1 = x-length/2.0*math.cos(ang)
                y1 = y-length/2.0*math.sin(ang)
                x2 = x+length/2.0*math.cos(ang)
                y2 = y+length/2.0*math.sin(ang)
                for Fx_1 in np.linspace(-max_strength, max_strength, density):
                    for Fy_1 in np.linspace(-max_strength, max_strength, density):
                        for T_1 in np.linspace(-max_strength, max_strength, density):
                            Fx_2 = T_1/(length)*math.sin(ang)-Fx_1
                            Fy_2 = -Fy_1-Fg-T_1/(length)*math.cos(ang)
                            T_2 = Fx_1*length*math.sin(ang+math.pi)-Fy_1*length*math.cos(ang+math.pi)-Fg*length*math.cos(ang+math.pi)/2.0-T_1
                            #TODO Save results in list
                            pts.append((x, y, ang, x1, y1, x2, y2, Fx_1, Fy_1, T_1, Fx_2, Fy_2, T_2, 1))
                for Fx_2 in np.linspace(-max_strength, max_strength, density):
                    for Fy_2 in np.linspace(-max_strength, max_strength, density):
                        for T_2 in np.linspace(-max_strength, max_strength, density):
                            #TODO ensure the RHS has the correct referrants and signs
                            Fx_1 = -T_2/(length)*math.sin(ang)-Fx_2
                            Fy_1 = -Fy_2-Fg+T_2/(length)*math.cos(ang)
                            T_1 = Fx_2*length*math.sin(ang)-Fy_2*length*math.cos(ang)-Fg*length*math.cos(ang)/2.0-T_2
                            pts.append((x, y, ang, x1, y1, x2, y2, Fx_1, Fy_1, T_1, Fx_2, Fy_2, T_2, 1))
    return pts

def nearests(condition, l, threshold=0.05):
    val = condition(min(l, key=lambda x:condition(x)))
    if abs(val)>threshold:
        return []
    ls = [v for v in l if condition(v)==val]
    return ls

def make_possible_predictor(pts, inputs, predictor):
    print "Training predictor at {}".format(time.ctime())
    Xs = np.array([[x[i] for i in inputs] for x in pts])
    Ys = np.array([x[predictor] for x in pts])
    Xtrain, Xtest, Ytrain, Ytest = sklearn.model_selection.train_test_split(Xs, Ys, test_size=0.0, random_state=100)
    model = sklearn.neighbors.KNeighborsClassifier(n_neighbors=1) #sklearn.svm.SVC()
    model.fit(Xtrain, Ytrain)
    #mse = sklearn.metrics.mean_squared_error(Ytest, model.predict(Xtest))
    #print "Model MSE:{}".format(mse)
    return model

def naive_cart_search(bar_pts, wheel1_pts, wheel2_pts, threshold=0.05):
    #step 1: condition cart points on x-condition
    bpts = nearests(lambda x:abs(x[0]-0.4), bar_pts)
    print any([b[1]==0.2 for b in bpts]), len(bpts)
    wheel_1_predictor = make_possible_predictor(wheel1_pts, [0, 1, 2, 3, 4], 5)
    wheel_2_predictor = make_possible_predictor(wheel2_pts, [0, 1, 2, 3, 4], 5)
    solns = []
    for bp in tqdm.tqdm(bpts):
        w1vals = np.array((bp[3], bp[4], -bp[7], -bp[8], -bp[9])).reshape(1, -1)
        w2vals = np.array((bp[5], bp[6], -bp[10], -bp[11], -bp[12])).reshape(1, -1)
        if wheel_1_predictor.predict(w1vals)==1:
            if wheel_2_predictor.predict(w2vals)==1:
                solns.append([bp])
        #find matching points for wheel 1
        #wls1 = nearests(lambda x:abs(bp[3]-x[0])+abs(bp[4]-x[1])+abs(bp[7]+x[2])+abs(bp[8]+x[3])+abs(bp[9]+x[4])+bp[13]+x[5], wheel1_pts)
        #if len(wls1)==0:
        #    continue
        #wls2 = nearests(lambda x:abs(bp[5]-x[0])+abs(bp[6]-x[1])+abs(bp[10]+x[2])+abs(bp[11]+x[3])+abs(bp[12]+x[4])+bp[13]+x[5], wheel2_pts)
        #if len(wls1)>0 and len(wls2)>0:
        #    solns.append(itertools.product([bp],wls1,wls2))
    return solns, wheel_1_predictor

if __name__ == '__main__':
    bar_pts = bar(0.2, 0.1, 1.0, 0.5, density=6)
    print len(bar_pts)
    wheel_pts = wheel_flat_points_gen(0.2, 1.0, 0.1)
    print len(wheel_pts)
    slns, model = naive_cart_search(bar_pts, wheel_pts, wheel_pts)
    print len(slns)
