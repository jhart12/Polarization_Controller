# Polarization_Controller 


## Components
### General Photonics PCD-M02 Polarization Controller
The General Photonics PCD-M02 Polarization Controller is a development board that has included the Polarite III (in our case, with 4 piezoelectric transducers) and the necessary electronics to drive each of the piezoelectric transducers. There are two different ways to interface with the board: an analog interface and a 20-pin digital interface. The set-up described here uses the digital interface. 

### Measurement Computing USB DIO24 Digital IO Board
The Measurement Computing USB DIO24 Digital IO Board is a board that takes a USB input and converts it to a 24 pin digital output. The set-up described here uses this device to control the General Photonics PCD-M02 Polarization Controller from a PC. This interface is implemented in PolarizationControllerDIO.py.

### Agilent N7788B Polarization Analyzer
The Agilent N7788B Polarization Analyzer is used to calibrate the General Photonics PCD-M02 Polarization Controller. The PC communicates with the polarization analyzer via GPIB. Dependencies include Agilent's Photonic Application Suite. An example of how to communicate with the analyzer can be found in sweepPolarizationController.py.

## Software
###
