# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 10:53:52 2018

@author: jdhart12
"""
import numpy as np
from scipy.optimize import root, minimize
from get_single_rotation_matrix import *

#this is the function that we will find the roots of: R*s0-sf
#where R is the matrix of just one rotation, s0 is the measured initial vector
#and sf is the desired final vector
def f2(theta,*vecs):
    #print vecs
    theta=theta[0]
    rot_vec = vecs[0]
    s0 = vecs[1]
    sf = vecs[2]
    R = np.matrix(get_single_rotation_matrix(theta,rot_vec))
    s0 = np.matrix(s0)
    sf = np.matrix(sf)
    return np.sum(np.abs(R*s0.T-sf.T))

def get_theta_from_s(rot_vec,s0,sf,N):
    '''
    rot_vecs is a unit vector that gives the axis of rotation of the pz transducer
    s0 is the measured initial unit vector and sf is the desired final unit vector
    '''
    vecs = (rot_vec,s0,sf)
    #Monte Carlo this guy to find the right initial conditions, where
    #"right" is defined as the ones that give us the shortest total angle of rotation
    #it's a highly nonlinear problem that's essentially solved using Newton's method
    #so it's highly dependend on initial conditions
    opt_cost = 100 #initialize to a big value
    for i in range(N):
        theta_guess = 2*np.pi*np.random.rand(1)
        
        sol = minimize(f2,theta_guess,args=vecs)#,method='broyden1')
        new_cost = sol.fun
        #x = np.mod(x,2*np.pi)
            
        if(new_cost < opt_cost):
            opt_cost = new_cost
            opt_x = np.mod(sol.x[0],2*np.pi)
        if new_cost<0.1:
            break
    return opt_x

def get_theta_of_v(fname,rot_vec):
    Ch = np.loadtxt(fname,skiprows=1)
    s0 = np.asarray([Ch[0,1],Ch[0,2],Ch[0,3]])
    vs = Ch[:,0]
    
    thetas=[]
    for i in np.arange(0,len(vs)):
        sf = np.asarray([Ch[i,1],Ch[i,2],Ch[i,3]])
        theta = get_theta_from_s(rot_vec,s0,sf,7)
        thetas.append(theta)
        
    if(thetas[60]<thetas[40]):
        thetas=[]
        rot_vec = -rot_vec
        for i in np.arange(0,len(vs)):
            sf = np.asarray([Ch[i,1],Ch[i,2],Ch[i,3]])
            theta = get_theta_from_s(rot_vec,s0,sf,7)
            thetas.append(theta)
    thetas = np.array(thetas)
    vs = np.array(vs)    
    return vs,thetas,rot_vec