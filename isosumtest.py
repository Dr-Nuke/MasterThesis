# isotopics
from __future__ import division
import matplotlib.cm as cm
import csv
import matplotlib.pyplot as plt
import numpy as np
import copy
import time
import pickle
    
# new mod for simulations of spring 2013    
    
def TestMapper(n,p,case):
    """
    converts the XSsection number into a radial and azimuthal coordinate.
    r=0 means inner part, r=2 ouurt and r=1 middle
    a followes the logic pointed out at programmers guide p 25
    for the decart high fidelity cases r gors down from 29 to 0
    """
    if case==3:
        r= -((n-1)//16-5)
        a=[(n-1)%16]  

    if case==30:

        r=-((n-1)//16-32)
        a=[(n-1)%16]            

    
    return r,a    
    
    
file1=['D:\\powertables\\new\\0\\iso_0_0500.isosum']

for i in range(len(file1)):
    f=open(file1[i], 'rb')
    f.next()
    reader = csv.reader(f,delimiter=' ', quotechar='"',quoting=csv.QUOTE_NONE, skipinitialspace=True)
    for row in reader:
        if reader.line_num%3000==0:
            print 'PLN, XSR, r,        a,   Line, IsoID,concentration, IsoID,concentration'

        if len(row)==7:
            p=int(row[1])-2 #plane. first value in the isosum file is 2, so i gauge to 0
            r,a=TestMapper(int(row[3][:-1]),p,30)   
            print '{0:3},{1:4},{2:2},{3:9},{4:7},'.format(p,int(row[3][:-1]),r,a, reader.line_num)
                   
                
    print '\n\n\n\n'            
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                