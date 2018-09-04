# -*- coding: utf-8 -*-
"""
Created on Mon May 21 14:22:24 2018
This is the main script that runs the polarization controller calibration and
control.

It calibrates the polarization controller using the polarization analyzer.

Then it allows the user to input a desired state of polarization (SOP), and
determines the polarization controller settings needed to obtain that SOP. 
It then applies those settings to the polarization controller, and gets the 
actual output SOP from the polarization analyzer for comparison with the 
desired result.

This last part (input, application, checking) is looped, so that the user can
repeatedly enter different SOPs and check that they work.

@author: jhart
"""
from sweepPolarizationController import sweepPolarizationController
from determine_rotation_vectors import determine_rotation_vectors
from solve_for_angles import find_optimal_rotation_angles
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
#fit theta(v) to a line, then invert
print 'get v(theta)'
p0,p1,p2,p3 = makeLUT.get_v_of_theta_fits(pol_fname,u1,u2,u3,u4)

#initialize polarization analyzer and pol controller
analyzer = win32com.client.Dispatch("AgServerN778xLib.AgN778x")
analyzer.Initialize("GPIB0::30::INSTR",0,0)
PC0 = PCDIO.PolarizationController(0)

#######THE REST OF THE CODE GOES IN THE LOOP############


def go():
    ##step 2: receive the desired output SOP from the user
    #read input from user when user clicks GO
    sf = [float(des_box0.get()),float(des_box1.get()),float(des_box2.get())]
    #determine the optimal rotation angles about v1,v2,v3,v4
    N = 10 #N is the number of random initial conditions to try in the optimizer
    thetas = find_optimal_rotation_angles((u1,u2,u3,u4),s0,sf,N)
    
    ##step 3: determine the correct voltages to apply to obtain the optimal rotation angles
    v0 = makeLUT.get_v2(thetas[0],p0)
    v1 = makeLUT.get_v2(thetas[1],p1)
    v2 = makeLUT.get_v2(thetas[2],p2)
    v3 = 0
    
    v0_str.set(str(v0))
    v1_str.set(str(v1))
    v2_str.set(str(v2))
    
    ##step 4: apply these voltages to the polarization controller, and check the SOP
    
    PC0.write(0,0)
    time.sleep(0.001)
    PC0.write(1,0)
    time.sleep(0.001)
    PC0.write(2,0)
    time.sleep(0.001)    
    
    PC0.write(0,v0)
    time.sleep(0.001)
    PC0.write(1,v1)
    time.sleep(0.001)
    PC0.write(2,v2)
    time.sleep(0.001)
    
    SOP = analyzer.SCPIQuery(":POL:SOP?")
    #SOP = '1,0.97,0.07,0.01'
    SOP = SOP.split(',')
    S1 = float(SOP[1])/float(SOP[0])
    S2 = float(SOP[2])/float(SOP[0])
    S3 = float(SOP[3])/float(SOP[0])
    S1_str.set(str(S1))
    S2_str.set(str(S2))
    S3_str.set(str(S3))
    #update the plots
    plot(S1,S2,S3,master,canvas,line)

#get the actual initial polarization from the pol analyzer
SOP = analyzer.SCPIQuery(":POL:SOP?")
#SOP = '1,0.02,.97,0.05'
SOP = SOP.split(',')
S1 = float(SOP[1])/float(SOP[0])
S2 = float(SOP[2])/float(SOP[0])
S3 = float(SOP[3])/float(SOP[0])

#create the GUI
master = Tkinter.Tk()

Tkinter.Label(master,text='Desired SOP').grid(row = 0,column=0)
Tkinter.Label(master,text='Applied Voltage').grid(row = 2,column=0)
Tkinter.Label(master,text='Actual SOP').grid(row = 4,column=0)

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

Tkinter.Label(master,textvariable=v0_str).grid(row=3,column=0)
Tkinter.Label(master,textvariable=v1_str).grid(row=3,column=1)
Tkinter.Label(master,textvariable=v2_str).grid(row=3,column=2)

Tkinter.Label(master,textvariable=S1_str).grid(row=5,column=0)
Tkinter.Label(master,textvariable=S2_str).grid(row=5,column=1)
Tkinter.Label(master,textvariable=S3_str).grid(row=5,column=2)


button = Tkinter.Button(master,text='GO',command=go).grid(row=6,column=0,pady=4)
Tkinter.Button(master, text='Quit', command=master.destroy).grid(row=6, column=1, pady=4)

#create the figure for plotting S parameters
fig = Figure(figsize=(6,6))
ax = fig.add_subplot(111,projection='3d')
line,=ax.plot([S1],[S2],S3,'bo',markerfacecolor='b')
#plot spherical grid
u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
x = np.cos(u)*np.sin(v)
y = np.sin(u)*np.sin(v)
z = np.cos(v)
ax.plot_wireframe(x, y, z, color="lightgray")
ax.set_xlabel('S1',fontsize=16)
ax.set_ylabel('S2',fontsize=16)
ax.set_zlabel('S3',fontsize=16)
#put on tkinter
canvas = FigureCanvasTkAgg(fig,master=master)
canvas.get_tk_widget().grid(row=0,column=5,columnspan=5,rowspan=6,padx=5,pady=5)
canvas.draw()    




#run the gui
Tkinter.mainloop()