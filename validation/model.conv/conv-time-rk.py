# -*- coding: utf-8 -*-
"""
test integration methods
"""

#import time
from pylab import *

from flowdyn.mesh  import *
import flowdyn.modelphy.convection as convection
import flowdyn.modeldisc as modeldisc
from flowdyn.field import *
from flowdyn.xnum  import *
from flowdyn.integration import *

mesh100 = unimesh(ncell=100, length=1.)
mesh50  = unimesh(ncell=50, length=1.)

mymodel     = convection.model(1.)

# TODO : make init method for scafield
# sinus packet
def init_sinpack(mesh):
    return sin(2*2*pi/mesh.length*mesh.centers())*(1+sign(-(mesh.centers()/mesh.length-.25)*(mesh.centers()/mesh.length-.75)))/2

# periodic wave
def init_sinper(mesh):
    k = 2 # nombre d'onde
    return sin(2*k*pi/mesh.length*mesh.centers())

# square signal
def init_square(mesh):
    return (1+sign(-(mesh.centers()/mesh.length-.25)*(mesh.centers()/mesh.length-.75)))/2

initm   = init_sinpack
meshs   = [ mesh100 ]

# First set of computations

endtime = 1.
ntime   = 1
tsave   = linspace(0, endtime, num=ntime+1)
cfls    = [ 0.6 ]
# extrapol1(), extrapol2()=extrapolk(1), centered=extrapolk(-1), extrapol3=extrapolk(1./3.)
xmeths  = [ extrapol3() ]
# explicit, rk2, rk3ssp, rk4, implicit, trapezoidal=cranknicolson
tmeths  = [ rk3ssp, rk4 , rk2]
legends = [ 'RK3SSP', 'RK4', 'RK2' ]

solvers = []
results = []
nbcalc  = max(len(cfls), len(tmeths), len(xmeths), len(meshs))
for i in range(nbcalc):
    curmesh = (meshs*nbcalc)[i]
    finit   = fdata(mymodel, curmesh, [ initm(curmesh) ] )
    rhs     = modeldisc.fvm(mymodel, curmesh, (xmeths*nbcalc)[i])
    solvers.append((tmeths*nbcalc)[i](curmesh, rhs))
    #start = time.clock()
    results.append(solvers[-1].solve(finit, (cfls*nbcalc)[i], tsave)) #, flush="resfilename"))
    #print("cpu time of "+"%-4s"%(legends[i])+" computation (",solvers[-1].nit(),"it) :",time.clock()-start,"s")


style = ['o', 'x', 'D', '*', '+', '>', '<', 'd']
fig = figure(1, figsize=(10,8))
#clf()
grid(linestyle='--', color='0.5')
fig.suptitle('integration of 3rd order flux, CFL %.1f'%cfls[0], fontsize=12, y=0.93)
plot(meshs[0].centers(), results[0][0].data[0], '-')
labels = ["initial condition"]
for t in range(1,len(tsave)):
    for i in range(nbcalc):
        plot((meshs*nbcalc)[i].centers(), results[i][t].data[0], style[i])
        labels.append(legends[i]+", t=%.1f"%results[i][t].time)
legend(labels, loc='upper left',prop={'size':10})
fig.savefig('conv-time1.png', bbox_inches='tight')
show()

