# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 16:11:09 2018
This script takes the polarization sweep data (S params as a function of voltage)
and uses it to obtain:
 1) the axis of rotation of each of the piezoelectric transducers
 2) a lookup table of rotation angle theta(v) for each of the piezoelectric transducers
@author: jhart
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
#from determine_rotation_vectors import determine_rotation_vectors
from get_theta_from_s import get_theta_of_v
#from get_single_rotation_matrix import get_single_rotation_matrix

def get_v_of_theta_fits(fname,v0,v1,v2,v3):
    #v0,v1,v2,v3 = determine_rotation_vectors()
    V0,thetas0 = get_theta_of_v(fname+str(0)+'.txt',v0)
    V1,thetas1 = get_theta_of_v(fname+str(1)+'.txt',v1)
    V2,thetas2 = get_theta_of_v(fname+str(2)+'.txt',v2)
    V3,thetas3 = get_theta_of_v(fname+str(3)+'.txt',v3)
    #fit unwrapped theta(v) to a line
    p0 = np.polyfit(V0[1:200],np.unwrap(thetas0[:199]),1)
    p1 = np.polyfit(V1[1:200],np.unwrap(thetas1[:199]),1)
    p2 = np.polyfit(V2[1:200],np.unwrap(thetas2[:199]),1)
    p3 = np.polyfit(V3[1:200],np.unwrap(thetas3[:199]),1)

    p0 = [1./p0[0],-p0[1]/p0[0]]    
    p1 = [1./p1[0],-p1[1]/p1[0]]
    p2 = [1./p2[0],-p2[1]/p2[0]]
    p3 = [1./p3[0],-p3[1]/p3[0]]
    return p0,p1,p2,p3

def get_v(theta,p):
    return int(np.round(p[0]*theta+p[1]))

def get_v2(theta,p):
    v=-1
    theta1 = theta
    while(v<0):
        v = np.round(p[0]*theta1+p[1])
        theta1 += 2.0*np.pi
    return int(v)

#p0,p1,p2,p3 = get_v_of_theta_fits()



'''
s0 = np.matrix(s0)
#trace out slow increase in v
sfs = []
#figure for plotting S parameters
fig = plt.figure()
ax = fig.add_subplot(111,projection='3d')
for theta in ch0_thetas:
    R = np.matrix(get_single_rotation_matrix(theta,v1))
    sf = np.asarray(R*s0.T)
    ax.plot(sf[0],sf[1],sf[2],'o')
#plot spherical grid
u, V = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
x = np.cos(u)*np.sin(V)
y = np.sin(u)*np.sin(V)
z = np.cos(V)
ax.plot_wireframe(x, y, z, color="lightgray")
ax.set_xlabel('S1',fontsize=16)
ax.set_ylabel('S2',fontsize=16)
ax.set_zlabel('S3',fontsize=16)
'''