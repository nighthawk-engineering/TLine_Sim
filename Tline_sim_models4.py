# -*- coding: utf-8 -*-
"""
Created on Fri Jun 15 14:32:28 2018

@author: mlgkschm
"""

from Tline_model4 import Parms,copy

#####################################################################
# C = type('C', (object,), {})
def Base():
    # DO NOT CHANGE THIS MODEL
    model = Parms
    #
    # values from VSp1R50_T50_VT0R50_1
    model.name = 'Base'
    model.animation = True
    model.movie = False
    model.movie_fname = model.name+'.mp4'
    model.note = None
    #
    model.clock_period = 0.01
    model.stop_time = 10
    #
    # scope probe list. 
    # 0 is first node, transmitter. -1 is last node, receiver.
    # 'None' for no nodes probed. 'All' for all nodes probed
    #model.probes = 'all'
    #model.probes = None
    model.probes = [0, -1]
    #
    Tparms = []
    T = Parms  # clever empty class, used like a struct var
    # create a list of transmission lines via their parameters
    T.Z = 50; T.G = 0.1; T.L = 20; Tparms.append(copy(T))
    model.Tparms = Tparms
    #model.TlSnaps = [0, 1, 2]  # List of tlines to snapshot
    model.TlSnaps = 'all'  # 'all' for all
    #
    # Source models
    model.Zsrc = 50  # source impedance
    model.Vstep = 1  # source voltage, max
    model.delay = 0.1  # delay before generating step
    model.risetime = 0.1  # risetime of step
    model.Pattern = '1'  # bit pattern to generate. '1' generates a step fnctn
    model.Baud = 1  # bit pattern baud rate
    
    #
    # Terminatoin models
    model.Zterm = 50  # terminated load
    model.Vterm = 0  # termination voltage
    model.Trise = 0.1  # for Vterm != 0, rise time from V=0
    #
    model.figwidth = None  # animation figure width
    model.figheight = None  # animation figure height
    model.suptitle = 'on'  # animation super-title on/off
    #
    return model

#####################################################################
def VSp1R50_T50_VT0R50_1():
    model = copy(Base())
    #
    model.name = 'VSp1R50_T50_VT0R50_1'
    model.movie_fname = model.name+'.mp4'
    #
    model.stop_time = 5
    #
    return model

def VSp1R50_T50_VT0R0_1():
    model = copy(VSp1R50_T50_VT0R50_1())
    #
    model.name = 'VSp1R50_T50_VT0R0_1'
    model.movie_fname = model.name+'.mp4'
    #
    model.Zterm = 0  # shorted load
    #
    model.stop_time = 5
    #
    return model

def VSp1R50_T50_VT0Rinf_1():
    model = copy(VSp1R50_T50_VT0R50_1())
    #
    model.name = 'VSp1R50_T50_VT0Rinf_1'
    model.movie_fname = model.name+'.mp4'
    #
    model.Zterm = 50e12  # open load
    #
    model.stop_time = 5
    #
    return model

#####################################################################
def VSp1R50_T50T150_VT0R150_1():
    model = copy(Base())
    #
    model.name = 'VSp1R50_T50T150_VT0R150_1'
    model.movie_fname = model.name+'.mp4'
    #
    #model.clock_period = 0.01
    model.stop_time = 30
    #
    # scope probe list. 
    # 0 is first node, transmitter. -1 is last node, receiver.
    # 'None' for no nodes probed. 'All' for all nodes probed
    #model.probes = 'all'
    #model.probes = None
    #model.probes = [0, -1]
    #
    Tparms = []
    T = Parms  # clever empty class, used like a struct var
    # create a list of transmission lines via their parameters
    T.Z = 50; T.G = 0.1; T.L = 20; Tparms.append(copy(T))
    T.Z = 150; T.G = 0.1; T.L = 20; Tparms.append(copy(T))
    model.Tparms = Tparms
    #
    #model.Zsrc = 50
    #model.Vstep = 1
    #model.delay = 0.1
    #model.risetime = 0.1
    #model.Pattern = '1'
    #model.Baud = 1
    #
    model.Zterm = 150
    #model.Vterm = 0
    #model.Trise = 0.1
    #
    return model

#####################################################################
def VSp1R50_T50T150T50_VT0R50_1():
    model = copy(Base())
    #
    model.name = 'VSp1R50_T50T150T50_VT0R50_1'
    model.movie_fname = model.name+'.mp4'
    #
    #model.clock_period = 0.01
    model.stop_time = 30
    #
    # scope probe list. 
    # 0 is first node, transmitter. -1 is last node, receiver.
    # 'None' for no nodes probed. 'All' for all nodes probed
    #model.probes = 'all'
    #model.probes = None
    #model.probes = [0, -1]
    #
    Tparms = []
    T = Parms  # clever empty class, used like a struct var
    # create a list of transmission lines via their parameters
    T.Z = 50; T.G = 0.1; T.L = 20; Tparms.append(copy(T))
    T.Z = 150; T.G = 0.1; T.L = 20; Tparms.append(copy(T))
    T.Z = 50; T.G = 0.1; T.L = 20; Tparms.append(copy(T))
    model.Tparms = Tparms
    #
    #model.Zsrc = 50
    #model.Vstep = 1
    #model.delay = 0.1
    #model.risetime = 0.1
    #model.Pattern = '1'
    #model.Baud = 1
    #
    #model.Zterm = 50
    #model.Vterm = 0
    #model.Trise = 0.1
    #
    return model

def VSp1R50_T50T150T50_VT0R50_2():
    model = copy(VSp1R50_T50T150T50_VT0R50_1())
    #
    model.name = 'VSp1R50_T50T150T50_VT0R50_2'
    model.movie_fname = model.name+'.mp4'
    #
    #model.clock_period = 0.01
    #model.stop_time = 30
    #
    # scope probe list. 
    # 0 is first node, transmitter. -1 is last node, receiver.
    # 'None' for no nodes probed. 'All' for all nodes probed
    #model.probes = 'all'
    #model.probes = None
    #model.probes = [0, -1]
    #
    Tparms = []
    T = Parms  # clever empty class, used like a struct var
    # create a list of transmission lines via their parameters
    T.Z = 50; T.G = 0.1; T.L = 33; Tparms.append(copy(T))
    T.Z = 150; T.G = 0.1; T.L = 10; Tparms.append(copy(T))
    T.Z = 50; T.G = 0.1; T.L = 33; Tparms.append(copy(T))
    model.Tparms = Tparms
    #
    #model.Zsrc = 50
    #model.Vstep = 1
    #model.delay = 0.1
    #model.risetime = 0.1
    #model.Pattern = '1'
    #model.Baud = 1
    #
    #model.Zterm = 50
    #model.Vterm = 0
    #model.Trise = 0.1
    #
    return model

def VSp1R50_T50T150T50_VT0R50_3():
    model = copy(VSp1R50_T50T150T50_VT0R50_1())
    #
    model.name = 'VSp1R50_T50T150T50_VT0R50_3'
    model.movie_fname = model.name+'.mp4'
    #
    #model.clock_period = 0.01
    #model.stop_time = 30
    #
    # scope probe list. 
    # 0 is first node, transmitter. -1 is last node, receiver.
    # 'None' for no nodes probed. 'All' for all nodes probed
    #model.probes = 'all'
    #model.probes = None
    #model.probes = [0, -1]
    #
    Tparms = []
    T = Parms  # clever empty class, used like a struct var
    # create a list of transmission lines via their parameters
    T.Z = 50; T.G = 0.1; T.L = 40; Tparms.append(copy(T))
    T.Z = 150; T.G = 0.1; T.L = 2; Tparms.append(copy(T))
    T.Z = 50; T.G = 0.1; T.L = 40; Tparms.append(copy(T))
    model.Tparms = Tparms
    #
    #model.Zsrc = 50
    #model.Vstep = 1
    #model.delay = 0.1
    model.risetime = 1
    #model.Pattern = '1'
    #model.Baud = 1
    #
    #model.Zterm = 50
    #model.Vterm = 0
    #model.Trise = 0.1
    #
    return model

def VSp1R75_T50T150T50_VT0R75_1():
    model = copy(VSp1R50_T50T150T50_VT0R50_1())
    #
    model.name = 'VSp1R75_T50T150T50_VT0R75_1'
    model.movie_fname = model.name+'.mp4'
    #
    model.Zsrc = 75
    model.Zterm = 75
    #
    return model

def VSp1R75_T50T150T50_VTn1R75_1():
    model = copy(VSp1R75_T50T150T50_VT0R75_1())
    #
    model.name = 'VSp1R75_T50T150T50_VTn1R75_1'
    model.movie_fname = model.name+'.mp4'
    #
    model.Vterm = -1
    #
    return model

#####################################################################
def VSp1R50_T50T150T50T150_VT0R150_1():
    model = copy(Base())
    #
    model.name = 'VSp1R50_T50T150T50T150_VT0R150_1'
    model.movie_fname = model.name+'.mp4'
    #
    #model.clock_period = 0.01
    model.stop_time = 40
    #
    # scope probe list. 
    # 0 is first node, transmitter. -1 is last node, receiver.
    # 'None' for no nodes probed. 'All' for all nodes probed
    #model.probes = 'all'
    model.probes = None
    #model.probes = [0, -1]
    #
    Tparms = []
    T = Parms  # clever empty class, used like a struct var
    # create a list of transmission lines via their parameters
    T.Z = 50; T.G = 0.1; T.L = 60; Tparms.append(copy(T))
    T.Z = 150; T.G = 0.1; T.L = 17; Tparms.append(copy(T))
    T.Z = 50; T.G = 0.1; T.L = 23; Tparms.append(copy(T))
    T.Z = 150; T.G = 0.1; T.L = 60; Tparms.append(copy(T))
    model.Tparms = Tparms
    #
    #model.Zsrc = 50
    #model.Vstep = 1
    #model.delay = 0.1
    #model.risetime = 0.1
    #model.Pattern = '1'
    #model.Baud = 1
    #
    model.Zterm = 150
    #model.Vterm = 0
    #model.Trise = 0.1
    #
    return model

#####################################################################
def VSp1R75_T50T150_VT0R75_1():
    model = copy(Base())
    #
    model.name = 'VSp1R75_T50T150_VT0R75_1'
    model.movie_fname = model.name+'.mp4'
    #
    #model.clock_period = 0.01
    model.stop_time = 30
    #
    # scope probe list. 
    # 0 is first node, transmitter. -1 is last node, receiver.
    # 'None' for no nodes probed. 'All' for all nodes probed
    #model.probes = 'all'
    #model.probes = None
    #model.probes = [0, -1]
    #
    model.Tparms = []
    T = Parms  # clever empty class, used like a struct var
    # create a list of transmission lines via their parameters
    T.Z = 50; T.G = 0.1; T.L = 20; model.Tparms.append(copy(T))
    T.Z = 150; T.G = 0.1; T.L = 20; model.Tparms.append(copy(T))
    #model.Tparms = Tparms
    #
    model.Zsrc = 75
    #model.Vstep = 1
    #model.delay = 0.1
    #model.risetime = 0.1
    #model.Pattern = '1'
    #model.Baud = 1
    #
    model.Zterm = 75
    #model.Vterm = 0
    #model.Trise = 0.1
    #
    return model

#####################################################################
def VSp1R50_T150T75T125T25_VT0R50_1():
    model = copy(Base())
    #
    model.name = 'VSp1R50_T150T75T125T25_VT0R50_1'
    model.movie_fname = model.name+'.mp4'
    #
    #model.clock_period = 0.01
    model.stop_time = 100
    #
    # scope probe list. 
    # 0 is first node, transmitter. -1 is last node, receiver.
    # 'None' for no nodes probed. 'All' for all nodes probed
    #model.probes = 'all'
    #model.probes = None
    #model.probes = [0, -1]
    #
    Tparms = []
    T = Parms  # clever empty class, used like a struct var
    # create a list of transmission lines via their parameters
    T.Z = 150; T.G = 0.1; T.L = 50; Tparms.append(copy(T))
    T.Z = 75; T.G = 0.1; T.L = 33; Tparms.append(copy(T))
    T.Z = 125; T.G = 0.1; T.L = 25; Tparms.append(copy(T))
    T.Z = 25; T.G = 0.1; T.L = 20; Tparms.append(copy(T))
    model.Tparms = Tparms
    #
    #model.Zsrc = 50
    #model.Vstep = 1
    #model.delay = 0.1
    #model.risetime = 0.1
    #model.Pattern = '1'
    #model.Baud = 1
    #
    #model.Zterm = 50
    #model.Vterm = 0
    #model.Trise = 0.1
    #
    return model

#####################################################################
def VSp1R50_T50T55T45T55_VT0R50_1():
    model = copy(Base())
    #
    model.name = 'VSp1R50_T50T55T45T55_VT0R50_1'
    model.movie_fname = model.name+'.mp4'
    #
    #model.clock_period = 0.01
    model.stop_time = 50
    #
    # scope probe list. 
    # 0 is first node, transmitter. -1 is last node, receiver.
    # 'None' for no nodes probed. 'All' for all nodes probed
    #model.probes = 'all'
    #model.probes = None
    #model.probes = [0, -1]
    #
    Tparms = []
    T = Parms  # clever empty class, used like a struct var
    # create a list of transmission lines via their parameters
    T.Z = 50; T.G = 0.1; T.L = 50; Tparms.append(copy(T))
    T.Z = 55; T.G = 0.1; T.L = 33; Tparms.append(copy(T))
    T.Z = 45; T.G = 0.1; T.L = 25; Tparms.append(copy(T))
    T.Z = 55; T.G = 0.1; T.L = 20; Tparms.append(copy(T))
    model.Tparms = Tparms
    #
    #model.Zsrc = 50
    #model.Vstep = 1
    #model.delay = 0.1
    #model.risetime = 0.1
    #model.Pattern = '1'
    #model.Baud = 1
    #
    #model.Zterm = 50
    #model.Vterm = 0
    #model.Trise = 0.1
    #
    return model

#####################################################################
# SI Basic demo models
def VSp2R50_T50_VT0R50_1():
    model = copy(VSp1R50_T50_VT0R50_1())
    #
    model.name = 'VSp2R50_T50_VT0R50_1'
    model.movie_fname = model.name+'.mp4'
    #
    model.risetime = 0.1
    model.stop_time = 2.5
    #
    model.Vstep = 2
    model.probes = None
    model.suptitle = 'off'
    #
    return model

def VSp2R50_T50_VT0R50_2():
    model = copy(VSp2R50_T50_VT0R50_1())
    #
    model.name = 'VSp2R50_T50_VT0R50_2'
    model.movie_fname = model.name+'.mp4'
    #
    model.risetime = 1
    model.stop_time = 4.2
    #
    return model

def VSp2R50_T50_VT0R50_3():
    model = copy(VSp2R50_T50_VT0R50_1())
    #
    model.name = 'VSp2R50_T50_VT0R50_3'
    model.movie_fname = model.name+'.mp4'
    #
    model.risetime = 10
    model.stop_time = 22
    #
    return model

#####################################################################
def VSp2R50_T50T150T50_VT0R50_TL20_1():
    model = copy(VSp1R50_T50T150T50_VT0R50_3())
    #
    model.name = 'VSp2R50_T50T150T50_VT0R50_TL20_1'
    model.movie_fname = model.name+'.mp4'
    #
    Tparms = []
    T = Parms  # clever empty class, used like a struct var
    # create a list of transmission lines via their parameters
    T.Z = 50; T.G = 0.1; T.L = 20; Tparms.append(copy(T))
    T.Z = 150; T.G = 0.1; T.L = 2; Tparms.append(copy(T))
    T.Z = 50; T.G = 0.1; T.L = 20; Tparms.append(copy(T))
    model.Tparms = Tparms
    #
    model.Vstep = 2
    model.risetime = 0.1
    model.stop_time = 7
    #
    return model

def VSp2R50_T50T150T50_VT0R50_TL30_1():
    model = copy(VSp2R50_T50T150T50_VT0R50_TL20_1())
    #
    model.name = 'VSp2R50_T50T150T50_VT0R50_TL30_1'
    model.movie_fname = model.name+'.mp4'
    #
    Tparms = []
    T = Parms  # clever empty class, used like a struct var
    # create a list of transmission lines via their parameters
    T.Z = 50; T.G = 0.1; T.L = 30; Tparms.append(copy(T))
    T.Z = 150; T.G = 0.1; T.L = 2; Tparms.append(copy(T))
    T.Z = 50; T.G = 0.1; T.L = 30; Tparms.append(copy(T))
    model.Tparms = Tparms
    #
    #model.Vstep = 2
    model.risetime = 0.6
    model.stop_time = 9
    #
    return model

def VSp2R50_T50T150T50_VT0R50_TL40_1():
    model = copy(VSp2R50_T50T150T50_VT0R50_TL20_1())
    #
    model.name = 'VSp2R50_T50T150T50_VT0R50_TL40_1'
    model.movie_fname = model.name+'.mp4'
    #
    Tparms = []
    T = Parms  # clever empty class, used like a struct var
    # create a list of transmission lines via their parameters
    T.Z = 50; T.G = 0.1; T.L = 40; Tparms.append(copy(T))
    T.Z = 150; T.G = 0.1; T.L = 2; Tparms.append(copy(T))
    T.Z = 50; T.G = 0.1; T.L = 40; Tparms.append(copy(T))
    model.Tparms = Tparms
    #
    #model.Vstep = 2
    model.risetime = 1.2
    model.stop_time = 12
    #
    return model

#####################################################################
#####################################################################
Model_List = {
        'Base': Base,
        'VSp1R50_T50_VT0R50_1': VSp1R50_T50_VT0R50_1,
        'VSp1R50_T50_VT0R0_1': VSp1R50_T50_VT0R0_1,
        'VSp1R50_T50_VT0Rinf_1': VSp1R50_T50_VT0Rinf_1,
        'VSp1R50_T50T150_VT0R150_1': VSp1R50_T50T150_VT0R150_1,
        'VSp1R50_T50T150T50_VT0R50_1': VSp1R50_T50T150T50_VT0R50_1,
        'VSp1R50_T50T150T50_VT0R50_2': VSp1R50_T50T150T50_VT0R50_2,
        'VSp1R50_T50T150T50_VT0R50_3': VSp1R50_T50T150T50_VT0R50_3,
        'VSp1R75_T50T150T50_VT0R75_1': VSp1R75_T50T150T50_VT0R75_1,
        'VSp1R75_T50T150T50_VTn1R75_1': VSp1R75_T50T150T50_VTn1R75_1,
        'VSp1R75_T50T150_VT0R75_1': VSp1R75_T50T150_VT0R75_1,
        'VSp1R50_T150T75T125T25_VT0R50_1': VSp1R50_T150T75T125T25_VT0R50_1,
        'VSp1R50_T50T55T45T55_VT0R50_1': VSp1R50_T50T55T45T55_VT0R50_1,
        'VSp2R50_T50_VT0R50_1': VSp2R50_T50_VT0R50_1,
        'VSp2R50_T50_VT0R50_2': VSp2R50_T50_VT0R50_2,
        'VSp2R50_T50_VT0R50_3': VSp2R50_T50_VT0R50_3,
        'VSp1R50_T50T150T50T150_VT0R150_1': VSp1R50_T50T150T50T150_VT0R150_1,
        'VSp2R50_T50T150T50_VT0R50_TL20_1': VSp2R50_T50T150T50_VT0R50_TL20_1,
        'VSp2R50_T50T150T50_VT0R50_TL30_1': VSp2R50_T50T150T50_VT0R50_TL30_1,
        'VSp2R50_T50T150T50_VT0R50_TL40_1': VSp2R50_T50T150T50_VT0R50_TL40_1,
    }
