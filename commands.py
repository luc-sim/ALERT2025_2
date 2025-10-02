# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 15:01:41 2025

@author: lsimonin

newp.plotD([],tmd1+tmd2d+tmd3d+tmd4d+tmd5d+tmd6d,['k','b','g','r','c','m'],[500,-0,500,0,0.25,-0.00,0.04,-0.06],['1','2','3','4','5','6'])
newp.plotD([],tmd1+tmd2l+tmd3l+tmd4l+tmd5l+tmd6l,['k','b','g','r','c','m'],[500,-0,500,0,0.25,-0.00,0.04,-0.06],['1','2','3','4','5','6'])
newp.plotU([],tmu1+tmu2d+tmu3d+tmu4d+tmu5d+tmu6d,['k','b','g','r','c','m'],[400,-0,250,0,0.05,-0.00,0.04,-0.06],['1','2','3','4','5','6'],yt1=4,yt2=4)

newp.plotD([],tmd1+tmd1bis,['k','k--'],[500,-0,500,0,0.25,-0.00,0.025,-0.08],['     m=0.7\n'+'non-linear elastic','     m=0\n'+'linear elastic'])
newp.plotU([],tmu1+tmu1bis,['k','k--'],[500,-0,500,0,0.05,-0.00,0.025,-0.08],['     m=0.7\n'+'non-linear elastic','     m=0\n'+'linear elastic'])

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

prec = 50
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
    fig = newp.plotA([],dt,['r-.'],[300,-0,200,0,0.05,-0.00,0.04,-0.06],[''],lab=['',''],ncl=1,lw=1.75,ttl='Drained test')
    return fig

mono(fu,h,b,NN)