# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 2019 

@author: mlgkschm (Ken Schmahl)
"""

from copy import copy

##############################################################################
# A generic object
# C = type('C', (object,), {})
class Parms(object):  # Called Parms, short for "Parameters"
    def copy(self):  # make it easy to make copies of this object
        return(copy(self))

##############################################################################
# useful functions
def defined(var):
    return(var != None)

##############################################################################
