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
from scipy.interpolate import griddata

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
# assign a number (or list) to plotcase: plotcase=[8]
# same for subcase
# 'run -i plotscript'
# sometimes additional scripts need to be run before, see comments

def LinPow(tp,i,j):
    """
    calculates the lineear power for  i,j.
    """
    a=sum(sum(tp[i,j,:,:,:],0),0)*np.pi*(0.004025**2)/(3*4)
    return a

def Block2(px,py,R,A,Z):
    """
    generates a 5D array that will allow segment representation
    with intuitive indexing by the indicators
    Arguments: px,py,A,R,Z -- Dimensoions of the array axes
    """
    a = [ [ [ [ [[] for i in range(Z)]  for j in range(A)]  for k in range(R)]
    for l in range(py)]  for m in range(px)]        
    return a

def Stepper(array,k):
    """
    returns a n array suited for the step plots
    """
    a=list(array)
    if k==0:    #usual case, have last point twice
        a.append(a[-1])
    if k==1:    #flux: need to dublicate first point (high energy)
        a.insert(0,a[0])
    return np.array(a)
 
def Btwn(a):
    """
    returns the points between the meshpoints. has len(a)-1
    """
    b=zeros(len(a)-1)
    for i in range(len(a)-1):
        b[i]=0.5*(a[i]+a[i+1])
        
    return b    
    
def PuDens(a,n):
    """
    calculates the Pu density average for each z plane
    a=tpu[i,j,:,:,:,n]
    n=number of radial section, 3 or 30
    
    """
    b=sum(sum(a,0)/n,0)/16
    return b
    
def PuMass(a):
    """
    calculates the pu mass in regions
    a=tpu[i,j,:,:,:,k]
    """
    mpu239=239.0521565      # atomic mass of pu 239               
    conv1=1.660538921E-24   # mass of one amu in gram 
    conv2=1E+30             # conversion from 1/barn*cm to 1/m^3
    conv=mpu239*conv1*conv2 # total conversion factor to get grams out of 1/barncm
    b=sum(a)
    return b
    
def set_fontsize(fig,fontsize):
    """
    For each text object of a figure fig, set the font size to fontsize
    """
    def match(artist):
        return artist.__module__ == "matplotlib.text"

    for textobj in fig.findobj(match=match):
        textobj.set_fontsize(fontsize)
    draw()
    return


gridgray=[0.7,0.7,0.7] 
annogray=[0.5,0.5,0.5]
    
radii2=[[0.0]*(len(radii[0])-1)]
for i in range(len(radii[0])-1):
    radii2[0][i]=(radii[0][i]+radii[0][i+1])/2  
radii2[0].insert(0,0)
radii2[0].append(0.00476)    

z_mesh3=[0.0]*(len(z_mesh)-1)
for i in range(len(z_mesh3)):
    z_mesh3[i]=(z_mesh[i]+z_mesh[i+1])/2
    
beamerfontsize=20

timesteps =['0','4','8','12','16','20','40','60','80','100','120','140','160',
'180','200','220','240','260','280','300','320','340','360','380','400','420',
'440','460','480','500']
TS=len(timesteps)



if 1 in plotcase: # 3x powervs z-axis, singlepin
           # run inputdeck before
    if 1 in subcase:       
        gd=0
        if gd==1:       
            path='G:\\powertables\\singlepin\\power500\\'
            powerfile=['power1.cpl','power2.cpl','power3.cpl']
            a=16
            F=len(powerfile)
            p= [Block2(1,1,5,a,49) for i in range(F)]
            z= [Block2(1,1,5,a,49) for i in range(F)]
        
            
            
            for h in range(F):
                file=path+powerfile[h]
                print file
                f=open(file, 'rb')
                f.next()
                reader = csv.reader(f,delimiter=' ', quotechar='"',skipinitialspace=True, quoting=csv.QUOTE_NONNUMERIC)
                for row in reader:
                    i,j,k,l,m=av.FindBin(row[2],row[3],row[4],pinmap,grid,z_mesh,a,0,pitch,radii,[0,0])
                    
                    
                    z[h][i][j][k][l][m].append(row[4]) 
                    p[h][i][j][k][l][m].append(row[0])
                f.close()
        
            for h in range(F):
                for i in range(1):
                    for j in range(1):
                        for k in range(5):
                            for l in range(a):
                                for m in range(49):
                                    p[h][i][j][k][l][m]=np.array(p[h][i][j][k][l][m])
                                    z[h][i][j][k][l][m]=np.array(z[h][i][j][k][l][m])
        
        plt.figure()
        fsize=20
    
        axis=plt.subplot(111)
        axis.set_ylabel('power density, [W/m^3]' ,size=14)
        axis.set_xlabel('axial position, [m]',size=14) 
        axis.set_title('axial power distribution at 500 EFPD,\n for all 3 radial sections',size=18)    
        ph=[[0 for i in range(49)] for j in range(F)]
        for h in range(F):
            c = cm.hot((h)/F,1)
            for k in range(3):
                for m in range(49):
                
                    ph[h][m],=plt.plot(z[h][0][0][k][0][m],p[h][0][0][k][0][m],'.',color=c,markeredgewidth=0)
        #axis.legend([ph[0][0],ph[1][0],ph[2][0]],['case 1','case 2','case 3'])        
        l=legend([ph[0][0],ph[1][0],ph[2][0]],["case 1","case 2","case 3"],loc=4)
        #axis.xaxis.grid(True,'minor')
        #axis.yaxis.grid(True,'minor')
        axis.xaxis.grid(True,'major',linewidth=2)
        axis.yaxis.grid(True,'major',linewidth=2)
        axis.set_xlim([0,3.6576])
        axis.set_ylim([0,8e8])
        axis.annotate('III.', xy=(1.7, 7.1e8),size=14)
        axis.annotate('II.', xy=(1.7, 5.6e8),size=14)
        axis.annotate('I.', xy=(1.7, 4.7e8),size=14)
        

        #axis.set_ylim([0,6e8])
    
        show()  
    if 2 in subcase: # powercycle cases 0 and 1

        figure('powercycle1')
        plt.clf()
        axis=plt.subplot(111)
        
        ph=[0]*29
        ii=[0,6,8,11,14,17,20,23,26,29]
        for i in range(len(ii)):
            c = cm.jet((i)/len(ii),1)
            ph[i],=step(z_mesh,Stepper(LinPow(tp,1,ii[i]),0)/1000,color=c,where='post',label='{} EFPD'.format(ts[ii[i]]))
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
        #savefig('D:/dropbox/Dropbox/plots/spring2013/1/powercycle_case1.pdf')
        
        #axis.set_ylim([500,1200])    
        
        
        show()
        

        figure('powercycle0')
        plt.clf()
        axis=plt.subplot(111)
        
        ph=[0]*29
        ii=[0,6,8,11,14,17,20,23,26,29]
        for i in range(len(ii)):
            c = cm.jet((i)/len(ii),1)
            ph[i],=step(z_mesh,Stepper(LinPow(tp,0,ii[i]),0)/1000,color=c,where='post',label='{} EFPD'.format(ts[ii[i]]))
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
        #savefig('D:/dropbox/Dropbox/plots/spring2013/0/powercycle_case0.pdf')
        #axis.set_ylim([500,1200])    
        
        
    show()

    if 2.1 in subcase:
        print shape(tp)
        figure('powercycleALL')
        plt.clf()
        axis=plt.subplot(111)
        
        ph=[0]*29
        ii=[0]
        for i in range(len(ii)):
            for j in [0,1,2,4,5,6]:
                c = cm.jet((j)/7,1)
                ph[j],=step(z_mesh,Stepper(LinPow(tp,j,ii[i]),0)/1000,color=c,where='post',label='case {}:{:>6.0f}'.format(j,dot(LinPow(tp,j,0),z_mesh2)))
        ph[3],=step(z_mesh,Stepper(LinPow(tp,3,0),0)/1000*12,color=c,where='post',label='case {}: {:>6.0f} W'.format(3,dot(LinPow(tp,3,0)*12,z_mesh2)))
        axis.yaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.xaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.set_ylabel('linear Power, [kW/m]' ,size=14)
        axis.set_xlabel('axial position, [m]',size=14) 
          
        l=legend(loc=8,ncol=2)
        axis.set_xlim([0,3.6576])
        tight_layout()
        axis.set_title('Linear Power and integral power ration \n of all cases, burnup 0',size=18)  
        #savefig('V:\\master report\\figures\\powercycle{0}.pdf'.format(C))
        #axis.set_title('Linear Power development with burnup \n case {0}'.format(C),size=18)   
        tight_layout()    
        #savefig('D:/dropbox/Dropbox/plots/spring2013/power0day_case0123456.pdf'.format(C))
        #axis.set_ylim([500,1200])    
    show()   

    if 2.2 in subcase:
        print shape(tp)
        figure('powercycle500ALL')
        plt.clf()
        axis=plt.subplot(111)
        
        ph=[0]*29
        ii=[29]
        for i in range(len(ii)):
            for j in [0,1,2,4,5,6]:
                c = cm.jet((j)/7,1)
                ph[j],=step(z_mesh,Stepper(LinPow(tp,j,ii[i]),0)/1000,color=c,where='post',label='case {}:{:>6.1f} '.format(j,dot(LinPow(tp,j,ii[i]),z_mesh2)))
        ph[3],=step(z_mesh,Stepper(LinPow(tp,3,ii[i]),0)/1000*12,color=c,where='post',label='case {}: {:>6.1f} '.format(3,dot(LinPow(tp,3,ii[i])*12,z_mesh2)))
        axis.yaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.xaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.set_ylabel('linear Power, [kW/m]' ,size=14)
        axis.set_xlabel('axial position, [m]',size=14) 
          
        l=legend(loc=8,ncol=2)
        axis.set_xlim([0,3.6576])
        tight_layout()
        #savefig('V:\\master report\\figures\\powercycle{0}.pdf'.format(C))
        axis.set_title('Linear Power and integral power ration \n of all cases, burnup 500',size=18)   
        tight_layout()    
        #savefig('D:/dropbox/Dropbox/plots/spring2013/power500day_case0123456.pdf'.format(C))
        #axis.set_ylim([500,1200])    
    show()       
########### end of axial power profile plot ###############    

########## temp & density ###################


if 2 in plotcase: #axial temperature profile
    if 1 in subcase:
        ph=[0,0,0,0,0,0]
        plt.figure()
        axis=plt.subplot(111)
        for h in [0,1,2]:#range(3):
            c = cm.hot((h)/3,1)
            for k in range(5):
                ph[h],=plot(z_mesh[:-1],tt5[h,0,k,0,:],'-',color=c)
        
        axis.set_xlim([0,3.7])
        axis.set_ylim([500,1100])
        
        axis.xaxis.grid(True,'major',linewidth=2)
        axis.yaxis.grid(True,'major',linewidth=2)
        
        axis.set_ylabel('section temperature, [K]' ,size=14)
        axis.set_xlabel('axial position, [m]',size=14) 
        axis.set_title('axial temperature profile at 0 EFPD,\n for all 5 radial sections',size=18)    
        l=legend([ph[0],ph[1],ph[2]],["case 1","case 2","case 3"],loc=2)
        axis.annotate('I.', xy=(3.2, 1030),size=14)
        axis.annotate('II.', xy=(3.2, 900),size=14)
        axis.annotate('III.', xy=(3.2, 760),size=14)
        axis.annotate('clad', xy=(3.1, 660),size=14)
        axis.annotate('coolant', xy=(3, 570),size=14)
        plt.show()    

    if 2 in subcase: #density axial
        figure('axdensity',figsize=(8.15, 3.075))
        axis=plt.subplot(111)
        step(z_mesh,Stepper(td[0,6,-1,0,:],1))
        axis.set_ylabel('coolant density, [kg/m^3]' ,size=14)
        axis.set_xlabel('axial position, [m]',size=14) 
        
        axis.xaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.yaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.set_ylim([400,800])
        axis.set_xlim([0,3.6576])
        axis.annotate('60 EPFD', xy=(1, 500),size=14,alpha=0.5)
        
        axis.set_yticks([400,500,600,700,800], minor=False)
        plt.tight_layout()
        #savefig('V:\\master report\\figures\\density.eps')
        #axis.set_title('Coolant Density Profile at 50 EFPD, case 0',size=18)
        plt.tight_layout()
        #savefig('D:/dropbox/Dropbox/plots/spring2013/0/density.pdf')
        show()
        
########## plotonium  #################
if 3 in plotcase:
    
  
    if 1 in subcase:    # plutonium buildup over cycle
        plt.figure('plutcycle0')
        axis=plt.subplot(111)
        
        ii=[0,6,8,11,14,17,20,23,26,29]
        lh=[0]*len(ii)
        for i in range(len(ii)):
            c = cm.jet((ii[i])/29,1)
            lh[i],=step(z_mesh,Stepper(PuDens(tpu[0][ii[i],:,:,:,0],30),0),color=c,where='post',label='{} EFPD'.format(ts[ii[i]]))
            step(z_mesh,Stepper(PuDens(tpu[0][ii[i],:,:,:,1],30),0),color=c,where='post')        
        
        
        # Shink current axis by 20%
        box = axis.get_position()
        axis.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        
        # Put a legend to the right of the current axis
        axis.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        
            
        axis.set_xlim([0,3.6576])
        #axis.set_ylim([500,1100])
        axis.ticklabel_format(style='sci', scilimits=(0,0), axis='y')
        axis.xaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.yaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        
        axis.set_ylabel('Pu concentration, [(barn cm)$^{-1}$]' ,size=14)
        axis.set_xlabel('axial position, [m]',size=14) 
        #l=legend([lh[0],lh[-1]],["50 EFPD","500 EFPD"],loc=2)    
        axis.annotate('Pu239', xy=(2.5, 0.00012),size=16,color=[0.5,0.5,0.5])
        axis.annotate('PU241', xy=(2.5, 0.00002),size=16,color=[0.5,0.5,0.5])     
        #tight_layout()        
        show()  
        savefig('D:/dropbox/Dropbox/plots/spring2013/0/plutcycle.pdf')

        
        
        #axis.set_title('The Plutonium buildup\n during the cycle',size=18)
        #set_fontsize([manager.canvas.figure for manager in matplotlib._pylab_helpers.Gcf.get_all_fig_managers()][0],beamerfontsize)	
        #tight_layout()
        # Shink current axis by 20%
        #box = axis.get_position()
        #axis.set_position([box.x0, box.y0, box.width * 0.6, box.height])
        
        # Put a legend to the right of the current axis
        #axis.legend(loc='center left', bbox_to_anchor=(1, 0.5),prop={'size':beamerfontsize})
        #draw()
        #savefig('V:\\master report\\figures\\Pu_buildupbeamer.pdf')

    if 1.08 in subcase:    # plutonium buildup over cycle
        plt.figure()
        axis=plt.subplot(111)

        i=9
        a,=step(z_mesh,Stepper(PuDens(tpu[0,i,:,:,:,0],30),0),color='blue',where='post',label='{} EFPD'.format(50*(i+1)))
        
        ax2 = twinx()
        b,=step(z_mesh,Stepper(PuDens((tpu[8,i,:,:,:,0]-tpu[0,i,:,:,:,0])/tpu[0,i,:,:,:,0]*100,30),0),color='red',where='post',label='{} EFPD'.format(50*(i+1)))


        axis.set_xlim([0,3.6576])
        #axis.set_ylim([500,1100])
        axis.ticklabel_format(style='sci', scilimits=(0,0), axis='y')
        axis.xaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.yaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        
        axis.set_ylabel('Pu concentration, [(barn cm)$^{-1}$]' ,size=14)
        axis.set_xlabel('axial position, [m]',size=14) 
        ax2.set_ylabel('relative difference, [$\%$]',size=14) 
        #l=legend([lh[0],lh[-1]],["50 EFPD","500 EFPD"],loc=2)    
        axis.annotate('Pu239', xy=(2.5, 0.00012),size=16,color=[0.5,0.5,0.5])
        axis.annotate('PU241', xy=(2.5, 0.00002),size=16,color=[0.5,0.5,0.5])     
        l=legend([a,b],["case 0","deviation of case 8",],loc=2)   
        plt.axhline(y=0,color='black')        
        show()  
        #savefig('V:\\master report\\figures\\Pu_buildup.eps')

        
        
        axis.set_title('The axial Pu concentration\n at 500  EFPD',size=18)
        set_fontsize([manager.canvas.figure for manager in matplotlib._pylab_helpers.Gcf.get_all_fig_managers()][0],beamerfontsize)	

        #savefig('D:\\dropbox\\Dropbox\\plots\\case8\\axial_relative_difference.png')
        #savefig('D:\\dropbox\\Dropbox\\plots\\case8\\axial_relative_difference.pdf')
            
    if 1.1 in subcase:    # plutonium buildup over cycle
        plt.figure()
        axis=plt.subplot(111)
        lh=[0]*10
        for i in range(10):
            c = cm.jet((i)/10,1)
            lh[i],=step(z_mesh,Stepper(PuDens(tpu[0,i,:,:,:,0],30),0),color=c,where='post',label='{} EFPD'.format(50*(i+1)))
            #step(z_mesh,Stepper(PuDens(tpu[0,i,:,:,:,1],30),0),color=c,where='post')        
        
        
        # Shink current axis by 20%
        box = axis.get_position()
        axis.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        
        # Put a legend to the right of the current axis
        axis.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        
            
        axis.set_xlim([0,3.6576])
        #axis.set_ylim([500,1100])
        axis.ticklabel_format(style='sci', scilimits=(0,0), axis='y')
        axis.xaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.yaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        
        axis.set_ylabel('Pu concentration, [(barn cm)$^{-1}$]' ,size=14)
        axis.set_xlabel('axial position, [m]',size=14) 
        #l=legend([lh[0],lh[-1]],["50 EFPD","500 EFPD"],loc=2)    
        #axis.annotate('Pu239', xy=(2.5, 0.00012),size=16,color=[0.5,0.5,0.5])
        #axis.annotate('PU241', xy=(2.5, 0.00002),size=16,color=[0.5,0.5,0.5])     
        #tight_layout()        


        
        
        #axis.set_title('The Plutonium buildup\n during the cycle',size=18)
        set_fontsize([manager.canvas.figure for manager in matplotlib._pylab_helpers.Gcf.get_all_fig_managers()][0],beamerfontsize)	
        tight_layout()
        # Shink current axis by 20%
        box = axis.get_position()
        axis.set_position([box.x0, box.y0, box.width * 0.6, box.height])
        
        # Put a legend to the right of the current axis
        axis.legend(loc='center left', bbox_to_anchor=(1, 0.5),prop={'size':beamerfontsize})
        show()
        #savefig('V:\\master report\\figures\\Pu_buildupbeamer.pdf')        
        
        
    if 1.5 in subcase:
        plt.figure()   # u235 depletion case 0
        axis=plt.subplot(111)
        lh=[0]*10
        for i in range(10):
            c = cm.jet((i)/10,1)
            lh[i],=step(z_mesh,Stepper(PuDens(tpu[0,i,:,:,:,2],30),0),color=c,where='post')
        #    plot(z_mesh[1:],tpu[1,i,2,0,:,3]/100,color=c)        
            
        axis.set_xlim([0,3.6576])
        #axis.set_ylim([500,1100])
        
        axis.xaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.yaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.ticklabel_format(style='sci', scilimits=(0,0), axis='y')
        axis.set_ylabel('U concentration, [1/(barn cm)]' ,size=14)
        axis.set_xlabel('axial position, [m]',size=14) 
        axis.set_title('U235 depletion over cycle\n case 0',size=18)    
        l=legend([lh[0],lh[-1]],["50 EFPD","500 EFPD"],loc=2)    
        #axis.annotate('U235', xy=(2.5, 0.00015),size=16,alpha=0.5)
        #axis.annotate('U238', xy=(2.5, 0.00003),size=16,alpha=0.5)        
        tight_layout()
        show() 
        #savefig('D:\dropbox\Dropbox\plots\case0\isotopics\U235_depletion.png')

        
    if 2 in subcase: #compare plut in cases 1-4, axial
        plt.figure()    
        axis=plt.subplot(111)
        lh=[0,0,0,0,0]
        for i in [0,5,9]:
            
            for j in [1,2,3,4]:
                c = cm.jet((j)/3,1)
                lh[j],=plt.plot(z_mesh[1:],tpu[j,i,2,0,:,0],color=c,)
        #axis.set_xlim([0,3.7])
        #axis.set_ylim([500,1100])
        
        axis.xaxis.grid(True,'major',linewidth=2)
        axis.yaxis.grid(True,'major',linewidth=2)
        
        axis.set_ylabel('Pu239 concentration, [1/(barn cm)]' ,size=14)
        axis.set_xlabel('axial position, [m]',size=14) 
        axis.set_title('Pu 239 concentration for 50, 300 and 500 EFPD\n cases 1-4, 3rd of 3 fuel regions',size=18)    
        l=legend([lh[0],lh[1],lh[2],lh[3]],["case 1","case 2","case 3","case 4"],loc=6)    
        axis.annotate('50 EFPD.', xy=(3.0, 0.00001),size=14)
        axis.annotate('300 EFPD', xy=(2.6, 0.00014),size=14)
        axis.annotate('500 EFPD', xy=(2.4, 0.000185),size=14)
        
        
        show()    

    if 3 in subcase: # radial pu
        plt.figure('radpu')    
        clf()
        axis=plt.subplot(111)
        #lh=[0,0,0,0]
        x=sqrt(linspace(0,30,31)/30)*0.004025
        ii=[6,19,29]
        for i in range(len(ii)):
            c = cm.jet((ii[i])/29,1)
            plt.step(x*1000,Stepper(sum(tpu[0][ii[i],:,:,24,0],1),0),'.-',color=c,where='post',label=ts[ii[i]])
        axis.set_xlim([0,4.025])
        #axis.set_ylim([500,1100])
        
        axis.xaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.yaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        
        axis.set_ylabel('Pu239 concentration, [1/(barn cm)]' ,size=14)
        axis.set_xlabel('radial position, [mm]',size=14) 
        
        l=legend(loc=2) 
        tight_layout()
        axis.ticklabel_format(style='sci', scilimits=(0,0), axis='y')
        #savefig('V:\\master report\\figures\\radial_Pu.eps')
        #axis.set_title('Radial Pu 239 distribution for 50, 300 and 500 EFPD\n case 0, at z=1.8m',size=18)    
        tight_layout()
        savefig('D:/dropbox/Dropbox/plots/spring2013/0/radial_pu.pdf')
        
        show()
        
        

    if 4 in subcase:
      
        j=29 #burn up set
        k=24# z-plane 
        
        figure('radpu vergleich')
        clf()
        axis=plt.subplot(111)
        r3=np.sqrt(np.linspace(0,3,4)/3)*0.004025*1000
        r30=np.sqrt(np.linspace(0,30,31)/30)*0.004025*1000
        for i in range(3):
            a,=plt.bar(r3[i],tpu[1][j,i,0,k,0],r3[i+1]-r3[i],0,color='red',edgecolor='black',alpha=0.3)
        
        for i in range(30):
            b,=plt.bar(r30[i],tpu[0][j,i,0,k,0],r30[i+1]-r30[i],0,color='blue',edgecolor='black',alpha=0.3)
        axis.xaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.yaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.set_ylabel('Pu239 concentration, [1/(barn cm)]' ,size=14)
        axis.set_xlabel('radial position, [mm]',size=14) 
        l=legend([a,b],["case 1","case 0",],loc=2)         
        axis.set_xlim([0,4.026])
        c=sum(tpu[1][j,:,0,k,0])*0.004025**2/3
        d=sum(tpu[0][j,:,0,k,0])*0.004025**2/30
        axis.ticklabel_format(style='sci',axis='y', scilimits=(0,0))
        e=(c-d)/d*100
        tight_layout()
        #axis.annotate( '{0} % difference\n in Pu 239 mass'.format("%.2f" % e) , xy=(0.0005, 0.00025),size=14)
        show()
        
        #savefig('V:\\master report\\figures\\radial_Pu01.eps')
        #axis.set_title('Radial Pu 239 distribution for 500 EFPD\n case 0 and 1, at z=1.8m',size=18)    
        tight_layout()
        savefig('D:/dropbox/Dropbox/plots/spring2013/radial_pu01.pdf')
  
        
    if 5 in subcase:    
        # mass plots 
        for k in range(10):
            for i in range(16):
                plt.figure(i)
                axis=plt.subplot(111)
                for j in range(30):
                    c = cm.jet((i)/16,1)
                    step(z_mesh,Stepper(tpu[0,k,j,i,:,0],0),color=c,where='post')
                    axis.xaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
                    axis.yaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
                    axis.set_ylabel('Pu239 concentration, [1/(barn cm)]' ,size=14)
                    axis.set_xlabel('axial position, [m]',size=14) 
                    axis.set_title('Axial Pu 239 distribution for %03d EFPD\n case 0, angle %02d ' % ((k+1)*50,i) ,size=18)    
            
                #savefig('D:\\dropbox\\Dropbox\\plots\\case0\\isotopics\\axial_pu39_bu%03d_a%02d.png' % ((k+1)*50,i))
            
                #show()
                
                
    if 6 in subcase:    
        # mass plots
        for k in range(10):
            for i in range(16):
                plt.figure(i)
                axis=plt.subplot(111)
                for j in range(30):
                    c = cm.jet((i)/16,1)
                    step(z_mesh,Stepper(tpu[0,k,j,i,:,1]),color=c,where='post')
                    axis.xaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
                    axis.yaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
                    axis.set_ylabel('Pu239 concentration, [1/(barn cm)]' ,size=14)
                    axis.set_xlabel('axial position, [m]',size=14) 
                    axis.set_title('Axial Pu 241 distribution for %03d EFPD\n case 0, angle %02d ' % ((k+1)*50,i) ,size=18)    
            
                #savefig('D:\\dropbox\\Dropbox\\plots\\case0\\isotopics\\axial_pu41_bu%03d_a%02d.png' % ((k+1)*50,i))
            
                #show()
                                
    if 7 in subcase:
      
        z=24# z-plane 
        
        figure()
        axis=plt.subplot(111)
        pmarker=['--','-.',':','o-']
        ### legend stuff
        plot([-2,-1],[0,0],'-',color=cm.jet((0)/10,1))
        plot([-2,-1],[0,0],'-',color=cm.jet((9)/10,1))
        plot([-2,-1],[0,0],'-',color=[0,0,0])
        plot([-2,-1],[0,0],'--',color=[0,0,0])
        plot([-2,-1],[0,0],'--',color=[0,0,0])
        plot([-2,-1],[0,0],'-.',color=[0,0,0])
        plot([-2,-1],[0,0],':',color=[0,0,0])
        legend(['50 EFPD','500 EFPD','case 0','case 1','case 2','case 3'],ncol=2,loc=3)
        ### end legend stuff
        for i in range(10):
            c = cm.jet((i)/10,1)
            plot(sum(tpu[0,i,20:30,:,24,0],axis=0)/10,'-',color=c)
            for j in range(1,4):
                plot(tpu[j,i,2,:,z,0],pmarker[j-1],color=c,ms=10)
            
                    
        axis.xaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.yaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.set_ylabel('Pu239 concentration, [1/(barn cm)]' ,size=14)
        axis.set_xlabel('something like azimuthal position',size=14) 
        axis.set_title('Azimuthal Pu 239 distribution for 50-500 EFPD\n case 0 - 3, at z=1.8m',size=18)    
        axis.set_ylim([0,0.00018])
        axis.set_xlim([0,15])
        axis.ticklabel_format(style='sci', scilimits=(0,0), axis='y')
        #l=legend([a,b],["3 nodes","30 nodes",],loc=2)         
        
        #c=sum(tpu[1,j,:,0,k,0])*0.004025**2/3
        #d=sum(tpu[0,j,:,0,k,0])*0.004025**2/30
        #e=(c-d)/d*100
        
        #axis.annotate( '{0} % difference\n in Pu 239 mass'.format("%.2f" % e) , xy=(0.0005, 0.00025),size=14)
        #savefig('D:\\dropbox\\Dropbox\\plots\\case0\\isotopics\\azimuthal_PU_0to3_50to500.png')
        
        show()
        
        
        
        
        z=24# z-plane 
        
        figure()
        axis=plt.subplot(111)
        pmarker=['--','-.',':','o-']

        for i in [9]:
            c = cm.jet((i)/10,1)
            plot(sum(tpu[0,i,20:30,:,24,0],axis=0)/10,'-',color=c)
            for j in range(1,4):
                plot(tpu[j,i,2,:,z,0],pmarker[j-1],color=c,ms=10)
            
        axis.ticklabel_format(style='sci', scilimits=(0,0), axis='y')
                
        axis.xaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.yaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.set_ylabel('Pu239 concentration, [1/(barn cm)]' ,size=14)
        axis.set_xlabel('something like azimuthal position',size=14) 
        axis.set_title('Azimuthal Pu 239 distribution for 500 EFPD\n case 0 - 3, at z=1.8m',size=18)    
        axis.set_ylim([0.00016,0.00017])
        axis.set_xlim([0,15])
        legend(["case 0","case 1","case 2","case 3"],loc=3)
        #savefig('D:\\dropbox\\Dropbox\\plots\\case0\\isotopics\\azimuthal_PU_0to3_500.png')
    


    if 8 in subcase:
        gd=1
        if gd==1:
            a=shape(tpu)
            volume=zeros(a[:-1])
            tpu_sum=zeros(a[:2])
            tpu_sum2=zeros(a[:3])
            tpu_sumz=zeros([a[0],a[1],a[4]])
            
            for i in range(a[0]):
                for j in range(a[1]):
                    for k in range(a[2]):
                        for l in range(a[3]):
                            for m in range(a[4]):
                                if i==0 :
                                    rr=0.004025**2/30 #case 0
                                else:
                                    rr=0.004025**2/3 #case 1
                                aa=2*pi/16
                                zz=z_mesh2[m]
                                volume[i,j,k,l,m]=rr*aa*zz
                                #pass
                        tpu_sum2[i,j,k]=sum(tpu[i,j,k,:,:,0]*volume[i,j,k,:,:])        
                    tpu_sum[i,j]=sum(tpu[i,j,:,:,:,0]*volume[i,j])   

                    
                    
        mpu239=239.0521565      # atomic mass of pu 239               
        conv1=1.660538921E-24   # mass of one amu in gram 
        conv2=1E+30             # conversion from 1/barn*cm to 1/m^3
        conv=mpu239*conv1*conv2 # total conversion factor to get grams
        
        figure()
        axis=plt.subplot(111)
        width=0.15
        lh=[0]*6
        
        bucases=arange(10)
        grd = axis.yaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7],zorder=4)
        for i in [0,1,2,3,4,5]:
            c = array(cm.hsv((i+1)/6,1))
            for j in bucases:
                for k in range(3):
                    if i==0:
                        case0plot=sum(tpu_sum2[i,j,(10*k):(10*(k+1))])
                        lh[i],=bar(k+(i+j/10)*width,case0plot*conv,width/5,0,color=c,zorder=10-j)
                
                    else:
                        lh[i],=bar(k+(i+j/10)*width,tpu_sum2[i,j,k]*conv,width/5,0,color=c,zorder=10-j)

        axis.set_ylabel('Pu239 mass, [g]' ,size=14)
        axis.set_xlabel('fuel region' ,size=14)
        legend([lh[0],lh[1],lh[2],lh[3],lh[4],lh[5]],['case 0','case 1','case 2','case 3','case 4','case 5'],loc=2)
        axis.set_title('Total Pu239 mass for the 3 fuel regions at during cycle\n case 0 - 3, 50 - 500 EFPD',size=18)    
        axis.set_xticks(arange(3)+0.375)
        axis.set_xticklabels( ('I.','II.','III.') ,size=14)
        axis.set_axisbelow(True)
        axis.annotate('case 5 data \n is missing ', xy=(1, 7),size=14,alpha=0.5)
        #savefig('D:\\dropbox\\Dropbox\\plots\\case0\\isotopics\\radial_barplot50500.png')
    
        figure()
        axis=plt.subplot(111)
        width=0.15
        lh=[0]*6
        
        bucases=arange(10)
        grd = axis.yaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7],zorder=4)
        for i in [0,1,2,3,4,5]:
            c = array(cm.hsv((i+1)/6,1))
            for j in [6,9]:
                for k in range(3):
                    if i==0:
                        case0plot=sum(tpu_sum2[i,j,(10*k):(10*(k+1))])
                        lh[i],=bar(k+(i+j/10)*width,case0plot*conv,width/2,0,color=c,zorder=10-j)
                
                    else:
                        lh[i],=bar(k+(i+j/10)*width,tpu_sum2[i,j,k]*conv,width/2,0,color=c,zorder=10-j)
                        
        axis.set_ylabel('Pu239 mass, [g]' ,size=14)
        axis.set_xlabel('fuel region' ,size=14)
        legend([lh[0],lh[1],lh[2],lh[3],lh[4],lh[5]],['case 0','case 1','case 2','case 3','case 4','case 5'],loc=2)
        axis.set_title('Total Pu239 mass for the 3 fuel regions \n case 0 - 3, 300 and 500 EFPD',size=18)    
        axis.set_xticks(arange(3)+0.375)
        axis.set_xticklabels( ('I.','II.','III.') ,size=14)
        axis.set_axisbelow(True)
        axis.annotate('case 5 data \n is missing ', xy=(0.8, 8),size=14,alpha=0.5)
        #savefig('D:\\dropbox\\Dropbox\\plots\\case0\\isotopics\\radial_barplot500.png')
    
    if 9 in subcase:
    
        gd=1
        if gd==1:
            a=shape(tpu)
            volume=zeros(a[:-1])
           
            
            tpu_sumz=zeros([a[0],a[1],a[4]])
            
            for i in range(a[0]):
                for j in range(a[1]):
                    for k in range(a[2]):
                        for l in range(a[3]):
                            for m in range(a[4]):
                                if i==0 :
                                    rr=0.004025**2/30 #case 0
                                else:
                                    rr=0.004025**2/3 #case 1
                                aa=2*pi/16
                                zz=z_mesh2[m]
                                volume[i,j,k,l,m]=rr*aa*zz
                                #pass
 
                    for m in range(a[4]):
                        if i==0:
                            tpu_sumz[i,j,m]=sum(tpu[i,j,:,:,m,0]/(30*16))
                        else:    
                            tpu_sumz[i,j,m]=sum(tpu[i,j,:,:,m,0]/(3*16))
                        
                        
        plt.figure()
        axis=plt.subplot(111)
        lh=[0]*10
        for i in range(6):
            c = cm.hsv((i)/6,1)
            for j in [6,9]:
                
                lh[i],=plot(z_mesh[1:],tpu_sumz[i,j,:],color=c)
      
            
        axis.set_xlim([0,3.7])
        #axis.set_ylim([500,1100])
        
        axis.xaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.yaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.set_ylim([0.00008,0.00016])
        axis.set_ylabel('Pu concentration, [1/(barn cm)]' ,size=14)
        axis.set_xlabel('axial position, [m]',size=14) 
        axis.set_title('Pu 239 and 241 buildup over cycle\n case 1, 3rd of 3 fuel regions',size=18)    
        l=legend([lh[0],lh[1],lh[2],lh[3],lh[4],lh[5]],['case 0','case 1','case 2','case 3','case 4','case 5'],loc=2,ncol=2)    
      
        show()  
        #savefig('D:\dropbox\Dropbox\plots\case0\isotopics\\axial_Pu_allcases300500.png')

    if 10 in subcase:    # plutonium buildup over cycle spring2013
  
        plt.figure()
        axis=plt.subplot(111)
        lh=[0]*TS
        for i in range(TS):
            c = cm.gist_rainbow((TS-i)/TS,1)
            lh[i],=plot(z_mesh3,sum(tpu[0,i,0,:,:,0],0)/16,color=c,label='{} EFPD'.format(timesteps[i]))
            #step(z_mesh,Stepper(PuDens(tpu[0,i,:,:,:,1],30),0),color=c,where='post')        
    
        
        # Shink current axis by 20%
        box = axis.get_position()
        #axis.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        
        # Put a legend to the right of the current axis
        axis.legend([lh[29],lh[5],lh[1]],['500 EFPD','20 EFPD','4 EFPD'],loc=4)
        
            
        axis.set_xlim([0,3.6576])
        #axis.set_ylim([500,1100])
        axis.ticklabel_format(style='sci', scilimits=(0,0), axis='y')
        axis.xaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.yaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        
        axis.set_ylabel('239Pu concentration, [(barn cm)$^{-1}$]' ,size=14)
        axis.set_xlabel('axial position, [m]',size=14) 
        #l=legend([lh[0],lh[-1]],["50 EFPD","500 EFPD"],loc=2)    
        axis.set_title('STAR-DECART coupled simulation:\n axial Pu 239 concentration  at the center \n fuel node (30 radial fuel nodes)',size=18)
        subplots_adjust(top=0.81)
        show()  
        #savefig('D:\\dropbox\\Dropbox\\plots\\spring2013\\teaser_center.pdf')
        
        
        plt.figure()
        axis=plt.subplot(111)
        lh=[0]*TS
        for i in range(TS):
            c = cm.gist_rainbow((TS-i)/TS,1)
            lh[i],=plot(z_mesh3,sum(tpu[0,i,29,:,:,0],0)/16,color=c,label='{} EFPD'.format(timesteps[i]))
            #step(z_mesh,Stepper(PuDens(tpu[0,i,:,:,:,1],30),0),color=c,where='post')        
    
        
        # Shink current axis by 20%
        box = axis.get_position()
        #axis.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        
        # Put a legend to the right of the current axis
        axis.legend([lh[29],lh[5],lh[1]],['500 EFPD','20 EFPD','4 EFPD'],loc=4)
        subplots_adjust(top=0.81)
            
        axis.set_xlim([0,3.6576])
        #axis.set_ylim([500,1100])
        axis.ticklabel_format(style='sci', scilimits=(0,0), axis='y')
        axis.xaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.yaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        
        axis.set_ylabel('239Pu concentration, [(barn cm)$^{-1}$]' ,size=14)
        axis.set_xlabel('axial position, [m]',size=14) 
        #l=legend([lh[0],lh[-1]],["50 EFPD","500 EFPD"],loc=2)    
        axis.set_title('STAR-DECART coupled simulation:\n axial Pu 239 concentration  at the peripheral \n fuel node (30 radial fuel nodes)',size=18)
        show()  
        #savefig('D:\\dropbox\\Dropbox\\plots\\spring2013\\teaser_periphery.pdf')       
        
if 3.5 in plotcase:

    for i in range(0,49,2):
        c = cm.hot((i)/50,1)
        plot(totalpu[3,9,2,:,i,0],color=c)
    

    show()
############ end of putonium

############ flux plot #################
if 4 in plotcase:

                
    grouplimit=[
    1E+07,       # upper bound
    6.0653E+06, # 1      #lower bound 1st group
    3.6788E+06, # 2
    2.2313E+06,  # 3
    1.3534E+06, #  4
    8.2085E+05, #  5
    4.9787E+05, #  6 
    1.8316E+05, #  7 
    6.7379E+04, #  8 
    9.1188E+03, #  9 
    2.0347E+03, # 10 
    1.3007E+02, # 11 
    7.8893E+01, # 12 
    4.7851E+01, # 13 
    2.9023E+01, # 14 
    1.3710E+01, # 15 
    1.2099E+01, # 16 
    8.3153E+00, # 17 
    7.3382E+00, # 18 
    6.4760E+00, # 19 
    5.7150E+00, # 20 
    5.0435E+00, # 21 
    4.4509E+00, # 22 
    3.9279E+00, # 23 
    2.3824E+00, # 24 
    1.8554E+00, # 25 
    1.4574E+00, # 26 
    1.2351E+00, # 27 
    1.1664E+00, # 28 
    1.1254E+00, # 29 
    1.0722E+00, # 30 
    1.0137E+00, # 31 
    9.7100E-01, # 32 
    9.1000E-01, # 33 
    7.8208E-01, # 34 
    6.2506E-01, # 35 
    5.0323E-01, # 36 
    3.5767E-01, # 37 
    2.7052E-01, # 38 
    1.8443E-01, # 39 
    1.4572E-01, # 40 
    1.1157E-01, # 41 
    8.1968E-02, # 42 
    5.6922E-02, # 43 
    4.2755E-02, # 44 
    3.0613E-02, # 45 
    1.2396E-02, # 46 
    1.0000E-04]#  47     
    if 1 in subcase:
        # spectrum. obsolete atm
        print '1'
        plt.figure()
        axis=plt.subplot(111)
        #axis.set_yscale('log')
        axis.set_xscale('log')
        for i in [0,10,20,30,40]:
            plot(grouplimit[1:],tnflx[0][9,29,0,i,:],'.-')
        axis.xaxis.grid(True,'major',linewidth=2)
        axis.yaxis.grid(True,'major',linewidth=2)
        
        axis.legend(['inner','outter fuel','mod'])
        
        axis.set_ylabel('Normalized Flux' ,size=14)
        axis.set_xlabel('Neutron Energy, [eV]',size=14) 
        axis.set_title('47 group spectrum at 500 EPFD for 5 z-planes,',size=18) 
        plt.show()
    if 2 in subcase:
        # planewise spectrum for spacer depression, zoom
        print '2'    
        plt.figure()
        r,a,z=18,0,30
        axis=plt.subplot(111)
        z=[31,32,33,34,35]
        lm=[0]*len(z)
    
        for j in range(len(z)):
            c = cm.jet((j)/len(z),1)
            lm[j],=step(grouplimit,Stepper(tnflx[0][0,r,a,z[j],:],1),color=c)
            #for i in range(len(grouplimit)):
            #    if i==0:
            #        lm[j]=plt.bar(grouplimit[i],tnflx[0][9,r,a,z[j],i],1e7-grouplimit[i],0,color='None',edgecolor=c)
            #        pass
            #    else:    
            #        plt.bar(grouplimit[i],tnflx[0][9,r,a,z[j],i],grouplimit[i-1]-grouplimit[i],color='None',edgecolor=c)
                    #print i,grouplimit[i],grouplimit[i-1]-grouplimit[i]
        legend(lm,['plane '+str(z[0]),'plane '+str(z[1]),'plane '+str(z[2])+' (spacer)','plane '+str(z[3]),'plane '+str(z[4])],loc=2)
        #axis.set_yscale('log')
        axis.set_xscale('log')   
        axis.set_ylabel('Normalized Flux' ,size=14)
        axis.set_xlabel('Neutron Energy, [eV]',size=14) 
        axis.set_title('47 group spectrum at 500 EPFD for 5 z-planes\n 30th of 30 radial fuel section ',size=18)     
        axis.xaxis.grid(True,'major',linewidth=1,alpha=0.3)
        axis.yaxis.grid(True,'major',linewidth=1,alpha=0.3)
        axis.set_xlim(0.005,1)
        axis.set_ylim(0,1)
        #pltfigure()
        #step(grouplimit,Stepper(tnflx[0][0,30,0,32,:],1),where='post')
        #savefig('D:\dropbox\Dropbox\plots\case0\isotopics\Spectrum at spacer plane')
        show()
        

        
    if 4 in subcase:
        pass
    
    
    if 5 in subcase: # flux vs burnup comparison
        plt.figure()
        axis=plt.subplot(111)
        
        step(grouplimit,Stepper((tnflx[0][0,29,0,24,:]),1))
        step(grouplimit,Stepper((tnflx[0][9,29,0,24,:]),1))
        axis.set_xscale('log')   
        axis.set_ylabel('Normalized Flux' ,size=14)
        axis.set_xlabel('Neutron Energy, [eV]',size=14) 
        axis.set_title('Flux at 50 and 500 EFPD \n case 0',size=18)     
        axis.xaxis.grid(True,'major',linewidth=1,alpha=0.3)
        axis.yaxis.grid(True,'major',linewidth=1,alpha=0.3)
        legend(['50 EFPD','500 EFPD'],loc=2)
        show()
        
        plt.figure()
        axis=plt.subplot(111)
        plt.figure()
        axis=plt.subplot(111)
        
        step(grouplimit,Stepper((tnflx[0][9,29,0,24,:]-tnflx[0][0,29,0,24,:])*100/tnflx[0][0,29,0,24,:],1))
        axis.set_xscale('log')   
        axis.set_ylabel('Change in Normalized Flux, [%]' ,size=14)
        axis.set_xlabel('Neutron Energy, [eV]',size=14) 
        axis.set_title('Relative change in Flux from 50 to 500 EFPD \n case 0',size=18)     
        axis.xaxis.grid(True,'major',linewidth=1,alpha=0.3)
        axis.yaxis.grid(True,'major',linewidth=1,alpha=0.3)
        show()
        
        plt.figure()
        axis=plt.subplot(111)
        
        step(grouplimit,Stepper((tnflx[0][9,29,0,24,:]-tnflx[0][0,29,0,24,:]),1))
        axis.set_xscale('log')   
        axis.set_ylabel('Change in Normalized Flux,' ,size=14)
        axis.set_xlabel('Neutron Energy, [eV]',size=14) 
        axis.set_title('Absolute change in Flux from 50 to 500 EFPD \n case 0',size=18)     
        axis.xaxis.grid(True,'major',linewidth=1,alpha=0.3)
        axis.yaxis.grid(True,'major',linewidth=1,alpha=0.3)
        show()
 
    if 6 in subcase: # flux vs burnup comparison
        plt.figure()
        axis=plt.subplot(111)
        
        step(grouplimit,Stepper((tnflx[1][0,2,0,24,:]),1))
        step(grouplimit,Stepper((tnflx[1][9,2,0,24,:]),1))
        axis.set_xscale('log')   
        axis.set_ylabel('Normalized Flux' ,size=14)
        axis.set_xlabel('Neutron Energy, [eV]',size=14) 
        axis.set_title('Flux at 50 and 500 EFPD \n case 1',size=18)     
        axis.xaxis.grid(True,'major',linewidth=1,alpha=0.3)
        axis.yaxis.grid(True,'major',linewidth=1,alpha=0.3)
        legend(["50 EFPD","500 EFPD"],loc=2)
        show()
        #savefig('D:\\dropbox\\Dropbox\\plots\\case0\\isotopics\\flux50and500.png')
        plt.figure()
        axis=plt.subplot(111)

        
        step(grouplimit,Stepper((tnflx[1][9,2,0,24,:]-tnflx[1][0,2,0,24,:])*100/tnflx[1][0,2,0,24,:],1))
        axis.set_xscale('log')   
        axis.set_ylabel('Change in Normalized Flux, [%]' ,size=14)
        axis.set_xlabel('Neutron Energy, [eV]',size=14) 
        axis.set_title('Relative change in Flux from 50 to 500 EFPD \n case 1',size=18)     
        axis.xaxis.grid(True,'major',linewidth=1,alpha=0.3)
        axis.yaxis.grid(True,'major',linewidth=1,alpha=0.3)
        show()
        #savefig('D:\\dropbox\\Dropbox\\plots\\case0\\isotopics\\flux50and500_relative change.png')
        
        
        plt.figure()
        axis=plt.subplot(111)
        
        step(grouplimit,Stepper((tnflx[1][9,2,0,24,:]-tnflx[1][0,2,0,24,:]),1))
        axis.set_xscale('log')   
        axis.set_ylabel('Change in Normalized Flux,' ,size=14)
        axis.set_xlabel('Neutron Energy, [eV]',size=14) 
        axis.set_title('Absolute change in Flux from 50 to 500 EFPD \n case 1',size=18)     
        axis.xaxis.grid(True,'major',linewidth=1,alpha=0.3)
        axis.yaxis.grid(True,'major',linewidth=1,alpha=0.3) 
        #savefig('D:\\dropbox\\Dropbox\\plots\\case0\\isotopics\\flux50and500_absolute change.png')
        
        
    if 7 in subcase:
        # 10 outter fuel shells and mean
        a=np.sum(tnflx[0][9,20:30,0,24,:],axis=0)/10
        
        plt.figure()
        axis=plt.subplot(111)
        
        step(grouplimit,Stepper(a,1),'x-',ms=8)
        for i in range(20,30):
            c = cm.jet((i-20)/10,1)
            step(grouplimit,Stepper((tnflx[0][9,i,0,24,:]),1),color=c)
        
        axis.set_xscale('log')   
        axis.set_ylabel('Normalized Flux,' ,size=14)
        axis.set_xlabel('Neutron Energy, [eV]',size=14) 
        axis.set_title('Flux for Case 0. outter 10 shalls and avg \n at 1.8m, outer fuel region',size=18)     
        axis.xaxis.grid(True,'major',linewidth=1,alpha=0.3)
        axis.yaxis.grid(True,'major',linewidth=1,alpha=0.3)  
        legend(["avg","shell 20","21","22","23","24","25","26","27","28","29"],loc=2)
        #savefig('D:\\dropbox\\Dropbox\\plots\\case0\\isotopics\\Flux case 0 avg10region 500.png')
        show()
    

        plt.figure()
        axis=plt.subplot(111)
        
        step(grouplimit,Stepper(a,1))
        for i in [1,2,3]:
            step(grouplimit,Stepper((tnflx[i][9,2,0,24,:]),1))
        
        axis.set_xscale('log')   
        axis.set_ylabel('Normalized Flux,' ,size=14)
        axis.set_xlabel('Neutron Energy, [eV]',size=14) 
        axis.set_title('Flux for Case 0 and 1-3 at 500 EFPD \n at 1.8m, outer fuel region',size=18)     
        axis.xaxis.grid(True,'major',linewidth=1,alpha=0.3)
        axis.yaxis.grid(True,'major',linewidth=1,alpha=0.3)  
        legend(["case 0","case 1","case 2","case 3"],loc=2)
        #savefig('D:\\dropbox\\Dropbox\\plots\\case0\\isotopics\\Flux case 0-3 500.png')
        show()
        
        
        plt.figure()
        axis=plt.subplot(111)
        

        
        for i in [1,2,3]:
            step(grouplimit,Stepper((tnflx[i][9,2,0,24,:]-a)*100/a,1))
            
            
        axis.set_xscale('log')   
        axis.set_ylabel('relative differene [%]' ,size=14)
        axis.set_xlabel('Neutron Energy, [eV]',size=14) 
        axis.set_title('relative Flux difference to Case 0 at 500 EFPD \n at 1.8m, outer fuel region',size=18)     
        axis.xaxis.grid(True,'major',linewidth=1,alpha=0.3)
        axis.yaxis.grid(True,'major',linewidth=1,alpha=0.3)  
        legend(["case 1","case 2","case 3"],loc=2)
        #savefig('D:\\dropbox\\Dropbox\\plots\\case0\\isotopics\\Flux difference to case 0 500.png')
        show()

        plt.figure()
        axis=plt.subplot(111)
        
        for i in [2,3]:
           step(grouplimit,Stepper(((tnflx[i][9,2,0,24,:]-tnflx[1][9,2,0,24,:])*100/tnflx[1][9,2,0,24,:]),1))
            
        axis.set_xscale('log')   
        axis.set_ylabel('relative differene [%],' ,size=14)
        axis.set_xlabel('Neutron Energy, [eV]',size=14) 
        axis.set_title('realative Flux difference to case 1 at 500 EFPD \n at 1.8m, outer fuel region',size=18)     
        axis.xaxis.grid(True,'major',linewidth=1,alpha=0.3)
        axis.yaxis.grid(True,'major',linewidth=1,alpha=0.3)  
        legend(["case 2","case 3"],loc=2)
        #savefig('D:\\dropbox\\Dropbox\\plots\\case0\\isotopics\\Flux case 1 and 0 500.png')
        show()
     
    if 8 in subcase: #Tilt plot
        figure()
        axis1=subplot(2,1,1)
        step(z_mesh,Stepper(tnflx[0][0,29,0,:,17],1))
        axis2=subplot(2,1,2)
        step(z_mesh,Stepper(tnflx[0][0,29,0,:,37],1))   
    
    if 9 in subcase:        # more tilt plot
        figure('fluxdip')
        bu=6 #(60) epfd
        axis=subplot2grid((2, 4), (0, 0),colspan=3)
        fluxnorm=zeros(47)
        fluxnorm=sum(tnflx[0][bu,29,0,:,:],0) # normalisation
            
        ind=range(0,47,3)   
        lh=[0]*len(ind)    
        for i in reversed(range(len(ind))):
            c = cm.jet((ind[i])/47,1)
            lh[i],=plot(Btwn(z_mesh),tnflx[0][bu,29,0,:,ind[i]]/fluxnorm[ind[i]]/0.025,label='group '+ str(ind[i]+1),color=c)   
        handles, labels = axis.get_legend_handles_labels()
        #legend(handles[::-1],labels[::-1],loc=8, borderaxespad=0.,ncol=2)  
        rect=Rectangle((1,0.9), 0.4, 0.15,edgecolor='black',facecolor='None')
        gca().add_patch(rect)
        axis.set_ylabel('normalized Flux' ,size=14)
        #axis.set_xlabel('axial position, [m]',size=14) 
        axis.xaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.yaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])  
        axis.set_xlim([0,3.6576])
        axis.set_ylim([0,1.1])
        legend(handles[::-1],labels[::-1],bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        #axis.annotate('50 EFPD', xy=(2.5, 0.2),size=14,color=[0.5,0.5,0.5])
        
        
        
        axis=subplot2grid((2, 4), (1, 0),colspan=3)
        #fluxnorm=zeros(47)
        #fluxnorm=sum(tnflx[0][0,29,0,:,:],0) # normalisation
            
        ind=range(0,47,3)   
        lh=[0]*len(ind)    
        for i in reversed(range(len(ind))):
            c = cm.jet((ind[i])/47,1)
            lh[i],=plot(Btwn(z_mesh),tnflx[0][bu,29,0,:,ind[i]]/fluxnorm[ind[i]]/0.025,label='group '+ str(ind[i]+1),color=c)   
        handles, labels = axis.get_legend_handles_labels()
        #legend(handles[::-1],labels[::-1],loc=8, borderaxespad=0.,ncol=2)  
  
        axis.set_ylabel('normalized Flux' ,size=14)
        axis.set_xlabel('axial position, [m]',size=14) 
        axis.xaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.yaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])  
        axis.set_xlim([1,1.3])
        axis.set_ylim([0.9,1.05])   
        #axis.annotate('500 EFPD', xy=(2.5, 0.2),size=14,color=[0.5,0.5,0.5])
        #tight_layout()    
        plt.tight_layout()
        savefig('D:/dropbox/Dropbox/plots/spring2013/0/fluxtilt.pdf')
        #axis.set_title('The axial mean neuton flux  ')
        #set_fontsize([manager.canvas.figure for manager in matplotlib._pylab_helpers.Gcf.get_all_fig_managers()][0],beamerfontsize)
        show()  

    if 9.1 in subcase:        # more tilt plot
        fate=['']*49
        fate[0]=', fast'
        fate[11]=', thermal'
        fig=figure(figsize=[10,5])
        bu=0
        axis=subplot2grid((2, 4), (0, 0),colspan=3)
        fluxnorm=zeros(47)
        fluxnorm=sum(tnflx[0][bu,29,0,:,:],0) # normalisation
        #axis.set_title('The mean axial neutron flux  ')    
        ind=range(0,47,4)   
        lh=[0]*len(ind)    
        for i in reversed(range(len(ind))):
            c = cm.jet((ind[i])/47,1)
            lh[i],=plot(Btwn(z_mesh),tnflx[0][bu,29,0,:,ind[i]]/fluxnorm[ind[i]]/0.025,label='group '+ str(ind[i]+1) + str(fate[i]),color=c)   
        handles, labels = axis.get_legend_handles_labels()
        #legend(handles[::-1],labels[::-1],loc=8, borderaxespad=0.,ncol=2)  
        rect=Rectangle((1,0.9), 0.4, 0.15,edgecolor='black',facecolor='None')
        gca().add_patch(rect)
        #axis.set_ylabel('normalized Flux' ,size=14)
        #axis.set_xlabel('axial position, [m]',size=14) 
        axis.xaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.yaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])  
        axis.set_xlim([0,3.6576])
        axis.set_ylim([0,1.1])
        fig.subplots_adjust(right=0.8)
        legend(handles[::-1],labels[::-1],bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        #axis.annotate('50 EFPD', xy=(2.5, 0.2),size=14,color=[0.5,0.5,0.5])
        
        
        
        axis=subplot2grid((2, 4), (1, 0),colspan=3)
        #fluxnorm=zeros(47)
        #fluxnorm=sum(tnflx[0][0,29,0,:,:],0) # normalisation
   
        ind=range(0,47,3)   
        lh=[0]*len(ind)    
        for i in reversed(range(len(ind))):
            print i
            c = cm.jet((ind[i])/47,1)
            lh[i],=plot(Btwn(z_mesh),tnflx[0][bu,29,0,:,ind[i]]/fluxnorm[ind[i]]/0.025,label='group '+ str(ind[i]+1),color=c)   
        handles, labels = axis.get_legend_handles_labels()
        #legend(handles[::-1],labels[::-1],loc=8, borderaxespad=0.,ncol=2)  
        axis.set_yticks((0.9,0.94,0.98, 1.02))
        axis.set_xticks((1,1.1,1.2,1.3))
        #axis.set_ylabel('normalized Flux' ,size=14)
        axis.set_xlabel('axial position, [m]',size=14) 
        axis.xaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.yaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])  
        axis.set_xlim([1,1.3])
        axis.set_ylim([0.9,1.05])   
        #axis.annotate('500 EFPD', xy=(2.5, 0.2),size=14,color=[0.5,0.5,0.5])
        #tight_layout()    
        #plt.tight_layout()
        fig.subplots_adjust(bottom=0.14)
        figtext(0.012,0.8,'normalized neutron flux',size=14,rotation='vertical')
        set_fontsize([manager.canvas.figure for manager in matplotlib._pylab_helpers.Gcf.get_all_fig_managers()][0],beamerfontsize)
        show()  
        #savefig('V:\\master report\\figures\\Fluxtilt2beamer.pdf')

        
    if 10 in subcase:        # more tilt plot
        figure()
        axis=subplot(1,1,1)
        fluxnorm=zeros(47)
        fluxnorm=sum(tnflx[0][0,29,0,:,:],0) # normalisation
            
        ind=range(0,47,3)   
        lh=[0]*len(ind)    
        for i in reversed(range(len(ind))):
            c = cm.jet((ind[i])/47,1)
            lh[i],=plot(Btwn(z_mesh),tnflx[0][0,29,0,:,ind[i]]/fluxnorm[ind[i]]/0.025,label='group '+ str(ind[i]+1),color=c)   
        handles, labels = axis.get_legend_handles_labels()
        legend(handles[::-1],labels[::-1],loc=8, borderaxespad=0.,ncol=2)  
    
        axis.set_ylabel('normalized Flux' ,size=14)
        axis.set_xlabel('axial position, [m]',size=14) 
        axis.xaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.yaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])  
        axis.set_xlim([0,3.6576])
        #savefig('V:\\master report\\figures\\Fluxtilt.eps')
        axis.set_title('The Tilt of the neutron flux for different energies\n case0, 50 EFPD',size=18)
        tight_layout()
        #savefig('D:\dropbox\Dropbox\plots\case0\Fluxstilt.png')
        show()        
###### arbitrary therm plot,
if 5 in plotcase:
    gd=0
    if gd==1:
        f=open('G:\\powertables\\singlepin\\tt5','rb')
        tt5=pickle.load(f)
        f.close()
        lh=[0]*10
    
    for i in [0]:
        plt.figure()
        axis=plt.subplot(111)
        for j in range(10):
            for k in range(5):
                c = cm.jet((j)/10,1)
                lh[j],=plt.plot(z_mesh[1:],tt5[1,i,j,k,0,:],color=c)
    
        axis.xaxis.grid(True,'major',linewidth=2)
        axis.yaxis.grid(True,'major',linewidth=2)
        
        axis.set_ylabel('Temperature, [K]' ,size=14)
        axis.set_xlabel('axial position, [m]',size=14) 
        axis.set_title('Case1: Temperature profile development with burnup,\n for all 5 radial sections',size=18)    
        l=legend([lh[0],lh[-1]],["50 EFPD","500 EFPD"],loc=2)
        axis.set_xlim([0,3.7])
        axis.annotate('I.', xy=(3.2, 1030),size=14)
        axis.annotate('II.', xy=(3.2, 900),size=14)
        axis.annotate('III.', xy=(3.2, 760),size=14)
        axis.annotate('clad', xy=(3.1, 660),size=14)
        axis.annotate('coolant', xy=(3, 570),size=14)
    show()
  

########### cladtempplot  
if 6 in plotcase:
    if 1 in subcase:
        figure()
        axis=plt.subplot(111)
        ph=[0]*9
        bu=[0]
        for i in range(len(bu)):
            c = cm.jet((i)/9,1)
            ph[i],=plot(z_mesh3,ttc[1,bu[i],0,1,:])
            ph[i],=plot(z_mesh3,ttc[2,bu[i],0,1,:])
            #ph[i],=plot(z_mesh3,ttc[3,bu[i],0,1,:],ls='--')
        axis.yaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.xaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.set_ylabel('cladding temperature, [K]' ,size=14)
        axis.set_xlabel('axial position, [m]',size=14) 
          
        l=legend(["case 1","case 2"],loc=2)
        axis.set_xlim([0,3.6576])
        tight_layout()
        #savefig('V:\\master report\\figures\\cladtemp2.pdf')
        #axis.set_title('Cladding temperature at 50 EFPD ',size=18) 
        set_fontsize([manager.canvas.figure for manager in matplotlib._pylab_helpers.Gcf.get_all_fig_managers()][0],beamerfontsize)        
        tight_layout()
        #savefig('V:\\master report\\figures\\cladtemp2beamer.pdf')
        #axis.set_ylim([500,1200])    
        show()  
        
        
    if 1.1 in subcase:
        figure()
        axis=plt.subplot(111)
        ph=[0]*9
        bu=[0]
        for i in range(len(bu)):
            c = cm.jet((i)/9,1)
            ph[i],=plot(z_mesh3,ttc[1,bu[i],0,1,:],'b')
            ph[i],=plot(z_mesh3,ttc[2,bu[i],0,1,:],'g')
            ph[i],=plot(z_mesh3,ttc[3,bu[i],0,1,:],'r',ls='--')
            #ph[i],=plot(z_mesh3,ttc[0,bu[i],0,1,:],ls='--')
        axis.yaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.xaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.set_ylabel('cladding temperature, [K]' ,size=14)
        axis.set_xlabel('axial position, [m]',size=14) 
          
        l=legend(["case A1","case A2","case A3"],loc=2)
        axis.set_xlim([0,3.6576])
        tight_layout()
        axis.set_title('Cladding temperature at 50 EFPD ',size=18) 
        set_fontsize([manager.canvas.figure for manager in matplotlib._pylab_helpers.Gcf.get_all_fig_managers()][0],beamerfontsize)        
        tight_layout()
        #savefig('V:\\master report\\figures\\cladtemp2beamer.pdf')
        #axis.set_ylim([500,1200])    
        show()          
        
    # comparison plot between original and averaged tables. here: heat flux & clad temp    
    if 2 in subcase: 
        if 0: # reading data from table
            path ='D:/powertables/new/5/'
            files=['flux_5_0500.cpl','flux_5_0500.cpl.bak']
            # 1) check if the coordinates are same
            
            Tlist=[[],[]]    
            Flist=[[],[]] 
            Zlist=[[],[]] 
            Alist=[[],[]] 
            rowind=[[0   ,1,   2,   3,4],[0   ,1,      3,4,5]]
            
            for enum,i in enumerate(files):
                f_in = open(path+i)
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
            print 'one file read complete'        
            #2) check if the coordinates match
            
            if not np.all(np.equal(Zlist[0],Zlist[1])):
                print "Zlist not equal"
                raise
            else:
                print 'Zlist fine'
            if not np.all(np.equal(Alist[0],Alist[1])):
                print "Alist not equal"
                raise
            else:
                print 'Alist fine'
            #for i in xrange(len(Tlist[0])):
            #
            #    if Zlist[0]!=Zlist[1]:
            #        print 'Zlist difference at line {:>6.0f}: {:>1.15f}, \
            #        {:>1.15f}'.format(i,Zlist[0][i],Zlist[1][i]) 
            #    if Alist[0]!=Alist[1]:
            #        print 'Alist difference at line {:>6.0f}: {:>1.15f}, \
            #        {:>1.15f}'.format(i,Alist[0][i],Alist[1][i])             
            #print 'one set checked'

        # plotting        
        grid_x,grid_y=np.mgrid[-pi:pi:100j,0:3.6576:400j]
        
        ex=(-pi,pi,0,3.6576)
        fig=plt.figure('cladtemp')
        clf()
        ti=['averaged\n as sent to MAMBA & DeCART','original \n as written by StarCCM+']
        if 1:
            for i in range(2):
                grid_z=griddata((Alist[i],Zlist[i]),Tlist[i],(grid_x,grid_y),method='linear')
                axis=plt.subplot(1,2,i)
                im=imshow(grid_z.T, interpolation='none',extent=ex, origin='lower', \
                clim=([580,640]),aspect=2)
                xticks([-np.pi,  0,  np.pi],
                [r'$-\pi$', r'$0$',  r'$+\pi$'])
                axis.set_xlabel('azimuthal position, [rad]')
                axis.set_title(ti[i])
                if i==1:
                    axis.set_ylabel('axial position, [m]')
                    axis.annotate('Tw_HFlux_XYZ_clad.csv.bak', xy=(-3, 1),size=14,color=[0.5,0.5,0.5])
                else:
                    axis.annotate('Tw_HFlux_XYZ_clad.csv', xy=(-3, 1),size=14,color=[0.5,0.5,0.5])
            cax = fig.add_axes([0.87, 0.1, 0.03, 0.8])
            cb=fig.colorbar(im, cax=cax,ticks=[580,600,620,640])  
            cb.set_label('cladding Temperature [deg C]')
            fig.subplots_adjust(top=0.90)
            fig.subplots_adjust(bottom=0.05)
            fig.subplots_adjust(left=0.1)
            fig.subplots_adjust(right=0.85)   
            fig.text(0.5,0.975,'Original and averaged cladding temperature \n\
            case 5, 500 EFPD',horizontalalignment='center',verticalalignment='top',size=14)
              
           # fig.text(0.5,0.03,'azimuthal position, [rad]',horizontalalignment='center',verticalalignment='bottom')        
            show()  
            savefig('D:/dropbox/Dropbox/plots/spring2013/compare_orig_avg_TClad.pdf')
        if 1:
            fig=plt.figure('heatflux')
            clf()
            for i in range(2):
                grid_z=griddata((Alist[i],Zlist[i]),Flist[i],(grid_x,grid_y),method='linear')
                axis=plt.subplot(1,2,i)
                corr=1000000
                im=imshow(grid_z.T/corr, interpolation='none',extent=ex, origin='lower', \
                clim=([0.8,1.2]),aspect=2)
                xticks([-np.pi,  0,  np.pi],
                [r'$-\pi$', r'$0$',  r'$+\pi$'])

                axis.set_title(ti[i])
                axis.set_xlabel('azimuthal position, [rad]')
                if i==1:
                    axis.set_ylabel('axial position, [m]')
                    axis.annotate('Tw_HFlux_XYZ_clad.csv.bak', xy=(-3, 1),size=14,color=[0.5,0.5,0.5])
                else:
                    axis.annotate('Tw_HFlux_XYZ_clad.csv', xy=(-3, 1),size=14,color=[0.5,0.5,0.5])
            cax = fig.add_axes([0.87, 0.1, 0.03, 0.8])
            cl=im.get_clim()
            cb=fig.colorbar(im, cax=cax,ticks=np.linspace(cl[0],cl[1],5))  
            cb.set_label('cladding heat flux [MW/m2]')
            fig.subplots_adjust(top=0.90)
            fig.subplots_adjust(bottom=0.05)
            fig.subplots_adjust(left=0.1)
            fig.subplots_adjust(right=0.85)   
            fig.text(0.5,0.975,'Original and averaged heat flux \n\
            case 5, 500 EFPD',horizontalalignment='center',verticalalignment='top',size=14)
            show() 
            savefig('D:/dropbox/Dropbox/plots/spring2013/compare_orig_avg_Hflux.pdf')
            #fig.text(0.5,0.03,'azimuthal position, [rad]',horizontalalignment='center',verticalalignment='bottom')        
                      
########### real data temp plot
# needs plottemperature.py before, which needs inputdeck.py

##### maybe outdated ######
if 7 in plotcase:
    gd=0
    if gd==1:
        
        picklefileT=['tt1','tt1.5','tt1.6','tt1.3']
        path='G:\\powertables\\singlepin\\1\\'
        pickhand=[0]*len(picklefileT)
        for i in range(len(pickhand)):       
            pickhand[i]=open(path+picklefileT[i],'rb')
        p_t=pickle.load(pickhand[0])
        p_t5=pickle.load(pickhand[1])
        p_t6=pickle.load(pickhand[2])
        p_t3=pickle.load(pickhand[3])
        for i in range(len(pickhand)):
            pickhand[i].close()
    
    ##### radial profiles
    #plt.figure()
    axis=plt.subplot(111)
    for i in range(5):
        plt.plot(np.sqrt(p_t[0][0][0][0][i][0][20][2]),p_t[0][0][0][0][i][0][20][0],'x')

    plt.show()   

############# radial averaginf plot
# for this plot, run plotsingletemp.py in advance with
#
#file=['G:\\powertables\\singlepin\\1\\thdata_50.cpl',
#        'G:\\powertables\\singlepin\\2\\thdata_50_avg6.cpl',
#        'G:\\powertables\\singlepin\\3\\thdata_50_avg3.cpl']
#ridx_s=[0,1,1]        
#
if 8 in plotcase:
    print '8'
    if 1 in subcase:
        plt.figure()
        axis=plt.subplot(111)
        ph=[0,0,0]
        for i in range(5):
            ph[0],=plot(p_t5[0][0][0][i][0][24][2],p_t5[0][0][0][i][0][24][0],'.',mew=0,mfc='r',)
            ph[1],=plot(p_t3[2][0][0][i][0][24][2],p_t3[2][0][0][i][0][24][0],'.',mew=0,mfc='g',)
        for i in range(6):                                                         
            ph[2],=plot(p_t6[1][0][0][i][0][24][2],p_t6[1][0][0][i][0][24][0],'.',mew=0,mfc='b',)
            
        for ii in radii[0]:
            plt.axvline(x=ii,color='black',alpha=0.5)
            
        #axis.xaxis.grid(True,'major',linewidth=2)
        axis.yaxis.grid(True,'major',linewidth=1,alpha=0.2)
        
        axis.set_ylabel('Temperature, [K]' ,size=14)
        axis.set_xlabel('radial position, [m]',size=14) 
        axis.set_title('Radial effect of both averaging routines',size=18)    
        l=legend([ph[0],ph[2],ph[1]],["original data","FD integration","flat fuel average"],loc=1,numpoints=3)
        axis.set_xlim([0,0.00624])
        axis.annotate('I.', xy=(0.0012, 530),size=14)
        axis.annotate('II.', xy=(0.0027, 530),size=14)
        axis.annotate('III.', xy=(0.0036, 530),size=14)
        axis.annotate('clad', xy=(0.0042, 530),size=14)
        axis.annotate('coolant', xy=(0.0051, 530),size=14)
    
        show()   
    if 2 in subcase:    
        plt.figure()
        axis=plt.subplot(111)   
        ph=[0,0,0,0,0]
        for k in [0,1,2]:
            c=[1,(k+1)/5,(k+1)/5]
            for i in range(49):
                ph[k],=plot(p_t5[0][0][0][k][0][i][1],p_t5[0][0][0][k][0][i][0],'.',mew=0,mfc=c,)
                ph[3],=plot(p_t3[2][0][0][k][0][i][1],p_t3[2][0][0][k][0][i][0],'.',mew=0,mfc='g',)
        
        for k in [0,1,2,3]:        
            for i in range(49):                                                     
                ph[4],=plot(p_t6[1][0][0][k][0][i][1],p_t6[1][0][0][k][0][i][0],'.',mew=0,mfc='b',)
        axis.xaxis.grid(True,'major',linewidth=2)
        axis.yaxis.grid(True,'major',linewidth=2)    
        axis.set_ylabel('Temperature, [K]' ,size=14)
        axis.set_xlabel('axial position, [m]',size=14)   
        axis.set_title('Axial effect of both averaging routines \n for the 3 fuel regions',size=18)     
        axis.set_xlim([0,3.7])    
        #axis.set_ylim([0,3.7])
        l=legend([ph[1],ph[3],ph[4]],["original data","FD integration","flat fuel average"],loc=2,numpoints=3)
        show()
        
        
    if 3 in subcase:
        plt.figure()
        axis=plt.subplot(111)
        ph=[0,0,0]
        for i in range(5):
            a,=plot(p_t5[0][0][0][i][0][24][2],p_t5[0][0][0][i][0][24][0],'.',mew=0,mfc='r',)
        
        for ii in radii[0]:
            plt.axvline(x=ii,color='black',alpha=0.5,ls='--')
        
        for i in range(len(radii2[0])-1):
            b,=plt.bar(radii2[0][i],tt6[1,0,i,0,24],radii2[0][i+1]-radii2[0][i],0,color='yellow',edgecolor='black',alpha=0.3)
        
        c,=plt.bar(0,tt3[1,0,0,0,24],radii[0][3],0,color='green',edgecolor='black',alpha=0.3)
        plt.bar(radii[0][3],tt3[1,0,3,0,24],radii[0][4]-radii[0][3],0,color='green',edgecolor='black',alpha=0.3)        
        plt.bar(radii[0][4],tt3[1,0,4,0,24],0.00624-radii[0][4],0,color='green',edgecolor='black',alpha=0.3)        
        
        #axis.xaxis.grid(True,'major',linewidth=2)
        axis.yaxis.grid(True,'major',linewidth=1,alpha=0.2)
        
        axis.set_ylabel('Temperature, [K]' ,size=14)
        axis.set_xlabel('radial position, [m]',size=14) 
        axis.set_title('Radial temperature profiles  \n passed to decart ',size=18)    
        l=legend([a,b,c],["original data","FD integration","flat fuel average"],loc=1,numpoints=3)
        axis.set_xlim([0,0.00624])
        axis.set_ylim([500,1200])
        #axis.annotate('I.', xy=(0.0013, 530),size=14)
        #axis.annotate('II.', xy=(0.0026, 530),size=14)
        #axis.annotate('III.', xy=(0.0036, 530),size=14)
        #axis.annotate('clad', xy=(0.0042, 530),size=14)
        #axis.annotate('coolant', xy=(0.0051, 530),size=14)
        
    show()
    
    if 4 in subcase:
        print radii2
        radii2=[[0.0]*(len(radii[0])-1)]
        for i in range(len(radii[0])-1):
            radii2[0][i]=np.sqrt((radii[0][i]**2+radii[0][i+1]**2)/2)  
        radii2[0].insert(0,0)
        radii2[0].append(0.00476) 
        print radii2
        plt.figure()
        axis=plt.subplot(111)
        ph=[0,0,0]
        
        for i in range(5):
            a,=plot(p_t5[0][0][0][i][0][24][2],p_t5[0][0][0][i][0][24][0],'.',mew=0,mfc='r',)
        
        for ii in radii[0]:
            plt.axvline(x=ii,color='black',alpha=0.5,ls='--')
        
        for i in range(len(radii2[0])-1):
            b,=plt.bar(radii2[0][i],tt6[1,0,i,0,24],radii2[0][i+1]-radii2[0][i],0,color='yellow',edgecolor='black',alpha=0.3)
        plt.bar(radii2[0][-1],tt6[1,0,-1,0,24],0.00624-radii2[0][-1],0,color='yellow',edgecolor='black',alpha=0.3)
        
        
        c,=plt.bar(0,tt3[1,0,0,0,24],radii[0][3],0,color='green',edgecolor='black',alpha=0.3)
        plt.bar(radii[0][3],tt3[1,0,3,0,24],radii[0][4]-radii[0][3],0,color='green',edgecolor='black',alpha=0.3)        
        plt.bar(radii[0][4],tt3[1,0,4,0,24],0.00624-radii[0][4],0,color='green',edgecolor='black',alpha=0.3)        
        
        #axis.xaxis.grid(True,'major',linewidth=2)
        axis.yaxis.grid(True,'major',linewidth=1,alpha=0.2)
        
        axis.set_ylabel('Temperature, [K]' ,size=14)
        axis.set_xlabel('radial position, [m]',size=14) 
        axis.set_title('Radial temperature profiles  \n with correct radial FD mesh ',size=18)    
        l=legend([a,b,c],["original data","FD integration","flat fuel average"],loc=1,numpoints=3)
        axis.set_xlim([0,0.00624])
        axis.set_ylim([500,1200])
        #axis.annotate('I.', xy=(0.0013, 530),size=14)
        #axis.annotate('II.', xy=(0.0026, 530),size=14)
        #axis.annotate('III.', xy=(0.0036, 530),size=14)
        #axis.annotate('clad', xy=(0.0042, 530),size=14)
        #axis.annotate('coolant', xy=(0.0051, 530),size=14)    
        show()
        
    if 5 in subcase:
        # for this plot, run plotsingletemp.py in advance with
        radii3=copy.deepcopy(radii[0])
        
        radii3.append(0.00642)
        plt.figure()
        axis=plt.subplot(111)
        ph=[0,0,0,0,0]
        for ii in radii[0]:
            plt.axvline(x=ii,color='black',alpha=0.5) 
        ph[4],=step(array(radii3)[[0,3,4,5]],Stepper(tt3[1,0,(0,3,4),0,24],0),'c',where='post',linewidth=2)  # sep function              
        
        for i in range(5): # data
            ph[0],=plot(p_t5[0][0][0][i][0][24][2],p_t5[0][0][0][i][0][24][0],'.',mew=0,mfc='b',)
            
        ph[1],=plot(radii[0],t[0,0,:-1,0,24],'rx',ms=10,mew=2)    # points #hardcode wardnig: t is stupid
        

        ph[3],=step(radii3,Stepper(tt5[1,0,:,0,24],0),'g',where='post',linewidth=2) # mean

        #t=copy.deepcopy(tt5[1,0,:,0,24])
        
        #for i in range(4):
        #    t[i]=0.5*(tt6[1,0,i,0,24]+tt6[1,0,i+1,0,24]) 
        ph[2],=step(radii3,Stepper(tt6[1,0,:-1,0,24],0),'r',ls='--',where='post',linewidth=2)  # sep function
        
        #axis.xaxis.grid(True,'major',linewidth=2)
        axis.yaxis.grid(True,'major',linewidth=1,c=[0.7,0.7,0.7])
        axis.set_ylim([500,1200])
        axis.set_ylabel('Temperature, [K]' ,size=14)
        axis.set_xlabel('radial position, [m]',size=14) 
           
        l=legend([ph[0],ph[1],ph[2],ph[3],ph[4]],["original CFD data","FD integration points","FD derived profile","5-volumetric mean","3-volumetric mean"],loc=1,numpoints=3)
        axis.set_xlim([0,0.00624])
        axis.annotate('I.', xy=(0.0012, 530),size=14)
        axis.annotate('II.', xy=(0.0027, 530),size=14)
        axis.annotate('III.', xy=(0.0036, 530),size=14)
        axis.annotate('clad', xy=(0.0042, 530),size=14)
        axis.annotate('coolant', xy=(0.0051, 530),size=14)
        
        #savefig('V:\\master report\\figures\\FDprofile.eps')
        axis.set_title('FD radial temperature profile',size=18) 
        #savefig('D:\\dropbox\\Dropbox\\plots\\averaging\\FDprofile.png')
        show()
    

        
if 9 in plotcase: #case 0 stuff
    #needs inputdeck and loading and isotopics
    if 1 in subcase:
        ph=[0]*10
        close(91)
        figure(91)
        axis=plt.subplot(111)
        for i in range(10):
            c = cm.jet((i)/10,1)
            for j in range(5):
                ph[i],=plot(z_mesh3,tt5[0,i,j,0,:],color=c)
    
        axis.yaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.xaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
        axis.set_ylabel('Temperature, [K]' ,size=14)
        axis.set_xlabel('axial position, [m]',size=14) 
        axis.set_title('Temperature distribution change with burnup \n case 0',size=18)    
        l=legend([ph[0],ph[-1]],["50 EFPD","500 EFPD"],loc=2)
        axis.set_xlim([0,3.7])
        #axis.set_ylim([500,1200])
        
        show()
        #savefig('D:\\dropbox\\Dropbox\\plots\\case0\\overview_burnup.png')
        
    if 2 in subcase: #radial tmperature step functions
        for h in [0]:#range(10): #bu
        #close(92)
        #figure(92)
            figure()
            axis=plt.subplot(111)
            for i in [0,10,20,30,40]: #z
                c = cm.jet((i)/49,1)
                for j in range(4): # angle
                    step(radii2[0],Stepper(tt5[0,0,:,j,i]),color=c,where='post')
                
            axis.yaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
            axis.xaxis.grid(True,'major',linewidth=1,color=[0.7,0.7,0.7])
            axis.set_ylabel('Temperature, [K]' ,size=14)
            axis.set_xlabel('axial position, [m]',size=14) 
            axis.set_title('Temperature distribution change with burnup \n case 0',size=18)    
            #l=legend([a,b,c],["original data","FD integration","flat fuel average"],loc=1,numpoints=3)
            #axis.set_xlim([0,3.7])
            #axis.set_ylim([500,1200])
            
            show()
            ###savefig('D:\\dropbox\\Dropbox\\plots\\case0\\Temp_azi_.png')




      