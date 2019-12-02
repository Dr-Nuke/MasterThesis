# isotopics
from __future__ import division
import csv
import numpy as np
import copy
import time
import pickle
import os    
# new mod for simulations of spring 2013    
    
def RegioMapper(n,p,case):
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
    
    
def Plut(ini):
    """
    creates an array that contains the plutonium data
    """

    
            
    
    path=os.getcwd()+'/'
    plutfolder=['0/','1/','2/','3/','4/','5/','6/','7/','8/']   
    timesteps =['0','4','8','12','16','20','40','60','80','100','120','140','160',
    '180','200','220','240','260','280','300','320','340','360','380','400','420',
    '440','460','480','500']    
    picklefn='tpu'
    
    len_z=49
    A=16
    R=[30,3,3,3,3,3,3,3,30]

    picklefile=path+picklefn
    if ini=='ini': # WARNIGN! resets database!!!
        print '   creating & dumping  fresh tpu array...',
        #totalpu=[[[[[[0.0,0.0,0.0,0.0] for m in range(49)] for l in range(A)] for k in range(max(R))] for j in range(len(timesteps))] for i in range(len(plutfolder))]
        totalpu=[0]*len(plutfolder)
        #             p39,p41,u35,u38
        f2=open(picklefile,'wb')
        pickle.dump(totalpu,f2)
        f2.close()
        print ' done.'
    else:
        print '   loading the pickle plut file...',
        f2=open(picklefile,'rb')
        totalpu=pickle.load(f2)
        f2.close()
        print ' done.'
    
    indfile='indfile.pickle'
    f=open(path+indfile,'rb')
    [ind_cases,ind_time]=pickle.load(f)
    f.close()
        
    for i in ind_cases:#range(len(plutfolder)):
        print '   processing isotopics case {}'.format(i)
        temppu=np.array([[[[[0.0,0.0,0.0,0.0] for mm in range(49)] for ll in range(A)] for kk in range(R[i])] for jj in range(len(timesteps))])
                
        for j in ind_time:#range(len(timesteps)):
            
            try:    
                cntr=1
                p_old=-1
                a=path+plutfolder[i]+'iso_'+str(i)+'_'+'{:04d}'.format(int(timesteps[j]))+'.isosum'
                print a
                f=open(a, 'rb')
                
                f.next()
                reader = csv.reader(f,delimiter=' ', quotechar='"',quoting=csv.QUOTE_NONE, skipinitialspace=True)
                for row in reader:
                    #if reader.line_num%3000==0:
                    #    print 'PLN, XSR, r,        a,   Line, IsoID,concentration, IsoID,concentration'
                    if len(row)==7:
                        p=int(row[1])-2   #plane. first value in the isosum file is 2, so i gauge to 0
                        r,a=RegioMapper(int(row[3][:-1]),p,R[i])
                        #print '{0:3},{1:4},{2:2},{3:9},{4:7},'.format(p,int(row[3][:-1]),r,a, reader.line_num)
                    elif row[0]=='94239':
                        for ii in a:
                            temppu[j,r,a,p,0]=float(row[1])
                            #print '{0:5},{1:13},'.format(int(row[0]),float(row[1])),    
                    elif row[0]=='94241':
                        for ii in a:
                            temppu[j,r,a,p,1]=float(row[1])
                            #print '{0:5},{1:13}'.format(int(row[0]),float(row[1]))
                    elif row[0]=='92235':
                        for ii in a:
                            temppu[j,r,a,p,2]=float(row[1])
                            #print '{0:5},{1:13}'.format(int(row[0]),float(row[1]))
                    elif row[0]=='92238':
                        for ii in a:
                            temppu[j,r,a,p,3]=float(row[1])
                            #print '{0:5},{1:13}'.format(int(row[0]),float(row[1]))                            
                f.close
                
            except IOError:
                print 'file ' + path+plutfolder[i]+'iso_'+timesteps[j]+'.isosum not read'
                
                # i dont have all files of the 5 cases, so....
        totalpu[i]=temppu    
    if 'i' in locals():        
        print 'dumping isotopics case {} to picklefile...'.format(i)        
    f2=open(picklefile,'wb')
    pickle.dump(totalpu,f2)
    f2.close()
    print 'done with plutonium.'

    return


def Flux(ini):
    import os
    """
    creates an array with the flux data 
    """
    cases=9
    busteps=30
    path=os.getcwd()+'/'
    picklefile=path+'tnflx'
    if ini=='ini':
        print 'initializing flux picklefile...',
        tnflx=[0]*cases
        f2=open(picklefile,'wb')
        pickle.dump(tnflx,f2)
        f2.close() 
        print ' done.'
        
    else:
        print 'loading flux picklefile...',
        f2=open(picklefile,'rb')
        tnflx=pickle.load(f2)
        f2.close()
        print ' done.'
        
    ngroups=47              # number of energy groups 
    bu=[ '03136','06272','09408','12545','15681','18817','21954','25090','28226','31363']
    bu=['00250','00501','00752','01003','01254','02509','03763','05018','06272',    '07527','08781','10036','11290','12545','13799','15054','16308','17563',    '18818','20072','21327','22581','23836','25090','26345','27599','28854',    '30108','31363']
    
    bu=['00000','00250','00501','00752','01003','01254','02509','03763','05018','06272',
    '07527','08781','10036','11290','12545','13799','15054','16308','17563',
    '18818','20072','21327','22581','23836','25090','26345','27599','28854',
    '30108','31363']

    len_z=49
    A=16
    R       =[30,3,3,3,3,3,3,3,30] # + 3 non fuel  sections
    #flx=np.array(Block2(1,38,16,49,47))
    #                      r  a  z, e
    indfile='indfile.pickle'
    f=open(path+indfile,'rb')
    [ind_cases,ind_time]=pickle.load(f)
    f.close()
    
    casefolder=['0/','1/','2/','3/','4/','5/','6/','7/','8/']
    for i in ind_cases:#range(cases):
        subflx=np.array([[[[[0.0 for ii in range(ngroups)] for j in range(len_z)] for k in range(A)] for l in range(R[i]+3)] for l in range(busteps)])
        print 'processing neutron flux data of case '+str(i)+'..., burnup ',
        for j in ind_time:#range(len(bu)):
            print ' {},'.format(j),
            for k in range(2,51):    # => 49 different planes, [2:50]->[0:48] (2 reflecor planes omitted)
                for l in range(1,48):  # => 47 different energy [1:47][0:46]groups
                    tempindex=[]
                    tempflux=[]
                    ifile='phismg_plane%03d_group%03d_%s.moc0' % (k,l,bu[j])
                    
                    #print ifile
                    f=file(path+casefolder[i]+ifile)
                    reader=csv.reader(f,delimiter=',', skipinitialspace = True, quoting=csv.QUOTE_NONNUMERIC)
                    for row in reader:
                        tempflux.append(row[2])
                        tempindex.append(int(row[1]))
                    f.close
                    #print np.shape(subflx)
                    
                    for m in range(len(tempflux)):
                        r,a=RegioMapper(tempindex[m],k-2,R[i])
                        for n in a:
                            subflx[j,r,n,k-2,l-1]=tempflux[m]
                            #print g,h,i,j,a,r,tempflux[i],flx[r,j,g-2,h-1]
        print ' done.'
        subflx=np.array(subflx)
        tnflx[i]=subflx
        
        
    print 'dumping flux picklefile...',
    f2=open(picklefile,'wb')
    pickle.dump(tnflx,f2)
    f2.close()  
    print ' done.'
    return

