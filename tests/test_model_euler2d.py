import pytest
#
import numpy as np
#
import pyfvm.mesh2d as mesh2d
import pyfvm.field as field
import pyfvm.integration as integ
import pyfvm.modelphy.euler as euler
import pyfvm.modeldisc      as modeldisc
from pyfvm.xnum  import *
#import pyfvm.solution.euler_riemann as sol

nx = 50
ny = 50
meshsim  = mesh2d.unimesh(nx, ny)

model = euler.euler2d()

rhs    = modeldisc.fvm2d(model, meshsim, num=None, numflux='centered', bclist={} )
solver = integ.rk3ssp(meshsim, rhs)

def fuv(x,y):
    vmag = .01 ; k = 10.
    return euler.datavector(0.*x+.4, 0.*x+.2)
def fp(x,y): # gamma = 1.4
    return 0.*x+1.
def frho(x,y):
    return 1.4 * (1+.2*np.exp(-((x-.5)**2+(y-.5)**2)/(.1)**2))

def test_densitypulse():
    endtime = 5.
    cfl     = 2.5
    xc, yc = meshsim.centers()
    finit = rhs.fdata_fromprim([ frho(xc, yc), fuv(xc, yc), fp(xc, yc) ]) # rho, (u,v), p
    fsol = solver.solve(finit, cfl, [endtime])
    assert not fsol[-1].isnan()
