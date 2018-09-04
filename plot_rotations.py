# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 22:30:59 2018
This just plots rotations of t1, t2, t3 about axes v1,v2,v3
R3*R2*R1*s0=sf
@author: jdhart12
"""
import numpy as np
from get_polarization_rotation_matrix import get_polarization_rotation_matrix
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def get_arc(theta,arcnum,s_last,v1,v2,v3,v4):
    arc = np.zeros((3,50))
    t_vec = np.linspace(0,theta,num=50)
    tstep = t_vec[1]-t_vec[0]
    vec = [0,0,0,0]
    vec[arcnum]=1
    R1 = get_polarization_rotation_matrix((tstep*vec[0],tstep*vec[1],tstep*vec[2],tstep*vec[3]),v1,v2,v3,v4)
    arc[:,0] = np.asarray(s_last)
    for i in range(50-1):
        temp_mat = R1*np.matrix(arc[:,i]).T
        arc[:,i+1] = temp_mat.A1
    return arc



def plot_rotations(fig,s0,t1,t2,t3,t4,v1,v2,v3,v4):
    R = np.matrix(get_polarization_rotation_matrix((t1,t2,t3,t4),v1,v2,v3,v4))
    
    s0 = s0/np.sqrt(s0[0]**2+s0[1]**2+s0[2]**2)
    s0x = np.linspace(0,s0[0],num=100)
    s0y = np.linspace(0,s0[1],num=100)
    s0z = np.linspace(0,s0[2],num=100)
    s0 = np.matrix(s0)
    
    sf = R*s0.T
    
    sfx = np.linspace(0,sf.A1[0],num=100)
    sfy = np.linspace(0,sf.A1[1],num=100)
    sfz = np.linspace(0,sf.A1[2],num=100)
    
    #figure for plotting S parameters
    fig = plt.figure()
    ax = fig.add_subplot(111,projection='3d')
    
    initial_line,=ax.plot(s0x,s0y,s0z,'b',linewidth = 2)
    initial_point,=ax.plot(s0x[-1:],s0y[-1:],s0z[-1:],'ob')
    
    final_line,=ax.plot(sfx,sfy,sfz,'r',linewidth = 2)
    final_point,=ax.plot(sfx[-1:],sfy[-1:],sfz[-1:],'or')
    
    #plot arcs that we rotated around
    arc1 = get_arc(t1,0,s0.A1,v1,v2,v3,v4)
    first_arc, = ax.plot(arc1[0,:],arc1[1,:],arc1[2,:],'orange')
    
    arc2 = get_arc(t2,1,arc1[:,-1],v1,v2,v3,v4)   
    second_arc, = ax.plot(arc2[0,:],arc2[1,:],arc2[2,:],'y')
    
    arc3 = get_arc(t3,2,arc2[:,-1],v1,v2,v3,v4)
    third_arc, = ax.plot(arc3[0,:],arc3[1,:],arc3[2,:],'g')
    
    
    #plot spherical grid
    u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
    x = np.cos(u)*np.sin(v)
    y = np.sin(u)*np.sin(v)
    z = np.cos(v)
    ax.plot_wireframe(x, y, z, color="lightgray")
    ax.set_xlabel('S1',fontsize=16)
    ax.set_ylabel('S2',fontsize=16)
    ax.set_zlabel('S3',fontsize=16)
    
    
    
    
    