# Polarization_Controller 


## Components
### General Photonics PCD-M02 Polarization Controller
The General Photonics PCD-M02 Polarization Controller is a development board that has included the Polarite III (in our case, with 4 piezoelectric transducers) and the necessary electronics to drive each of the piezoelectric transducers. There are two different ways to interface with the board: an analog interface and a 20-pin digital interface. The set-up described here uses the digital interface. 

### Measurement Computing USB DIO24 Digital IO Board
The Measurement Computing USB DIO24 Digital IO Board is a board that takes a USB input and converts it to a 24 pin digital output. The set-up described here uses this device to control the General Photonics PCD-M02 Polarization Controller from a PC. This interface is implemented in PolarizationControllerDIO.py.

### Agilent N7788B Polarization Analyzer
The Agilent N7788B Polarization Analyzer is used to calibrate the General Photonics PCD-M02 Polarization Controller. The PC communicates with the polarization analyzer via GPIB. Dependencies include Agilent's Photonic Application Suite. An example of how to communicate with the analyzer can be found in sweepPolarizationController.py.

## Software
**PolarizationControllerDIO.py**
This python file contains a class called PolarizationController. 

The class has two methods: write and read.

The first method is
```
write(self, channel, value)
```
*channel* is an integer from 0 to 3 that tells which of the 4 piezoelectric transducers you would like to write to. *value* is an integer between 0 and 2^12-1 that tells the polarization controller how much voltage to apply to the chosen piezoelectric transducer.

The second method is 
```
read(self,channel)
```
*channel* is an integer from 0 to 3 that tells which of the 4 piezoelectric transducers you would like to read the current value of.

**sweepPolarizationController.py**
```
sweepPolarizationController(fname)
```
This function sweeps the voltages applied to the piezoelectric transducers of the polarization controller one at a time, and records the output state of polarization from the polarization analyzer. The digital voltage value of 0 is applied to the 3 piezoelectric transducers that are fixed, while the other is swept. The sweep is controlled by the internal variables *Vmin*, *Vmax*, and *Vstep*. The results of the polarization measurements are written to a text file whose title is given by the input *fname*. These measurements are the basis of the calibration of the polarization controller, as discussed below.

**get_theta_from_s.py**
This file contains 3 python functions that are used internally in other functions described above. The main function is
```
vs,thetas,rot_vec = get_theta_of_v(fname,rot_vec)
```
*get_theta_of_v* reads in the data from *sweepPolarizationController* described above stored in *fname*. It then determines *theta*(*v*) by iterating through all the voltages applied to the piezoelectric transducer and determining the angle of rotation *theta* on the Poincare sphere about the axis of rotation *rot_vec* caused by the application of that voltage. The voltages are returned as *vs*, the angles are returned as *thetas*, and the *rot_vec* is returned because this function will invert the input *rot_vec* so that all angles *theta* are positive/counterclockwise.

```
theta = get_theta_from_s(rot_vec,s0,sf,N)
```
*get_theta_from_s* is a helper function used by *get_theta_of_v*. It finds the rotation angle *theta* that describes the rotation on the Poincare sphere from *s0* to *sf* about the axis of rotation *rot_vec*. It uses Newton's method to find the roots of R(sf-s0), where *R* is the rotation matrix about the axis of rotation *rot_vec*. Because Newton's method is initial condition dependent and can get stuck at an undesired root it performs the calculation *N* times from different random initial conditions and selects the root with smallest absolute value.

```
y = f2(theta,*vecs)
```
is a helper function used by *get_theta_from_s*. It is the function that we find the roots of: R*s0-sf. *vecs* = [*rot_vec*,*s0*,*sf*].

**determine_rotation_vectors.py**
```
u1,u2,u3,u4,s0 = determine_rotation_vectors(fname)
```
This function reads in the polarization sweep data from *fname* and returns the axis of rotation (*u1,*u2*,*u3*,*u4*) on Poincare sphere of each of the piezoelectric transducers of the polarization controller. Also returns the initial condition *s0*, which is the position of the SOP on Poincare sphere when the digital voltage applied to each of the transducers is 0.

#### Dependencies
##### mcculw
The mcculw package contains an API (Application Programming Interface) for interacting with the I/O Library for Measurement Computing Data Acquisition products, Universal Library. It can be obtained for free by typing in the command line 
```
pip install mcculw
```

##### win32com
The win32com python package allows python to communicate with the COM port on a Windows machine. This port is used to communicate with the Agilent N7788B Polarization Analyzer via GPIB. 


