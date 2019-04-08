# -*- coding: utf-8 -*-
"""
    The ``base`` module of modelphy library
    =========================
 
    Provides virtual class for all other model
 
    :Example:
 
    >>> model = modelbase.model(name='test', neq=1)
    >>> import pyfvm.modelphy.base as modelbase
    >>> print model.neq, model.equation
    1 test
 
    Available functions
    -------------------
 
    Provides ...
 """

import numpy as np
import math
#import pyfvm.modelphy.base as base

# ===============================================================
# implementation of MODEL class

class model():
    """
    Class model (as virtual class)

    attributes:
        neq
        islinear            
        has_firstorder_terms 
        has_secondorder_terms
        has_source_terms     

    """
    def __init__(self, name='not defined', neq=0):
        self.equation = name
        self.neq      = neq
        self.islinear = 0
        self.has_firstorder_terms  = 0
        self.has_secondorder_terms = 0
        self.has_source_terms      = 0
        self._vardict = { }
        self._bcdict  = { 'dirichlet': self.bc_dirichlet }

    def __repr__(self):
        print "model: ", self.equation
        print "nb eq: ", self.neq

    def list_bc(self):
        return self._bcdict.keys()

    def list_var(self):
        return self._vardict.keys()
        
    def cons2prim(self):
        print "cons2prim method not implemented"
    
    def prim2cons(self):
        print "prim2cons method not implemented"
    
    def initdisc(self, mesh):
        return
    
    def numflux(self):
        pass
    
    def timestep(self, data, dx, condition):
        pass

    def nameddata(self, name, data):
        return (self._vardict[name])(data)

    def namedBC(self, name, dir, data, param):
        return (self._bcdict[name])(dir, data, param)

    def bc_dirichlet(self, dir, data, param):
        return param['prim']

 
# ===============================================================
# automatic testing

if __name__ == "__main__":
    import doctest
    doctest.testmod()

