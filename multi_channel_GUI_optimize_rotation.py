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
from plot_rotations import get_arc
import makeLUT
import win32com
import PolarizationControllerDIO as PCDIO
import time
import Tkinter
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
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
#sweepPolarizationController(pol_fname)
#then determine the rotation vectors and angles
print 'determine rotation vectors'
u1,u2,u3,u4,s0 = determine_rotation_vectors(pol_fname)

VLUT0,thetas0,u1 = makeLUT.get_theta_of_v(pol_fname+str(0)+'.txt',0,u1)
VLUT1,thetas1,u2 = makeLUT.get_theta_of_v(pol_fname+str(1)+'.txt',1,u2)
VLUT2,thetas2,u3 = makeLUT.get_theta_of_v(pol_fname+str(2)+'.txt',2,u3)
VLUT3,thetas3,u4 = makeLUT.get_theta_of_v(pol_fname+str(3)+'.txt',3,u4)

#initialize polarization analyzer and pol controller
analyzer = win32com.client.Dispatch("AgServerN778xLib.AgN778x")
analyzer.Initialize("GPIB0::30::INSTR",0,0)
PC0 = PCDIO.PolarizationController(0)

#######THE REST OF THE CODE GOES IN THE LOOP############


def go():
    
    PC0.write(0,0)
    time.sleep(0.001)
    PC0.write(1,0)
    time.sleep(0.001)
    PC0.write(2,0)
    time.sleep(0.001)   
    
    S1 = []
    S2=[]
    S3=[]
    
    SOP = analyzer.SCPIQuery(":POL:SOP?")
    SOP = SOP.split(',')
    S1.append(float(SOP[1])/float(SOP[0]))
    S2.append(float(SOP[2])/float(SOP[0]))
    S3.append(float(SOP[3])/float(SOP[0]))    
    
    ##step 2: receive the desired output SOP from the user
    #read input from user when user clicks GO
    #theta_des = [float(des_box0.get()),float(des_box1.get()),float(des_box2.get()),0]
    sf = [float(des_box0.get()),float(des_box1.get()),float(des_box2.get())]
    sf = sf/np.sqrt(sf[0]**2.0+sf[1]**2.0+sf[2]**2.0)
    #determine the optimal rotation angles about v1,v2,v3,v4
    N = 10 #N is the number of random initial conditions to try in the optimizer
    theta_des = find_optimal_rotation_angles((u1,u2,u3,u4),[S1[0],S2[0],S3[0]],sf,N)
  
  
  
    ##step 3: determine the correct voltages to apply to obtain the optimal rotation angles
    ndx0 = np.argmin(np.abs(thetas0[:150]-theta_des[0]))
    v0 = int(VLUT0[ndx0])
    ndx1 = np.argmin(np.abs(thetas1[:150]-theta_des[1]))
    v1 = int(VLUT1[ndx1])
    ndx2 = np.argmin(np.abs(thetas2[:150]-theta_des[2]))
    v2 = int(VLUT2[ndx2])
    
    v0_str.set(str(v0))
    v1_str.set(str(v1))
    v2_str.set(str(v2))
    
    ##step 4: apply these voltages to the polarization controller, and check the SOP
    ##SLOWLY INCRASE THE VOLTAGES TO THE PC SO THAT WE CAN MEASURE THE SWEEP AND
    #COMPARE WITH THE DESIRED SWEEP FOR DEBUGGING
    V0 = np.arange(0,v0,20)
    V1 = np.arange(0,v1,20)
    V2 = np.arange(0,v2,20)

    for i in V0:
        PC0.write(0,i)
        time.sleep(0.001)
        SOP = analyzer.SCPIQuery(":POL:SOP?")
        #SOP = '1,0.97,0.07,0.01'
        SOP = SOP.split(',')
        S1.append(float(SOP[1])/float(SOP[0]))
        S2.append(float(SOP[2])/float(SOP[0]))
        S3.append(float(SOP[3])/float(SOP[0])) 


    for i in V1:
        PC0.write(1,i)
        time.sleep(0.001)
        SOP = analyzer.SCPIQuery(":POL:SOP?")
        #SOP = '1,0.97,0.07,0.01'
        SOP = SOP.split(',')
        S1.append(float(SOP[1])/float(SOP[0]))
        S2.append(float(SOP[2])/float(SOP[0]))
        S3.append(float(SOP[3])/float(SOP[0]))      
    
    for i in V2:
        PC0.write(2,i)
        time.sleep(0.001)
        SOP = analyzer.SCPIQuery(":POL:SOP?")
        #SOP = '1,0.97,0.07,0.01'
        SOP = SOP.split(',')
        S1.append(float(SOP[1])/float(SOP[0]))
        S2.append(float(SOP[2])/float(SOP[0]))
        S3.append(float(SOP[3])/float(SOP[0]))
        
    S1_str.set(str(S1[-1]))
    S2_str.set(str(S2[-1]))
    S3_str.set(str(S3[-1]))
    #update the plots
    plot(S1,S2,S3,master,canvas_act,line_act)
    
    arc0 = get_arc(theta_des[0],0,[S1[0],S2[0],S3[0]],u1,u2,u3,u4)
    arc1 = get_arc(theta_des[1],1,arc0[:,-1],u1,u2,u3,u4)
    arc2 = get_arc(theta_des[2],2,arc1[:,-1],u1,u2,u3,u4)
    
    
    S1d_str.set(str(arc2[0,-1]))
    S2d_str.set(str(arc2[1,-1]))
    S3d_str.set(str(arc2[2,-1]))
    
    plot(arc0[0],arc0[1],arc0[2],master,canvas_des,line_des0)
    plot(arc1[0],arc1[1],arc1[2],master,canvas_des,line_des1)
    plot(arc2[0],arc2[1],arc2[2],master,canvas_des,line_des2)
    '''
    R = np.matrix(get_polarization_rotation_matrix(theta_des,u1,u2,u3,u4))
    sf = R * np.matrix([S1[0],S2[0],S3[0]]).T
    plot(sf[0],sf[1],sf[2],master,canvas_des,line_full_rotation)
    '''

#get the actual initial polarization from the pol analyzer
SOP = analyzer.SCPIQuery(":POL:SOP?")
#SOP = '1,0.02,.97,0.05'
SOP = SOP.split(',')
S1 = float(SOP[1])/float(SOP[0])
S2 = float(SOP[2])/float(SOP[0])
S3 = float(SOP[3])/float(SOP[0])

#create the GUI
master = Tkinter.Tk()

Tkinter.Label(master,text='Desired State of Polarization').grid(row = 0,column=0)
Tkinter.Label(master,text='Applied Voltage').grid(row = 2,column=0)
Tkinter.Label(master,text='Actual SOP').grid(row = 4,column=0)
Tkinter.Label(master,text='Desired SOP').grid(row = 6,column=0)

des_box0 = Tkinter.Entry(master)
des_box0.grid(row=1,column=0)
des_box1 = Tkinter.Entry(master)
des_box1.grid(row=1,column=1)
des_box2 = Tkinter.Entry(master)
des_box2.grid(row=1,column=2)


v0_str = Tkinter.StringVar()
v1_str = Tkinter.StringVar()
v2_str = Tkinter.StringVar()

v0_str.set(str(0))
v1_str.set(str(0))
v2_str.set(str(0))

S1_str = Tkinter.StringVar()
S2_str = Tkinter.StringVar()
S3_str = Tkinter.StringVar()

S1_str.set(str(S1))
S2_str.set(str(S2))
S3_str.set(str(S3))

S1d_str = Tkinter.StringVar()
S2d_str = Tkinter.StringVar()
S3d_str = Tkinter.StringVar()

S1d_str.set(str(S1))
S2d_str.set(str(S2))
S3d_str.set(str(S3))

Tkinter.Label(master,textvariable=v0_str).grid(row=3,column=0)
Tkinter.Label(master,textvariable=v1_str).grid(row=3,column=1)
Tkinter.Label(master,textvariable=v2_str).grid(row=3,column=2)


Tkinter.Label(master,textvariable=S1_str).grid(row=5,column=0)
Tkinter.Label(master,textvariable=S2_str).grid(row=5,column=1)
Tkinter.Label(master,textvariable=S3_str).grid(row=5,column=2)

Tkinter.Label(master,textvariable=S1d_str).grid(row=7,column=0)
Tkinter.Label(master,textvariable=S2d_str).grid(row=7,column=1)
Tkinter.Label(master,textvariable=S3d_str).grid(row=7,column=2)


button = Tkinter.Button(master,text='GO',command=go).grid(row=8,column=0,pady=4)
Tkinter.Button(master, text='Quit', command=master.destroy).grid(row=8, column=1, pady=4)

#create the figure for plotting actual S parameters
fig_act = Figure(figsize=(6,6))
#fig_act = plt.figure()
ax_act = fig_act.add_subplot(111,projection='3d')
ax_act.mouse_init()
line_act,=ax_act.plot([S1],[S2],S3,'bo',markerfacecolor='b')
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
ax_act.plot([0,u1[0]],[0,u1[1]],[0,u1[2]],'c')
ax_act.plot([0,u2[0]],[0,u2[1]],[0,u2[2]],'m')
ax_act.plot([0,u3[0]],[0,u3[1]],[0,u3[2]],'g')
#put on tkinter
canvas_act = FigureCanvasTkAgg(fig_act,master=master)
canvas_act.get_tk_widget().grid(row=0,column=5,columnspan=5,rowspan=6,padx=5,pady=5)
canvas_act.draw()    

#create the figure for plotting desired S parameters
fig_des = Figure(figsize=(6,6))
ax_des = fig_des.add_subplot(111,projection='3d')
line_des0,=ax_des.plot([S1],[S2],S3,'ro',markerfacecolor='g')
line_des1,=ax_des.plot([S1],[S2],S3,'ro',markerfacecolor='orange')
line_des2,=ax_des.plot([S1],[S2],S3,'ro',markerfacecolor='r')
#line_full_rotation,=ax_des.plot([S1],[S2],S3,'ro',markerfacecolor='k')
ax_des.set_title('desired SOP',fontsize=20)
#plot spherical grid
ax_des.plot_wireframe(x, y, z, color="lightgray")
ax_des.set_xlabel('S1',fontsize=16)
ax_des.set_ylabel('S2',fontsize=16)
ax_des.set_zlabel('S3',fontsize=16)

ax_des.plot([0,u1[0]],[0,u1[1]],[0,u1[2]],'c')
ax_des.plot([0,u2[0]],[0,u2[1]],[0,u2[2]],'m')
ax_des.plot([0,u3[0]],[0,u3[1]],[0,u3[2]],'g')
#put on tkinter
canvas_des = FigureCanvasTkAgg(fig_des,master=master)
canvas_des.get_tk_widget().grid(row=0,column=11,columnspan=5,rowspan=6,padx=5,pady=5)
canvas_des.draw()    


#run the gui
Tkinter.mainloop()