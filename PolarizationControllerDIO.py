# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 17:23:06 2017

@author: joe
"""

from mcculw import ul
from mcculw.enums import DigitalIODirection
from props.digital import DigitalProps

class PolarizationController(object):
    def __init__(self,boardnum):
        #number the pins
        #numbering on the physical board goes like this:
        #pins 0-7 are port A
        #pins 8-15 are port B
        #pins 16-23 are port C
        #for physical pin layout, see USB-DIO24/37 manual
        self.RW_Pin=12
        self.CS_Pin=11
        self.RESET_Pin=10
        self.Control_Pins=[8,9]
        self.DB_Pins=[0,1,2,3,4,5,6,7,16,17,18,19]
        
        #current values of each channel
        self.DB_values=[0,0,0,0]
        
        #initialize the DIO board
        #ignore instacal because it does magic and i don't like magic
        ul.ignore_instacal()
        #see what devices are available
        x=ul.get_daq_device_inventory(1)
        #assign a board number
        self.board_num = boardnum
        #activate the DIO board
        ul.create_daq_device(self.board_num,x[0])
        #get info that we need about the board/ports
        dig_props = DigitalProps(self.board_num)
        self.port = dig_props.port_info
        #activate the output pins that we'll need
        #there are 4 ports for this device
        #port 0 and 1 are 8 bits each
        #ports 2 and 3 are 4 bits each
        ul.d_config_port(self.board_num, self.port[0].type, DigitalIODirection.OUT)
        ul.d_config_port(self.board_num, self.port[1].type, DigitalIODirection.OUT)
        ul.d_config_port(self.board_num, self.port[2].type, DigitalIODirection.OUT)
        
        
        
        #set all channels to 0 upon initialization
        self.write(0,0)
        self.write(1,0)
        self.write(2,0)
        self.write(3,0)
        
    def write(self,channel,value):
        #channel is 0,1,2,3 for the 4 piezoelectric wave plates
        #value is an integer between 0 and 2^12-1
        
        #convert channel to binary and store as Control1 and Control2
        ch_str="{0:02b}".format(channel)
        #convert value to binary and store as DB#
        val_str="{0:012b}".format(value)
        
        control_vec=[]
        value_vec=[]
        for bit in ch_str:
            control_vec.append(int(bit))
        for bit in val_str:
            value_vec.append(int(bit))
        
        #write to DIO pins
        #write control pins
        cnt = 0
        for pin in self.Control_Pins:
            ul.d_bit_out(self.board_num,self.port[0].type,pin,control_vec[cnt])
            cnt += 1
        #write DB pins
        cnt = 0
        for pin in self.DB_Pins:
            ul.d_bit_out(self.board_num,self.port[0].type,pin,value_vec[cnt])
            cnt += 1
        #write RW pins
        ul.d_bit_out(self.board_num,self.port[0].type,self.RW_Pin,0)

        #ul.d_out(self.board_num, self.port[0].type, portA_value)

        #do write sequence
        ul.d_bit_out(self.board_num,self.port[0].type,self.CS_Pin,0)
        #time.sleep(0.0001)#pause for 10 micro seconds
        ul.d_bit_out(self.board_num,self.port[0].type,self.CS_Pin,1)
        ul.d_bit_out(self.board_num,self.port[0].type,self.RW_Pin,1)
        
        #save value
        self.DB_values[channel]=value
        
    def read(self,channel):
        return self.DB_values[channel]
        
    def __del__(self):
        ul.release_daq_device(self.board_num)

    


