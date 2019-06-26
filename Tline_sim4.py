# -*- coding: utf-8 -*-
"""
Created on Mon May  7 14:47:28 2018

@author: mlgkschm
"""

import sys
from getopt import getopt
from os.path import basename
import simpy
import Tline_model4 as tline
from Tline_model4 import plt_plot
from matplotlib import pyplot as plt
#
from Local import *
from Tline_sim_models4 import *

#####################################################################
#####################################################################
'''
Get any command line arguments
If command line arguments are being ignored in Windows
you'll need to add "%*" to two lines in the registry that have this value:
    "C:\Python\python.exe" "%1"
should be:
    "C:\Python\python.exe" "%1" "%*"
'''
progname = basename(sys.argv[0])
if len(sys.argv[1:])==1:
    args = sys.argv[1].split()
else:
    args = sys.argv[1:]
optlist, args = getopt(args, 'hamW:M:N:H:p:s:r:v:T:R:P:n:b:')
Opts = dict()
for opt in optlist:
    if opt[0] == '-h':
        print('%s help:'%progname)
        print('''\
Available command line arguments are:
-h           -- Print help message
-a           -- Turn OFF animation
-m           -- Make a movie file
-W <width>   -- Set animation width (default: 6.4)
-H <height>  -- Set animation height (default: 4.8)
-p <pattern> -- Use this pattern
-s <time>    -- Set stop time
-r <time>    -- Set risetime
-v <voltage> -- Set input voltage
-T <value>   -- Set TX or source impedance to value
-R <value>   -- Set RX or receiver impedance to value
-P on/off    -- Turn animation super-title on/off
-n <list>    -- List and order of Tlines to animate: '1,2,...' or 'all'
-b <list>    -- List of probes to display: '1,2,..', 'all' or 'None'
-N <text>    -- Add note <text>
-M <Name>    -- Set model to <Name>
\
''')
        exit(0)
    else:
        Opts[opt[0]] = opt[1]

#####################################################################
#####################################################################
'''
The whole simulator environment is parameterized
This allows easy invocation of a library of models
'''
# Get the model
Model = None
try:
    Model = Opts['-M']  # Model flag 'M' exists
    print('Found model flag\nLooking for model',Model)
    LibModel = Model_List[Model]()  # Model <Model> exists
    print('Found model',Model)
except KeyError:
    if defined(Model):
        print('Couldn''t find model',Model)
    from Tline_sim_Select import *

#####################################################################
#####################################################################
#####################################################################
'''
OK, let's build and simulate a model!
'''

if defined(LibModel):
    #
    animation =    LibModel.animation
    movie =        LibModel.movie
    movie_fname  = LibModel.movie_fname
    note =         LibModel.note
    clock_period = LibModel.clock_period
    stop_time =    LibModel.stop_time
    probes =       LibModel.probes
    Tparms =       LibModel.Tparms
    TlSnaps =      LibModel.TlSnaps
    Zsrc =         LibModel.Zsrc
    Vstep =        LibModel.Vstep
    delay =        LibModel.delay
    risetime =     LibModel.risetime
    Pattern =      LibModel.Pattern
    Baud =         LibModel.Baud
    Zterm =        LibModel.Zterm
    Vterm =        LibModel.Vterm
    Trise =        LibModel.Trise
    figwidth =     LibModel.figwidth
    figheight =    LibModel.figheight
    suptitle =     LibModel.suptitle
    #
    print('Using model %s from library' % LibModel.name)
else:
    print('No library model found -- using program defaults')
    #####################################################################
    #####################################################################
    #####################################################################
    # simulator features and time parameters
    animation = True
    movie = False
    movie_fname = 'tline_sim4_test.mp4'
    note = None
    
    # master clock parameters
    #clock_period = 0.001
    clock_period = 0.01
    stop_time = 30
    #stop_time = 5
    
    # scope probe list. 
    # 0 is first node, transmitter. -1 is last node, receiver.
    # 'None' for no nodes probed. 'All' for all nodes probed
    probes = [0, -1]
    #probes = 'all'
    #robes = None
    
    #####################################################################
    # transmission line parameters
    # Z in Ohms
    # G, Gamma, in time/length
    # L, Length, in length
    
    Tparms = []
    T = Parms()# clever empty class, used like a struct var
    
    # create a list of transmission lines via their parameters
    T.Z = 50; T.G = 0.1; T.L = 20; Tparms.append(T.copy())
    #T.Z = 150; T.G = 0.1; T.L = 20; Tparms.append(T.copy())
    #T.Z = 50; T.G = 0.1; T.L = 20; Tparms.append(T.copy())
    #T.Z = 50; T.G = 0.1; T.L = 20; Tparms.append(T.copy())
    #T.Z = 50; T.G = 0.1; T.L = 20; Tparms.append(T.copy())
    #T.Z = 50; T.G = 0.1; T.L = 20; Tparms.append(T.copy())
    #TlSnaps = [0, 1, 2]  # List of tlines to snapshot
    TlSnaps = 'all'  # 'all' for all
    
    #####################################################################
    # signal source parameters
    Zsrc = 50
    #Zsrc = 50
    Vstep = 1
    delay = 0.1
    risetime = 0.1  # edge rise time, (s)
    #risetime = 0.5  # edge rise time, (s)
    Pattern = '1'
    Baud = 1
    
    #####################################################################
    # termination parameters
    Zterm = 50E12
    #Zterm = 75
    #Zterm = 50
    #Zterm = 0
    #Vterm = -1
    Vterm = 0
    Trise = 0.1

#####################################################################
# Override values from command line arguments
for opt in optlist:
    if opt[0] == '-m':
        print('make movie')
        movie = True
    if opt[0] == '-a':
        print('turn OFF animation')
        animation = False
    if opt[0] == '-N':
        print('adding note %s' % opt[1])
        note = opt[1]
    if opt[0] == '-p':
        print('use pattern=%s'%opt[1])
        Pattern = opt[1]
    if opt[0] == '-W':
        print('setting animation figure width to %g'%float(opt[1]))
        figwidth = float(opt[1])
    if opt[0] == '-H':
        print('setting animation figure height to %g'%float(opt[1]))
        figheight = float(opt[1])
    if opt[0] == '-s':
        print('setting stop time to %g'%float(opt[1]))
        stop_time = float(opt[1])
    if opt[0] == '-r':
        print('setting risetime to %g'%float(opt[1]))
        risetime = float(opt[1])
    if opt[0] == '-v':
        print('setting input voltage to %g'%float(opt[1]))
        Vstep = float(opt[1])
    if opt[0] == '-T':
        print('setting TX impedance to %g'%float(opt[1]))
        Zsrc = float(opt[1])
    if opt[0] == '-R':
        print('setting RX impedance to %g'%float(opt[1]))
        Zterm = float(opt[1])
    if opt[0] == '-P':
        print('setting suptitle to %s'%opt[1])
        suptitle = opt[1]
    if opt[0] == '-n':
        print('setting animation list to %s'%opt[1])
        TlSnaps = opt[1]
    if opt[0] == '-b':
        print('setting scope list to %s'%opt[1])
        probes = opt[1]

#####################################################################
#####################################################################
#####################################################################
'''
Model creation
'''

# create the SimPy environment
env = simpy.Environment()

# create the master timing clock
clk = tline.clock(env, clock_period, unit='Mclk')

# create voltage source
Vsrc = Vstep
#src = tline.SrcStep(env, clk, Zsrc, Vsrc, delay, risetime, unit='src')
src = tline.SrcPattern(env, clk, Zsrc, Vsrc, delay, risetime, Pattern, Baud, unit='src')

# create multiple Tlines. We'll connected them later via 'Node's:
Tlines = []
for n, tl in enumerate(Tparms):
    Tlines.append(tline.Tline(env, clk, tl.Z, tl.G, tl.L, unit='tl'+str(n+1)))
    #print(n, tl.Z, Tlines[-1].unit)

# create the termination. Allow a termination voltage, Vterm
term = tline.SrcStep(env, clk, Zterm, Vterm, 0, Trise, unit='term')

# Now connect the Tlines using Node objects
Nodes = []
# Source to TL1
Nodes.append(tline.node(env, clk, src, Tlines[0].port1, unit=src.unit))
#print(0, Nodes[-1].unit)
# Tl1 to ... to TLn (no iteration if only one tline)
for n in range(len(Tlines)-1):
    Nodes.append(tline.node(env, clk, Tlines[n].port2, Tlines[n+1].port1, unit='node'+str(n+1)))
    #print(n+1, Nodes[-1].unit)
# TLn to Term
Nodes.append(tline.node(env, clk, Tlines[-1].port2, term, unit=term.unit))
#print(len(Tlines), Nodes[-1].unit)

###################################################
'''
Probe the simulation in preparation of plotting data
'''

prbs = []
#for n in range(len(Tlines)+1):
for n in range(len(Nodes)):
    prbs.append(tline.scope(env,clk,(Nodes[n],'V'), unit='V'+str(n+1)))
    #print(n, Nodes[n].unit, prbs[-1].unit)
#

if str(TlSnaps) == 'all':
    snapshots = Tlines
else:
    snapshots = []
    for n in TlSnaps.split(sep=','):
        snapshots.append(Tlines[int(n)-1])

if animation:
    prb_snaps = []
    #for n, tl in enumerate(Tlines):
    for n, tl in enumerate(snapshots):
        prb_snaps.append(tline.scope(env,clk,(tl,'snapshot'),unit=tl.unit+"_snap"))
        #print(n+1, prb_snaps[-1].unit)

#####################################################################
#####################################################################
#####################################################################
'''
Run the simulation!
'''

if stop_time == None:
    env.run()
else:
    env.run(until=stop_time)
# All done! mark end of time and finish the bq25570 state log
print('Time stop: @ %f' % env.now)

#####################################################################
#####################################################################
#####################################################################
'''
Plot the data collected by the scope probes above
'''

fontsize='x-large'

fig = plt.figure()  # 
for prb in prbs:
    plt_plot(prb)
title = 'Node Voltage Waveforms'
if int(Pattern) != 1:
    title += ' - pattern=\'%s\'' % Pattern
plt.title(title, fontsize=fontsize)
if defined(note):
    plt.text(0.5,0.1,'Note: %s'%note,ha='center')
plt.xlabel('Time (s)', fontsize=fontsize)
plt.ylabel('Voltage (V)', fontsize=fontsize)
plt.legend(fontsize=fontsize)
plt.show(block=False)
"""
"""

if probes == 'none' or probes == 'None':
    probes = None
elif probes == 'all' or probes == 'All':
    probes = range(len(Nodes))
elif isinstance(probes,type('')):
    probes = probes.split(sep=',')

if defined(probes):
    prb_nodes = []
    for n in probes:
        prb_nodes.append(prbs[int(n)])
else:
    prb_nodes = None

suptitle = not (suptitle == 'off' or suptitle == 'Off' or suptitle == 'OFF')
    
if animation:
    ani = tline.animate(prb_snaps, prb_nodes, Pattern, start=0, intv=1)
    ani.figwidth = figwidth
    ani.figheight = figheight
    ani.suptitle = suptitle
    anim = ani.gen(frames=int(stop_time/clock_period))
    if movie:
        print('Creating movie file',movie_fname)
        anim.save(movie_fname, writer=ani.Mpeg4writer(fps=30, outrate=30))

###################################################
###################################################
###################################################
'''
close the windows and shut down
'''

if not (animation and movie):
    plt.show()
