# -*- coding: utf-8 -*-
"""
@author: lsimonin
"""

from HyperDrive import Commands as H
import newplot as newp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker
TC = __import__('2025_10_test_commands')

H.init()
H.title(["ALERT school"])
H.g_form()
H.acc([0.5])
H.mode([1,2])
H.quiet()

prec = 100
bug = 0     # bug detector

#Parameters
K = 20000   # Bulk modulus at pr
G = 16000   # Shear modulus at pr

fu = 250   # Friction angle at critical state
h = 8000    # Hardening modulus for most inner yield surface at densest state
b = 2       # Hardening exponent
NN = 5      # number of yield surfaces

H.model(["2025_10_Alert"])


def mono(fu,h,b,NN):
    pt,qt=0.01,0 # Initial stress values
    vt = 2
    params = [NN,K,G,fu,h,b]
    H.const(params)
    H.start()
    H.init_stress([pt,qt])
    H.general_inc([1,0,0,1,0,0,0,0,0.0,0.01,1,10,prec])
    H.general_inc([1,0,0,0,0,0,0,1,0.0,0.005,1,10,prec])
    H.general_inc([1,0,0,0,0,0,0,1,0.0,0.015,1,10,prec])
    H.general_inc([1,0,0,0,0,0,0,1,0.0,0.03,1,10,prec])
    dt = H.returnrec()
    # w,dt = TC.drained_test(pt,qt,vt,eqd,prec,params,bug)
    fig = newp.plotA([],dt,['r-.'],[300,-0,200,0,0.05,-0.00,0.04,-0.06],[''],lab=['',''],ncl=1,lw=1.75,ttl='Monotonic test')
    return fig

mono(fu,h,b,NN)

def cyclic(fu,h,b,NN):
    prec = 10
    pt,qt=0.01,0 # Initial stress values
    vt = 2
    params = [NN,K,G,fu,h,b]
    H.const(params)
    H.start()
    H.init_stress([pt,qt])
    H.general_inc([1,0,0,1,0,0,0,0,0.0,0.01,1,10,prec])
    for i in range(5):
        H.general_inc([1,0,0,1,0,0,0,0,0.0,200,1,10,prec])
        H.general_inc([1,0,0,1,0,0,0,0,0.0,-200,1,10,prec])
        H.general_inc([1,0,0,1,0,0,0,0,0.0,-200,1,10,prec])
        H.general_inc([1,0,0,1,0,0,0,0,0.0,200,1,10,prec])
    H.general_inc([1,0,0,0,0,0,0,1,0.0,0.05,1,50,prec])

    dt2 = H.returnrec()
    # w,dt = TC.drained_test(pt,qt,vt,eqd,prec,params,bug)
    fig = newp.plotA([],dt2,['r-.'],[250,-250,200,0,0.02,-0.02,0.04,-0.06],[''],lab=['',''],ncl=1,lw=1.75,ttl='Cyclic test')
    return fig
