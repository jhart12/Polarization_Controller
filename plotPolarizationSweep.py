# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 16:58:24 2017

@author: jhart
"""

import numpy as np
import matplotlib.pyplot as plt
from get_polarization_rotation_matrix import get_polarization_rotation_matrix
from get_theta_from_s import get_theta_from_s
from mpl_toolkits.mplot3d import Axes3D

data = np.loadtxt('v0v1_test_ch2_ch1.txt',skiprows=1)


def get_theta_of_v0(rot_vec):
    s0 = np.asarray([data[0,2],data[0,3],data[0,4]])
    vs = data[:startv1,0]
    thetas=[]
    for i in np.arange(0,len(vs)):
        sf = np.asarray([data[i,2],data[i,3],data[i,4]])
        theta = get_theta_from_s(rot_vec,s0,sf,7)
        thetas.append(theta)
    return vs,thetas
    
def get_theta_of_v1(rot_vec):
    s0 = np.asarray([data[startv1,2],data[startv1,3],data[startv1,4]])
    vs = data[startv1:,1]
    thetas=[]
    for i in np.arange(0,len(vs)):
        sf = np.asarray([data[startv1+i,2],data[startv1+i,3],data[startv1+i,4]])
        theta = get_theta_from_s(rot_vec,s0,sf,7)
        thetas.append(theta)
    return vs,thetas


startv1 = np.argwhere(data[:,1]>0)
startv1 = startv1[0][0]
 
fig = plt.figure()
ax = fig.add_subplot(111,projection='3d')
ax.plot(data[:startv1,2],data[:startv1,3],data[:startv1,4],'b')
ax.plot(data[startv1:,2],data[startv1:,3],data[startv1:,4],'r')

#ax.plot(data[:100,2],data[:100,3],data[:100,4],'b')
#ax.plot(data[startv1:startv1+100,2],data[startv1:startv1+100,3],data[startv1:startv1+100,4],'r')

#calculate and plot u0 and u1
ch0_s1_max = np.max(data[:startv1,2])
ch0_s1_min = np.min(data[:startv1,2])
ch0_s1_center = (ch0_s1_max+ch0_s1_min)/2.
ch0_s2_max = np.max(data[:startv1,3])
ch0_s2_min = np.min(data[:startv1,3])
ch0_s2_center = (ch0_s2_max+ch0_s2_min)/2.
ch0_s3_max = np.max(data[:startv1,4])
ch0_s3_min = np.min(data[:startv1,4])
ch0_s3_center = (ch0_s3_max+ch0_s3_min)/2.
u0 = np.asarray([ch0_s1_center,ch0_s2_center,ch0_s3_center])
u0 = u0/np.linalg.norm(u0,ord=2)



ch1_s1_max = np.max(data[startv1:,2])
ch1_s1_min = np.min(data[startv1:,2])
ch1_s1_center = (ch1_s1_max+ch1_s1_min)/2.
ch1_s2_max = np.max(data[startv1:,3])
ch1_s2_min = np.min(data[startv1:,3])
ch1_s2_center = (ch1_s2_max+ch1_s2_min)/2.
ch1_s3_max = np.max(data[startv1:,4])
ch1_s3_min = np.min(data[startv1:,4])
ch1_s3_center = (ch1_s3_max+ch1_s3_min)/2.
u1 = np.asarray([ch1_s1_center,ch1_s2_center,ch1_s3_center])
u1 = u1/np.linalg.norm(u1,ord=2)

ax.plot([0,u0[0]],[0,u0[1]],[0,u0[2]],'b')

ax.plot([0,u1[0]],[0,u1[1]],[0,u1[2]],'r')

s0 = data[0,2:]/np.linalg.norm(data[0,2:],ord=2)    
ax.plot([s0[0]],[s0[1]],s0[2],'bo')

s0r = data[startv1,2:]/np.linalg.norm(data[startv1,2:],ord=2)    
ax.plot([s0r[0]],[s0r[1]],s0r[2],'ro')

s0k = data[-1,2:]/np.linalg.norm(data[-1,2:],ord=2)    
ax.plot([s0k[0]],[s0k[1]],s0k[2],'ko')

#determine theta(v)
v0,theta0 = get_theta_of_v0(u0)
v1,theta1 = get_theta_of_v1(u1)


#get polarization rotation matrix
for i in range(len(v0)):
    R = get_polarization_rotation_matrix((theta0[i],0,0,0),u0,u1,u1,u1)
    sf = np.matmul(R,s0)
    ax.plot([sf[0]],[sf[1]],sf[2],'.c')

for i in range(len(v1)):
    R = get_polarization_rotation_matrix((0,theta1[i],0,0),u0,u1,u1,u1)
    sf = np.matmul(R,s0r)
    ax.plot([sf[0]],[sf[1]],sf[2],'.m')



#plot theta(v)
plt.figure()
plt.plot(v0,theta0,'b')
plt.plot(v1,theta1,'r')








ax.set_xlabel('S1')
ax.set_ylabel('S2')
ax.set_zlabel('S3')
ax.set_title('run 1')

u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
x = np.cos(u)*np.sin(v)
y = np.sin(u)*np.sin(v)
z = np.cos(v)
ax.plot_wireframe(x, y, z, color="lightgray")
