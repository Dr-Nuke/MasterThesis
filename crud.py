from __future__ import division
import sys
import numpy as np
import time
import copy
import pickle
import csv
import math as m
import os 


def CrudBinFinder(x,y,z):
    """
    returns the bin indicators for the crud deposition.
    """
    A=18
    ind_a=-1
    ind_z=-1
    temp= m.atan2(y,x) % (2*m.pi)
    angle=np.linspace(0,(2*m.pi)*17/18,18)
    
    for i in range(len(angle)):
        if temp>((2*m.pi)*35/36):
            ind_a=0
            break
        if abs(temp-angle[i])<=(2*m.pi)/36: #within 10 degrees
            
            ind_a=i
            break 
                 
    for i in range(75):
        if z/5<i+1:
            ind_z=i
            break
    if z==368.75:
        ind_z=74
    return ind_a,ind_z

    
path=os.getcwd()+'/'
casefolder =['4/','5/','6/']

timesteps= ['0000','0002','0004','0006','0008','0010','0012','0014','0016',
'0018','0020','0030','0040','0050','0060','0070','0080','0090','0100','0110',
'0120','0130','0140','0150','0160','0170','0180','0190','0200','0210','0220',
'0230','0240','0250','0260','0270','0280','0290','0300','0310','0320','0330',
'0340','0350','0360','0370','0380','0390','0400','0410','0420','0430','0440',
'0450','0460','0470','0480','0490','0500']

picklefile=path+'tcrd'
pickhand=[0]*len(casefolder)
x=[]
y=[]
z=[]
z_crud=np.arange(0,3.66,0.05)

R=20

if 1: #DONT!!! resets the database
    print 'initializing & dumping  crud datafile...',
    crud=[[[[[[0.0 for h in range(3)] for i in range(73)] for j in range(18)] for jj in range(R)] for k in range(len(timesteps))] for l in range(len(casefolder))]
    crud=np.array(crud)
    f=open(picklefile,'wb')
    pickle.dump(crud,f)
    f.close()    
    print ' done.'
    print np.shape(crud)
    
else: 
    print 'loading crud datafile...',
    f=open(picklefile,'rb')
    crud=pickle.load(f)
    f.close()
    print ' done.'
    
indfile='indfile_crud.pickle'
f=open(path+indfile,'rb')
[ind_cases,ind_time]=pickle.load(f)
f.close()
ind_cases2=np.array(ind_cases)-4

    
    
for i in ind_cases2:
    if i in ind_time:
        print 'processing crud case {}... burnup'.format(i+4)
        for j in range(len(timesteps)):#range(len(timesteps)):
            
            file=path+casefolder[i]+'crud_'+str(i+4)+'_'+timesteps[j]
        # try:    #         3 substances                   73 z- layers      18 angular section   19 radial layers                  
            tempcrud=[[[[0.0 for ii in range(3)] for kk in range(73)] for ll in range(18)] for jj in range(R)]   
            print np.shape(tempcrud)
            tempcrud=np.array(tempcrud)
            print file
            f=open(file, 'rb')
            for ii in range(9):
                f.next()
            reader = csv.reader(f,delimiter=' ', quotechar='"',quoting=csv.QUOTE_NONNUMERIC, skipinitialspace=True)
            for row in reader:
                
                r=int(row[1]/5-1)
                
                a=int(row[2]/20)
                z=int(row[3]/5-1)
                #print '{:>6f}, {:>6d}, {:>6d}, {:>6d}'.format(row[0],r,a,z)
                bor10=row[4]
                bor11=row[5]
                NiF=row[6]
                
                tempcrud[r,a,z,0]=bor10
                tempcrud[r,a,z,1]=bor11            
                tempcrud[r,a,z,2]=NiF
            
                #if [ind_a,ind_z]==[0,0]:
                #    print row
            #tempcrud[:,:,0]=tempcrud[:,:,0]/tempcrud[:,:,2]
            #tempcrud[:,:,1]=tempcrud[:,:,1]/tempcrud[:,:,2]
            crud[i,j,:,:,:,:]=tempcrud[:,:,:,:]
            
            f=open(picklefile,'wb')
            pickle.dump(crud,f)
            f.close()
    else:
        print 'no crud data for case {}'.format(i+4)
print ' done.'            
        #except:
        #    
        #    print file+' has not been read'
        #    f.close()
        #    raise

    
#for i in [4,5]:
#    for j in range(len(timesteps)):
#        file=path+casefolder[i]+'crud_'+str(i)+'_'+timesteps[j]+'.cpl'
#        try:
#            tempcrud=[[[[0.0 for ii in range(3)] for kk in range(73)] for ll in range(18)] for jj in range(18)]   
#            tempcrud=np.array(tempcrud)
#            print file
#            f=open(file, 'rb')
#            for ii in range(9):
#                f.next()
#            reader = csv.reader(f,delimiter=' ', quotechar='"',quoting=csv.QUOTE_NONNUMERIC, skipinitialspace=True)
#            for row in reader:
#                
#                r=int(row[1]/5-1)
#                
#                a=int(row[2]/20)
#                z=int(row[3]/5-1)
#                #print '{:>6f}, {:>6d}, {:>6d}, {:>6d}'.format(row[0],r,a,z)
#                bor10=row[4]
#                bor11=row[5]
#                NiF=row[6]
#                
#                tempcrud[r,a,z,0]=tempcrud[r,a,z,0]+bor10
#                tempcrud[r,a,z,1]=tempcrud[r,a,z,1]+bor11            
#                tempcrud[r,a,z,2]=tempcrud[r,a,z,2]+NiF
#             
#                #if [ind_a,ind_z]==[0,0]:
#                #    print row
#            #tempcrud[:,:,0]=tempcrud[:,:,0]/tempcrud[:,:,2]
#            #tempcrud[:,:,1]=tempcrud[:,:,1]/tempcrud[:,:,2]
#            crud[i,j,:,:,:,0:2]=tempcrud[:,:,:,0:2]
#            
#            f=open(picklefile,'wb')
#            pickle.dump(crud,f)
#            f.close()
#            
#        except:
#            
#            print file+' has not been read'
#            f.close()
#            raise
#