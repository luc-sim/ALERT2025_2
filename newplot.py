# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 15:08:13 2022

@author: Luc Simonin

Plotting routines
"""
import matplotlib.pyplot as plt
from matplotlib import ticker
import numpy as np

# font = {'family' : 'normal',
#         'weight' : 'bold',
#         'size'   : 18}
font = {'family':'Tahoma','weight':'normal'}

plt.rc('font', **font)
cols=['k','grey','b','g','r','m','orange','c','lime','pink','yellow']
qmaj, qmin = 100, -100
pmaj, pmin = 220, 0
e2maj, e2min = 0.02, -0.02 #deviatoric
e1maj, e1min = 0.03, -0.08 #volumetric
q22, e22 = 120, 0.0001
limits0=[qmaj,qmin,pmaj,pmin,e2maj,e2min,e1maj,e1min]
nr=2
nc=2
names = ['\u03b5'+'$_p$','\u03b5'+'$_q$',"p'",'q']
high=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
legend00 = ['','','','','','','','','','','','','','','','','','','']

def plotA(data,model,test_col=cols,limits=limits0,legend0=legend00,lab=['a)','b)'],lw=1.0,mw=1.0,ncl=3,xt1=5,yt1=5,xt2=5,yt2=5,ttl="",save=0,ori='v'):
    [qmaj,qmin,pmaj,pmin,e2maj,e2min,e1maj,e1min]=limits
    fig, axes = plt.subplots(1, 1,figsize=(6,6)) 
    fig.tight_layout()
    
    for i in range(len(data)):
        recl = data[i]
        e1 = [item[1] for item in recl]-recl[0][1]
        e2 = [item[2] for item in recl]-recl[0][2]
        s1 = [item[3] for item in recl]
        s2 = [item[4] for item in recl]
        v = [item[6] for item in recl]
        axes.plot(e2, s2, test_col[i],label=legend0[i],linewidth=lw,markersize=mw)
    k = 40
    axes.plot(np.linspace(0,0.05,50),250*np.tanh(k*np.linspace(0,0.05,50)**0.8),'k')
    for j in range(len(model)):
        recl = model[j]
        e1 = [item[1] for item in recl]-recl[0][1]
        e2 = [item[2] for item in recl]
        s1 = [item[3] for item in recl]
        s2 = [item[4] for item in recl]
        i = j+len(data)
        axes.plot(e2, s2, test_col[i],label=legend0[i],linewidth=lw,markersize=mw)
    fonts = 12
    fig.suptitle(ttl,fontsize=15,font='Garamond',weight='semibold')
    if ori == 'v':
        fig.legend(ncol=ncl, loc='center', prop={'size': fonts-1}, bbox_to_anchor=(0.5, 0.075),facecolor='whitesmoke')
        plt.subplots_adjust(bottom=0.25,top=0.925,left=0.23,right=0.925,wspace=0.25, hspace=0.3)
    if ori == 'h':
        fig.legend(ncol=1, loc='center', prop={'size': fonts-2}, bbox_to_anchor=(0.92, 0.5),facecolor='whitesmoke')
    plt.subplots_adjust(bottom=0.15,top=0.87,left=0.15,right=0.90,wspace=0.25, hspace=0.1)
    axes.set_xlim([e2min,e2maj])
    axes.set_ylim([qmin,qmaj])
    axes.set_ylabel('$\it{q}$',fontsize=fonts+2)
    axes.set_xlabel('\u03b5'+'$_q$',fontsize=fonts+2)
    axes.tick_params(axis='x',labelsize=fonts)
    axes.tick_params(axis='y',labelsize=fonts)
    axes.xaxis.set_major_locator(ticker.MaxNLocator(xt2))
    axes.yaxis.set_major_locator(ticker.MaxNLocator(yt2))
    axes.grid(linestyle=':',linewidth=1)
    axes.text(0.01*(e2maj-e2min)+e2min,0.89*(qmaj-qmin)+qmin,lab[1],horizontalalignment='left',verticalalignment='bottom',fontsize=fonts+1)
    if save==1:
        plt.savefig('last_fig.jpg',dpi=300) 
    return fig
