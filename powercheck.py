from __future__ import division
import sys
#sys.path.append('/home/cbolesch/simulations/sinclepin/scripttest')

import averaging as av
import numpy as np
import time
import copy
import pickle
import os
import csv

path= 'D:/powertables/new/5flux/'

files=[['MAM_Hflux_5_0000.csv'],['MAM_Hflux_5_0000.csv.bak']]
F=[[],[]]
A=[]
path ='D:/powertables/new/5flux/'


for en,i in enumerate(ts2): 
    files=['MAM_Hflux_5_0'+i+'.csv','MAM_Hflux_5_0'+i+'.csv.bak']
    F=[[],[]]
    A=[]
    
    f0= open(path+files[0], 'rb')
    f0.next()           # skip header
    reader0 = csv.reader(f0,delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
    f1= open(path+files[1], 'rb')
    f1.next()           # skip header
    reader1 = csv.reader(f1,delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
    for row0 in reader0:
        
        row1=reader1.next()
        F[0].append(row0[1])
        F[1].append(row1[1])
        A.append(row1[2])
    
    print '{:> 6.20f}'.format((np.dot(A,F[0])-np.dot(A,F[1]))/np.dot(A,F[1]))    
    #print '{:>6.20f}'.format(np.dot(A,F[1]))
    #print ""
    f0.close()
    f1.close()