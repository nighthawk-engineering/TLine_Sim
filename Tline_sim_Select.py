# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 15:05:36 2018

@author: mlgkschm
"""

from Tline_sim_models4 import *

#####################################################################
#####################################################################
'''
The whole simulator environment is parameterized
This allows easy invocation of a library of models
'''

LibModel = None
#LibModel = VSp1R50_T50_VT0R50_1()  # Vs=50R, 1TL 50R, Vt=50R 0v
#LibModel = VSp1R50_T50_VT0R0_1()  # Vs=50R, 1TL 50R, Vt=0R 0v
#LibModel = VSp1R50_T50_VT0Rinf_1()  # Vs=50R, 1TL 50R, Vt=infR 0V
#LibModel = VSp1R50_T50T150_VT0R150_1()  # Vs=50R, 2TL 50/150, Vt=150R 0v
#LibModel = VSp1R50_T50T150T50_VT0R50_1()  # Vs=50R, 3TL 50/150/50R, Vt=50R 0v
LibModel = VSp1R50_T50T150T50_VT0R50_2()  # Vs=50R, 3TL 50/150/50R, Vt=50R 0v
#LibModel = VSp1R75_T50T150T50_VT0R75_1()  # Vs=75R, 3TL 50/150/50R, Vt=75R 0v
#LibModel = VSp1R75_T50T150T50_VTn1R75_1()  # Vs=75R, 3TL 50/150/50R, Vt=75R -1v
#LibModel = VSp1R75_T50T150_VT0R75_1()  # Vs=75R, 3TL 50/150/50R, Vt=75R 0v
#LibModel = VSp1R50_T150T75T125T25_VT0R50_1()  # Vs=50R, 4TL 150/75/125/25, Vt=50R 0v
#LibModel = VSp1R50_T50T55T45T55_VT0R50_1()  # Vs=50R, 4TL 45/55/50/55, Vt=50R 0v

LibModel.probes = '0,-1'
#LibModel.probes = 'all'
#LibModel.Pattern = '1001011'
#LibModel.Baud = 0.75
