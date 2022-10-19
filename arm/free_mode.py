#!/usr/bin/env python
#coding: utf-8

import b3mCtrl
import time
    
aaa = b3mCtrl.B3mClass()
aaa.begin("/dev/ttyUSB0",1500000)
    
   
print("enter FREE MODE")
input()
print (aaa.setMode(255,"FREE"))