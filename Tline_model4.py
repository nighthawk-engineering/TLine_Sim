# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 09:30:40 2018

@author: mlgkschm
"""

import csv
from math import ceil, floor
from collections import deque
from warnings import warn
from matplotlib.animation import FuncAnimation, FFMpegWriter
from matplotlib import pyplot as plt
plt.rcParams['animation.ffmpeg_path'] = 'C:\\FFmpeg\\bin\\ffmpeg.exe'
#
from Local import *

##############################################################################
##############################################################################
# A master clock object
class clock:
    type = 'S'  # type = Support

    def __init__(self,env,period,unit=1):
        self.env = env
        self.period = period  # Primary clock period
        self.unit = str(unit)
        #
        self.name = 'Clock_'+self.unit
        self.Tpost = period/10  # Secondary clock delay from primary
        self.tick = None  # Primary time marker, for computing
        self.tock = None  # Secondary time marker, for post processing
        self.req = {}  # list of devices relying on 'clock'
        self.running = True
        self.env.process(self.runTick(self.period))  # start Primary
        self.env.process(self.runTock(self.period))  # start Secondary

    def runTick(self, period):
        print('Clock start: @ %f' % self.env.now)
        #
        while len(self.req) == 0:
            self.tick = self.env.process(self.step(period))
            yield self.tick
        #
        while len(self.req) > 0:
            self.tick = self.env.process(self.step(period))
            yield self.tick
        #
        print('Clock stop: @ %f' % self.env.now)
        self.running = False
        self.tick = None

    def runTock(self, period):
        self.tock = self.env.timeout(self.Tpost)  # delay from T=0
        yield self.tock
        #
        while self.running:  # then start secondary clock
            self.tock = self.env.process(self.step(period))
            yield self.tock
        #
        print('Tock stop: @ %f' % self.env.now)
        self.tock = None

    def step(self, delT):
        yield self.env.timeout(delT)

    def start(self, req):
        print('Req clock start: %s @ %f' % (req.name, self.env.now))
        self.req[req] = req.name

    def stop(self, req):
        print('Req clock stop: %s @ %f' % (req.name, self.env.now))
        del self.req[req]

##############################################################################
# An object to collect data on any node
class scope:
    type = 'S'  # type = Support

    def __init__(self, env, clock, node, unit=1):
        self.env = env
        self.clock = clock
        self.unit = str(unit)
        self.node = node
        #
        self.name = 'Scope_'+self.unit
        self.obj = node[0]
        self.obj_atr = node[1]
        self.time = []
        self.data = []
        self.env.process(self.run())

    def run(self):
        # self.clock.start(self)
        collect = True
        while collect and self.clock.running:
            yield self.clock.tock
            data = getattr(self.obj, self.obj_atr)
            collect = defined(data)
            if collect:
                self.time.append(self.env.now)
                self.data.append(data)

    @property
    def period(self):
        return(self.clock.period)


"""
##############################################################################
# Begin element descriptions
##############################################################################
# Driver, or wave source, model
"""
class SrcStep:
    type = 'R'  # type = Resistor

    def __init__(self, env, clock, Zc, Vs, Tdelay, risetime, unit=1):
        self.env = env
        self.clock = clock
        self.Zc = Zc  # source impedance
        self.Vmax = Vs  # source voltage
        self.delay = Tdelay  # start delay
        self.risetime = risetime
        self.unit = str(unit)
        #
        self.name = 'SrcStep_'+self.unit
        # Weighted average smoother for edge boundaries
        self.firlen = round(self.risetime / self.clock.period)
        self.firinit = 0
        self.firque = deque([self.firinit] * self.firlen)
        self.firval = 0
        #
        self.env.process(self.run())

    def run(self):
        while self.clock.running:
            last = self.firque.popleft()
            first = self.step()
            self.firque.append(first)
            self.firval += (first-last)
            yield self.clock.tock

    def step(self):
        if (self.env.now - self.delay) < 0:
            edge = 0
        elif (self.env.now - self.delay) / self.risetime < 1:
            edge = (self.env.now - self.delay) / self.risetime * self.Vmax
        else:
            edge = self.Vmax
        return(edge)

    @property
    def Vin(self):
        return(None)

    @Vin.setter
    def Vin(self,V):
        return(None)

    @property
    def Vout(self):
        return(self.Vs)

    @property
    def Vs(self):
        return(self.firval/self.firlen)

    @property
    def period(self):
        return(self.clock.period)

##############################################################################
# Driver, or wave source, model
class SrcPattern(SrcStep):
    type = 'R'  # type = Resistor

    def __init__(self, env, clock, Zc, Vs, Tdelay, risetime, pattern, baud, unit=1):
        self.pattern = pattern
        self.baud = baud
        #
        self.prevbit = '0'
        self.Vo = []
        for n, bit in enumerate(pattern):
            bits = '%s%s' % (self.prevbit, bit)
            if bits == '01':
                self.Vo.append(SrcStep(env,clock,Zc,Vs,Tdelay+n*baud,risetime,unit='bit%d'%n))
            elif bits == '10':
                self.Vo.append(SrcStep(env,clock,Zc,-Vs,Tdelay+n*baud,risetime,unit='bit%d'%n))
            self.prevbit = bit
        #
        SrcStep.__init__(self, env, clock, Zc, Vs, Tdelay, risetime, unit)
        self.name = 'SrcPattern_'+unit

    def run(self):
        while self.clock.running:
            yield self.clock.tick

    @property
    def Vs(self):
        Vs = 0
        for edge in self.Vo:
            Vs += edge.Vs
        return(Vs)

##############################################################################
# Transmission line termination
class Term:
    type = 'R'  # type = Resistor

    def __init__(self,env,clock,Zc,Vt=0,gamma=None,length=None,unit=1):
        self.env = env
        self.clock = clock
        self.Zc = Zc
        self.Vs = Vt  # termination voltage
        self.unit = str(unit)
        #
        self.name = 'Term_'+self.unit
        #
        self.env.process(self.run())

    def run(self):
        while self.clock.running:
            yield self.clock.tick

    @property
    def Vin(self):
        return(None)

    @Vin.setter
    def Vin(self,V):
        return(None)

    @property
    def Vout(self):
        return(self.Vs)

    @property
    def period(self):
        return(self.clock.period)

##############################################################################
# Transmission line model parent
class Tline:
    type = 'T'  # type = Transmission line

    def __init__(self, env, clock, Zc, gamma, length, unit=1):
        self.env = env
        self.clock = clock
        self.Zc = Zc
        self.gamma = gamma  # time per unit length
        self.length = length
        self.unit = str(unit)
        #
        self.name = 'Tline_'+self.unit
        #
        try:
            # does 'parent' exist?
            self.parent
        except AttributeError:
            # Nope, looks like I'm the parent
            self.parent = self
            # parents have lots to do...
            #
            # Make some ports as 'children' objects
            self.port1 = Tio(env, clock, Zc, gamma, length, self, 1, unit='%sp%d'%(unit,1))
            self.port2 = Tio(env, clock, Zc, gamma, length, self, 2, unit='%sp%d'%(unit,2))
            # Make the T-line shift registers and pointers
            self.Vf_next = 0
            self.Vr_next = 0
            self.delay = self.gamma * self.length  # delay, in to out, in (s)
            self.vel = self.length / self.delay  # velocity
            self.fline = deque([0] * ceil(self.delay/self.period))
            self.rline = deque([0] * ceil(self.delay/self.period))
        #
        self.snap = None
        #
        self.env.process(self.run())

    def run(self):
        while self.clock.running:
            self.fline.pop()
            self.fline.appendleft(self.Vf_next)
            self.rline.popleft()
            self.rline.append(self.Vr_next)
            yield self.clock.tock

    @property
    def snapshot(self):
        line = []
        for i in range(len(self.parent.fline)):
            line.append(self.parent.fline[i]+self.parent.rline[i])
        return(line)

    @property
    def snapfline(self):
        line = []
        for i in range(len(self.parent.fline)):
            line.append(self.parent.fline[i])
        return(line)

    @property
    def snaprline(self):
        line = []
        for i in range(len(self.parent.rline)):
            line.append(self.parent.rline[i])
        return(line)

    """ Next four are good for debugging """
    @property
    def Vfin(self):
        return(self.parent.fline[0])

    @property
    def Vfout(self):
        return(self.parent.fline[-1])

    @property
    def Vrin(self):
        return(self.parent.rline[-1])

    @property
    def Vrout(self):
        return(self.parent.rline[0])
    """ end debug methods """

    @property
    def period(self):
        return(self.clock.period)

##############################################################################
# Transmission line model child, IO creator
class Tio(Tline):
    def __init__(self, env, clock, Zc, gamma, length, parent, portID, unit=1):
        self.parent = parent
        self.portID = portID
        Tline.__init__(self, env, clock, Zc, gamma, length, unit)

    # Tline controls state variables in the method called 'run'. 
    # We must eliminate that functionality via overloading in child classes
    def run(self):
        yield self.clock.tick

    @property
    def Vin(self):
        if self.portID == 1:
            return(self.parent.fline[0])
        elif self.portID == 2:
            return(self.parent.rline[-1])
        else:
            warn('Warning: Tline.inp: invalid port value ',self.portID)

    @Vin.setter
    def Vin(self,V):
        if self.portID == 1:
            self.parent.Vf_next = V
        elif self.portID == 2:
            self.parent.Vr_next = V
        else:
            warn('Warning: Tline.inp: invalid port value ',self.portID)

    @property
    def Vout(self):
        if self.portID == 2:
            return(self.parent.fline[-1])
        elif self.portID == 1:
            return(self.parent.rline[0])
        else:
            warn('Warning: Tline.out: invalid port value ',self.portID)

##############################################################################
# Node model -- used to connect components
class node:
    type = 'N'  # type = Node

    def __init__(self, env, clock, port1, port2, unit=1,meas=None):
        self.env = env
        self.clock = clock
        self.dev1 = port1
        self.dev2 = port2
        self.unit = str(unit)
        self.meas = meas
        #
        self.name = 'Node_'+self.unit
        #
        self.Vnode = None
        self.Vnode2 = None
        #
        self.env.process(self.run())
        self.env.process(self.assertn())

    def run(self):
        while self.clock.running:
            if self.dev1.type == 'T' and self.dev2.type == 'T':
                self.setReflection()  # used for two transmission lines
            else:
                self.setVoltage()  # used for Tline to resistor
            yield self.clock.tick

    """ 
    Assertion generator
    Very useful to find numeric errors due to algorithm errors
    """
    def assertn(self):
        while self.clock.running:
            assertion('%s#%d'%(self.unit,1),self.env.now,self.Vnode,self.Vnode2)
            if defined(self.meas):
                measure('%s#%d'%(self.unit,1),self.env.now,self.Vnode,0.1,prec=0.002)
                measure('%s#%d'%(self.unit,2),self.env.now,self.Vnode,0.5,prec=0.001)
                measure('%s#%d'%(self.unit,3),self.env.now,self.Vnode,0.9,prec=0.0002)
            yield self.clock.tock

    def setReflection(self):
        dev1_Vin = self.calcTx(self.dev1, self.dev2)
        self.dev1.Vin = dev1_Vin
        dev2_Vin = self.calcTx(self.dev2, self.dev1)
        self.dev2.Vin = dev2_Vin
        #
        self.Vnode  = self.add(dev1_Vin, self.dev1.Vout)
        self.Vnode2 = self.add(dev2_Vin, self.dev2.Vout) #  for debug

    def add(self,a,b):
        if a == None:
            return(b)
        elif b == None:
            return(a)
        else:
            return(a+b)

    def setVoltage(self):
        self.Vres = self.R.Vs * (1 - self.T.Zc/(self.R.Zc + self.T.Zc))
        self.T_in = self.R.Vs - self.Vres + self.T.Vout * self.Gamma(self.T,self.R)
        self.T.Vin = self.T_in
        #
        self.T_out = self.T.Vout
        self.Vnode = self.T_in + self.T_out

    def calcTx(self, p1, p2):
        return(p1.Vout * self.Gamma(p1,p2) + p2.Vout * (1 + self.Gamma(p2,p1)))

    @property
    def T(self):
        if self.dev1.type == 'T':
            return(self.dev1)
        elif self.dev2.type == 'T':
            return(self.dev2)
        else:
            return(None)

    @property
    def R(self):
        if self.dev1.type == 'R':
            return(self.dev1)
        elif self.dev2.type == 'R':
            return(self.dev2)
        else:
            return(None)

    @property
    def V(self):
        return(self.Vnode)

    def Gamma(self, p1, p2):  # Reflection coefficient, gamma
        return(p2.Zc - p1.Zc)/(p2.Zc + p1.Zc)

    @property
    def period(self):
        return(self.clock.period)

##############################################################################
##############################################################################
##############################################################################
# description here
##############################################################################
class animate:
    type = 'S'  # type = support

    def __init__(self, byPos, byTime, pattern, start=0, intv=200, fontsize='x-large', note=None):
        self.byPos = byPos
        self.byTime = byTime
        self.start = start
        self.intv = intv
        self.pattern = pattern
        self.fontsize = fontsize
        self.note = note
        #
        self.fgwidth = None  # original=6.4 modified=12.8
        self.fgheight = None  # original=4.8 modified=11.48
        self.suptitle = True
        #
        # lets figure out the range, or Y, extent
        self.miny =  1e12
        self.maxy = -1e12
        for obj in self.byPos:
            if defined(obj):
                for d in obj.data:
                    self.miny = min([self.miny]+d)
                    self.maxy = max([self.maxy]+d)
        self.miny = floor(20 * 1.01 * min(-0.0495, self.miny))/20  # no higher than -0.05
        self.maxy = ceil(5 * 1.01 * self.maxy)/5  # always fall on a 0.2 increment
        #
        # initialize handles for the animation process
        if defined(self.byTime):
            self.fig, (self.ax1, self.ax2) = plt.subplots(nrows=2,ncols=1)
            self.fig.subplots_adjust(hspace=0.3)
        else:
            self.fig, self.ax1 = plt.subplots(nrows=1,ncols=1)
        #
        if defined(self.note):
            self.fig.text(0.5,0.1,'Note: %s'%self.note,ha='center')
        #
        self.title = 'T-line Voltage by Position'
        if int(self.pattern) != 1:
            self.title = self.title + ' - pattern=\'%s\'' % self.pattern
        self.ax1.set_title(self.title)
        self.ax1.set_ylabel('Voltage (V)', size=12)
        self.ax1.set_xlabel('Position (x)', size=12)
        #
        if defined(self.byTime):
            self.ax2.set_title('Output Voltage by Time')
            self.ax2.set_ylabel('Voltage (V)', size=12)
            self.ax2.set_xlabel('Time (t)', size=12)
        #
        # Graph #1
        self.ln1, = self.ax1.plot([], [], 'b-', animated=True)
        #
        # lets create labels for the Tline sections
        self.tltext = []  
        for n, obj in enumerate(self.byPos):
            if defined(obj):
                self.tltext.append(Parms())
                self.tltext[-1].name = obj.obj.unit
                self.tltext[-1].Zc = obj.obj.Zc
                self.tltext[-1].l = obj.obj.length
        maxlen=0
        for obj in self.tltext:
            maxlen += obj.l
        len_step = 0
        # bbox_props = dict(boxstyle='darrow',fc='w')
        for obj in self.tltext:
            dx = obj.l/maxlen
            obj.x = len_step + dx/2
            len_step += dx
            obj.y = 0.92
            obj.h_text = self.ax1.text(obj.x, obj.y, 
                                       '$\Leftarrow Z_c=$%d$\Omega \Rightarrow$' % obj.Zc, 
                                       ha='center', size=10, transform=self.ax1.transAxes)
        #                               bbox=bbox_props)
        #
        # create a time counter display in the Position graph
        self.timetxt = self.ax1.text(1, 0.88, '', size=10, ha='right', transform=self.ax1.transAxes)
        #
        # Graph #2
        if defined(self.byTime):
            self.ln2 = []
            for obj in self.byTime:
                if defined(obj):
                    label = "%s_%s" % (obj.obj.unit,obj.obj_atr)
                    x, = self.ax2.plot([], [], '-', label=label, animated=True)
                    self.ln2.append(x)
        #

    def Mpeg4writer(self, fps=30, outrate=30):
        extra_args = ['-vcodec', 'libx264', '-r', '%d'%outrate]
        writer = FFMpegWriter(fps=fps, extra_args=extra_args)
        return(writer)

    def animPosition(self, click):
        idx = round(click / self.period)  # index to snapshot at t='click'
        xdata, ydata = [], []
        #
        for obj in self.byPos:
            if defined(obj):
                numpts = len(obj.data[idx])
                # obj.data is [stop_time/clock_period][length*gamma/clock_period]
                # which is [time of sample][voltage at position (x)]
                # and it appears to be [30000][2000] at the time of this writing
                nextx = xdata[-1]+self.period/self.gamma if len(xdata)>0 else 0
                #
                xdata += [nextx + x*self.period/self.gamma for x in range(numpts)]
                ydata += obj.data[idx]
        #
        return(xdata, ydata)

    def animTime(self, click):
        idx = round(click / self.period)  # index to snapshot at t='click'
        #print('animTime idx=%g'%idx)
        xdata, ydata = [], []
        for obj in self.byTime:
            if defined(obj):
                xdata.append(obj.time[0 : idx])
                ydata.append(obj.data[0 : idx])
        #
        return(xdata, ydata)

    def init(self):
        if self.suptitle:
            self.fig.suptitle('Transmission Line Simulation', size=20)
        if defined(self.note):
            self.fig.text(0.5,0.1,'Note: %s'%self.note,ha='center')
        #
        if not defined(self.fgwidth):
            self.fgwidth = self.fig.get_figwidth()*2
            self.fig.set_figwidth(self.fgwidth)
        if not defined(self.fgheight):
            self.fgheight = self.fig.get_figheight()*2.4
            self.fig.set_figheight(self.fgheight)
        #print('new figwidth=%g figheight=%g'%(self.fig.get_figwidth(),self.fig.get_figheight()))
        #
        # initialize graph #1
        xmax = 0
        objbounds = []
        for obj in self.byPos:
            if defined(obj):
                xmax += len(obj.data[0])*self.period/self.gamma
                objbounds.append(xmax)
        objbounds.pop()  # dump the last one -- we only want the internal boundaries
        self.ax1.set_xlim(0, xmax)
        self.ax1.set_ylim(self.miny, self.maxy)
        self.ax1.grid(axis='y', linestyle='-.')
        #self.ln1.get_window_extent
        #
        for bound in objbounds:
            self.ax1.arrow(bound, self.miny, 0, self.maxy - self.miny)
        #
        # initialize graph #2
        if defined(self.byTime):
            self.fig.subplots_adjust(hspace=3/self.fgheight)
            xmax = 0
            for obj in self.byTime:
                if defined(obj):
                    xmax = max(xmax, obj.time[-1])
            self.ax2.set_xlim(0, xmax)
            self.ax2.set_ylim(self.miny, self.maxy)
            self.ax2.grid(axis='y', linestyle='-.')
            self.ax2.legend()
            #self.ln2.get_window_extent
            #
            lines = [self.ln1]+self.ln2+[]
        else:
            lines = [self.ln1]+[]
        #
        plt.subplots_adjust(hspace=0.6, top=0.85)
        return(lines)

    def update(self, frame):  # frame is merely a scalar value, an 'x'
        click = self.start + frame*self.period  # time snapshot is taken, (s)
        lines = []
        #print('lastx=%d xdata.len=%d ydata.len=%d' % (xdata[-1],len(xdata),len(ydata)))
        #
        self.ln1.set_data(self.animPosition(click))
        self.timetxt.set_text('t=%1.1f' % click)
        lines.append(self.ln1)
        lines.append(self.timetxt)
        #
        if defined(self.byTime):
            xdata, ydata = self.animTime(click)
            for n, ln2 in enumerate(self.ln2):
                ln2.set_data(xdata[n], ydata[n])
                lines.append(ln2)
        #
        return(lines)

    def gen(self, frames):
        self.frames = frames
        anim = FuncAnimation(self.fig, self.update, self.frames,
                        init_func=self.init, interval=self.intv,
                        blit=True, repeat=False)
        plt.show(block=False)
        return(anim)

    @property
    def figwidth(self):
        return(self.fgwidth)

    @figwidth.setter
    def figwidth(self,w):
        self.fgwidth = w
        if defined(self.fgwidth):
            self.fig.set_figwidth(self.fgwidth)
        return(self.fgwidth)
    
    @property
    def figheight(self):
        return(self.fgheight)

    @figheight.setter
    def figheight(self,h):
        self.fgheight = h
        if defined(self.fgheight):
            self.fig.set_figheight(self.fgheight)
        return(self.fgheight)
    
    @property
    def period(self):
        return(self.byPos[0].clock.period)

    @property
    def gamma(self):
        return(self.byPos[0].obj.gamma)

##############################################################################
##############################################################################
##############################################################################
# useful functions
def defined(var):
    return(var != None)

def assertion(num,now,val1,val2,prec=0.00001):
    if defined(val1) and defined(val2):
        delta = abs(val2 - val1)
        if val1 != val2:
            if val1 != 0:
                delta /= val1
            elif val2 != 0:
                delta /= val2
            if delta > prec:
                print('ASSERTION %s @ t=%f: %2G != %2G, %%error=%1.2f' % 
                     (num,now,val1,val2,delta*100))

def measure(num,now,val1,val2,prec=0.00001):
    if defined(val1) and defined(val2):
        delta = abs(val2 - val1)
        if val1 != val2:
            if val1 != 0:
                delta /= val1
            elif val2 != 0:
                delta /= val2
            if delta < prec:
                print('MEASURE %s @ t=%f: %2G != %2G, %%error=%1.2f' % 
                     (num,now,val1,val2,delta*100))

def plt_plot(node):
    label = "%s_%s" % (node.obj.unit,node.obj_atr)
    plt.plot(node.time, node.data, label=label)

def mkFrame(prb, fignum=0, start=0, size='x-large'):
    click = start + fignum*prb.clock.period  # time snapshot is taken, (s)
    click_str = str('%02.03f'%click)
    idx = round(click / prb.clock.period)  # index to snapshot at t='click'
    numpts = len(prb.data[idx])
    domain = [x*prb.clock.period/prb.obj.gamma for x in range(numpts)]
    #
    fig = plt.figure()  # plot the voltages inside a Tline at a specific time
    plt.plot(domain, prb.data[idx])
    plt.title(prb.unit+' voltages at '+click_str+'sec', size=fontsize)
    plt.xlabel('Position (x)', size=fontsize)
    plt.ylabel('Voltage (V)', size=fontsize)
    plt.ylim((-0.1, 2))
    #plt.legend(size=fontsize)
    #plt.close()
    return(fig)
