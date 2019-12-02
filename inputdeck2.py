from __future__ import division
import sys
#sys.path.append('/home/cbolesch/simulations/sinclepin/scripttest')

import averaging as av
import numpy as np
import time
import copy
import pickle
import os

print 'starting the thdata processing of inputdek.py...'
# neu smulation spring 2013

# this script converts the th_data from star into subachannel like
# th data for an n by n pin model

# geometric convention: (0,0,0) is the centerline bottom of a pin, and the model 
# extends into positive x,y, and z direction and (pitch+owt)/2 in negative
# x and y direction. (see the grid example below) 
# everything in SI units m kg s

# ----- Short description of the workflow -----

# the user sets all proerties, geometries, etc in this file. previous
# input cases are provided as template. when run, this script
# 1) sets presetting 
# 2) reads in thefiles
# 3) calculates the region averages
# 4) writes the tables that become decart input

# in total, the code reads the th file line by line. it decides to which 
# subchannel region ('bin') a cell belongs to, and adds the cells values
# of desity and temperature (weighted by volume) to the bin. after the 
# complete file was read in, the bin average values for density and temp-
# erature are callculated based on the formula
# T_avg = (Sum_i(V_i*T_i))/(Sum_i(V_i)). 
# Now the file is read again line by line, and the according bin detemined
# again. This time, the bin value is written to the line and the line
# written to the output file.

# ----- Manual -----
# setting all setting in the 'User Settings' paragraph of this 'input deck'
# should be sufficient. then run this script from python.
# make sure the averaging.py module is found in the correct folder.



# ----- known issues /todo list
# 1) done
# 2) done
# 3) angle indicator function has a bug.... 4*e-12
# 4) done
# 5) perform total volume check. 
# 6) done
# 7) make FindRadius idiot-proof (accepts huge radius)
# 8) implement finite differences 

# ----- User Settings -----


#ifile_flux
case=1  # 0: 4by4 
        # 1: long_v2 ste2inglepin
   
if case == 1: # singlepin
    if 0: #if running on my laptop 
        ifile_b='G:/powertables/thdata.csv' # F # TH file to read from
        ofile_b='G:/powertables/thdataout.csv'  # TH file to write to
        path_s='G:/powertables/'
        ifile_s=np.array([['flux.csv']])           # Flux file to read from
        ofile_s=np.array([['thfluxout.csv']])           # Flux file to write to
        
    if 1: #if running on my laptop 
        ifile_b='G:/powertables/singlepin/1/thdata_50.cpl' # F # TH file to read from
        ofile_b='G:/powertables/singlepin/1/thdata_50_avg4.cpl'  # TH file to write to
        path_s='G:/powertables/singlepin/1/'
        ifile_s=np.array([['flux_50.cpl']])           # Flux file to read from
        ofile_s=np.array([['flux_50avg.cpl']])           # Flux file to write to 
        x_offset=np.array([0])
        y_offset=np.array([0])        
    
    if 0: #if running on vics machine
        ifile_b='cfd_thdata_0001_1.csv' # F # TH file to read from
        ofile_b='cfd_thdata_0001_1.cpl'  # TH file to write to
        path_s=''
        ifile_s=np.array([['cfd_flux_0001.csv']])           # Flux file to read from
        ofile_s=np.array([['cfd_flux_0001.cpl']])           # Flux file to write to
    
        x_offset=np.array([0])
        y_offset=np.array([0])

    #row index for bulk:
    ri_b_tot= [[1,   2,   3,  4,  5,6,7],[1,   2,   3,  1,  4,5,6]]
    #=index for[Temp,Dens,Vol,Pow,X,Y,Z] clumn in the bulk csv file, for 
    #unprocessed and processed tables (w/o power colum)
    # that means, if the power column is there, put in a 0, else a 1
    
    ri_s=       [0   ,1,   2,   3,4,5]
    #=index for [Temp,Flux,Area,X,Y,Z] clumn in the surf csv file
    
    # definition of the different pin geometries. 
    # the first is 0 and the others are decart region edges
    radii=[[0,0.002324,0.003286,0.004025,0.00476]]
    
    # radius values for the finite difference & interpolation 
    r_interp=np.array([0,0.001162,0.002324,0.002805,0.003286,0.0036555,0.004025,0.0043925,0.00476])
    
    pitch=  0.01284         # distance between pin centers
    owt=    0.0             # outter wall thickness
    z_max=  3.6576
    
    num_angle   =   4       # number of angle divisions of the fluid region
    num_R       =   5       # number of radial segments, according to decart
                           
    grid=[[0]]  # this should be an intuitive map of the pin grid.
                # (0,0) is the center of the lower left pin with 
                # x increasing to the right and y increasing to the top.
                # 0 = fuel pin
                # 1 = guide tube

    
    cntr_print_b   =2000000 # after these many lines a printout is given
    cntr_print_s   =2000000 # after these many lines a printout is given
    subchannel_mode =0      # 0: 4 subchannels per pin
    # doesnt make a         # 1: 4 quarter of subchannels per pin (coarser)
    # difference for        #    only affects the water temperature indices
    # singlepin
    
    #fd_mode=0               # 0: temperature averaging will be according to cfd data
    #                        # 1: finite difference method is used instead for the 
    #                        #    fuel temperature

    z_mesh2=[0.068,0.068,0.068,        # the delta_z nodalisation from decart model
    0.040,                            
    0.08344,0.08344,0.08344,0.08344,0.08344,
    0.040,
    0.08344,0.08344,0.08344,0.08344,0.08344,
    0.040,
    0.08344,0.08344,0.08344,0.08344,0.08344,
    0.040,
    0.08344,0.08344,0.08344,0.08344,0.08344,
    0.040,
    0.08344,0.08344,0.08344,0.08344,0.08344,
    0.040,
    0.08344,0.08344,0.08344,0.08344,0.08344,
    0.040,
    0.08344,0.08344,0.08344,0.08344,0.08344,
    0.040,
    0.07106667,0.07106667,0.07106667,]
    
    # debug mesh
    #z_mesh2=[z_max/10]*10

######## most of the  following section is for post processing
######## comment out for usage in coupling

#A,AT,AF,V,VT,VD,VP,V_p,pinmap,grid,q_max,z_mesh=av.Preparer(pitch,owt,z_max,grid,num_R,num_angle,z_mesh2)

path=os.getcwd()+'/'
casefolder =['0/','1/','2/','3/','4/','5/','6/','7/','8/']

# avgmode is later used to specify the kind of averaginf process and 
# the corresponding changes in table columns (area in case of flux table)
avgmode=[5,5,6,3,5,6,5,5,6] #original
avgmode=[5,5,6,3,5,6,5,5,6]
#        0 1 2 3 4 5 6 7 8
ri_bs  =[0,0,0,0,0,0,0,0,0] #row index bulk set. ## dont know anymore ahat it is, but
                                                # my guess is the numbering of rows
                                                # of the .cpl table
# userpower ist enthalten in : 2 nicht enthalten: 0
                                                
timesteps =['0','4','8','12','16','20','40','60','80','100','120','140','160',
'180','200','220','240','260','280','300','320','340','360','380','400','420',
'440','460','480','500']
picklefile=['tt5','tt6','tp','td','tf','ttc','tt3']
# 5-vol-avg, FD-avg, pow-avg,dens-avg,heatflux-avg,cladtemp-avg, 3-vol-avg

pickhand=[0]*len(picklefile)

tetot=[]
te2tot=[]
tctot=[]
fxtot=[]
ptot=[]

if 0: # DONT!!! resets the database
    print 'creating fresh pickle files...'
   
       
    totaltemp5=av.Block(len(casefolder),len(timesteps),len(radii[0]),num_angle,len(z_mesh2))
    totaltemp6=av.Block(len(casefolder),len(timesteps),len(radii[0])+1,num_angle,len(z_mesh2))
    totalpow  =av.Block(len(casefolder),len(timesteps),len(radii[0]),num_angle,len(z_mesh2))
    totaldens =av.Block(len(casefolder),len(timesteps),len(radii[0]),num_angle,len(z_mesh2))
    totalflux =av.Block(len(casefolder),len(timesteps),1,num_angle,len(z_mesh2))
    totaltcld =av.Block(len(casefolder),len(timesteps),1,num_angle,len(z_mesh2))
    totaltemp3=av.Block(len(casefolder),len(timesteps),len(radii[0]),num_angle,len(z_mesh2))
    
    
    totaltemp5=np.array(totaltemp5)
    totaltemp6=np.array(totaltemp6)
    totalpow  =np.array(totalpow)
    totaldens =np.array(totaldens)
    totalflux =np.array(totalflux)
    totaltcld =np.array(totaltcld)
    totaltemp3=np.array(totaltemp3)
    
    
    
    for i in range(len(pickhand)):
        pickhand[i]=open(path+picklefile[i],'wb')
        
    pickle.dump(totaltemp5,pickhand[0])    
    pickle.dump(totaltemp6,pickhand[1])
    pickle.dump(totalpow,pickhand[2])
    pickle.dump(totaldens,pickhand[3])    
    pickle.dump(totalflux,pickhand[4])
    pickle.dump(totaltcld,pickhand[5])
    pickle.dump(totaltemp3,pickhand[6])
    
    for i in range(len(pickhand)):
        pickhand[i].close()    
tim=time.clock()    

indfile='indfile.pickle'
f=open(indfile,'rb')
[ind_cases,ind_time]=pickle.load(f)
f.close()

    
for kkk in ind_cases:#range(len(casefolder)): #iteration over cases
    
    for lll in ind_time: #range(len(timesteps)): #iteration over BUsteps
        print 'processing thdata case {}, burnup {}...'.format(kkk,timesteps[lll])  
        kk=casefolder[kkk]      #which cases files to be used
        ll=timesteps[lll]       #which burnup step file to be used
        ri_b=ri_b_tot[ri_bs[kkk]] #which set of row indices to be used
        mode=[subchannel_mode,avgmode[kkk]]
        #try
        ifile_b=path+kk+'thdata_'+str(kkk)+'_'+'{:04d}'.format(int(ll))+'.cpl'
        ofile_b=path+kk+'thdata_'+str(kkk)+'_'+'{:04d}'.format(int(ll))+'_avg.cpl'
        
        # !! for singlepin only. if there are multiple pins (4by4, for example) the flux file
        # name must be created inside the 2 forloops at "read in the flux data" a couple
        # of lines further
        ifile_s=path+kk+  'flux_'+str(kkk)+'_'+'{:04d}'.format(int(ll))+'.cpl'
        ofile_s=path+kk+  'flux_'+str(kkk)+'_'+'{:04d}'.format(int(ll))+'_avg.cpl'
        #print ifile_b
        #print ofile_b
        #print ifile_s
        #print ofile_s
        #print lll,ll
        #print ''


##### end of post processing block


                            
                            

        ## prepare meshes, bins,...                            
        A,AT,AF,V,VT,VD,VP,V_p,pinmap,grid,q_max,z_mesh=av.Preparer(pitch,owt,z_max,grid,num_R,num_angle,z_mesh2)                     
        
        #read in the bulk data
        V,VT,VD,V_p,VP=av.BulkReader(ifile_b,ri_b,cntr_print_b,pinmap,grid,z_mesh,radii,num_angle,mode,V,VT,VD,V_p,VP,pitch)
        
        # read in the fux data
        
        for i in range(len(x_offset)): # this 2 forloops iterate the 
            for j in range(len(y_offset)):
                ind_pin=np.array([x_offset[i],y_offset[j]])
                ## multipe pin geometries need the flux file name defined here, not up there
                A,AT,AF=av.SurfReader(ifile_s,ri_s,cntr_print_s,pinmap,grid,z_mesh,num_angle,A,AT,AF,pitch,ind_pin)
                           
        # average values
        Temp,Dens,Powr=av.BulkAvg(V,VT,VD,V_p,VP,q_max)
        TCld,Flux=av.SurfAvg(A,AT,AF,q_max)
        
        if mode[1]==6: # the normal FD averaging
            Temp2_old,Temp2,coef,radiinew,t=av.FD(copy.deepcopy(Temp),TCld,Flux,Powr,copy.deepcopy(radii),q_max,mode)
        elif mode[1]==3 or mode[1]==5:
            Temp2=copy.deepcopy(np.array(Temp))    
            radiinew=radii
        else:
            print 'avgmode=%i is not a valid avg mode. Script abort'
            raise
            
        #print radii, radiinew
        # writing to file
        
        #if kkk in [0,1,2,3,4,5,6,7,8]:
        #    av.BulkWriter(ifile_b,ofile_b,ri_b,cntr_print_b,pinmap,grid,z_mesh,radii,radiinew,num_angle,mode,Temp2,Dens,pitch)
        
        #     
        #for i in range(len(x_offset)):
        #    for j in range(len(y_offset)):
        #        ind_pin=np.array([x_offset[i],y_offset[j]])
        #        av.SurfWriter(ifile_s,ofile_s,ri_s,cntr_print_s,pinmap,grid,z_mesh,radii,num_angle,TCld,Flux,pitch,ind_pin)
        

        if 1: # this part is for postprocessing only. dont use it for actual simulations
            te=np.array(Temp)   #create numpy arrays
            te2=np.array(Temp2)
            tc=np.array(TCld)
            fx=np.array(Flux)
            p=np.array(Powr)
            den=np.array(Dens)
         
            # these lines dont make any sense to me anymore:
            #tetot.append(te)
            #te2tot.append(te2)
            #tctot.append(tc)
            #fxtot.append(fx)
            #ptot.append(p)
        
        
            # opening existing dumpfiles and loadint total files
            for i in range(len(pickhand)):
                pickhand[i]=open(path+picklefile[i],'rb')
                
            #loading into workspace    
            totaltemp5=pickle.load(pickhand[0])    
            totaltemp6=pickle.load(pickhand[1])
            totalpow=pickle.load(pickhand[2])
            totaldens=pickle.load(pickhand[3])    
            totalflux=pickle.load(pickhand[4])
            totaltcld=pickle.load(pickhand[5])
            totaltemp3=pickle.load(pickhand[6]) #should have benn totaltemp3, not 4
            
            # modifying total variables
            if mode[1] == 6:# or mode[1] == 5:
                totaltemp6[kkk,lll,:,:,:]=copy.deepcopy(te2[0,0,:,:,:])
            totaltemp5[kkk,lll,:,:,:]=copy.deepcopy(te[0,0,:,:,:])
            totalpow[kkk,lll,:,:,:]=copy.deepcopy(p[0,0,:,:,:])
            totaldens[kkk,lll,:,:,:]=copy.deepcopy(den[0,0,:,:,:])
            totalflux[kkk,lll,:,:,:]=copy.deepcopy(fx[0,0,:,:,:])
            totaltcld[kkk,lll,:,:,:]=copy.deepcopy(tc[0,0,:,:,:])
            if mode[1]==3:
                totaltemp3[kkk,lll,:,:,:]=copy.deepcopy(te[0,0,:,:,:])
            
            
            for i in range(len(pickhand)):
                pickhand[i].close()    
            
            #writing the new dumpfiles
            for i in range(len(pickhand)):
                pickhand[i]=open(path+picklefile[i],'wb')
            
            pickle.dump(totaltemp5,pickhand[0])    
            pickle.dump(totaltemp6,pickhand[1])
            pickle.dump(totalpow,pickhand[2])
            pickle.dump(totaldens,pickhand[3])    
            pickle.dump(totalflux,pickhand[4])
            pickle.dump(totaltcld,pickhand[5])
            pickle.dump(totaltemp3,pickhand[6])
            
            #close handles
            for i in range(len(pickhand)):
                pickhand[i].close()                
        
                
        print str((time.clock()-tim)/60)+' mins so far; '

print 'done with processing thdata.'        
    
#print str((time.clock()-tim)/60)+' mins total '
#if 0:  # for that radial averaing plot 8 5
#    pickhand=open(path+'tttt','wb')
#    pickle.dump(t,pickhand)
#    pickhand.close()
#
#tt5=totaltemp5
#tt6=totaltemp6 
#tt3=totaltemp3