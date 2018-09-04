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

def determine_rotation_vectors(fname):
    Ch0 = np.loadtxt(fname+'0.txt',skiprows=1)
    Ch1 = np.loadtxt(fname+'1.txt',skiprows=1)
    Ch2 = np.loadtxt(fname+'2.txt',skiprows=1)
    Ch3 = np.loadtxt(fname+'3.txt',skiprows=1)
    
    ch0_s1_max = np.max(Ch0[:,1])
    ch0_s1_min = np.min(Ch0[:,1])
    ch0_s1_center = (ch0_s1_max+ch0_s1_min)/2.
    ch0_s2_max = np.max(Ch0[:,2])
    ch0_s2_min = np.min(Ch0[:,2])
    ch0_s2_center = (ch0_s2_max+ch0_s2_min)/2.
    ch0_s3_max = np.max(Ch0[:,3])
    ch0_s3_min = np.min(Ch0[:,3])
    ch0_s3_center = (ch0_s3_max+ch0_s3_min)/2.
    u0 = np.asarray([ch0_s1_center,ch0_s2_center,ch0_s3_center])
    u0 = u0/np.linalg.norm(u0,ord=2)
    
    
    ch1_s1_max = np.max(Ch1[:,1])
    ch1_s1_min = np.min(Ch1[:,1])
    ch1_s1_center = (ch1_s1_max+ch1_s1_min)/2.
    ch1_s2_max = np.max(Ch1[:,2])
    ch1_s2_min = np.min(Ch1[:,2])
    ch1_s2_center = (ch1_s2_max+ch1_s2_min)/2.
    ch1_s3_max = np.max(Ch1[:,3])
    ch1_s3_min = np.min(Ch1[:,3])
    ch1_s3_center = (ch1_s3_max+ch1_s3_min)/2.
    u1 = np.asarray([ch1_s1_center,ch1_s2_center,ch1_s3_center])
    u1 = u1/np.linalg.norm(u1,ord=2)
    
    ch2_s1_max = np.max(Ch2[:,1])
    ch2_s1_min = np.min(Ch2[:,1])
    ch2_s1_center = (ch2_s1_max+ch2_s1_min)/2.
    ch2_s2_max = np.max(Ch2[:,2])
    ch2_s2_min = np.min(Ch2[:,2])
    ch2_s2_center = (ch2_s2_max+ch2_s2_min)/2.
    ch2_s3_max = np.max(Ch2[:,3])
    ch2_s3_min = np.min(Ch2[:,3])
    ch2_s3_center = (ch2_s3_max+ch2_s3_min)/2.
    u2 = np.asarray([ch2_s1_center,ch2_s2_center,ch2_s3_center])
    u2 = u2/np.linalg.norm(u2,ord=2)
    
    ch3_s1_max = np.max(Ch3[:,1])
    ch3_s1_min = np.min(Ch3[:,1])
    ch3_s1_center = (ch3_s1_max+ch3_s1_min)/2.
    ch3_s2_max = np.max(Ch3[:,2])
    ch3_s2_min = np.min(Ch3[:,2])
    ch3_s2_center = (ch3_s2_max+ch3_s2_min)/2.
    ch3_s3_max = np.max(Ch3[:,3])
    ch3_s3_min = np.min(Ch3[:,3])
    ch3_s3_center = (ch3_s3_max+ch3_s3_min)/2.
    u3 = np.asarray([ch3_s1_center,ch3_s2_center,ch3_s3_center])
    u3 = u3/np.linalg.norm(u3,ord=2)
    
    s0 = Ch3[-1,1:]/np.linalg.norm(Ch3[-1,1:],ord=2)    
    
    return u0,u1,u2,u3,s0