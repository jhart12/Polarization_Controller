# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 10:51:07 2018
This code is a first attempt to solve for the rotation angles needed to 
rotate about given axes to get from a given s0 to a desired sf.
@author: jdhart12
"""

import numpy as np
from scipy.optimize import root
from get_polarization_rotation_matrix import get_polarization_rotation_matrix

#this is the function that we will find the roots of: R*s0-sf
#where R is the matrix of all 3 rotations, s0 is the measured initial vector
#and sf is the desired final vector
def f(thetas,*vecs):
    rot_vecs = vecs[0:4]
    s0 = vecs[4]
    sf = vecs[5]
    thetas = np.append(thetas,0) #set the fourth rotation to 0 bc underdetermined problem
    R = np.matrix(get_polarization_rotation_matrix(thetas,*rot_vecs))
    s0 = np.matrix(s0)
    sf = np.matrix(sf)
    return np.asarray(R*s0.T-sf.T)


def find_optimal_rotation_angles(rot_vecs,s0,sf,N):
    '''
    rot_vecs is a tuple of unit vectors that give the axis of rotation of the four pz transducers
    s0 is the measured initial unit vector and sf is the desired final unit vector
    '''
    a_vec = rot_vecs[0]
    b_vec = rot_vecs[1]
    c_vec = rot_vecs[2]
    d_vec = rot_vecs[3]
    
    vecs = (a_vec,b_vec,c_vec,d_vec,np.matrix(s0),np.matrix(sf))
    #print "vecs"
    #print vecs
    #Monte Carlo this guy to find the right initial conditions, where
    #"right" is defined as the ones that give us the shortest total angle of rotation
    #it's a highly nonlinear problem that's essentially solved using Newton's method
    #so it's highly dependend on initial conditions
    opt_cost = 1000 #initialize to a big value
    for i in range(N):
        theta_guess = 2*np.pi*np.random.rand(3)
        
        sol = root(f,theta_guess,args=vecs,method='broyden1')
        x = sol.x
        x = np.mod(x,2*np.pi)
        
        new_cost = np.sum(x)
        
        if(new_cost < opt_cost):
            opt_cost = new_cost
            opt_x = x
    return opt_x
    