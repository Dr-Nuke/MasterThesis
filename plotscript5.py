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

C=5
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
        
        savefig('V:\\master report\\figures\\powercycle{0}.pdf'.format(C))
        axis.set_title('Linear Power development with burnup \n case 1 and {0}'.format(C),size=18)    
        tight_layout()
        savefig('D:\\dropbox\\Dropbox\\plots\\case{0}\\powercycle.png'.format(C))
        #axis.set_ylim([500,1200])    
        show()  
        
        
    if 1.5 in subcase: #relative linpow diff
        for iii in [0,2,4,6,9]:
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
            
            savefig('V:\\master report\\figures\\linpowrel4.pdf')
            axis.set_title('Relative difference in linear power of cases 4-7 to case 0',size=18)
            tight_layout()
            savefig('D:\dropbox\Dropbox\plots\case4\linpowrel4.png')  
            show()           


    if 2 in subcase:
        print shape(tp)
        figure('powercycle5')
        plt.clf()
        axis=plt.subplot(111)
        
        ph=[0]*29
        ii=[0,6,8,11,14,17,20,23,26,29]
        for i in range(len(ii)):
            c = cm.jet((i)/len(ii),1)
            ph[i],=step(z_mesh,Stepper(LinPow(tp,5,ii[i]),0)/1000,color=c,where='post',label='{} EFPD'.format(ts[ii[i]]))
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
        savefig('D:/dropbox/Dropbox/plots/spring2013/powercycle_case5.pdf'.format(C))
        #axis.set_ylim([500,1200])    
        show()     

        print shape(tp)
        figure('powercycle4and5')
        plt.clf()
        axis=plt.subplot(111)
        
        
        ph=[0]*29
        ii=[0,8,14,20,29]
        for i in range(len(ii)):
            c = cm.jet((i)/len(ii),1)
            ph[i],=step(z_mesh,Stepper(LinPow(tp,4,ii[i]),0)/1000,color=c,where='post',label='{} EFPD'.format(ts[ii[i]]))
            ph[i],=step(z_mesh,Stepper(LinPow(tp,5,ii[i]),0)/1000,color=c,where='post',label='{} EFPD'.format(ts[ii[i]]),alpha=0.5)
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
        savefig('D:/dropbox/Dropbox/plots/spring2013/powercycle_case4and5.pdf'.format(C))
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
        savefig('V:\\master report\\figures\\Pu_buildup{0}.pdf'.format(C))
        axis.set_title('Pu 239 and 241 buildup over cycle\n case {0}'.format(C),size=18)
        savefig('D:\dropbox\Dropbox\plots\case{0}\Pu_buildup.png'.format(C))        
        
        
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
        savefig('D:\dropbox\Dropbox\plots\case{0}\U235_depletion.png'.format(C))
        
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
         
        
        savefig('V:\\master report\\figures\\Pu_buildup{0}_1_5.pdf'.format(C))
        axis.set_title('Pu 239 buildup at 50 & 500 EFPD\n case {0} and 1'.format(C),size=18)
        tight_layout()
        savefig('D:\dropbox\Dropbox\plots\case{0}\Pu_buildup1.5.png'.format(C))            
        show()
    if 1.6 in subcase:
        figure()
        axis=plt.subplot(111)
        
        ph=[0,0,0,0]
        c=['b', 'g', 'r','c']
        ii=[9]
        ls1=['--','-']
        
        for i in range(len(ii)):
        
            ph[0],=step(z_mesh,Stepper((PuDens(tpu[4,ii[i],:,:,:,0],3)-PuDens(tpu[0,ii[i],:,:,:,0],30))/PuDens(tpu[0,ii[i],:,:,:,0],30),0),color='b',where='post')
            ph[1],=step(z_mesh,Stepper((PuDens(tpu[5,ii[i],:,:,:,0],3)-PuDens(tpu[0,ii[i],:,:,:,0],30))/PuDens(tpu[0,ii[i],:,:,:,0],30),0),color='g',where='post')
            ph[2],=step(z_mesh,Stepper((PuDens(tpu[6,ii[i],:,:,:,0],3)-PuDens(tpu[0,ii[i],:,:,:,0],30))/PuDens(tpu[0,ii[i],:,:,:,0],30),0),color='r',where='post')
            ph[3],=step(z_mesh,Stepper((PuDens(tpu[7,ii[i],:,:,:,0],3)-PuDens(tpu[0,ii[i],:,:,:,0],30))/PuDens(tpu[0,ii[i],:,:,:,0],30),0),color='c',where='post')
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
        savefig('V:\\master report\\figures\\purel467.pdf')
        axis.set_title('Relative difference in Pu239 buildup of cases 4-7 to case 0',size=18)
        tight_layout()
        savefig('D:\dropbox\Dropbox\plots\case0\purel456.png')  
        show()        
    if 1.7 in subcase:
        figure()
        axis=plt.subplot(111)
        
        ph=[0,0,0,0]
        c=['b', 'g', 'r','c']
        ii=[9]
        ls1=['--','-']
        
        for i in range(len(ii)):
        
            ph[0],=step(z_mesh,Stepper((PuDens(tpu[C,ii[i],:,:,:,0],3)-PuDens(tpu[4,ii[i],:,:,:,0],3))/PuDens(tpu[1,ii[i],:,:,:,0],3),0),where='post')
            #step(z_mesh,Stepper((PuDens(tpu[1,case[i],:,:,:,0],3)-PuDens(tpu[0,case[i],:,:,:,0],30))/PuDens(tpu[0,case[i],:,:,:,0],30),0),where='post')
        axis.yaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.xaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.set_ylabel('relative difference, [-]' ,size=14)
        axis.set_xlabel('axial position, [m]',size=14) 
        axis.annotate('500 EFPD', xy=(0.5, -0.003),size=16,color=[0.5,0.5,0.5]) 
        #axis.annotate('50 EFPD', xy=(1.5, -0.006),size=16,color=[0.5,0.5,0.5])
        #l=legend(["case 4","case 5","case 6","case 7"],loc=2)
        plt.axhline(y=0,color=[0.5,0.5,0.5])
        axis.set_xlim([0,3.6576])
        tight_layout()
        savefig('V:\\master report\\figures\\purel4.pdf')
        axis.set_title('Relative difference in Pu239 buildup of case 5 to case 4',size=18)
        tight_layout()
        savefig('D:\dropbox\Dropbox\plots\case0\purel4.png')  
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
        
        
        savefig('V:\\master report\\figures\\radial_Pu1{0}.pdf'.format(C))
        axis.set_title('Radial Pu 239 distribution for 500 EFPD\n case 1 and {0}, at z=1.8m'.format(C),size=18)    
        tight_layout()
        savefig('D:\\dropbox\\Dropbox\\plots\\case{0}\\radial_Pu.png'.format(C))    
        show()
        
if 10 in plotcase:
    if 1 in subcase:
        # cycle averaged crud
        figure()
        axis=plt.subplot(111)
        for i in [0,1,2,3]:
            c = cm.jet(i/9,1)
            step(z_crud,Stepper(Crudder(crud[C,i,:,:,1]),0),color=c,label='{:>5} EPFD'.format((i+1)*50))
        axis.set_ylabel('B10 , [mol] ' ,size=14)
        axis.set_xlabel('axial position, [m]',size=14) 
        axis.ticklabel_format(style='sci', scilimits=(0,0), axis='y')
        axis.set_ylim([0,0.00001])
        axis.set_xlim([0,3.6576])
        axis.xaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.yaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])             
        legend(loc=2)
        tight_layout()
        savefig('V:\\master report\\figures\\crud_cycle{0}.pdf'.format(C))
        axis.set_title('Crud vs. z-position during cycle \n case {0}'.format(C),size=18)
        tight_layout()
            
        savefig('D:\dropbox\Dropbox\plots\case{0}\crud_cycle.pdf'.format(C))
        show()
        
    if 2 in subcase:
        figure()
        for i in range(18):
            c = cm.jet(i/18,1)
            plot(crud[C,3,i,:,0],color=c)
            show()