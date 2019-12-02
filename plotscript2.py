from __future__ import division
import math as m
import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.path import Path
import matplotlib.cm as cm
import averaging as av
import time
import pickle
import copy



# 1) axial power profile
# 2) axial temperature and density
# 3) plotonium
# 4) flux plot
# 5) axial temp case 1 all burnup
# 6) cladtempplot
# 7) temperature plots with actual data
# 8) averaing
# 9) case 0 stuff
# 10) crud plots


### how to use this script:
# run loading.py
# run plotscript.py once (auxillary functions....)
# assign a number (or list) to plotcase: plotcase=[8]
# same for subcase
# 'run -i plotscript'
# sometimes additional scripts need to be run before, see comments

if 1 in plotcase:
    if 1 in subcase: #plutonium
    
    
        figure()
        axis=plt.subplot(111)
        
        ph=[[0,0,0],[0,0,0]]
        c=['b', 'g', 'r']
        ii=[0,9]
        
        for i in range(len(ii)):
           
            ph[i][0],=step(z_mesh,Stepper(LinPow(tp,0,ii[i]),0)/1000,color='b',where='post')
            ph[i][1],=step(z_mesh,Stepper(LinPow(tp,1,ii[i]),0)/1000,color='g',where='post')
            ph[i][2],=step(z_mesh,Stepper(LinPow(tp,2,ii[i]),0)/1000,lw=2,color='r',where='post')
            
            
            a=max(abs((LinPow(tp,2,ii[i])-LinPow(tp,0,ii[i]))/LinPow(tp,0,ii[i])))
            b=max(abs((LinPow(tp,2,ii[i])-LinPow(tp,1,ii[i]))/LinPow(tp,1,ii[i])))
            print 'maximum deviation for case 0 bu='+str((ii[i]+1)*50)+': '+str(a)
            print 'maximum deviation for case 1 bu='+str((ii[i]+1)*50)+': '+str(b)
        axis.yaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.xaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.set_ylabel('linear Power, [kW/m]' ,size=14)
        axis.set_xlabel('axial position, [m]',size=14) 
        axis.annotate('50 EFPD', xy=(0.6, 36),size=16,color=[0.5,0.5,0.5]) 
        axis.annotate('500 EFPD', xy=(1.6, 26),size=16,color=[0.5,0.5,0.5])
        l=legend([ph[0][0],ph[0][1],ph[0][2]],["case 0","case 1","case 2"],loc=8)
        axis.set_xlim([0,3.6576])
        savefig('V:\\master report\\figures\\powercycle2.pdf')
        axis.set_title('Linear Power development with burnup \n case 2, with 0 and 1',size=18)    
        tight_layout()
        savefig('D:\\dropbox\\Dropbox\\plots\\case2\\powercycle.png')
        show()
        
        
        
        
        
if 3 in plotcase:        
        
        
    if 1 in subcase:    # plutonium buildup over cycle
        plt.figure()
        axis=plt.subplot(111)
        lh=[0]*10

        for i in range(10):
            c = cm.jet((i)/10,1)
            lh[i],=step(z_mesh,Stepper(PuDens(tpu[2,i,:,:,:,0],3),0),color=c,where='post')
            step(z_mesh,Stepper(PuDens(tpu[2,i,:,:,:,1],3),0),color=c,where='post')        
            
        axis.set_xlim([0,3.6576])
        #axis.set_ylim([500,1100])
        axis.ticklabel_format(style='sci', scilimits=(0,0), axis='y')
        axis.xaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.yaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        
        axis.set_ylabel('Pu concentration, [1/(barn cm)]' ,size=14)
        axis.set_xlabel('axial position, [m]',size=14) 
            
        l=legend([lh[0],lh[-1]],["50 EFPD","500 EFPD"],loc=2)    
        axis.annotate('Pu239', xy=(2.5, 0.00012),size=16,color=[0.5,0.5,0.5])
        axis.annotate('PU241', xy=(2.5, 0.00002),size=16,color=[0.5,0.5,0.5])        
        show()         
        
    if 1.5 in subcase:
        
        plt.figure()
        axis=plt.subplot(111)
        lh=[[0,0],[0,0]]
        case=[0,9]
        c=['b', 'g', 'r']
        for i in range(len(case)):
            c = cm.jet((case[i])/10,1)
            lh[i][0],=step(z_mesh,Stepper(PuDens(tpu[2,case[i],:,:,:,0],3),0),color=c,where='post')
            lh[i][1],=step(z_mesh,Stepper(PuDens(tpu[0,case[i],:,:,:,0],30),0),ls=':',color=c,where='post')        
            
            dif=(PuDens(tpu[2,case[i],:,:,:,0],3)-PuDens(tpu[0,case[i],:,:,:,0],30))/PuDens(tpu[0,case[i],:,:,:,0],30)
            print 'maximum deviation for bu='+str((case[i]+1)*50)+': '+str(max(abs(dif)))
            
            
        axis.set_xlim([0,3.6576])
        #axis.set_ylim([500,1100])
        axis.ticklabel_format(style='sci', scilimits=(0,0), axis='y')
        axis.xaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.yaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.set_xlim([0,3.6576])
        axis.set_ylim([0,0.00015])
        axis.set_ylabel('Pu concentration, [1/(barn cm)]' ,size=14)
        axis.set_xlabel('axial position, [m]',size=14) 
        #legend()    
        l=legend([lh[1][0],lh[0][0],lh[1][1],lh[0][1]],["case 2","case 2","case 0","case 0"],loc=5)    
        axis.annotate( '50 EFPD', xy=(1, 0.00003),size=16,color=[0.5,0.5,0.5])
        axis.annotate( '500 EFPD', xy=(1, 0.00012),size=16,color=[0.5,0.5,0.5])
         
        
        savefig('V:\\master report\\figures\\Pu_buildup2_1_5.pdf')
        axis.set_title('Pu 239 buildup at 50 & 500 EFPD\n case 2 and 0',size=18)
        tight_layout()
        savefig('D:\dropbox\Dropbox\plots\case2\Pu_buildup1.5.png')            
        show()
         
        
        
        
        
        