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


if 1 in plotcase: #linwoper
    if 1 in subcase:
    
    
        figure()
        axis=plt.subplot(111)
        
        ph=[[0,0],[0,0]]
        c=['b', 'g', 'r']
        ii=[0,9]
        for i in range(len(ii)):
           
            ph[i][0],=step(z_mesh,Stepper(LinPow(tp,0,ii[i]),0)/1000,color='b',where='post')
            ph[i][1],=step(z_mesh,Stepper(LinPow(tp,1,ii[i]),0)/1000,lw=2,color='g',where='post')
            
            a=max(abs((LinPow(tp,1,ii[i])-LinPow(tp,0,ii[i]))/LinPow(tp,0,ii[i])))
            print 'maximum deviation for bu='+str((ii[i]+1)*50)+': '+str(a)
        axis.yaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.xaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.set_ylabel('linear Power, [kW/m]' ,size=14)
        axis.set_xlabel('axial position, [m]',size=14) 
        axis.annotate('50 EFPD', xy=(0.6, 36),size=16,color=[0.5,0.5,0.5]) 
        axis.annotate('500 EFPD', xy=(1.6, 26),size=16,color=[0.5,0.5,0.5]) 
        l=legend([ph[0][0],ph[0][1]],["case 0","case 1"],loc=1)
        axis.set_xlim([0,3.6576])
        
        savefig('V:\\master report\\figures\\powercycle1.eps')
        axis.set_title('Linear Power development with burnup \n case 0 and 1',size=18)    
        tight_layout()
        savefig('D:\\dropbox\\Dropbox\\plots\\case1\\powercycle.png')
        #axis.set_ylim([500,1200])    
        show()  
        
    if 1.5 in subcase: #relative linpow diff
        
        figure()
        axis=plt.subplot(111)
        plt.axhline(y=0,color=[0.5,0.5,0.5])
        ph=[0,0,0]
        c=['b', 'g', 'r','c']
        ii=[8]
        ls1=['-','-']
        for i in range(len(ii)):
        
            ph[0],=step(z_mesh,Stepper((LinPow(tp,1,ii[i])     *(dot(LinPow(tp,0,ii[i]),z_mesh2)/dot(LinPow(tp,1,ii[i]),z_mesh2))       -LinPow(tp,0,ii[i]))/LinPow(tp,0,ii[i]),0),ls=ls1[i],color='b',where='post')
            ph[1],=step(z_mesh,Stepper((LinPow(tp,2,ii[i])     *(dot(LinPow(tp,0,ii[i]),z_mesh2)/dot(LinPow(tp,2,ii[i]),z_mesh2))       -LinPow(tp,0,ii[i]))/LinPow(tp,0,ii[i]),0),ls=ls1[i],color='g',where='post')
            ph[2],=step(z_mesh,Stepper((LinPow(tp,3,ii[i])*3*4 *(dot(LinPow(tp,0,ii[i]),z_mesh2)/dot(LinPow(tp,3,ii[i])*3*4,z_mesh2))   -LinPow(tp,0,ii[i]))/LinPow(tp,0,ii[i]),0),ls=ls1[i],color='r',where='post')
            #step(z_mesh,Stepper((PuDens(tpu[1,case[i],:,:,:,0],3)-PuDens(tpu[0,case[i],:,:,:,0],30))/PuDens(tpu[0,case[i],:,:,:,0],30),0),where='post')
        axis.yaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.xaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        #axis.set_ylim([-0.04,0.04])
        axis.set_ylabel('relative difference, [-]' ,size=14)
        axis.set_xlabel('axial position, [m]',size=14) 
        axis.annotate('450 EFPD', xy=(1.5, 0.025),size=16,color=[0.5,0.5,0.5]) 
        #axis.annotate('50 EFPD', xy=(1.5, -0.006),size=16,color=[0.5,0.5,0.5])
        l=legend([ph[0],ph[1],ph[2]],["case 1","case 2","case 3"],loc=3)
        axis.set_xlim([0,3.6576])
        tight_layout()
        
        savefig('V:\\master report\\figures\\linpowrel1.pdf')
        axis.set_title('Relative difference in linear power of cases 1-3 to case 0',size=18)
        tight_layout()
        savefig('D:\dropbox\Dropbox\plots\case0\linpowrel1.png')  
        show()        
        
        
        
if 3 in plotcase:        
        
        
    if 1 in subcase:    # plutonium buildup over cycle
        plt.figure()
        axis=plt.subplot(111)
        lh=[0]*10

        for i in range(10):
            c = cm.jet((i)/10,1)
            lh[i],=step(z_mesh,Stepper(PuDens(tpu[1,i,:,:,:,0],3),0),color=c,where='post')
            step(z_mesh,Stepper(PuDens(tpu[1,i,:,:,:,1],3),0),color=c,where='post')        
            
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
        savefig('V:\\master report\\figures\\Pu_buildup1.pdf')
        axis.set_title('Pu 239 and 241 buildup over cycle\n case 1',size=18)
        savefig('D:\dropbox\Dropbox\plots\case1\Pu_buildup.png')        
        
        
        plt.figure()   # u235 depletion case 0
        axis=plt.subplot(111)
        lh=[0]*10
        for i in range(10):
            c = cm.jet((i)/10,1)
            lh[i],=step(z_mesh,Stepper(PuDens(tpu[1,i,:,:,:,2],3),0),color=c,where='post')
        #    plot(z_mesh[1:],tpu[1,i,2,0,:,3]/100,color=c)        
            
        axis.set_xlim([0,3.6576])
        #axis.set_ylim([500,1100])
        
        axis.xaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.yaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.ticklabel_format(style='sci', scilimits=(0,0), axis='y')
        axis.set_ylabel('U concentration, [1/(barn cm)]' ,size=14)
        axis.set_xlabel('axial position, [m]',size=14) 
        axis.set_title('U235 depletion over cycle\n case 1',size=18)    
        l=legend([lh[0],lh[-1]],["50 EFPD","500 EFPD"],loc=2)    
        #axis.annotate('U235', xy=(2.5, 0.00015),size=16,alpha=0.5)
        #axis.annotate('U238', xy=(2.5, 0.00003),size=16,alpha=0.5)        
        show() 
        savefig('D:\dropbox\Dropbox\plots\case1\U235_depletion.png')
        
    if 1.5 in subcase:
        
        plt.figure()
        axis=plt.subplot(111)
        lh=[[0,0],[0,0]]
        case=[0,9]
        c=['b', 'g', 'r']
        for i in range(len(case)):
            c = cm.jet((case[i])/10,1)
            lh[i][0],=step(z_mesh,Stepper(PuDens(tpu[1,case[i],:,:,:,0],3),0),color=c,where='post')
            lh[i][1],=step(z_mesh,Stepper(PuDens(tpu[0,case[i],:,:,:,0],30),0),ls=':',color=c,where='post')        
            
            dif=(PuDens(tpu[1,case[i],:,:,:,0],3)-PuDens(tpu[0,case[i],:,:,:,0],30))/PuDens(tpu[0,case[i],:,:,:,0],30)
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
        l=legend([lh[1][0],lh[0][0],lh[1][1],lh[0][1]],["case 1","case 1","case 0","case 0"],loc=5)    
        axis.annotate( '50 EFPD', xy=(1, 0.00003),size=16,color=[0.5,0.5,0.5])
        axis.annotate( '500 EFPD', xy=(1, 0.00012),size=16,color=[0.5,0.5,0.5])
         
        
        savefig('V:\\master report\\figures\\Pu_buildup1_1_5.pdf')
        axis.set_title('Pu 239 buildup at 50 & 500 EFPD\n case 1 and 0',size=18)
        tight_layout()
        savefig('D:\dropbox\Dropbox\plots\case1\Pu_buildup1.5.png')            
        show()
        
    if 1.6 in subcase:
        figure()
        axis=plt.subplot(111)
        
        ph=[0,0,0]
        c=['b', 'g', 'r','c']
        ii=[8]
        ls1=['--','-']
        
        for i in range(len(ii)):
        
            ph[0],=step(z_mesh,Stepper((PuDens(tpu[1,ii[i],:,:,:,0],3)-PuDens(tpu[0,ii[i],:,:,:,0],30))/PuDens(tpu[0,ii[i],:,:,:,0],30),0),color='b',where='post',zorder=10)
            ph[1],=step(z_mesh,Stepper((PuDens(tpu[2,ii[i],:,:,:,0],3)-PuDens(tpu[0,ii[i],:,:,:,0],30))/PuDens(tpu[0,ii[i],:,:,:,0],30),0),color='g',where='post',zorder=9)
            ph[2],=step(z_mesh,Stepper((PuDens(tpu[3,ii[i],:,:,:,0],3)-PuDens(tpu[0,ii[i],:,:,:,0],30))/PuDens(tpu[0,ii[i],:,:,:,0],30),0),color='r',where='post',zorder=8)
            #step(z_mesh,Stepper((PuDens(tpu[1,case[i],:,:,:,0],3)-PuDens(tpu[0,case[i],:,:,:,0],30))/PuDens(tpu[0,case[i],:,:,:,0],30),0),where='post')
        axis.yaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.xaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.set_ylabel('relative difference, [-]' ,size=14)
        axis.set_xlabel('axial position, [m]',size=14) 
        axis.annotate('450 EFPD', xy=(0.5, -0.003),size=16,color=[0.5,0.5,0.5]) 
        #axis.annotate('50 EFPD', xy=(1.5, -0.006),size=16,color=[0.5,0.5,0.5])
        l=legend(["case 1","case 2","case 3"],loc=4)
        plt.axhline(y=0,color=[0.5,0.5,0.5])
        axis.set_xlim([0,3.6576])
        tight_layout()
        savefig('V:\\master report\\figures\\purel123.pdf')
        axis.set_title('Difference in Pu-239 buildup\n of cases 1-3 to case 0/450',size=18)
        set_fontsize([manager.canvas.figure for manager in matplotlib._pylab_helpers.Gcf.get_all_fig_managers()][0],beamerfontsize)
        tight_layout()
        
        show() 
        
    if 1.61 in subcase:
        figure()
        axis=plt.subplot(111)
        
        ph=[0,0,0]
        c=['b', 'g', 'r','c']
        ii=[8]
        ls1=['--','-']
        
        for i in range(len(ii)):
        
            ph[0],=step(z_mesh,Stepper((PuDens(tpu[0,ii[i],:,:,:,0],30)-PuDens(tpu[1,ii[i],:,:,:,0],3))/PuDens(tpu[1,ii[i],:,:,:,0],3)*100,0),color='b',where='post',zorder=10)
            ph[1],=step(z_mesh,Stepper((PuDens(tpu[2,ii[i],:,:,:,0],3)-PuDens(tpu[1,ii[i],:,:,:,0],3))/PuDens(tpu[1,ii[i],:,:,:,0],3)*100,0),color='g',where='post',zorder=9)
            ph[2],=step(z_mesh,Stepper((PuDens(tpu[3,ii[i],:,:,:,0],3)-PuDens(tpu[1,ii[i],:,:,:,0],3))/PuDens(tpu[1,ii[i],:,:,:,0],3)*100,0),color='r',where='post',zorder=8)
            #step(z_mesh,Stepper((PuDens(tpu[1,case[i],:,:,:,0],3)-PuDens(tpu[0,case[i],:,:,:,0],30))/PuDens(tpu[0,case[i],:,:,:,0],30),0),where='post')
        axis.yaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.xaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.set_ylabel('relative difference, [$\%$]' ,size=14)
        axis.set_xlabel('axial position, [m]',size=14) 
        #axis.annotate('450 EFPD', xy=(0.5, -0.003),size=16,color=[0.5,0.5,0.5]) 
        #axis.annotate('50 EFPD', xy=(1.5, -0.006),size=16,color=[0.5,0.5,0.5])
        l=legend(["case A0","case A2","case A3"],loc=3)
        plt.axhline(y=0,color=[0.5,0.5,0.5])
        axis.set_xlim([0,3.6576])
        tight_layout()

        axis.set_title('Difference in Pu239 Concentration\n relative to to case A1, 450 EFPD',size=18)
        set_fontsize([manager.canvas.figure for manager in matplotlib._pylab_helpers.Gcf.get_all_fig_managers()][0],beamerfontsize)
        tight_layout()
        savefig('V:\\master report\\figures\\purel123beamer.pdf')
        show() 
    if 1.62 in subcase:
        figure()
        axis=plt.subplot(111)
        
        ph=[0,0,0]
        c=['b', 'g', 'r','c']
        ii=[8]
        ls1=['--','-']
        
        for i in range(len(ii)):
        
            #ph[0],=step(z_mesh,Stepper((PuDens(tpu[1,ii[i],:,:,:,0],3)-PuDens(tpu[0,ii[i],:,:,:,0],30))/PuDens(tpu[0,ii[i],:,:,:,0],30),0),color='b',where='post',zorder=10)
            ph[1],=step(z_mesh,Stepper((PuDens(tpu[2,ii[i],:,:,:,0],3)-PuDens(tpu[1,ii[i],:,:,:,0],3))/PuDens(tpu[1,ii[i],:,:,:,0],3),0),color='g',where='post',zorder=9)
            ph[2],=step(z_mesh,Stepper((PuDens(tpu[3,ii[i],:,:,:,0],3)-PuDens(tpu[1,ii[i],:,:,:,0],3))/PuDens(tpu[2,ii[i],:,:,:,0],3),0),color='r',where='post',zorder=8)
            #step(z_mesh,Stepper((PuDens(tpu[1,case[i],:,:,:,0],3)-PuDens(tpu[0,case[i],:,:,:,0],30))/PuDens(tpu[0,case[i],:,:,:,0],30),0),where='post')
        axis.yaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.xaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.set_ylabel('relative difference, [-]' ,size=14)
        axis.set_xlabel('axial position, [m]',size=14) 
        axis.annotate('450 EFPD', xy=(0.5, -0.003),size=16,color=[0.5,0.5,0.5]) 
        #axis.annotate('50 EFPD', xy=(1.5, -0.006),size=16,color=[0.5,0.5,0.5])
        l=legend(["case A2","case A3"],loc=4)
        plt.axhline(y=0,color=[0.5,0.5,0.5])
        axis.set_xlim([0,3.6576])
        tight_layout()
        savefig('V:\\master report\\figures\\purel123paper.png')
        #axis.set_title('Difference in Pu-239 buildup\n of cases 1-3 to case 0/450',size=18)
        set_fontsize([manager.canvas.figure for manager in matplotlib._pylab_helpers.Gcf.get_all_fig_managers()][0],beamerfontsize)
        tight_layout()
        
        show() 

        
    if 4.5 in subcase:
      
        j=8 #burn up set
        k=24# z-plane 
        
        figure()
        axis=plt.subplot(111)
        r3=np.sqrt(np.linspace(0,3,4)/3)*0.004025
        r30=np.sqrt(np.linspace(0,30,31)/30)*0.004025
        for i in range(3):
            a,=plt.bar(r3[i]*1000,tpu[1,j,i,0,k,0],(r3[i+1]-r3[i])*1000,0,color='red',edgecolor='black',alpha=0.3)
        
        for i in range(30):
            b,=plt.bar(r30[i]*1000,tpu[0,j,i,0,k,0],(r30[i+1]-r30[i])*1000,0,color='blue',edgecolor='black',alpha=0.3)
        axis.xaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.yaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.set_ylabel('Pu239 concentration, [1/(barn cm)]' ,size=14)
        axis.set_xlabel('radial position, [mm]',size=14) 
        axis.set_xlim([0,4.025])
        l=legend([a,b],["case 1","case 0",],loc=2)         
        axis.ticklabel_format(style='sci', scilimits=(0,0), axis='y')
        c=sum(tpu[1,j,:,0,k,0])*0.004025**2/3
        d=sum(tpu[0,j,:,0,k,0])*0.004025**2/30
        #e=(c-d)/d*100
        
        #axis.annotate( '{0} % difference\n in Pu 239 mass'.format("%.2f" % e) , xy=(0.0005, 0.00025),size=14)
        
        
        savefig('V:\\master report\\figures\\radial_Pu01.pdf')
        axis.set_title('The Rim Effect at 450 EFPD',size=18)
        set_fontsize([manager.canvas.figure for manager in matplotlib._pylab_helpers.Gcf.get_all_fig_managers()][0],beamerfontsize)	
        tight_layout()
        savefig('V:\\master report\\figures\\radial_Pu01beamer.pdf')
   
        show()
        
    if 4.6 in subcase:
      
        j=8 #burn up set
        k=24# z-plane 
        
        figure()
        axis=plt.subplot(111)
        r3=np.sqrt(np.linspace(0,3,4)/3)*0.004025
        r30=np.sqrt(np.linspace(0,30,31)/30)*0.004025
        for i in range(30):
            
            b,=plt.bar(r30[i]*1000,(tpu[0,j,i,0,k,0]),(r30[i+1]-r30[i])*1000,0,color='blue',edgecolor='black',alpha=0.3)
        ax2 = twinx()    
        
        for i in range(30):
            a,=plt.bar(r30[i]*1000,(tpu[0,j,i,0,k,0]-tpu[8,j,i,0,k,0])/tpu[0,j,i,0,k,0]*100,(r30[i+1]-r30[i])*1000,0,color='red',edgecolor='black',alpha=0.3)
        
        #for i in range(30):
        #    b,=plt.bar(r30[i]*1000,tpu[8,j,i,0,k,0],(r30[i+1]-r30[i])*1000,0,color='blue',edgecolor='black',alpha=0.3)
        axis.xaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.yaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.set_ylabel('Pu239 concentration, [1/(barn cm)]' ,size=14)
        ax2.set_ylabel('relative difference, [$\%$]' ,size=14)
        axis.set_xlabel('radial position, [mm]',size=14) 
        axis.set_xlim([0,4.025])
        l=legend([b,a],["case 0","deviation of case 8",],loc=2)         
        axis.ticklabel_format(style='sci', scilimits=(0,0), axis='y')
        ax2.ticklabel_format(style='sci', scilimits=(0,0), axis='y')
        c=sum(tpu[1,j,:,0,k,0])*0.004025**2/3
        d=sum(tpu[0,j,:,0,k,0])*0.004025**2/30    
        axis.set_title('The relativve difference in radial Pu 239 prediction for\n case 0 (cfd) and case 8 (subchannel)')
        show()
        savefig('D:\\dropbox\\Dropbox\\plots\\case8\\radial relative difference.png')
        savefig('D:\\dropbox\\Dropbox\\plots\\case8\\radial relative difference.pdf')