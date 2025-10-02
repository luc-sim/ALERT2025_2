# -*- coding: utf-8 -*-
"""
Created on Thu Oct  2 10:51:12 2025

@author: lsimonin
"""

# -*- coding: utf-8 -*-
"""
Created on Ocober 2th

@author: Luc Simonin

Creating a simple von-mises multi-surface model for ALERT doctoral school

"""
# import autograd.numpy as np
import numpy as np
from HyperDrive import Utils as hu

check_eps = np.array([0.01,0.04])
check_sig = np.array([60.1,13.1])
check_alp = np.array([[0.05,0.13], [0.09,0.18], [0.02,0.05]])
check_chi = np.array([[9.0,0.1], [10,0.2], [11.0,0.3]])

file = "HySand_base"
name = "HySand_base"
mode = 1
ndim = 2
n_y = 3
n_int = 3
n_inp = 1
const =      [  3 ,50000,40000, 34   ,  10 , 5]
name_const = ['NN', "K" , "G" ,"fu",'h','b']


def deriv():
    global NN,K,G,fu,h0,b,m
    m = 0
    NN = int(const[0])
    [K,G,fu,h0,b] =  [float(i) for i in const[1:]]
    global rN, n_int, n_y
    rN = 1/NN
    n_int = NN
    n_y = NN
    global pref, kref, gref
    pref = 100
    kref = K/pref
    gref = G/pref
    # global mu
    # mu = np.tan(phic*np.pi/180)
    global H0
    H0 = np.zeros([NN])    
    for i in range(NN):
        H0[i]=h0*(1-(i+1)*rN)**b
deriv()

def update(t,eps,sig,alp,chi,dt,deps,dsig,dalp,dchi):
    return alp

def pm(sig):
    pm =  ((sig[0])**2 + (kref/(3*gref)) * (1-m) * sig[1]**2 )**(1/2)
    return (pm)

def g(sig,alp):
    temp= - pref / ( kref*(1-m)*(2-m) ) * (pm(sig)/pref)**(2-m) \
          - rN * sig[0] * sum(alp[i,0] for i in range(NN)) \
          - rN * sig[1] * sum(alp[i,1] for i in range(NN))
    return (temp)
def dgds(sig,alp):
    temp=-np.array([ ((sig[0]) / (pref*kref*(1-m)) * ( ((sig[0])**2 + kref*(1-m)*sig[1]**2/(3*gref)) / pref**2)**(-m/2))  + rN * sum(alp[i,0] for i in range(NN)),
                      (sig[1]/(3*gref*pref) * ( ((sig[0])**2 + kref*(1-m)*sig[1]**2/(3*gref)) / pref**2)**(-m/2))            + rN * sum(alp[i,1] for i in range(NN)) ])
    return (temp)    
def dgda(sig,alp):
    temp = np.zeros([n_int,ndim])
    for i in range(NN):
        temp[i,0] = -rN * sig[0]
        temp[i,1] = - rN * sig[1]
    return temp
def d2gdsds(sig,alp):
    brack=( ((sig[0])**2 + kref*(1-m)*sig[1]**2 / (3*gref)) / pref**2)
    temp=-np.array([[ (1 / (kref*(1-m)*pref) * brack**(-m/2) - m*(sig[0])**2 / ((1-m)*kref*pref**3) * brack**(-m/2-1))  
                            ,  -m*(sig[0])*sig[1] / (3*gref*pref**3) * brack**(-m/2-1)] ,
                      [-m*(sig[0])*sig[1] / (3*gref*pref**3) * brack**(-m/2-1)
                            ,  1 / (3*gref*pref) * brack**(-m/2) - m*kref*(1-m)*sig[1]**2 / (((3*gref)**2)*pref**3)  * brack**(-m/2-1) ]]) 
    return (temp)
def d2gdsda(sig,alp):
    temp = np.zeros([ndim,n_int,ndim])
    for j in range(NN):
        temp[0,j,0] = - rN
        temp[1,j,1] = - rN
    return temp
def d2gdads(sig,alp):
    temp = np.zeros([n_int,ndim,ndim])
    for j in range(NN):
        temp[j,0,0] = - rN
        temp[j,1,1] = - rN
    return temp
def d2gdada(sig,alp):
    temp = np.zeros([n_int,ndim,n_int,ndim])
    return temp

y_exclude = True

# denominator of Matsuoka-Nakai gauge function
def f_MN_pq(sig):
    return fu**2
def d_f_MN_pq_ds(sig):
    temp = np.zeros([ndim])
    # temp[0] = 4 * mu**2 * ( (sig[0]+2/3*sig[1]) + (sig[0]-sig[1]/3) )
    # temp[1] = 4 * mu**2 * ( -1/3 * (sig[0]+2/3*sig[1]) + 2/3 * (sig[0]-sig[1]/3) )
    return temp

# Modified deviatoric generalised stress
def f_CHI(eps,sig,alp,chi):
    temp = np.zeros([NN])
    H = H0
    for i in range(NN):
        temp[i] = (chi[i,1]*NN \
                  - 3*H[i]*alp[i,1] )
    return temp
def d_f_CHI_de(eps,sig,alp,chi):
    temp = np.zeros([NN,ndim])
    return temp
def d_f_CHI_ds(eps,sig,alp,chi):
    temp = np.zeros([NN,ndim])
    H = H0
    # for i in range(NN):
    #     temp[i,0] = - 3*H[i]*alp[i,1]
    return temp
def d_f_CHI_da(eps,sig,alp,chi):
    temp = np.zeros([NN,n_int,ndim])
    H = H0
    for i in range(NN):
        temp[i,i,1] = - 3*H[i]
    return temp
def d_f_CHI_dc(eps,sig,alp,chi):
    temp = np.zeros([NN,n_int,ndim])
    H = H0
    for i in range(NN):
        temp[i,i,1] = NN
    return temp


# Definition of the yield surface(s)
def y(eps,sig,alp,chi):
    temp=np.zeros([n_y])
    MN_pq = f_MN_pq(sig)
    CHI = f_CHI(eps,sig,alp,chi)
    for i in range(NN):
        temp[i] = CHI[i]**2 / ( ((i+1)*rN)**2 * MN_pq )     # Matsuoka-Nakai part
        temp[i] -= 1
    return temp
def dyde(eps,sig,alp,chi):
    tempy=np.zeros([n_y,ndim])
    MN_pq = f_MN_pq(sig)
    CHI = f_CHI(eps,sig,alp,chi)
    dCHI = d_f_CHI_de(eps,sig,alp,chi)
    for i in range(NN):
        tempy[i,0] = 2*dCHI[i,0]*CHI[i] / ( ((i+1)*rN)**2 * MN_pq )         # Matsuoka-Nakai part
    return tempy
def dyds(eps,sig,alp,chi):
    tempy=np.zeros([n_y,ndim])
    MN_pq = f_MN_pq(sig)
    dMN_pq = d_f_MN_pq_ds(sig)
    CHI = f_CHI(eps,sig,alp,chi)
    dCHI = d_f_CHI_ds(eps,sig,alp,chi)
    for i in range(NN):
        u = CHI[i]**2
        du_dp = 2*dCHI[i,0]* CHI[i]
        du_dq = 2*dCHI[i,1]* CHI[i]
        v = ((i+1)*rN)**2 * MN_pq
        dv_dp = ((i+1)*rN)**2 * dMN_pq[0]
        dv_dq = ((i+1)*rN)**2 * dMN_pq[1]
        tempy[i,0] = (du_dp*v-u*dv_dp) / v**2                               # Matsuoka-Nakai part
        tempy[i,1] = (du_dq*v-u*dv_dq) / v**2                               # Matsuoka-Nakai part
    return tempy
def dyda(eps,sig,alp,chi):
    tempy = np.zeros([n_y,n_int,ndim])
    MN_pq = f_MN_pq(sig)
    CHI = f_CHI(eps,sig,alp,chi)
    dCHI = d_f_CHI_da(eps,sig,alp,chi)
    for i in range(NN):
        for j in range(n_int):
            tempy[i,j] = 2*dCHI[i,j] *CHI[i] / ( ((i+1)*rN)**2 * MN_pq )        # Matsuoka-Nakai part
    return tempy
def dydc(eps,sig,alp,chi):
    tempy = np.zeros([n_y,n_int,ndim])
    MN_pq = f_MN_pq(sig)
    CHI = f_CHI(eps,sig,alp,chi)
    dCHI = d_f_CHI_dc(eps,sig,alp,chi)
    for i in range(NN):
        for j in range(n_int):
            tempy[i,j] = 2*dCHI[i,j] *CHI[i] / ( ((i+1)*rN)**2 * MN_pq )    # Matsuoka-Nakai part
    return tempy