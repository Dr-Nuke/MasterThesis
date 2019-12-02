from __future__ import division
import pickle
import averaging
import numpy as np

import matplotlib as mpl
mpl.rcParams['figure.figsize'] = 8,5

picklefile=['tt5','tt6','tp','td','tf','ttc','tt3','tpu']
path='D:\\powertables\\new\\'
pickhand=[0]*len(picklefile)


for i in range(len(pickhand)):
    pickhand[i]=open(path+picklefile[i],'rb')
    
tt5=pickle.load(pickhand[0])    
tt6=pickle.load(pickhand[1])
tp=pickle.load(pickhand[2])
td=pickle.load(pickhand[3])    
thfx=pickle.load(pickhand[4])
ttc=pickle.load(pickhand[5])

tt3=pickle.load(pickhand[6]) 
tpu=pickle.load(pickhand[7])


for i in range(len(pickhand)):
    pickhand[i].close()    
    
    ## the flux file
picklefile=path+'tnflx'
f2=open(picklefile,'rb')
tnflx=pickle.load(f2)
f2.close()

picklefn='tcrd'    
picklefile=path+picklefn
f2=open(picklefile,'rb')
crud=pickle.load(f2)
f2.close()

z_crud=np.arange(-5.0,375.0,5)
z_crud[0]=0
z_crud[1]=1.25
z_crud[-1]=368.75
z_crud=z_crud/100

z_crud=np.arange(0,370.0,5)/100
tscrud=[0,2,4,6,8,10,12,14,16,18,20,30,40,50,60,70,80,90,100,110,120,130,140,
150,160,170,180,190,200,210,220,230,240,250,260,270,280,290,300,310,320,330,
340,350,360,370,380,390,400,410,420,430,440,450,460,470,480,490,500]


#the special radial averaging plot.
# i think its the one of my thesis where i plot the radial average values 
#together with CFD datapoints
if 0:
    pickhand=open(path+'tttt','rb')
    t=pickle.load(pickhand)
    pickhand.close()

#######
x_offset=np.array([0])
y_offset=np.array([0])

#row index for bulk:
ri_b_tot= [[1,   2,   3,  4,  5,6,7],[1,   2,   3,  1,  4,5,6]]
#=index for[Temp,Dens,Vol,Pow,X,Y,Z] clumn in the bulk csv file, for 
#unprocessed and processed tables (w/o power colum)

ri_s=       [0   ,1,   2,   3,4,5]
#=index for [Temp,Flux,Area,X,Y,Z] clumn in the surf csv file

# definition of the different pin geometries. 
# the first is 0 and the others are decart region edges
radii=[[0,0.002324,0.003286,0.004025,0.00476]]
radii2=[[0.0]*(len(radii[0])-1)]
for i in range(len(radii[0])-1):
    radii2[0][i]=(radii[0][i]+radii[0][i+1])/2  
radii2[0].insert(0,0)
radii2[0].append(0.00476) 

# radius values for the finite difference & interpolation 
r_interp=np.array([0,0.001162,0.002324,0.002805,0.003286,0.0036555,0.004025,0.0043925,0.00476])

pitch=  0.01284         # distance between pin centers
owt=    0.0             # outter wall thickness
z_max=  3.6576

num_angle   =   4       # number of angle divisions of the fluid region
num_R       =   5       # number of radial segments, according to decart
                       
grid=[[0]]  # this should be an intuitive map of the pin grid.
subchannel_mode =0      # 0: 4 subchannels per pin

timesteps =['0','4','8','12','16','20','40','60','80','100','120','140','160',
'180','200','220','240','260','280','300','320','340','360','380','400','420',
'440','460','480','500']
ts=np.array(timesteps)

ts2 =np.array(['000','004','008','012','016','020','040','060','080','100','120','140','160',
'180','200','220','240','260','280','300','320','340','360','380','400','420',
'440','460','480','500'])

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

A,AT,AF,V,VT,VD,VP,V_p,pinmap,grid,q_max,z_mesh=averaging.Preparer(pitch,owt,z_max,grid,num_R,num_angle,z_mesh2)
z_mesh3=[0.0]*(len(z_mesh)-1)
for i in range(len(z_mesh3)):
    z_mesh3[i]=(z_mesh[i]+z_mesh[i+1])/2
    