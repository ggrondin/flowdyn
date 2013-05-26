# -*- coding: utf-8 -*-
"""
Created on Fri May 10 17:39:03 2013

@author: j.gressier
"""
import math
import numpy as np
from field import *

class timemodel():
    def __init__(self, mesh, num):
        self.mesh  = mesh
        self.num   = num
        
    def calcrhs(self, field):
        field.cons2prim()
        field.calc_grad(self.mesh)
        field.calc_bc_grad(self.mesh)
        field.interp_face(self.mesh, self.num)
        field.calc_bc()
        field.calc_flux()
        return field.calc_res(self.mesh)
 
    def step():
        print "not implemented for virtual class"

    def solve(self, field, condition, tsave):
        self.nit       = 0
        self.condition = condition
        itfield = numfield(field)
        results = []
        for t in np.arange(tsave.size):
            endcycle = 0
            while endcycle == 0:
                dtloc = itfield.calc_timestep(self.mesh, condition)
                dtloc = min(dtloc)
                if itfield.time+dtloc >= tsave[t]:
                    endcycle = 1
                    dtloc    = tsave[t]-itfield.time
                self.nit += 1
                itfield.time += dtloc
                if dtloc > np.spacing(dtloc):
                    itfield = self.step(itfield, dtloc)
            itfield.cons2prim()
            results.append(itfield.copy())
        return results

    
class time_explicit(timemodel):
    def step(self, field, dtloc):
        self.calcrhs(field)
        field.add_res(dtloc)
        return field

#--------------------------------------------------------------------
# RUNGE KUTTA MODELS
#--------------------------------------------------------------------
    
class rkmodel(timemodel):
    def step(self, field, dtloc, butcher):
        #butcher = [ np.array([1.]), \
        #            np.array([0.25, 0.25]), \
        #            np.array([1., 1., 4.])/6. ]
        prhs = []
        pfield = numfield(field)            
        for pcoef in butcher:
            # compute residual of previous stage and memorize it in prhs[]
            prhs.append([ q.copy() for q in self.calcrhs(pfield)])
            # revert to initial step
            pfield.qdata = [ q.copy() for q in field.qdata ]
            # aggregate residuals
            for qf in pfield.residual:
                qf *= pcoef[-1]
            for i in range(pcoef.size-1):
                for q in range(pfield.neq):
                    pfield.residual[q] += pcoef[i]*prhs[i][q]
            pfield.add_res(dtloc)        
        return pfield

class time_rk2(timemodel):
    def step(self, field, dtloc):
        reffield = numfield(field)
        self.calcrhs(field)
        field.add_res(dtloc/2)
        self.calcrhs(field)
        reffield.residual = field.residual
        reffield.add_res(dtloc)
        return reffield

class time_rk3ssp(rkmodel):
    def step(self, field, dtloc):
        butcher = [ np.array([1.]), \
                    np.array([0.25, 0.25]), \
                    np.array([1., 1., 4.])/6. ]
        return rkmodel.step(self, field, dtloc, butcher)

class time_rk4(rkmodel):
    def step(self, field, dtloc):
        butcher = [ np.array([0.5]), \
                    np.array([0., 0.5]), \
                    np.array([0., 0., 1.]), \
                    np.array([1., 2., 2., 1.])/6. ]
        return rkmodel.step(self, field, dtloc, butcher)

#--------------------------------------------------------------------
# IMPLICIT MODELS
#--------------------------------------------------------------------

class implicitmodel(timemodel):
    def step(self, field, dtloc):
        print "not implemented for virtual implicit class"
        
    def calc_jacobian(self, field):
        self.neq = field.neq
        self.dim = self.neq * field.nelem
        self.jacobian = np.zeros([self.dim, self.dim])
        eps = [ math.sqrt(np.spacing(1.))*np.sum(np.abs(q))/field.nelem for q in field.qdata ] 
        refrhs = [ qf.copy() for qf in self.calcrhs(field) ]
        #print 'refrhs',refrhs
        for i in range(field.nelem):
            for q in range(self.neq):
                dfield = numfield(field)
                dfield.qdata[q][i] += eps[q]
                drhs = [ qf.copy() for qf in self.calcrhs(dfield) ]
                for qq in range(self.neq):
                    #self.jacobian[i*self.neq+q][qq::self.neq] = (drhs[qq]-refrhs[qq])/eps[q]
                    self.jacobian[qq::self.neq][i*self.neq+q] = (drhs[qq]-refrhs[qq])/eps[q]

    def solve_implicit(self, field, dtloc, invert=np.linalg.solve):
        diag = np.repeat(np.ones(field.nelem)/dtloc, self.neq)   # dtloc can be scalar or np.array
        mat = np.diag(diag)-self.jacobian.transpose()
        rhs = np.linalg.solve(mat, np.concatenate(field.residual))
        field.residual = [ rhs[iq::self.neq]/dtloc for iq in range(self.neq) ]
    
class time_implicit(implicitmodel):
    def step(self, field, dtloc):
                
        self.calc_jacobian(field)
        self.calcrhs(field)
        self.solve_implicit(field, dtloc)
        field.add_res(dtloc)
        return field
    
