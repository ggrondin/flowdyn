# -*- coding: utf-8 -*-
"""
Created on Fri May 10 15:42:29 2013

@author: j.gressier
"""

from optparse import OptionParser
import sys
import math
import numpy as np

class virtualmesh():
    " virtual class for a domain and its mesh"
    def __init__(self, ncell=0, length=0.):
        self.ncell  = ncell
        self.length = length

    def centers(self):
        "compute centers of cells in a mesh"
        xc = np.zeros(self.ncell)
        for i in np.arange(self.ncell):
            xc[i] = (self.xf[i]+self.xf[i+1])/2.
        return xc

    def dx(self):
        "compute cell sizes in a mesh"
        dx = np.zeros(self.ncell)
        for i in np.arange(self.ncell):
            dx[i] = (self.xf[i+1]-self.xf[i])
        return dx

    def __repr__(self):
        print("length : ", self.length)
        print("ncell  : ", self.ncell)
        dx = self.dx()
        print("min dx : ", dx.min())
        print("max dx : ", dx.max())

class nonunimesh(virtualmesh):
    " class defining a domain and a non-uniform mesh"
    #non-uniform symmetric mesh
        
    def __init__(self, length, nclass, ncell0, periods):

        self.periods = periods        
        self.length = length*periods
        self.nclass = nclass
        self.ncell0 = ncell0
                
        regions = 2*nclass
        rlength = length/regions
        
        rcells = np.zeros(nclass)
        for r in range(nclass):
            rcells[r]=ncell0*2**r
      
        for i in range(periods):
            if i == 0:
                self.xf = np.linspace(0.,rlength, rcells[nclass-1]+1) #creates linspace array of rcell cells
            else:
                idel = len(self.xf)
                self.xf = np.hstack((self.xf,np.linspace(i*length,rlength+i*length,rcells[nclass-1]+1))) #stacks another linspace array
                self.xf = np.delete(self.xf,idel) #deleting item in index ncell1 due to duplication  

            for r in range(nclass-2,-1,-1):  #creates from left to right till the middle
                idel = len(self.xf)
                self.xf = np.hstack((self.xf,np.linspace((nclass-r-1)*rlength+i*length,(nclass-r)*rlength+i*length,rcells[r]+1))) #stacks another linspace array
                self.xf = np.delete(self.xf,idel) #deleting item in index ncell1 due to duplication   
            
            for r in range(nclass):        #creates from left to right from the middle
                idel = len(self.xf)
                self.xf = np.hstack((self.xf,np.linspace((nclass+r)*rlength+i*length,(nclass+r+1)*rlength+i*length,rcells[r]+1))) #stacks another linspace array
                self.xf = np.delete(self.xf,idel) #deleting item in index ncell1 due to duplication               
        
        self.ncell = len(self.xf)-1
        self.xc = self.centers()
        
class meshramzi(nonunimesh):
    
    def __init__(self, size, nclass, length):
        self.size   = size
        self.nclass = nclass
        
        Nclass = int(self.nclass)
    
        size1    = np.zeros(Nclass)
        size2    = int(0)
        
        size1[0] = int(size)
        size2    = size2 + size1[0]

        for i in range(1,Nclass):
            size1[i] = size1[i-1]*2
            size2    = size2 + size1[i]
        size2 = int(2*size2 + 1)

        dxx  = np.zeros(Nclass)
        for i in range(Nclass):
            dxx[i]=0.5/size1[i]/Nclass
        
        self.xf  = np.zeros(size2)
        i     = int(0) 
        self.xf[i] = float(0)
        for j in range(Nclass):
            indx  = int(Nclass-j-1)
            indx2 = int(size1[indx])
            for k in range(indx2):
                i    = i + 1 
                self.xf[i]= self.xf[i-1]+dxx[indx] 
        for j in range(Nclass):
            indx  = int(j)
            indx2 = int(size1[indx])
            for k in range(indx2):
                i    = i + 1 
                self.xf[i]= self.xf[i-1]+dxx[indx] 
        
        self.ncell = len(self.xf)-1
        self.xc = self.centers()

        self.xc *= length
        self.xf *= length
        
        self.length = 0.
        for i in range(len(self.xf)-1):
            self.length += self.xf[i+1]-self.xf[i]


class unimesh(virtualmesh):
    " class defining a uniform mesh: ncell and length"
    def __init__(self, ncell=100, length=1., x0=0.):
        virtualmesh.__init__(self, ncell, length)
        self.xf     = np.linspace(0., length, ncell+1)+x0
        self.xc     = self.centers()

class refinedmesh(virtualmesh):
    " class defining a mesh with 2 uniform parts and a cell ratio"
    def __init__(self, ncell=100, length=1., ratio=2.):
        virtualmesh.__init__(self, ncell, length)
        dx1 = 2* length / ((1.+ratio)*ncell)
        dx2 = ratio*dx1
        nc1 = ncell/2
        nc2 = ncell-nc1
        self.xf = np.append(
                    np.linspace(0., dx1*nc1, nc1+1)[0:-1],
                    np.linspace(dx1*nc1, length, nc2+1) )
        self.xc = self.centers()

class morphedmesh(virtualmesh):
    " class defining a mesh with a morphing function: ncell and length"
    def __init__(self, ncell=100, length=1., x0=0., morph=lambda x: x):
        virtualmesh.__init__(self, ncell, length)
        self.xf     = morph(np.linspace(0., length, ncell+1)+x0)
        self.xc     = self.centers()
