# this script finally handles the whole post processing of the 
# star-decart-mamba coulped multiphysics simulations done by D J Walter
# in spring 2013. 
from __future__ import division
import sys
import os
import pickle
import numpy as np

dir=os.getcwd()
sys.path.append(dir)

print ' totalprocessing. cwd is '+dir

#ind_case=sys.argv[1]
    
        
path=os.getcwd()+'/'
casefolder =['0/','1/','2/','3/','4/','5/','6/','7/','8/']
              
              
timesteps =['0','4','8','12','16','20','40','60','80','100','120','140','160',
'180','200','220','240','260','280','300','320','340','360','380','400','420',
'440','460','480','500']

ind_cases = [4] # [0,1,2,3,4,5,6,8]
ind_time = [1] #range(len(timesteps))
indfile='indfile.pickle'
f=open(path+indfile,'wb')
pickle.dump([ind_cases,ind_time],f)
f.close()

    

#path='D:\\powertables\\new\\'
#casefolder =['0\\','1\\','2\\','3\\','4\\','5\\','6\\','7\\','8\\']
#timesteps =['0','4','8','12','16','20','40','60','80','100','120','140','160',
#'180','200','220','240','260','280','300','320','340','360','380','400','420',
#'440','460','480','500']
#bu=['00000','00250','00501','00752','01003','01254','02509','03763','05018','06272',
#'07527','08781','10036','11290','12545','13799','15054','16308','17563',
#'18818','20072','21327','22581','23836','25090','26345','27599','28854',
#'30108','31363']


# isotopics & flux
import isotopics
isotopics.Plut('not ini')
isotopics.Flux('not ini')

import inputdeck
import crud