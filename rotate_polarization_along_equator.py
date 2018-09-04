# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 09:39:56 2018
single channel calibration testing
step 1: sweep single channel
step 2: do calibrations/fits for that channel
step 3: see if the calibrations/fits worked
@author: jhart
"""

from sweepPolarizationController import sweepPolarizationController
from determine_rotation_vectors import determine_rotation_vectors
from solve_for_angles import find_optimal_rotation_angles
from get_polarization_rotation_matrix import get_polarization_rotation_matrix
from plot_rotations import get_arc
import get_theta_from_s
import win32com
import PolarizationControllerDIO as PCDIO
import time
from matplotlib.figure import Figure
import numpy as np
import matplotlib.pyplot as plt


def plot(S1,S2,S3,master,canvas,line):
    line.set_xdata(S1)
    line.set_ydata(S2)
    line.set_3d_properties(S3)
    canvas.draw()   

##step 1: calibrate the polarization controller (this only needs to be done once)
#first do the sweep (apply a voltage, measure a SOP)
pol_fname = 'SOP_measurement1_ch'
sweepPolarizationController(pol_fname)
#then determine the rotation vectors and angles
print 'determine rotation vectors'
u1,u2,u3,u4,s0 = determine_rotation_vectors(pol_fname)

VLUT0,thetas0,u1 = get_theta_from_s.get_theta_of_v(pol_fname+str(0)+'.txt',0,u1)
VLUT1,thetas1,u2 = get_theta_from_s.get_theta_of_v(pol_fname+str(1)+'.txt',1,u2)
VLUT2,thetas2,u3 = get_theta_from_s.get_theta_of_v(pol_fname+str(2)+'.txt',2,u3)
VLUT3,thetas3,u4 = get_theta_from_s.get_theta_of_v(pol_fname+str(3)+'.txt',3,u4)

#initialize polarization analyzer and pol controller
analyzer = win32com.client.Dispatch("AgServerN778xLib.AgN778x")
analyzer.Initialize("GPIB0::30::INSTR",0,0)
PC0 = PCDIO.PolarizationController(0)

PC0.write(0,0)
time.sleep(0.001)
PC0.write(1,0)
time.sleep(0.001)
PC0.write(2,0)
time.sleep(0.001)   

S1 = []
S2 = []
S3 = []

SOP = analyzer.SCPIQuery(":POL:SOP?")
SOP = SOP.split(',')
S1.append(float(SOP[1])/float(SOP[0]))
S2.append(float(SOP[2])/float(SOP[0]))
S3.append(float(SOP[3])/float(SOP[0]))   
    
rot_angles_used = []    
    
##step 2: receive the desired output SOP from the user
#read input from user when user clicks GO
sf = [0,0,0]
Nsteps = 20
for step in range(Nsteps):
    print 'step number ' + str(step) + ' out of ' + str(Nsteps)
    #reset to 0    
    PC0.write(0,0)
    time.sleep(0.001)    
    PC0.write(1,0) 
    time.sleep(0.001)       
    PC0.write(2,0)
    time.sleep(0.001)    
    #measure initial condition (in case it changed)
    SOP = analyzer.SCPIQuery(":POL:SOP?")
    SOP = SOP.split(',')
    S1_0=float(SOP[1])/float(SOP[0])
    S2_0=float(SOP[2])/float(SOP[0])
    S3_0=float(SOP[3])/float(SOP[0]) 
    
    sf[0] = np.cos(np.pi*step/Nsteps) 
    sf[1] = np.sin(np.pi*step/Nsteps)
    
    #determine the optimal rotation angles about v1,v2,v3,v4
    N = 10 #N is the number of random initial conditions to try in the optimizer
    theta_des = find_optimal_rotation_angles((u1,u2,u3,u4),[S1_0,S2_0,S3_0],sf,N)
    rot_angles_used.append(theta_des)
  
    ##step 3: determine the correct voltages to apply to obtain the optimal rotation angles
    ndx0 = np.argmin(np.abs(thetas0[:143]-theta_des[0]))
    v0 = int(VLUT0[ndx0])
    ndx1 = np.argmin(np.abs(thetas1[:140]-theta_des[1]))
    v1 = int(VLUT1[ndx1])
    ndx2 = np.argmin(np.abs(thetas2[:143]-theta_des[2]))
    v2 = int(VLUT2[ndx2])
    
    ##step 4: apply these voltages to the polarization controller, and check the SOP
   
    PC0.write(0,v0)
    time.sleep(0.001)    
    PC0.write(1,v1) 
    time.sleep(0.001)       
    PC0.write(2,v2)
    time.sleep(0.001)   

    SOP = analyzer.SCPIQuery(":POL:SOP?")
    SOP = SOP.split(',')
    S1.append(float(SOP[1])/float(SOP[0]))
    S2.append(float(SOP[2])/float(SOP[0]))
    S3.append(float(SOP[3])/float(SOP[0])) 
    
   

#create the figure for plotting actual S parameters
fig_act = plt.figure()
ax_act = fig_act.add_subplot(111,projection='3d')
ax_act.mouse_init()
line_act,=ax_act.plot(S1,S2,S3,'bo-',markerfacecolor='b')
ax_act.set_title('actual SOP',fontsize=20)
#plot spherical grid
u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
x = np.cos(u)*np.sin(v)
y = np.sin(u)*np.sin(v)
z = np.cos(v)
ax_act.plot_wireframe(x, y, z, color="lightgray")
ax_act.set_xlabel('S1',fontsize=16)
ax_act.set_ylabel('S2',fontsize=16)
ax_act.set_zlabel('S3',fontsize=16)

'''
ax_act.plot([0,u1[0]],[0,u1[1]],[0,u1[2]],'c')
ax_act.plot([0,u2[0]],[0,u2[1]],[0,u2[2]],'m')
ax_act.plot([0,u3[0]],[0,u3[1]],[0,u3[2]],'g')
'''
#2d subplots
fig, (ax1, ax2,ax3) = plt.subplots(3, sharey=True)

ax1.plot(S1[1:], 'bo-')
ax1.plot(np.cos(np.arange(Nsteps)*np.pi/Nsteps),'k',linewidth=2.)
ax1.set(ylabel='S1')

ax2.plot(S2[1:], 'bo-')
ax2.plot(np.sin(np.arange(Nsteps)*np.pi/Nsteps),'k',linewidth=2.)
ax2.set(ylabel='S2')

ax3.plot(S3[1:],'bo-')
ax3.plot(np.arange(Nsteps)*0,'k',linewidth=2.)
ax3.set(ylabel='S3')


plt.show()
