# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 17:38:47 2017

@author: lab
"""

import numpy as np
import PolarizationControllerDIO
import time
import win32com.client

def sweepPolarizationController(fname):
    #initialize the polarization analyzer Agilent N7788B
    device = win32com.client.Dispatch("AgServerN778xLib.AgN778x")
    device.Initialize("GPIB0::30::INSTR",0,0)
    
    
    PC = PolarizationControllerDIO.PolarizationController(0)
    Vmin = 0
    Vmax = 2000
    Vstep = 10
    
    Vvec = np.arange(Vmin,Vmax,Vstep)
    Vvec=np.append(Vvec,np.arange(Vmax,0,-Vstep))
    
    foutname = fname
    
    for ch in np.arange(0,4):
        fout = open(foutname+str(ch)+'.txt','w')
        fout.write('v\tS1\tS2\tS3\n')
        for v in Vvec:
            #send signal to polarization controller
            PC.write(ch,v)
            time.sleep(0.001)
            #read in from agilent polarization analyzer
            SOP = device.SCPIQuery(":POL:SOP?")
            SOP = SOP.split(',')
            S1 = float(SOP[1])/float(SOP[0])
            S2 = float(SOP[2])/float(SOP[0])
            S3 = float(SOP[3])/float(SOP[0])
            fout.write('{:4d}\t{:05.3f}\t{:05.3f}\t{:05.3f}\n'.format(v,S1,S2,S3))
        fout.close()
        PC.write(ch,0)
        
    device.Close()
    #save to file