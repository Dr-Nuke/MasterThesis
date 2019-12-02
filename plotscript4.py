from __future__ import division
import math as m
import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.path import Path
from matplotlib.colors import LogNorm
from mpl_toolkits.axes_grid.axes_grid  import AxesGrid
from mpl_toolkits.axes_grid.anchored_artists import AnchoredText
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

def Crudder(a):
    """
    returns the azimuthally averaged values of crud
    a=tcrd[i,j,:,:,m]
    """
    return sum(a,0)

C=4
if 1 in plotcase:
    if 1 in subcase: #linear power profile
    
    
        figure()
        axis=plt.subplot(111)
        
        ph=[[0,0],[0,0]]
        c=['b', 'g', 'r']
        ii=[0,9]
        for i in range(len(ii)):
           
            ph[i][0],=step(z_mesh,Stepper(LinPow(tp,1,ii[i]),0)/1000,color='b',where='post')
            ph[i][1],=step(z_mesh,Stepper(LinPow(tp,C,ii[i]),0)/1000,lw=2,color='g',where='post')
            
            a=max(abs((LinPow(tp,C,ii[i])-LinPow(tp,1,ii[i]))/LinPow(tp,1,ii[i])))
            print 'maximum linear power (1,1) deviation for bu='+str((ii[i]+1)*50)+': '+str(a)
        axis.yaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.xaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.set_ylabel('linear Power, [kW/m]' ,size=14)
        axis.set_xlabel('axial position, [m]',size=14) 
        axis.annotate('50 EFPD', xy=(0.6, 36),size=16,color=[0.5,0.5,0.5]) 
        axis.annotate('500 EFPD', xy=(1.6, 26),size=16,color=[0.5,0.5,0.5]) 
        l=legend([ph[0][0],ph[0][1]],["case 1","case {0}".format(C)],loc=1)
        axis.set_xlim([0,3.6576])
        
        ##savefig('V:\\master report\\figures\\powercycle{0}.pdf'.format(C))
        #axis.set_title('Linear Power development with burnup \n case 1 and {0}'.format(C),size=18)    
        #tight_layout()
        ##savefig('D:\\dropbox\\Dropbox\\plots\\case{0}\\powercycle.png'.format(C))
        #axis.set_ylim([500,1200])    
        show()  
        
        
    if 1.5 in subcase: #relative linpow diff
        for iii in [0,9]:
            figure()
            axis=plt.subplot(111)
            plt.axhline(y=0,color=[0.5,0.5,0.5])
            ph=[0,0,0,0]
            c=['b', 'g', 'r','c']
            ii=[iii]
            ls1=['-','-']
            for i in range(len(ii)):
            
                ph[0],=step(z_mesh,Stepper((LinPow(tp,4,ii[i])-LinPow(tp,0,ii[i]))/LinPow(tp,0,ii[i]),0),ls=ls1[i],color='b',where='post')
                ph[1],=step(z_mesh,Stepper((LinPow(tp,5,ii[i])-LinPow(tp,0,ii[i]))/LinPow(tp,0,ii[i]),0),ls=ls1[i],color='g',where='post')
                ph[2],=step(z_mesh,Stepper((LinPow(tp,6,ii[i])-LinPow(tp,0,ii[i]))/LinPow(tp,0,ii[i]),0),ls=ls1[i],color='r',where='post')
                ph[3],=step(z_mesh,Stepper((LinPow(tp,7,ii[i])-LinPow(tp,0,ii[i]))/LinPow(tp,0,ii[i]),0),ls=ls1[i],color='c',where='post')
                #step(z_mesh,Stepper((PuDens(tpu[1,case[i],:,:,:,0],3)-PuDens(tpu[0,case[i],:,:,:,0],30))/PuDens(tpu[0,case[i],:,:,:,0],30),0),where='post')
            axis.yaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
            axis.xaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
            axis.set_ylabel('relative difference, [-]' ,size=14)
            axis.set_xlabel('axial position, [m]',size=14) 
            axis.annotate('500 EFPD', xy=(1.5, 0.028),size=16,color=[0.5,0.5,0.5]) 
            #axis.annotate('50 EFPD', xy=(1.5, -0.006),size=16,color=[0.5,0.5,0.5])
            l=legend([ph[0],ph[1],ph[2],ph[3]],["case 4","case 5","case 6","case 7"],loc=1)
            axis.set_xlim([0,3.6576])
            tight_layout()
            
            #savefig('V:\\master report\\figures\\linpowrel4.pdf')
            axis.set_title('Relative difference in linear power of cases 4-7 to case 0',size=18)
            tight_layout()
            #savefig('D:\dropbox\Dropbox\plots\case4\linpowrel4.png')  
            show()           

    if 2 in subcase:
        print shape(tp)
        figure('powercycle4')
        plt.clf()
        axis=plt.subplot(111)
        
        ph=[0]*29
        ii=[0,6,8,11,14,17,20,23,26,29]
        for i in range(len(ii)):
            c = cm.jet((i)/len(ii),1)
            ph[i],=step(z_mesh,Stepper(LinPow(tp,4,ii[i]),0)/1000,color=c,where='post',label='{} EFPD'.format(ts[ii[i]]))
        axis.yaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.xaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.set_ylabel('linear Power, [kW/m]' ,size=14)
        axis.set_xlabel('axial position, [m]',size=14) 
          
        l=legend(loc=8,ncol=2)
        axis.set_xlim([0,3.6576])
        tight_layout()
        #savefig('V:\\master report\\figures\\powercycle{0}.pdf'.format(C))
        #axis.set_title('Linear Power development with burnup \n case {0}'.format(C),size=18)   
        tight_layout()    
        savefig('D:/dropbox/Dropbox/plots/spring2013/powercycle_case4.pdf'.format(C))
        #axis.set_ylim([500,1200])    
    show()                
        
if 3 in plotcase:        
        
        
    if 1 in subcase:    # plutonium buildup over cycle
        plt.figure()
        axis=plt.subplot(111)
        lh=[0]*10

        for i in range(10):
            c = cm.jet((i)/10,1)
            lh[i],=step(z_mesh,Stepper(PuDens(tpu[C,i,:,:,:,0],3),0),color=c,where='post')
            step(z_mesh,Stepper(PuDens(tpu[C,i,:,:,:,1],3),0),color=c,where='post')        
            
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
        #savefig('V:\\master report\\figures\\Pu_buildup{0}.pdf'.format(C))
        axis.set_title('Pu 239 and 241 buildup over cycle\n case {0}'.format(C),size=18)
        #savefig('D:\dropbox\Dropbox\plots\case{0}\Pu_buildup.png'.format(C))        
        
        
        plt.figure()   # u235 depletion
        axis=plt.subplot(111)
        lh=[0]*10
        for i in range(10):
            c = cm.jet((i)/10,1)
            lh[i],=step(z_mesh,Stepper(PuDens(tpu[C,i,:,:,:,2],3),0),color=c,where='post')
        #    plot(z_mesh[1:],tpu[1,i,2,0,:,3]/100,color=c)        
            
        axis.set_xlim([0,3.6576])
        #axis.set_ylim([500,1100])
        
        axis.xaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.yaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.ticklabel_format(style='sci', scilimits=(0,0), axis='y')
        axis.set_ylabel('U concentration, [1/(barn cm)]' ,size=14)
        axis.set_xlabel('axial position, [m]',size=14) 
        axis.set_title('U235 depletion over cycle\n case 4',size=18)    
        l=legend([lh[0],lh[-1]],["50 EFPD","500 EFPD"],loc=2)    
        #axis.annotate('U235', xy=(2.5, 0.00015),size=16,alpha=0.5)
        #axis.annotate('U238', xy=(2.5, 0.00003),size=16,alpha=0.5)        
        show() 
        #savefig('D:\dropbox\Dropbox\plots\case{0}\U235_depletion.png'.format(C))
        
    if 1.5 in subcase:
        
        plt.figure()
        axis=plt.subplot(111)
        lh=[[0,0],[0,0]]
        case=[0,9]
        c=['b', 'g', 'r']
        for i in range(len(case)):
            c = cm.jet((case[i])/10,1)
            lh[i][0],=step(z_mesh,Stepper(PuDens(tpu[C,case[i],:,:,:,0],3),0),color=c,where='post')
            lh[i][1],=step(z_mesh,Stepper(PuDens(tpu[1,case[i],:,:,:,0],3),0),ls=':',color=c,where='post')        
            
            dif=(PuDens(tpu[C,case[i],:,:,:,0],3)-PuDens(tpu[1,case[i],:,:,:,0],3))/PuDens(tpu[1,case[i],:,:,:,0],3)
            print 'maximum z-plane-Pu (1,1.5) deviation for bu='+str((case[i]+1)*50)+': '+str(max(abs(dif)))
            
            
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
        l=legend([lh[1][0],lh[0][0],lh[1][1],lh[0][1]],["case {0}".format(C),"case {0}".format(C),"case 1","case 1"],loc=5)    
        axis.annotate( '50 EFPD', xy=(1, 0.00003),size=16,color=[0.5,0.5,0.5])
        axis.annotate( '500 EFPD', xy=(1, 0.00012),size=16,color=[0.5,0.5,0.5])
         
        
        #savefig('V:\\master report\\figures\\Pu_buildup{0}_1_5.pdf'.format(C))
        axis.set_title('Pu 239 buildup at 50 & 500 EFPD\n case {0} and 1'.format(C),size=18)
        tight_layout()
        #savefig('D:\dropbox\Dropbox\plots\case{0}\Pu_buildup1.5.png'.format(C))            
        show()
    if 1.6 in subcase:
        figure()
        axis=plt.subplot(111)
        
        ph=[0,0,0,0]
        c=['b', 'g', 'r','c']
        ii=[8]
        ls1=['--','-']
        
        for i in range(len(ii)):
        
            ph[0],=step(z_mesh,Stepper((PuDens(tpu[4,ii[i],:,:,:,0],3)-PuDens(tpu[1,ii[i],:,:,:,0],3))/PuDens(tpu[1,ii[i],:,:,:,0],3),0),color='b',where='post',zorder=10)
            ph[1],=step(z_mesh,Stepper((PuDens(tpu[5,ii[i],:,:,:,0],3)-PuDens(tpu[1,ii[i],:,:,:,0],3))/PuDens(tpu[1,ii[i],:,:,:,0],3),0),color='g',where='post',zorder=9)
            ph[2],=step(z_mesh,Stepper((PuDens(tpu[7,ii[i],:,:,:,0],3)-PuDens(tpu[1,ii[i],:,:,:,0],3))/PuDens(tpu[1,ii[i],:,:,:,0],3),0),color='r',where='post',zorder=8)
            #ph[3],=step(z_mesh,Stepper((PuDens(tpu[7,ii[i],:,:,:,0],3)-PuDens(tpu[1,ii[i],:,:,:,0],3))/PuDens(tpu[1,ii[i],:,:,:,0],3),0),color='c',where='post')
            #step(z_mesh,Stepper((PuDens(tpu[1,case[i],:,:,:,0],3)-PuDens(tpu[0,case[i],:,:,:,0],30))/PuDens(tpu[0,case[i],:,:,:,0],30),0),where='post')
        axis.yaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.xaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.set_ylabel('relative difference, [-]' ,size=14)
        axis.set_xlabel('axial position, [m]',size=14) 
        axis.annotate('500 EFPD', xy=(0.5, -0.003),size=16,color=[0.5,0.5,0.5]) 
        #axis.annotate('50 EFPD', xy=(1.5, -0.006),size=16,color=[0.5,0.5,0.5])
        l=legend(["case 4","case 5","case 6","case 7"],loc=2)
        plt.axhline(y=0,color=[0.5,0.5,0.5])
        axis.set_xlim([0,3.6576])
        tight_layout()
        #savefig('V:\\master report\\figures\\purel467.pdf')
        axis.set_title('Relative difference in Pu239 buildup of cases 4-7 to case 1',size=18)
        tight_layout()
        #savefig('D:\dropbox\Dropbox\plots\case0\purel456.png')  
        show()        
        
    if 1.61 in subcase:
        close('all')
        figure()
        axis=plt.subplot(111)
        
        ph=[0,0,0,0]
        c=['b', 'g', 'r','c']
        ii=[8]
        ls1=['--','-']
        
        for i in range(len(ii)):
        
            #ph[0],=step(z_mesh,Stepper((PuDens(tpu[4,ii[i],:,:,:,0],3)-PuDens(tpu[1,ii[i],:,:,:,0],3))/PuDens(tpu[1,ii[i],:,:,:,0],3),0),color='b',where='post',zorder=10)
            ph[1],=step(z_mesh,Stepper((PuDens(tpu[5,ii[i],:,:,:,0],3)-PuDens(tpu[4,ii[i],:,:,:,0],3))/PuDens(tpu[4,ii[i],:,:,:,0],3),0)*100,color='b',where='post',zorder=9,label='case B2')
            ph[1],=step(z_mesh,Stepper((PuDens(tpu[1,ii[i],:,:,:,0],3)-PuDens(tpu[4,ii[i],:,:,:,0],3))/PuDens(tpu[4,ii[i],:,:,:,0],3),0)*100,color='g',where='post',zorder=9,label='case A1')
            #ph[2],=step(z_mesh,Stepper((PuDens(tpu[7,ii[i],:,:,:,0],3)-PuDens(tpu[1,ii[i],:,:,:,0],3))/PuDens(tpu[1,ii[i],:,:,:,0],3),0),color='r',where='post',zorder=8)
            #ph[3],=step(z_mesh,Stepper((PuDens(tpu[7,ii[i],:,:,:,0],3)-PuDens(tpu[1,ii[i],:,:,:,0],3))/PuDens(tpu[1,ii[i],:,:,:,0],3),0),color='c',where='post')
            #step(z_mesh,Stepper((PuDens(tpu[1,case[i],:,:,:,0],3)-PuDens(tpu[0,case[i],:,:,:,0],30))/PuDens(tpu[0,case[i],:,:,:,0],30),0),where='post')
        axis.yaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.xaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.set_ylabel('relative difference, [$\%$]' ,size=14)
        axis.set_xlabel('axial position, [m]',size=14) 
        #axis.annotate('500 EFPD', xy=(0.5, -0.003),size=16,color=[0.5,0.5,0.5]) 
        #axis.annotate('50 EFPD', xy=(1.5, -0.006),size=16,color=[0.5,0.5,0.5])
        l=legend(loc=2)
        plt.axhline(y=0,color=[0.5,0.5,0.5])
        axis.set_xlim([0,3.6576])
        tight_layout()
        
        axis.set_title('Difference in Pu239 Buildup relative to Case B1',size=18)
        set_fontsize([manager.canvas.figure for manager in matplotlib._pylab_helpers.Gcf.get_all_fig_managers()][0],beamerfontsize)        
        tight_layout()

        show()        
        #savefig('V:\\master report\\figures\\purel467beamer.pdf')

    if 1.62 in subcase:
        figure()
        axis=plt.subplot(111)
        
        ph=[0,0,0,0]
        c=['b', 'g', 'r','c']
        ii=[8]
        ls1=['--','-']
        
        for i in range(len(ii)):
        
            ph[0],=step(z_mesh,Stepper((PuDens(tpu[4,ii[i],:,:,:,0],3)-PuDens(tpu[1,ii[i],:,:,:,0],3))/PuDens(tpu[1,ii[i],:,:,:,0],3),0),color='b',where='post',zorder=10)
            ph[1],=step(z_mesh,Stepper((PuDens(tpu[5,ii[i],:,:,:,0],3)-PuDens(tpu[1,ii[i],:,:,:,0],3))/PuDens(tpu[1,ii[i],:,:,:,0],3),0),color='g',where='post',zorder=9)
            ph[2],=step(z_mesh,Stepper((PuDens(tpu[7,ii[i],:,:,:,0],3)-PuDens(tpu[1,ii[i],:,:,:,0],3))/PuDens(tpu[1,ii[i],:,:,:,0],3),0),color='r',where='post',zorder=8)
            #ph[3],=step(z_mesh,Stepper((PuDens(tpu[7,ii[i],:,:,:,0],3)-PuDens(tpu[1,ii[i],:,:,:,0],3))/PuDens(tpu[1,ii[i],:,:,:,0],3),0),color='c',where='post')
            #step(z_mesh,Stepper((PuDens(tpu[1,case[i],:,:,:,0],3)-PuDens(tpu[0,case[i],:,:,:,0],30))/PuDens(tpu[0,case[i],:,:,:,0],30),0),where='post')
        axis.yaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.xaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.set_ylabel('relative difference, [-]' ,size=14)
        axis.set_xlabel('axial position, [m]',size=14) 
        axis.annotate('500 EFPD', xy=(0.5, -0.003),size=16,color=[0.5,0.5,0.5]) 
        #axis.annotate('50 EFPD', xy=(1.5, -0.006),size=16,color=[0.5,0.5,0.5])
        l=legend(["case B4","case B5","case B6","case B7"],loc=2)
        plt.axhline(y=0,color=[0.5,0.5,0.5])
        axis.set_xlim([0,3.6576])
        tight_layout()
        #savefig('V:\\master report\\figures\\purel467paper.png')
        #axis.set_title('Relative difference in Pu239 buildup of cases 4-7 to case 1',size=18)
        tight_layout()
        #savefig('D:\dropbox\Dropbox\plots\case0\purel456paper.png')  
        show()          
        
    if 1.7 in subcase:
        figure()
        axis=plt.subplot(111)
        
        ph=[0,0,0,0]
        c=['b', 'g', 'r','c']
        ii=[9]
        ls1=['--','-']
        
        for i in range(len(ii)):
        
            ph[0],=step(z_mesh,Stepper((PuDens(tpu[C,ii[i],:,:,:,0],3)-PuDens(tpu[1,ii[i],:,:,:,0],3))/PuDens(tpu[1,ii[i],:,:,:,0],3),0),where='post',label='case 4')
            ph[0],=step(z_mesh,Stepper((PuDens(tpu[5,ii[i],:,:,:,0],3)-PuDens(tpu[1,ii[i],:,:,:,0],3))/PuDens(tpu[1,ii[i],:,:,:,0],3),0),where='post',label='case 5')
            #step(z_mesh,Stepper((PuDens(tpu[1,case[i],:,:,:,0],3)-PuDens(tpu[0,case[i],:,:,:,0],30))/PuDens(tpu[0,case[i],:,:,:,0],30),0),where='post')
        axis.yaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.xaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.set_ylabel('relative difference, [-]' ,size=14)
        axis.set_xlabel('axial position, [m]',size=14) 
        axis.annotate('500 EFPD', xy=(0.5, -0.003),size=16,color=[0.5,0.5,0.5]) 
        #axis.annotate('50 EFPD', xy=(1.5, -0.006),size=16,color=[0.5,0.5,0.5])
        legend(loc=2)
        plt.axhline(y=0,color=[0.5,0.5,0.5])
        axis.set_xlim([0,3.6576])
        tight_layout()
        #savefig('V:\\master report\\figures\\purel4.pdf')
        axis.set_title('Relative difference in Pu239 buildup of case 4 to case 1',size=18)
        tight_layout()
        #savefig('D:\dropbox\Dropbox\plots\case0\purel4.png')  
        show()    
        
    if 4.5 in subcase: #radial pu
      
        j=9 #burn up set
        k=24# z-plane 
        
        figure()
        axis=plt.subplot(111)
        r3=np.sqrt(np.linspace(0,3,4)/3)*0.004025
        r30=np.sqrt(np.linspace(0,30,31)/30)*0.004025
        for i in range(3):
            a,=plt.bar(r3[i]*1000,tpu[C,j,i,0,k,0],(r3[i+1]-r3[i])*1000,0,color='red',edgecolor='black',alpha=0.3)
        
        for i in range(3):
            b,=plt.bar(r3[i]*1000,tpu[1,j,i,0,k,0],(r3[i+1]-r3[i])*1000,0,color='blue',edgecolor='black',alpha=0.3)
        axis.xaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.yaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.set_ylabel('Pu239 concentration, [1/(barn cm)]' ,size=14)
        axis.set_xlabel('radial position, [mm]',size=14) 
        axis.set_xlim([0,4.025])
        l=legend([a,b],["case {0}".format(C),"case 1",],loc=2)         
        axis.ticklabel_format(style='sci', scilimits=(0,0), axis='y')
        c=sum(tpu[1,j,:,0,k,0])*0.004025**2/3
        d=sum(tpu[0,j,:,0,k,0])*0.004025**2/30
        e=(c-d)/d*100
        
        #axis.annotate( '{0} % difference\n in Pu 239 mass'.format("%.2f" % e) , xy=(0.0005, 0.00025),size=14)
        
        
        #savefig('V:\\master report\\figures\\radial_Pu1{0}.pdf'.format(C))
        axis.set_title('Radial Pu 239 distribution for 500 EFPD\n case 1 and {0}, at z=1.8m'.format(C),size=18)    
        tight_layout()
        #savefig('D:\\dropbox\\Dropbox\\plots\\case{0}\\radial_Pu.png'.format(C))    
        show()
        
if 4 in plotcase: # flux plots


    if 9 in subcase:        # 2 fold tilt plot
        figure()
        bu=8
        axis=subplot2grid((2, 4), (0, 0),colspan=3)
        fluxnorm=zeros(47)
        fluxnorm=sum(tnflx[1][bu,2,0,:,:],0) # normalisation
            
        ind=range(0,47,3)   
        lh=[0]*len(ind)    
        for i in reversed(range(len(ind))):
            c = cm.jet((ind[i])/47,1)
            lh[i],=plot(Btwn(z_mesh),tnflx[1][bu,2,0,:,ind[i]]/fluxnorm[ind[i]]/0.025,label='group '+ str(ind[i]+1),color=c)   
        handles, labels = axis.get_legend_handles_labels()
        #legend(handles[::-1],labels[::-1],loc=8, borderaxespad=0.,ncol=2)  

        axis.set_ylabel('normalized Flux' ,size=14)
        #axis.set_xlabel('axial position, [m]',size=14) 
        axis.xaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.yaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])  
        axis.set_xlim([0,3.6576])
        axis.set_ylim([0,1.1])
        legend(handles[::-1],labels[::-1],bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        #axis.annotate('50 EFPD', xy=(2.5, 0.2),size=14,color=[0.5,0.5,0.5])
        axis.annotate('case 1', xy=(2, 0.2),size=14,alpha=0.5)
        
        axis=subplot2grid((2, 4), (1, 0),colspan=3)
        fluxnorm=zeros(47)
        fluxnorm=sum(tnflx[C][bu,2,0,:,:],0) # normalisation
            
        ind=range(0,47,3)   
        lh=[0]*len(ind)    
        for i in reversed(range(len(ind))):
            c = cm.jet((ind[i])/47,1)
            lh[i],=plot(Btwn(z_mesh),tnflx[C][bu,2,0,:,ind[i]]/fluxnorm[ind[i]]/0.025,label='group '+ str(ind[i]+1),color=c)   
        handles, labels = axis.get_legend_handles_labels()
        
        axis.set_ylabel('normalized Flux' ,size=14)
        
        axis.set_xlabel('axial position, [m]',size=14) 
        axis.xaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.yaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])  
        axis.set_xlim([0,3.6576])
        axis.set_ylim([0,1.1])
        axis.annotate('case 4', xy=(2, 0.2),size=14,alpha=0.5)
        plt.tight_layout()
        #savefig('V:\\master report\\figures\\Fluxtilt24.pdf')
        plt.figtext(0.5, 0.965,  'The Tilt of the neutron flux for different energies, case0+2',
               ha='center', color='black', weight='bold', size='large')
        tight_layout()
        #savefig('D:\dropbox\Dropbox\plots\case4\Fluxstilt24.png')
        show()  
if 6 in plotcase:
    # comparison plot between original and averaged tables. here: heat flux & clad temp    
    if 2 in subcase: 
        path ='D:/powertables/new/5flux/'
        grid_x,grid_y=np.mgrid[-pi:pi:100j,0:3.6576:400j]
        
        ex=(-pi,pi,0,3.6576)
        fig=plt.figure('cladtemp',figsize=[8,170])
        clf()
        ti=['averaged\n as sent to MAMBA & DeCART','original \n as written by StarCCM+']
        
        
        for en,i in enumerate(ts2): 
            files=['MAM_Hflux_5_0'+i+'.csv','MAM_Hflux_5_0'+i+'.csv.bak']
            #'MAM_Tke_5_0'+i+.csv,
            #'MAM_Tke_5_0'+i+.csv.bak]
            Tlist=[[],[]]    
            Flist=[[],[]] 
            Zlist=[[],[]] 
            Alist=[[],[]] 
            rowind=[[0   ,1,   2,   3,4],[0   ,1,      3,4,5]]
            
            for enum,j in enumerate(files):
                print j
                f_in = open(path+j)
                f_in.next()           # skip header
                reader = csv.reader(f_in,delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
                for row in reader:
                    T=row[rowind[enum][0]]
                    f=row[rowind[enum][1]]
                    x=row[rowind[enum][2]]
                    y=row[rowind[enum][3]]
                    z=row[rowind[enum][4]]
                    a=m.atan2(y,x)
                
                    Tlist[enum].append(T)        
                    Flist[enum].append(f)
                    Zlist[enum].append(z)
                    Alist[enum].append(a)         
                f_in.close()   

                # plotting        
        
                axis=plt.subplot(len(ts2),2,2*en+enum+1)
                grid_z=griddata((Alist[enum],Zlist[enum]),Tlist[enum],(grid_x,grid_y),method='linear')
                #grid_z=zeros([100,400])
                
                im=imshow(grid_z.T, interpolation='none',extent=ex, origin='lower', \
                clim=([580,640]),aspect=2)
                xticks([-np.pi,  0,  np.pi],[r'$-\pi$', r'$0$',  r'$+\pi$'])
                xticks([])
                if enum==0:
                    axis.set_yticks([0,1,2,3])
                    axis.set_ylabel('axial position, [m]')
                else:
                    axis.set_yticks([])
                
                if en == 29:
                    xticks([-np.pi,  0,  np.pi],[r'$-\pi$', r'$0$',  r'$+\pi$'])
                    axis.set_xlabel('azimuthal position, [rad]')
                
               
                if en==0:
                    axis.set_title(ti[enum]+'\n {} EFPD'.format(ts[en]))
                else:
                    axis.set_title('{} EFPD'.format(ts[en]))

        cax = fig.add_axes([0.1, 0.005, 0.8, 0.002])
        cb=fig.colorbar(im, cax=cax,ticks=[580,600,620,640],orientation='horizontal')  
        cb.set_label('cladding Temperature [deg C]')
        fig.subplots_adjust(top=0.98)
        fig.subplots_adjust(bottom=0.01)
        #fig.subplots_adjust(left=0.1)
        #fig.subplots_adjust(right=0.85)   
        fig.text(0.5,0.99,'Original and averaged cladding temperature, case 5',
        horizontalalignment='center',verticalalignment='top',size=14)
              
                
        show()  
        savefig('D:/dropbox/Dropbox/plots/spring2013/5_new/fluxandtemp/compare_orig_avg_TClad.pdf')
        close()
        
    if 2.5 in subcase: 
        
        ts3=ts2
        close('all')
        grid_x,grid_y=np.mgrid[-pi:pi:100j,0:3.6576:400j]
        
        ex=(-pi,pi,0,3.6576)
        
        fig=plt.figure('temp',figsize=[16,6*len(ts3)])
        
        fig=plt.figure('flux',figsize=[16,6*len(ts3)])
        clf()
        ti='averaged\n as sent to MAMBA '
        cases=[1,2,4,5,6]
        
        for enh,h in enumerate(cases):
            path ='D:/powertables/new/{}flux/'.format(h)
            for en,i in enumerate(ts3): 
                
                files='flux_'+str(h)+'_0'+str(i)+'.cpl'
                print path + files
                #'MAM_Tke_5_0'+i+.csv,
                #'MAM_Tke_5_0'+i+.csv.bak]
                Tlist=[]    
                Flist=[] 
                Alist=[]
                Zlist=[] 
                Anglist=[] 
                rowind=[[0   ,1,   2,   3,4],[0   ,1,      3,4,5]]
                rowind=[0,1,2,3,4,5] #T,HF,A,X,Y,Z

                f_in = open(path+files)
                f_in.next()           # skip header
                reader = csv.reader(f_in,delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
                for row in reader:
                    T=row[0]
                    f=row[1]
                    a=row[2]
                    x=row[3]
                    y=row[4]
                    z=row[5]
                    ang=m.atan2(y,x)
                
                    Tlist.append(T)        
                    Flist.append(f)
                    Alist.append(a)
                    Zlist.append(z)
                    Anglist.append(ang)         
                f_in.close()   
                
                # plotting        
                figure('temp')
                axis=plt.subplot(len(ts3),len(cases),len(cases)*en+enh+1)
                grid_z=griddata((Anglist,Zlist),Tlist,(grid_x,grid_y),method='linear')
                #grid_z=zeros([100,400])
                
                im=imshow(grid_z.T, interpolation='none',extent=ex, origin='lower', \
                clim=([580,640]),aspect=2)
                xticks([-np.pi,  0,  np.pi],[r'$-\pi$', r'$0$',  r'$+\pi$'])
                xticks([])
                #axis.set_title(str(h)+', '+str(i))
                if enh==0:
                    axis.set_yticks([0,1,2,3])
                    axis.set_ylabel('axial position, [m]')
               
                    
                else:
                    axis.set_yticks([])
                if enh==2:
                    axis.set_title('{} EFPD'.format(i))
                if en == 29:
                    xticks([-np.pi,  0,  np.pi],[r'$-\pi$', r'$0$',  r'$+\pi$'])
                    axis.set_xlabel('azimuthal position, [rad]')
                
                
                if en%5==0:
                    temptitle=axis.get_title()
                    axis.set_title('case {}\n'.format(h)+temptitle)

                    
                    
                # plotting        
                figure('flux')
                axis=plt.subplot(len(ts3),len(cases),len(cases)*en+enh+1)
                print len(ts3),len(cases),2*en+enh+1
                corr=1000000
                grid_z=griddata((Anglist,Zlist),Flist,(grid_x,grid_y),method='linear')/corr
                #grid_z=zeros([100,400])
                
                im=imshow(grid_z.T, interpolation='none',extent=ex, origin='lower', \
                clim=([0.8,1.5]),aspect=2)
                xticks([-np.pi,  0,  np.pi],[r'$-\pi$', r'$0$',  r'$+\pi$'])
                xticks([])
                #axis.set_title(str(h)+', '+str(i))
                if enh==0:
                    axis.set_yticks([0,1,2,3])
                    axis.set_ylabel('axial position, [m]')
                else:
                    axis.set_yticks([])
                if enh==2:
                    axis.set_title('{} EFPD'.format(i))                
                if en == 29:
                    xticks([-np.pi,  0,  np.pi],[r'$-\pi$', r'$0$',  r'$+\pi$'])
                    axis.set_xlabel('azimuthal position, [rad]')
                
                #axis.set_title(ti[i])
                if en%5==0:
                    temptitle=axis.get_title()
                    axis.set_title('case {}\n'.format(h)+temptitle)

                    
        fig=figure('temp')
        cax = fig.add_axes([0.1, 0.005, 0.8, 0.002])
        cb=fig.colorbar(im, cax=cax,ticks=[580,600,620,640],orientation='horizontal')  
        cb.set_label('cladding Temperature [deg C]')
        fig.subplots_adjust(top=0.98)
        fig.subplots_adjust(bottom=0.01)
        #fig.subplots_adjust(left=0.1)
        #fig.subplots_adjust(right=0.85)   
        fig.text(0.5,0.99,'StarCCMs cladding temperature',
        horizontalalignment='center',verticalalignment='top',size=14)
        show()
        savefig('D:/dropbox/Dropbox/plots/spring2013/5_new/fluxandtemp/compare_TClad_1245.pdf')    
           
        fig=figure('flux')        
        cax = fig.add_axes([0.1, 0.005, 0.8, 0.002])
        cl=im.get_clim()
        cb=fig.colorbar(im, cax=cax,ticks=[0.8,1,1.2,1.5],orientation='horizontal')  #ticks=np.linspace(cl[0],cl[1],6)
        cb.set_label('cladding heat flux [MW/m2]')
        fig.subplots_adjust(top=0.98)
        fig.subplots_adjust(bottom=0.01)
        #fig.subplots_adjust(left=0.1)
        #fig.subplots_adjust(right=0.85)   
        fig.text(0.5,0.99,'StarCCMs cladding heat flux',
        horizontalalignment='center',verticalalignment='top',size=14)
        show()
        savefig('D:/dropbox/Dropbox/plots/spring2013/5_new/fluxandtemp/compare_Flux_1245.pdf')              
        
        
        
        
        
        #show()  
        #savefig('D:/dropbox/Dropbox/plots/spring2013/5_new/fluxandtemp/compare_orig_avg_TClad.pdf')
        #close()
                    
    if 3 in subcase: 
        path ='D:/powertables/new/5flux/'
        grid_x,grid_y=np.mgrid[-pi:pi:100j,0:3.6576:400j]
        
        ex=(-pi,pi,0,3.6576)
        fig=plt.figure('cladtemp',figsize=[8,170])
        clf()
        ti=['averaged\n as sent to MAMBA & DeCART','original \n as written by StarCCM+']
        
        PWR=[]
        for en,i in enumerate(ts2): 
            files=['MAM_Hflux_5_0'+i+'.csv','MAM_Hflux_5_0'+i+'.csv.bak']
            #files=['MAM_Hflux_5_0'+i+'.csv','flux_5_0'+i+'.cpl']
            
            #'MAM_Tke_5_0'+i+.csv,
            #'MAM_Tke_5_0'+i+.csv.bak]
            Tlist=[[],[]]    
            Flist=[[],[]] 
            Zlist=[[],[]] 
            Alist=[[],[]] 
            AreaList=[[],[]]
            rowind=[[0   ,1,   2,   3,4],[0   ,1,      3,4,5]]
            
            for enum,j in enumerate(files):
                print j
                f_in = open(path+j)
                f_in.next()           # skip header
                reader = csv.reader(f_in,delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
                for row in reader:
                    T=row[rowind[enum][0]]
                    f=row[rowind[enum][1]]
                    x=row[rowind[enum][2]]
                    if 'bak' in j:
                        AreaList[enum].append(row[2]) 
                    y=row[rowind[enum][3]]
                    z=row[rowind[enum][4]]
                    a=m.atan2(y,x)
                
                    Tlist[enum].append(T)        
                    Flist[enum].append(f)
                    Zlist[enum].append(z)
                    Alist[enum].append(a)         
                f_in.close()   

                # consistency chek:
                if 'bak' in j:
                    FL=np.array(Flist)
                    AL=np.array(AreaList) 
                    pwr=np.dot(FL[enum],AL[enum])   
                    PWR.append(pwr)        
                    print pwr    
                    print FL.max()       
                # plotting        
        
                axis=plt.subplot(len(ts2),2,2*en+enum+1)
                corr=1000000
                grid_z=griddata((Alist[enum],Zlist[enum]),Flist[enum],(grid_x,grid_y),method='linear')/corr
                #grid_z=zeros([100,400])
                
                im=imshow(grid_z.T, interpolation='none',extent=ex, origin='lower', \
                clim=([0.8,1.5]),aspect=2)
                xticks([-np.pi,  0,  np.pi],[r'$-\pi$', r'$0$',  r'$+\pi$'])
                xticks([])
                if enum==0:
                    axis.set_yticks([0,1,2,3])
                    axis.set_ylabel('axial position, [m]')
                else:
                    axis.set_yticks([])
                
                if en == 29:
                    xticks([-np.pi,  0,  np.pi],[r'$-\pi$', r'$0$',  r'$+\pi$'])
                    axis.set_xlabel('azimuthal position, [rad]')
                
                #axis.set_title(ti[i])
                if en==0:
                    axis.set_title(ti[enum]+'\n {} EFPD'.format(ts[en]))
                else:
                    axis.set_title('{} EFPD'.format(ts[en]))
                                
                #if j==1:
                    #axis.set_ylabel('axial position, [m]')
                    #axis.annotate('Tw_HFlux_XYZ_clad.csv.bak', xy=(-3, 1),size=14,color=[0.5,0.5,0.5])
                #else:
                    #axis.annotate('Tw_HFlux_XYZ_clad.csv', xy=(-3, 1),size=14,color=[0.5,0.5,0.5])
        cax = fig.add_axes([0.1, 0.005, 0.8, 0.002])
        cl=im.get_clim()
        cb=fig.colorbar(im, cax=cax,ticks=[0.8,1,1.2,1.5],orientation='horizontal')  #ticks=np.linspace(cl[0],cl[1],6)
        cb.set_label('cladding heat flux [MW/m2]')
        fig.subplots_adjust(top=0.98)
        fig.subplots_adjust(bottom=0.01)
        #fig.subplots_adjust(left=0.1)
        #fig.subplots_adjust(right=0.85)   
        fig.text(0.5,0.99,'Original and averaged cladding heat flux, case 5',
        horizontalalignment='center',verticalalignment='top',size=14)
              
           # fig.text(0.5,0.03,'azimuthal position, [rad]',horizontalalignment='center',verticalalignment='bottom')        
        show()  
        savefig('D:/dropbox/Dropbox/plots/spring2013/5_new/fluxandtemp/compare_orig_avg_Hflux.pdf')
        close()      

        if 1:
            figure()
            axis=plt.subplot(111)
            corr=1000
            plot(ts.astype(int),np.array(PWR)/corr,label='clad surf integral case 5')
            PWR_vol=[]
            for en,i in enumerate(ts):
                PWR_vol.append(dot(LinPow(tp,5,en),z_mesh2))
            plot(ts.astype(int),np.array(PWR_vol)/corr,label='UO2 vol integral case 5')
            PWR_vol=[]
            for en,i in enumerate(ts):
                PWR_vol.append(dot(LinPow(tp,4,en),z_mesh2))
            plot(ts.astype(int),np.array(PWR_vol)/corr,'o',label='UO2 vol integral case 4')
            legend()
            PWR_vol=[]
            for en,i in enumerate(ts):
                PWR_vol.append(dot(LinPow(tp,6,en),z_mesh2))
            plot(ts.astype(int),np.array(PWR_vol)/corr,label='UO2 vol integral case 6')
            axis.set_xlabel('burnup, [EFPD]')
            axis.set_ylabel('rod power, [kW]')
            axis.grid('on')
            axis.set_title('Rod power during cycle for cases 4,5 and 6 during cycle')
            
            legend(loc=7)  
            savefig('D:/dropbox/Dropbox/plots/spring2013/5_new/fluxandtemp/powercycle456.pdf')
 
    if 2 in subcase: 
        path ='D:/powertables/new/5flux/'
        grid_x,grid_y=np.mgrid[-pi:pi:100j,0:3.6576:400j]
        
        ex=(-pi,pi,0,3.6576)
        fig=plt.figure('cladtemp',figsize=[8,170])
        clf()
        ti=['averaged\n as sent to MAMBA & DeCART','original \n as written by StarCCM+']
        
        
        for en,i in enumerate(ts2): 
            files=['MAM_Hflux_5_0'+i+'.csv','MAM_Hflux_5_0'+i+'.csv.bak']
            #'MAM_Tke_5_0'+i+.csv,
            #'MAM_Tke_5_0'+i+.csv.bak]
            Tlist=[[],[]]    
            Flist=[[],[]] 
            Zlist=[[],[]] 
            Alist=[[],[]] 
            rowind=[[0   ,1,   2,   3,4],[0   ,1,      3,4,5]]
            
            for enum,j in enumerate(files):
                print j
                f_in = open(path+j)
                f_in.next()           # skip header
                reader = csv.reader(f_in,delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
                for row in reader:
                    T=row[rowind[enum][0]]
                    f=row[rowind[enum][1]]
                    x=row[rowind[enum][2]]
                    y=row[rowind[enum][3]]
                    z=row[rowind[enum][4]]
                    a=m.atan2(y,x)
                
                    Tlist[enum].append(T)        
                    Flist[enum].append(f)
                    Zlist[enum].append(z)
                    Alist[enum].append(a)         
                f_in.close()   

                # plotting        
        
                axis=plt.subplot(len(ts2),2,2*en+enum+1)
                grid_z=griddata((Alist[enum],Zlist[enum]),Tlist[enum],(grid_x,grid_y),method='linear')
                #grid_z=zeros([100,400])
                
                im=imshow(grid_z.T, interpolation='none',extent=ex, origin='lower', \
                clim=([580,640]),aspect=2)
                xticks([-np.pi,  0,  np.pi],[r'$-\pi$', r'$0$',  r'$+\pi$'])
                xticks([])
                if enum==0:
                    axis.set_yticks([0,1,2,3])
                    axis.set_ylabel('axial position, [m]')
                else:
                    axis.set_yticks([])
                
                if en == 29:
                    xticks([-np.pi,  0,  np.pi],[r'$-\pi$', r'$0$',  r'$+\pi$'])
                    axis.set_xlabel('azimuthal position, [rad]')
                
               
                if en==0:
                    axis.set_title(ti[enum]+'\n {} EFPD'.format(ts[en]))
                else:
                    axis.set_title('{} EFPD'.format(ts[en]))

        cax = fig.add_axes([0.1, 0.005, 0.8, 0.002])
        cb=fig.colorbar(im, cax=cax,ticks=[580,600,620,640],orientation='horizontal')  
        cb.set_label('cladding Temperature [deg C]')
        fig.subplots_adjust(top=0.98)
        fig.subplots_adjust(bottom=0.01)
        #fig.subplots_adjust(left=0.1)
        #fig.subplots_adjust(right=0.85)   
        fig.text(0.5,0.99,'Original and averaged cladding temperature, case 5',
        horizontalalignment='center',verticalalignment='top',size=14)
              
                
        show()  
        savefig('D:/dropbox/Dropbox/plots/spring2013/5_new/fluxandtemp/compare_orig_avg_TClad_in_crud.pdf')
        close()
        
            
            
      #  if 1:
      #      fig=plt.figure('heatflux')
      #      clf()
      #      for i in range(2):
      #          grid_z=griddata((Alist[i],Zlist[i]),Flist[i],(grid_x,grid_y),method='linear')
      #          axis=plt.subplot(1,2,i)
      #          corr=1000000
      #          im=imshow(grid_z.T/corr, interpolation='none',extent=ex, origin='lower', \
      #          clim=([0.8,1.2]),aspect=2)
      #          xticks([-np.pi,  0,  np.pi],
      #          [r'$-\pi$', r'$0$',  r'$+\pi$'])
      #
      #          axis.set_title(ti[i])
      #          axis.set_xlabel('azimuthal position, [rad]')
      #          if i==1:
      #              axis.set_ylabel('axial position, [m]')
      #              axis.annotate('Tw_HFlux_XYZ_clad.csv.bak', xy=(-3, 1),size=14,color=[0.5,0.5,0.5])
      #          else:
      #              axis.annotate('Tw_HFlux_XYZ_clad.csv', xy=(-3, 1),size=14,color=[0.5,0.5,0.5])
      #      cax = fig.add_axes([0.87, 0.1, 0.03, 0.8])
      #      cl=im.get_clim()
      #      cb=fig.colorbar(im, cax=cax,ticks=np.linspace(cl[0],cl[1],5))  
      #      cb.set_label('cladding heat flux [MW/m2]')
      #      fig.subplots_adjust(top=0.90)
      #      fig.subplots_adjust(bottom=0.05)
      #      fig.subplots_adjust(left=0.1)
      #      fig.subplots_adjust(right=0.85)   
      #      fig.text(0.5,0.975,'Original and averaged heat flux \n\
      #      case 5, 500 EFPD',horizontalalignment='center',verticalalignment='top',size=14)
      #      show() 
      #      #savefig('D:/dropbox/Dropbox/plots/spring2013/compare_orig_avg_Hflux.pdf')
      #      #fig.text(0.5,0.03,'azimuthal position, [rad]',horizontalalignment='center',verticalalignment='bottom')        
                      
        
if 10 in plotcase:
    mbo10=10.0129370
    mbo11=11.0093054
    mNiFe=58.6934+55.845*2+15.999*4
    xmeshmeter=[0,21,41,61]
    if 1 in subcase: # not for the report
        # cycle averaged crud
        fig=figure(figsize=[8,20])
        suptitle('B10 cycle for case 4 (right, CFD) and case 5 (left, SUB)\n plotted is the azimuthally averaged density [mol/cm^3] \n xaxis: z-position (5cm steps), yaxis: radial psoition (5micron steps above clad)')
        thismanager = get_current_fig_manager()
        thismanager.window.wm_geometry("+2000+-400")
        ii=[0,1,2,3,4,5,6,7,8,9]
        jj=[0,1]
        for i in range(len(ii)):
            for j in range(len(jj)):
                axis=plt.subplot(10,2,2*ii[i]+j+1)
                im=axis.imshow(sum(crud[jj[j],ii[i],:,:,:,0],1)/18,clim=([0,0.00003]),interpolation='none',origin='lower')
        #cbar = fig.colorbar(cax, ticks=[0, 0.00003])
        #cbar.ax.set_yticklabels(['0', '3e-5'])
                #axis.set_xlabel('{},{},{}'.format(i,j,ii[i]+j),size=14)
                #xticks(xmeshmeter,('0','1','2','3'))
               
        
        
        
        #axis.set_ylabel('radial position' ,size=14)
                axis.set_xlabel('{} EFPD'.format((ii[i]+1)*50),size=14) 
        cax = fig.add_axes([0.125, 0.05, 0.775, 0.03])
        cb=fig.colorbar(im, cax=cax,orientation='horizontal',ticks=[0,0.00003])               
        #savefig('V:\\master report\\figures\\crud_axial{0}.pdf'.format(C))
        #axis.set_title('Crud map of radius vs. z-position \n case {0}'.format(C),size=18)
        #savefig('D:\dropbox\Dropbox\plots\case{0}\crudb10_axial.pdf'.format(C))
        show()
        
        
        fig=figure(figsize=[8,20])
        suptitle('B11 cycle for case 4 (right, CFD) and case 5 (left, SUB) \n plotted is the azimuthally averaged density [mol/cm^3] \n xaxis: z-position (5cm steps), yaxis: radial psoition (5micron steps above clad)')
        thismanager = get_current_fig_manager()
        thismanager.window.wm_geometry("+2000+-400")
        ii=[0,1,2,3,4,5,6,7,8,9]
        jj=[0,1]
        for i in range(len(ii)):
            for j in range(len(jj)):
                axis=plt.subplot(10,2,2*ii[i]+j+1)
                im=axis.imshow(sum(crud[jj[j],ii[i],:,:,:,1],1)/18,clim=([0,0.0001]),interpolation='none',origin='lower')
        #cbar = fig.colorbar(cax, ticks=[0, 0.00003])
        #cbar.ax.set_yticklabels(['0', '3e-5'])
                #axis.set_xlabel('{},{},{}'.format(i,j,ii[i]+j),size=14)
                #xticks(xmeshmeter,('0','1','2','3'))
               
        
        
        
        #axis.set_ylabel('radial position' ,size=14)
                axis.set_xlabel('{} EFPD'.format((ii[i]+1)*50),size=14) 
                
        cax = fig.add_axes([0.125, 0.05, 0.775, 0.03])
        cb=fig.colorbar(im, cax=cax,orientation='horizontal',ticks=[0,0.0001])
      
        ##savefig('V:\\master report\\figures\\crud_axial{0}.pdf'.format(C))
        ##axis.set_title('Crud map of radius vs. z-position \n case {0}'.format(C),size=18)
        #savefig('D:\dropbox\Dropbox\plots\case{0}\crudb11_cycle.pdf'.format(C))
        show()
        
        
        fig=figure(figsize=[8,20])
        suptitle('NiFe04 cycle for case 4 (right, CFD) and case 5 (left, SUB) \n plotted is the azimuthally averaged density [mol/cm^3] \n xaxis: z-position (5cm steps), yaxis: radial psoition (5micron steps above clad)')
        thismanager = get_current_fig_manager()
        thismanager.window.wm_geometry("+2000+-400")
        ii=[0,1,2,3,4,5,6,7,8,9]
        jj=[0,1]
        for i in range(len(ii)):
            for j in range(len(jj)):
                axis=plt.subplot(10,2,2*ii[i]+j+1)
                im=axis.imshow(sum(crud[jj[j],ii[i],:,:,:,2],1)/18,clim=([0,0.016]),interpolation='none',origin='lower')
        #cbar = fig.colorbar(cax, ticks=[0, 0.00003])
        #cbar.ax.set_yticklabels(['0', '3e-5'])
                #axis.set_xlabel('{},{},{}'.format(i,j,ii[i]+j),size=14)
                #xticks(xmeshmeter,('0','1','2','3'))
               
        
        
        
        #axis.set_ylabel('radial position' ,size=14)
                axis.set_xlabel('{} EFPD'.format((ii[i]+1)*50),size=14) 
                
        cax = fig.add_axes([0.125, 0.05, 0.775, 0.03])
        cb=fig.colorbar(im, cax=cax,orientation='horizontal',ticks=[0,0.016])
      
        ##savefig('V:\\master report\\figures\\crud_axial{0}.pdf'.format(C))
        ##axis.set_title('Crud map of radius vs. z-position \n case {0}'.format(C),size=18)
        #savefig('D:\dropbox\Dropbox\plots\case{0}\crudbNiFe_cycle.pdf'.format(C))
        show()
        
    if 2 in subcase:    
        # cycle averaged crud
        fig=figure('crudcycle 3 cases',figsize=[8,11])
        clf()
        thismanager = get_current_fig_manager()
        thismanager.window.wm_geometry("+2000+-400")
        ii=[1,3,5,7,9]
        
        ii=[0,1,2,3,4]
        iii=[18,28,38,48,58]
        
        jj=[0,1,2]
        for i in range(len(ii)):
            for j in range(len(jj)):
                axis=plt.subplot(5,3,3*i+j+1)
                #im=axis.imshow((sum(crud[jj[j],iii[i],:,:,:,0]*mbo10,1)+sum(crud[jj[j],iii[i],:,:,:,1]*mbo11,1))/18*1000,clim=([0,2]),interpolation='none',origin='lower',aspect=2.5)
                im=axis.imshow((crud[jj[j],iii[i],:,5,:,0]*mbo10+crud[jj[j],
                iii[i],:,5,:,1]*mbo11)*1000,clim=([0.1,200]),interpolation='none',
                origin='lower',aspect=2.5,norm=LogNorm())
                if j==1:
                    axis.set_title('{} EFPD'.format(tscrud[iii[i]]),size=14) 
                xticks(xmeshmeter,('0','1','2','3'))
                yticks([0,5,10,15],[0,25,50,75])
        cax = fig.add_axes([0.10, 0.06, 0.8, 0.03])
        cb=fig.colorbar(im, cax=cax,orientation='horizontal',ticks=[0.1,1,10,100])   
        fig.subplots_adjust(top=0.95)
        fig.subplots_adjust(bottom=0.15)
        fig.subplots_adjust(left=0.1)
        fig.subplots_adjust(right=0.9)
        #figtext(0.18,0.97,'Case 4',size=16)
        #figtext(0.48,0.97,'Case 5',size=16)
        #figtext(0.74,0.97,'Case 6',size=16)
        figtext(0.40,0.13,'axial position [m]',size=14)
        figtext(0.03,0.65,'radial position above cladding [$\mu$m]',size=14,rotation='vertical')
        figtext(0.31,0.02,'Boron concentration [mg/cm$^3$]',size=14)

        #savefig('V:\\master report\\figures\\crud_axial{0}.pdf'.format(C))
        #axis.set_title('Crud map of radius vs. z-position \n case {0}'.format(C),size=18)
        savefig('D:/dropbox/Dropbox/plots/spring2013/5_new/crudcycle.pdf')
        savefig('D:/dropbox/Dropbox/plots/spring2013/5_new/crudcycle.png')
        show()    

        
    if 2 in subcase:    
        # cycle averaged crud
        fig=figure('crudcycle 3 cases old',figsize=[8,11])
        clf()
        thismanager = get_current_fig_manager()
        thismanager.window.wm_geometry("+2000+-400")
        ii=[1,3,5,7,9]
        
        ii=[0,1,2,3,4]
        iii=[18,28,38,48,58]
        
        jj=[0,1,2]
        for i in range(len(ii)):
            for j in range(len(jj)):
                axis=plt.subplot(5,3,3*i+j+1)
                #im=axis.imshow((sum(crud[jj[j],iii[i],:,:,:,0]*mbo10,1)+sum(crud[jj[j],iii[i],:,:,:,1]*mbo11,1))/18*1000,clim=([0,2]),interpolation='none',origin='lower',aspect=2.5)
                im=axis.imshow((crud[jj[j],iii[i],:,5,:,0]*mbo10+crud[jj[j],
                iii[i],:,5,:,1]*mbo11)*1000,clim=([0,2]),interpolation='none',
                origin='lower',aspect=2.5)
                if j==1:
                    axis.set_title('{} EFPD'.format(tscrud[iii[i]]),size=14) 
                xticks(xmeshmeter,('0','1','2','3'))
                yticks([0,5,10,15],[0,25,50,75])
        cax = fig.add_axes([0.10, 0.06, 0.8, 0.03])
        cb=fig.colorbar(im, cax=cax,orientation='horizontal',ticks=[0,0.5,1,1.5,2])   
        fig.subplots_adjust(top=0.95)
        fig.subplots_adjust(bottom=0.15)
        fig.subplots_adjust(left=0.1)
        fig.subplots_adjust(right=0.9)
        #figtext(0.18,0.97,'Case 4',size=16)
        #figtext(0.48,0.97,'Case 5',size=16)
        #figtext(0.74,0.97,'Case 6',size=16)
        figtext(0.40,0.13,'axial position [m]',size=14)
        figtext(0.03,0.65,'radial position above cladding [$\mu$m]',size=14,rotation='vertical')
        figtext(0.31,0.02,'Boron concentration [mg/cm$^3$]',size=14)

        #savefig('V:\\master report\\figures\\crud_axial{0}.pdf'.format(C))
        #axis.set_title('Crud map of radius vs. z-position \n case {0}'.format(C),size=18)
        savefig('D:/dropbox/Dropbox/plots/spring2013/5_new/crudcycle_original.pdf')
        savefig('D:/dropbox/Dropbox/plots/spring2013/5_new/crudcycle_original.png')
        show()    

    if 2.05 in subcase:    
        # cycle averaged crud
        fig=figure('crudcycle 3 cases overview',figsize=[8,30])
        clf()
        thismanager = get_current_fig_manager()
        thismanager.window.wm_geometry("+2000+-400")
        ii=[1,3,5,7,9]
        
        ii=[0,1,2,3,4]
        iii=[0,3,6,9,12,15,18,21,24,27,30,33,36,39,42,45,48,51,54,58]
        
        jj=[0,1,2]
        for i in range(len(iii)):
            for j in range(len(jj)):
                axis=plt.subplot(21,3,3*i+j+1)
                #im=axis.imshow((sum(crud[jj[j],iii[i],:,:,:,0]*mbo10,1)+sum(crud[jj[j],iii[i],:,:,:,1]*mbo11,1))/18*1000,clim=([0,2]),interpolation='none',origin='lower',aspect=2.5)
                im=axis.imshow((crud[jj[j],iii[i],:,5,:,0]*mbo10+crud[jj[j],
                iii[i],:,5,:,1]*mbo11)*1000,clim=([0,2.5]),interpolation='none',
                origin='lower',aspect=2.5)
                if j==1:
                    #axis.set_title('{} EFPD'.format(tscrud[iii[i]]),size=14) 
                    fp=dict(size=10)
                    _at=AnchoredText("BU {}".format(tscrud[iii[i]]),prop=fp,loc=2)
                    axis.add_artist(_at)
                if iii[i]==58:    
                    xticks(xmeshmeter,['0','1','2','3'])
                else:
                    xticks([])
                yticks([0,5,10,15],[0,25,50,75])
        cax = fig.add_axes([0.10, 0.03, 0.8, 0.015])
        cb=fig.colorbar(im, cax=cax,orientation='horizontal',ticks=[0,0.5,1,1.5,2,2.5])   
        fig.subplots_adjust(top=0.95)
        fig.subplots_adjust(bottom=0.02)
        fig.subplots_adjust(left=0.1)
        fig.subplots_adjust(right=0.9)
        #figtext(0.18,0.97,'Case 4',size=16)
        #figtext(0.48,0.97,'Case 5',size=16)
        #figtext(0.74,0.97,'Case 6',size=16)
        #figtext(0.40,0.13,'axial position [m]',size=14)
        figtext(0.03,0.65,'radial position above cladding [$\mu$m]',size=14,rotation='vertical')
        figtext(0.31,0.01,'Boron concentration [mg/cm$^3$]',size=14)

        #savefig('V:\\master report\\figures\\crud_axial{0}.pdf'.format(C))
        #axis.set_title('Crud map of radius vs. z-position \n case {0}'.format(C),size=18)
        savefig('D:/dropbox/Dropbox/plots/spring2013/5_new/crudcycle_overview.pdf')
        savefig('D:/dropbox/Dropbox/plots/spring2013/5_new/crudcycle_overview.png')
        show()          
    if 2.06 in subcase:  

        R=20
        A=18
        Ca=len(tscrud)
        crudvol=array([[[0.0 for i in range(73)] for j in range(A)] for jj in range(R)])
        dz=5
        r0=0.476
        dr=0.0005
        a=zeros((A,73))+1.0
        for i in range(R):
            r1=r0+i*dr
            r2=r0+(i+1)*dr
            vol=pi*(r2**2-r1**2)*dz/A
            crudvol[i,:,:]=copy.deepcopy(vol*a)

        # cycle averaged crud
        fig=figure('crudcycle 3 cases overview NiFe2o4',figsize=[8,30])
        clf()
        thismanager = get_current_fig_manager()
        thismanager.window.wm_geometry("+2000+-400")
        ii=[1,3,5,7,9]
        
        ii=[0,1,2,3,4]
        iii=[0,3,6,9,12,15,18,21,24,27,30,33,36,39,42,45,48,51,54,58]
        
        jj=[0,1,2]
        for i in range(len(iii)):
            for j in range(len(jj)):
                axis=plt.subplot(21,3,3*i+j+1)
                #im=axis.imshow((sum(crud[jj[j],iii[i],:,:,:,0]*mbo10,1)+sum(crud[jj[j],iii[i],:,:,:,1]*mbo11,1))/18*1000,clim=([0,2]),interpolation='none',origin='lower',aspect=2.5)
                im=axis.imshow((sum(multiply(crud[jj[j],iii[i],:,:,:,2],crudvol),1)/A*mNiFe),
                clim=([0,5]),interpolation='none',
                origin='lower',aspect=2.5)
                if j==1:
                    #axis.set_title('{} EFPD'.format(tscrud[iii[i]]),size=14) 
                    fp=dict(size=10)
                    _at=AnchoredText("BU {}".format(tscrud[iii[i]]),prop=fp,loc=2)
                    axis.add_artist(_at)
                if iii[i]==58:    
                    xticks(xmeshmeter,['0','1','2','3'])
                else:
                    xticks([])
                yticks([0,5,10,15],[0,25,50,75])
        cax = fig.add_axes([0.10, 0.03, 0.8, 0.015])
        cb=fig.colorbar(im, cax=cax,orientation='horizontal',ticks=[0,1,2,3,4,5])   
        fig.subplots_adjust(top=0.95)
        fig.subplots_adjust(bottom=0.02)
        fig.subplots_adjust(left=0.1)
        fig.subplots_adjust(right=0.9)
        #figtext(0.18,0.97,'Case 4',size=16)
        #figtext(0.48,0.97,'Case 5',size=16)
        #figtext(0.74,0.97,'Case 6',size=16)
        #figtext(0.40,0.13,'axial position [m]',size=14)
        figtext(0.03,0.65,'radial position above cladding [$\mu$m]',size=14,rotation='vertical')
        figtext(0.31,0.01,'crud concentration [g/cm$^3$]',size=14)

        #savefig('V:\\master report\\figures\\crud_axial{0}.pdf'.format(C))
        #axis.set_title('Crud map of radius vs. z-position \n case {0}'.format(C),size=18)
        savefig('D:/dropbox/Dropbox/plots/spring2013/5_new/crudcycle_overview_NiFe.pdf')
        savefig('D:/dropbox/Dropbox/plots/spring2013/5_new/crudcycle_overview_NiFe.png')
        show()          

 
 
    if 2.1 in subcase: 
        close('all')
        # cycle averaged crud
        fig=figure(figsize=[14,5])
        thismanager = get_current_fig_manager()
        thismanager.window.wm_geometry("+2000+-400")
        ii=[1,3,5,7,9]
        ii=[0,2,4,6,8]
        


        jj=[4,5]
        for i in range(len(ii)):
            for j in range(len(jj)):
                axis=plt.subplot(2,5,i+5*j+1)
                im=axis.imshow((sum(crud[jj[j],ii[i],:,:,:,0]*mbo10,1)+sum(crud[jj[j],ii[i],:,:,:,1]*mbo11,1))/18*1000,clim=([0,1.6]),interpolation='none',origin='lower',aspect=2.5)
                if j==0:
                    axis.set_title('{} EFPD'.format((ii[i]+1)*50),size=14) 
                
                if j==1:
                    xticks(xmeshmeter,('0','1','2','3'))
                else:
                    axis.get_xaxis().set_visible(False)
                if i==0:
                    yticks([0,10],[0,50])
                else:
                    axis.get_yaxis().set_visible(False)
                
        cax = fig.add_axes([0.18, 0.13, 0.72, 0.03])
        cb=fig.colorbar(im, cax=cax,orientation='horizontal',ticks=[0,0.5,1,1.5])   
        fig.subplots_adjust(top=0.92)
        fig.subplots_adjust(bottom=0.3)
        fig.subplots_adjust(left=0.18)
        fig.subplots_adjust(right=0.9)
        figtext(0.02,0.70,'Case B1,\n reference',size=16)
        figtext(0.02,0.35,'Case B2,\n comparison ',size=16)
        #figtext(0.02,0.35,'Case 6',size=16)
        rc('text', usetex=True) #latex
        rc('font', family='sans-serif')
        figtext(0.44,0.23,'axial position [m]' +r"$\rightarrow$",size=14)
        figtext(0.115,0.85,'radial position [$\mu$m]'+ r"$\rightarrow$",size=14,rotation='vertical')
        rc('text', usetex=False) #latex
        figtext(0.35,0.02,'Boron concentration [mg/cm$^3$]',size=14)
        set_fontsize([manager.canvas.figure for manager in matplotlib._pylab_helpers.Gcf.get_all_fig_managers()][0],beamerfontsize)        
        #savefig('V:\\master report\\figures\\crud_axial4beamer.pdf'.format(C))
        #axis.set_title('Crud map of radius vs. z-position \n case {0}'.format(C),size=18)
        
        show()   
        
    if 3 in subcase:
        R=20
        A=18
        Ca=len(tscrud)
        crudvol=array([[[0.0 for i in range(73)] for j in range(A)] for jj in range(R)])
        dz=5
        r0=0.476
        dr=0.0005
        a=zeros((A,73))+1.0
        for i in range(R):
            r1=r0+i*dr
            r2=r0+(i+1)*dr
            vol=pi*(r2**2-r1**2)*dz/A
            crudvol[i,:,:]=copy.deepcopy(vol*a)
            
        crudmol=zeros((3,Ca,3))
        for i in [0,1,2]:
            for j in range(Ca):
                for k in range(3):
                    crudmol[i,j,k]=sum(multiply(crudvol,crud[i,j,:,:,:,k]))
                
        mbo10=10.0129370
        mbo11=11.0093054
                
        figure('crudintegral',figsize=[8,4])
        clf()
        axis=subplot(211)
        x=(arange(10)+1)*50
        plot(tscrud,(crudmol[0,:,0]*mbo10*1000),zorder = 10,lw=2,color='b',label='case 1')
        #plot(tscrud,(crudmol[0,:,1]*mbo11*1000),zorder = 10,lw=2,color='b',label='case 4 B-11',ls='--')
        plot(tscrud,(crudmol[1,:,0]*mbo10*1000),color='g',label='case 2')
        #plot(tscrud,(crudmol[1,:,1]*mbo11*1000),color='g',label='case 5 B-11',ls='--')
        plot(tscrud,(crudmol[2,:,0]*mbo10*1000),color='r',label='case 3')
        #plot(tscrud,(crudmol[2,:,1]*mbo11*1000),color='r',label='case 6 B-11',ls='--')
        axis.annotate('Boron-10', xy=(200, 2),size=14,color=[0.5,0.5,0.5])

        
        legend(loc=2)
        mcrud=2*55.845+ 58.6934+4* 15.999
        axis.xaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.yaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.set_ylabel('mass, [mg]',size=14) 
        
        #tight_layout()
        axis=subplot(212)
        plot(tscrud,(crudmol[0,:,2]*mcrud),zorder = 10,lw=2,color='b',label='case 1',ls='-')
        plot(tscrud,(crudmol[1,:,2]*mcrud),color='g',label='case 2',ls='-')
        plot(tscrud,(crudmol[2,:,2]*mcrud),color='r',label='case 3',ls='-')
        legend(loc=2)
        axis.annotate('crud (NiFe$_2$O$_4$)', xy=(200, 6),size=14,color=[0.5,0.5,0.5])
        axis.xaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.yaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.set_ylabel('mass, [g]',size=14) 
        axis.set_xlabel('burnup, [EFPD]' ,size=14)
        #axis.set_ylim([0,10])
        tight_layout()
        savefig('D:/dropbox/Dropbox/plots/spring2013/5_new/crudcycle_integrated_mass.pdf')
        savefig('D:/dropbox/Dropbox/plots/spring2013/5_new/crudcycle_integrated_mass.png')
        #axis.set_title('Total boron mass versus burnup',size=18)
        #tight_layout()
          
        show()

    if 3.1 in subcase:
        close('all')
        crudvol=array([[[0.0 for i in range(73)] for j in range(18)] for jj in range(18)])
        dz=5
        r0=0.476
        dr=0.0005
        a=zeros((18,73))+1.0
        for i in range(18):
            r1=r0+i*dr
            r2=r0+(i+1)*dr
            vol=pi*(r2**2-r1**2)*dz/18
            crudvol[i,:,:]=copy.deepcopy(vol*a)
            
        crudmol=zeros((8,10,3))
        for i in [4,5,6,7]:
            for j in range(10):
                for k in range(3):
                    crudmol[i,j,k]=sum(multiply(crudvol,crud[i,j,:,:,:,k]))
                
        mbo10=10.0129370
        mbo11=11.0093054
                
        figure(figsize=[8,6])
        axis=subplot2grid((5,1),(0,0),rowspan=3)
        x=(arange(10)+1)*50
        plot(x[:-1],(crudmol[4,:-1,0]*mbo10*1000),zorder = 10,lw=2,color='b',label='case B1 B-10')
        plot(x[:-1],(crudmol[4,:-1,1]*mbo11*1000),zorder = 10,lw=2,color='b',label='case B1 B-11',ls='--')
        plot(x[:-1],(crudmol[5,:-1,0]*mbo10*1000),color='g',label='case B2 B-10')
        plot(x[:-1],(crudmol[5,:-1,1]*mbo11*1000),color='g',label='case B2 B-11',ls='--')
        #plot(x[:-1],(crudmol[6,:-1,0]*mbo10*1000),color='r',label='case 6   $^{10}$B ')
        #plot(x[:-1],(crudmol[6,:-1,1]*mbo11*1000),color='r',label='case 6   $^{11}$B ',ls='--')
        #plot(x[:-1],(crudmol[7,:-1,0]*mbo10*1000),color='r',label='case 6 B-10')
        #plot(x[:-1],(crudmol[7,:-1,1]*mbo11*1000),color='r',label='case 6 B-11',ls='--')
        axis.annotate('Boron', xy=(270, 17),size=14,color=[0.5,0.5,0.5])

        
        legend(loc=2)
        mcrud=2*55.845+ 58.6934+4* 15.999
        axis.xaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.yaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.set_ylabel('mass, [mg]',size=14) 
        
        #tight_layout()
        axis=subplot2grid((5,1),(3,0),rowspan=2)
        plot(x[:-1],(crudmol[4,:-1,2]*mcrud),zorder = 10,lw=2,color='b',label='case B1',ls='-')
        plot(x[:-1],(crudmol[5,:-1,2]*mcrud),color='g',label='case B2',ls='-')
        #plot(x[:-1],(crudmol[7,:-1,2]*mcrud),color='r',label='case 6',ls='-')
        legend(loc=2)
        axis.annotate('CRUD (NiFe$_2$O$_4$)', xy=(200, 6),size=14,color=[0.5,0.5,0.5])
        axis.xaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.yaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.set_ylabel('mass, [g]',size=14) 
        axis.set_xlabel('burnup, [EFPD]' ,size=14)
        axis.set_ylim([0,10])
        yticks([0,5,10])
        #axis.set_title('Total boron mass versus burnup',size=18)
        #tight_layout()
        set_fontsize([manager.canvas.figure for manager in matplotlib._pylab_helpers.Gcf.get_all_fig_managers()][0],beamerfontsize)        
        tight_layout()
        show()
        #savefig('V:\\master report\\figures\\boron_total_allbeamer.pdf'.format(C))
        
        
    if 4 in subcase:
        zcrud=zeros([10,73,3])
        for i in range(10):
            for k in range(73):
                for l in range(3):
                    zcrud[i,k,l]=sum(multiply(crud[5,i,:,:,k,l],crudvol[:,:,k]))
        figure()
        axis=plt.subplot(111)
        for i in range(9):
            c = cm.jet((i)/10,1)
            plot(z_crud[:-1],zcrud[i,:,1]*mbo11*1000,color=c,label='{} EFPD'.format((i+1)*50))
        legend(loc=2)    
        axis.xaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.yaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.set_xlabel( 'axial position, [m]',size=14)
        axis.set_ylabel('B-10 mass, [mg]',size=14)         
        show()
        
    if 5 in subcase:
        figure()
        fig = figure(figsize=(8,8))
        ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], polar=True)
        
        N = 20
        theta = np.arange(0.0, 2*np.pi, 2*np.pi/N)
        radii = 10*np.random.rand(N)
        width = np.pi/4*np.random.rand(N)
        bars = ax.bar(theta, radii, width=width, bottom=0.0)
        for r,bar in zip(radii, bars):
            bar.set_facecolor( cm.jet(r/10.))
            bar.set_alpha(0.5)
        
        show()
    if 6 in subcase: # an imshow plot of crud / boron concentration
        R=20
        A=18
        Ca=len(tscrud)
        crudvol=array([[[0.0 for i in range(73)] for j in range(A)] for jj in range(R)])
        dz=5 # all in cm
        r0=0.476
        dr=0.0005
        a=zeros((A,73))+1.0
        for i in range(R):
            r1=r0+i*dr
            r2=r0+(i+1)*dr
            vol=pi*(r2**2-r1**2)*dz/A
            crudvol[i,:,:]=copy.deepcopy(vol*a)
        m=[mbo10,mbo11,mNiFe]
        # cycle averaged crud
        fig=figure('bormap', figsize=[16,12])
         
        clf()
        TS=[18,28,38,48,58] # 100 to 200
        TS=[38,40,42,44,46]
       # TS=[10,12,14,16,18]
       # TS=[0,1,2,3,4]
        for en, j in enumerate(TS): 
            for i in range(3):
                axis=plt.subplot(3,len(TS),i*5+en+1)
                ex=(-pi,pi,0,3.6576)
                im=axis.imshow((sum(multiply(crud[i,j,:,:,:,0],crudvol),0).T
                *mbo10+sum(multiply(crud[i,j,:,:,:,1],crudvol),0).T*mbo11)
                /(2*np.pi*r0*dz/A)*1000,extent=ex,interpolation='none', 
                origin='lower',aspect=2.5,clim=([0,0.35]))
                if i==0:
                    axis.set_title(str(tscrud[j])+' EPFD' )
                
                if i==2:
                    xticks([-np.pi,  0,  np.pi],[r'$-\pi$', r'$0$',  r'$+\pi$'])
                    if en==2:
                        axis.set_xlabel('azimuthal position, [m]',size =14)
                       
                            
                else:
                    xticks([])
                #axis.set_xlabel('azimuthal position, [rad]')
                if en==0:
                    if i==1:
                        axis.set_ylabel('axial position, [m]\n case'+str(i+1)+'\n',size =14,horizontalalignment='center')
                    else:
                        axis.set_ylabel('\n case '+str(i+1)+'\n',size =14,horizontalalignment='center')
                    
                else:
                    yticks([])
    
        cbar_ax = fig.add_axes([0.05, 0.04, 0.9, 0.02])
        cl=im.get_clim()
        cb=fig.colorbar(im,ticks=np.linspace(cl[0],cl[1],8), orientation='horizontal',cax=cbar_ax)
        cb.set_label('boron area density [mg/cm2]')
        fig.text(0.5,0.98,'Boron concentration on rod surface'
        ,horizontalalignment='center',verticalalignment='top',size=14)
     
        show()  
        fig.subplots_adjust(top=0.9)
        fig.subplots_adjust(left=0.05)
        fig.subplots_adjust(right=0.95)    
        draw()    
        savefig('D:/dropbox/Dropbox/plots/spring2013/5_new/compare_boron_densities300to380.pdf')
        
    if 6.1 in subcase: # an imshow plot of crud / boron concentration
        R=20
        A=18
        Ca=len(tscrud)
        crudvol=array([[[0.0 for i in range(73)] for j in range(A)] for jj in range(R)])
        dz=5 # all in cm
        r0=0.476
        dr=0.0005
        a=zeros((A,73))+1.0
        for i in range(R):
            r1=r0+i*dr
            r2=r0+(i+1)*dr
            vol=pi*(r2**2-r1**2)*dz/A
            crudvol[i,:,:]=copy.deepcopy(vol*a)
        m=[mbo10,mbo11,mNiFe]
        # cycle averaged crud
        fig=figure('bor10map', figsize=[16,12])
         
        clf()
        TS=[18,28,38,48,58] # 100 to 200
        TS=[38,40,42,44,46]
       # TS=[10,12,14,16,18]
       # TS=[0,1,2,3,4]
        for en, j in enumerate(TS): 
            for i in range(3):
                axis=plt.subplot(3,len(TS),i*5+en+1)
                ex=(-pi,pi,0,3.6576)
                im=axis.imshow((sum(multiply(crud[i,j,:,:,:,0],crudvol),0).T
                *mbo10)
                /(2*np.pi*r0*dz/A)*1000,extent=ex,interpolation='none', 
                origin='lower',aspect=2.5,clim=([0,0.07]))
                if i==0:
                    axis.set_title(str(tscrud[j])+' EPFD' )
                
                if i==2:
                    xticks([-np.pi,  0,  np.pi],[r'$-\pi$', r'$0$',  r'$+\pi$'])
                    if en==2:
                        axis.set_xlabel('azimuthal position, [m]',size =14)
                       
                            
                else:
                    xticks([])
                #axis.set_xlabel('azimuthal position, [rad]')
                if en==0:
                    if i==1:
                        axis.set_ylabel('axial position, [m]\n case'+str(i+1)+'\n',size =14,horizontalalignment='center')
                    else:
                        axis.set_ylabel('\n case '+str(i+1)+'\n',size =14,horizontalalignment='center')
                    
                else:
                    yticks([])
    
        cbar_ax = fig.add_axes([0.05, 0.04, 0.9, 0.02])
        cl=im.get_clim()
        cb=fig.colorbar(im,ticks=np.linspace(cl[0],cl[1],8), orientation='horizontal',cax=cbar_ax)
        cb.set_label('boron-10 area density [mg/cm2]')
        fig.text(0.5,0.98,'Boron-10 concentration on rod surface'
        ,horizontalalignment='center',verticalalignment='top',size=14)
     
        show()  
        fig.subplots_adjust(top=0.9)
        fig.subplots_adjust(left=0.05)
        fig.subplots_adjust(right=0.95)    
        draw()    
        savefig('D:/dropbox/Dropbox/plots/spring2013/5_new/compare_boron10_densities300to380.pdf') 

    if 6.2 in subcase: # an imshow plot of crud / boron concentration
        R=20
        A=18
        Ca=len(tscrud)
        crudvol=array([[[0.0 for i in range(73)] for j in range(A)] for jj in range(R)])
        dz=5 # all in cm
        r0=0.476
        dr=0.0005
        a=zeros((A,73))+1.0
        for i in range(R):
            r1=r0+i*dr
            r2=r0+(i+1)*dr
            vol=pi*(r2**2-r1**2)*dz/A
            crudvol[i,:,:]=copy.deepcopy(vol*a)
        m=[mbo10,mbo11,mNiFe]
        # cycle averaged crud
        fig=figure('bor11map', figsize=[16,12])
         
        clf()
        TS=[18,28,38,48,58] # 100 to 200
        TS=[38,40,42,44,46]
       # TS=[10,12,14,16,18]
       # TS=[0,1,2,3,4]
        for en, j in enumerate(TS): 
            for i in range(3):
                axis=plt.subplot(3,len(TS),i*5+en+1)
                ex=(-pi,pi,0,3.6576)
                im=axis.imshow((sum(multiply(crud[i,j,:,:,:,1],crudvol),0).T
                *mbo11)
                /(2*np.pi*r0*dz/A)*1000,extent=ex,interpolation='none', 
                origin='lower',aspect=2.5,clim=([0,0.07*4]))
                if i==0:
                    axis.set_title(str(tscrud[j])+' EPFD' )
                
                if i==2:
                    xticks([-np.pi,  0,  np.pi],[r'$-\pi$', r'$0$',  r'$+\pi$'])
                    if en==2:
                        axis.set_xlabel('azimuthal position, [m]',size =14)
                       
                            
                else:
                    xticks([])
                #axis.set_xlabel('azimuthal position, [rad]')
                if en==0:
                    if i==1:
                        axis.set_ylabel('axial position, [m]\n case'+str(i+1)+'\n',size =14,horizontalalignment='center')
                    else:
                        axis.set_ylabel('\n case '+str(i+1)+'\n',size =14,horizontalalignment='center')
                    
                else:
                    yticks([])
    
        cbar_ax = fig.add_axes([0.05, 0.04, 0.9, 0.02])
        cl=im.get_clim()
        cb=fig.colorbar(im,ticks=np.linspace(cl[0],cl[1],8), orientation='horizontal',cax=cbar_ax)
        cb.set_label('boron-11 area density [mg/cm2]')
        fig.text(0.5,0.98,'Boron-11 concentration on rod surface'
        ,horizontalalignment='center',verticalalignment='top',size=14)
     
        show()  
        fig.subplots_adjust(top=0.9)
        fig.subplots_adjust(left=0.05)
        fig.subplots_adjust(right=0.95)    
        draw()    
        savefig('D:/dropbox/Dropbox/plots/spring2013/5_new/compare_boron11_densities300to380.pdf') 

        
    if 7 in subcase:
        TS=[18,28,38,48,58] # 100 to 200
      #  TS=[38,40,42,44,46]
       # TS=[10,12,14,16,18]
       # TS=[0,1,2,3,4]
        R=20
        A=18
        Ca=len(tscrud)
        crudvol=array([[[0.0 for i in range(73)] for j in range(A)] for jj in range(R)])
        dz=5 # all in cm
        r0=0.476
        dr=0.0005
        a=zeros((A,73))+1.0
        for i in range(R):
            r1=r0+i*dr
            r2=r0+(i+1)*dr
            vol=pi*(r2**2-r1**2)*dz/A
            crudvol[i,:,:]=copy.deepcopy(vol*a)
        m=[mbo10,mbo11,mNiFe]
        # cycle averaged crud
        fig=figure('crudmap',figsize=[16,12])
        clf()
        for en, j in enumerate(TS): 
            for i in range(3):
                axis=plt.subplot(3,len(TS),i*5+en+1)
                ex=(-pi,pi,0,3.6576)
                im=axis.imshow((sum(multiply(crud[i,j,:,:,:,2],crudvol),0).T
                *mNiFe)/(2*np.pi*r0*dz/A)*1000,extent=ex,interpolation='none', 
                origin='lower',aspect=2.5,clim=([0,25]))
                #axis.set_title('case '+str(i+1))
                xticks([-np.pi,  0,  np.pi],
                [r'$-\pi$', r'$0$',  r'$+\pi$'])
                if i==0:
                    axis.set_title(str(tscrud[j])+' EPFD' )
                
                if i==2:
                    xticks([-np.pi,  0,  np.pi],[r'$-\pi$', r'$0$',  r'$+\pi$'])
                    if en==2:
                        axis.set_xlabel('azimuthal position, [m]',size =14)
                       
                            
                else:
                    xticks([])
                #axis.set_xlabel('azimuthal position, [rad]')
                if en==0:
                    if i==1:
                        axis.set_ylabel('axial position, [m]\n case'+str(i+1)+'\n',size =14,horizontalalignment='center')
                    else:
                        axis.set_ylabel('\n case '+str(i+1)+'\n',size =14,horizontalalignment='center')
                    
                else:
                    yticks([])
    
        cbar_ax = fig.add_axes([0.05, 0.04, 0.9, 0.02])
        cl=im.get_clim()
        cb=fig.colorbar(im,ticks=np.linspace(cl[0],cl[1],6), orientation='horizontal',cax=cbar_ax)
        cb.set_label('crud area density [mg/cm2]')
        fig.text(0.5,0.95,'Crud concentration on rod surface'
        ,horizontalalignment='center',verticalalignment='top',size=14)
        fig.subplots_adjust(top=0.98)
        show()  
        fig.subplots_adjust(top=0.9)
        fig.subplots_adjust(left=0.05)
        fig.subplots_adjust(right=0.95)    
        draw()    
        savefig('D:/dropbox/Dropbox/plots/spring2013/5_new/compare_crud_densities100to500.pdf')
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        