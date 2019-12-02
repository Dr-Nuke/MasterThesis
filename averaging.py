from __future__ import division
import csv
import math as m
import numpy as np
import sys
import copy
import pdb

### --------
# this module contains all functions used in the  decart/ star (/ mamba)
# coupledrun cfd-to-subchannel- data processing.

# TODO:
# 1) done
# 2) write comments & manual
# 3) done
# 4) compress variables into less variable, so the functions take less arguments
#    geom:  z_mesh,pinmap,pitch,owt,z_max,grid,radii,   
#        :  ri_b,num_angle,num_R,ri_s
#    mode:  subchannel_mode, fd_mode,q_max, FlatFuelMod
#    file:  files*4
#    use dicts, for example        
# 5) V_P is now obsolete, remove it from code
# 6) there is not complete support of multiple pin geometries. fix it
# 7) the submode is not completely implemented, no guarantee bot on/off work
# 8) when the FD is used, the temp averages of fuel & clad dont need to be#
#    calculated. (unneccessary overhead)
# 9) the pintype feature is screwed. remove or fix it (see 6))
# 10) make consisten np.array or lists, not both (Tem, Temp2, Flux,...)


# ----- function definitions -----
def LinePrint(linenumber,n):
    """
    displays the line number at desired occasions. used for command line output
    during execution of read/write
    
    """
    if n ==0:
        print str(linenumber) + ' th line read.'
    if n ==1:
        print str(linenumber) + ' th line written.'
 
def FindBin(x,y,z,pinmap,grid,z_mesh,num_angle,modes,pitch,radii,ind_pin):
    """
    returns the bin indexes (px,py,R,A,Z) to which the point (x,y,z) belongs or
                            (px,py,0,A,Z), depending on bulk or surf cases
    or put it that way: it maps the continous coordinates x,y,z to discrete 
    zylindrical coordinates xpin ypin r theta z'(the latter 3 are unique only
    within a pin) 
    
    Arguments:
    x,y,z coordinates of the point to check
    pinmap contains the information about the pin edges
    grid tells what kind of pin a pin is
    z_mesh is the axial nodalisation
    num_angle is the number of angular segments.
    """
    submode=modes[0]
    flatmode=modes[1]
    if ind_pin==None:                   # Bulk case
        ind_pinx= FindLinear(x,pinmap)  # what x pin
        ind_piny= FindLinear(y,pinmap)  # what y pin
        xx      = x-ind_pinx*pitch      # reduce x coordinate to single pin
        yy      = y-ind_piny*pitch
    else:
        ind_pinx=ind_pin[0]             # surf case; 
        ind_piny=ind_pin[1]             # special coordinate system
        xx      =x
        yy      =y
                  # reduce y coordinate to single pin
    pintype = grid[ind_piny][ind_pinx]          # find the pin type
    if radii!=None: # Bulk case
        ind_r   = FindRadius(xx,yy,radii[pintype])  # find radial section
    else:           # Surface case
        ind_r=0     
    ind_z   = FindLinear(z,z_mesh)              # find z section
    ind_a   = FindAngle(xx,yy,num_angle)    # find angle section 
        
    if ((submode == 1) and (ind_r == 4)): #if we take the coarser mesh (applies to fluid only)
        if -1 not in [ind_pinx,ind_piny,ind_a]:
            ind_pinx,ind_piny,ind_a= ReMapper(ind_pinx,ind_piny,ind_a)
    
    if flatmode==3:
        ind_r,ind_a=FlatFuelMod(ind_r,ind_a)  # brutal averaging  
    
    #print '%+.4f' % x,'%+.4f' % y,'%+.4f' % xx,'%+.4f' % yy, ind_pinx,ind_piny,pintype,ind_r,ind_a, ind_z
    # x,y,reduced x, reduced y, pinx, piny, pintype, r, a z,
    return ind_pinx,ind_piny,ind_r,ind_a,ind_z
    
    



    
def FindLinear(x,map):
    """
    finds the index of the section of map in which x lies. map[0] must be the 
    lowest allowed value, map[-1] the highest
    """
    if x< map[0] or x>map[-1]:    # sort out points out of the geometry
        return -1
    for i in range(len(map[1:])):    # 
        if x<=map[i+1]:
            return i
    return -1
    
    
def FindRadius(x,y,radii):
    
    """
    returns the radial segment indicator. this is 0 center region, increasing to 
    outwards and -1 if none of these are true
    Arguments:  x,y     --  coordinates
                radii   --  radius data of the according pin
                
    """
    r=m.sqrt(x**2+y**2)
    for i in reversed(range(len(radii))):
        if r>= radii[i]:
            return i
    return -1
        
def FindAngle(x,y,A):
    
    """
    returns the angle section indicator of a point (x,y) for A azimuthal segments
    """
    #if ind_r !=2:   # hardcode warning
    #    return 0    # prevents fuel & clad to be divided
    # the outcommented part above is from the time when fuel and
    # clad should  not be angle-divided
    
    temp= m.atan2(y,x) % (2*m.pi)
    ind = int(m.floor(temp/(2*m.pi)*A)) #map angle to segment-#
    return min(ind,A-1)
    
    
    
def PinMapper(pitch,owt,num_pins):
    """
    creates the pin boundary map
    """
    pinmap=[0]*num_pins
    for i in range(num_pins):
        pinmap[i]= (2*i+1)*pitch/2  # each pins upper bound in terms of coordinates
    pinmap[-1]=pinmap[-1] + owt/2   # need to add half the wall on the last one
    pinmap.insert(0,-(pitch+owt)/2) # the lower bound of the first pin as first entry
    return pinmap
        
        
def Block(px,py,R,A,Z):
    """
    generates a 5D array that will allow segment representation
    with intuitive indexing by the indicators
    Arguments: px,py,A,R,Z -- Dimensoions of the array axes
    """
    a = [ [ [ [ [0.0 for i in range(Z)]  for j in range(A)]  for k in range(R)]
    for l in range(py)]  for m in range(px)]
    return a

def ReMapper(ind_pinx,ind_piny,ind_a):
    """
    turns the 4 channel per pin submesh into 4 quater channel per pin
    submesh. the idea is to use the south west bin of a pin for the
    coarse submesh data(see ascii art in the user settings paragraph)
    and redirect the 3 other bins of the same subchannel into that bin.
    """
    if ind_a == 0: #north east edge
        ind_pinx=ind_pinx+1 # move up & to the right 
        ind_piny=ind_piny+1
        ind_a=2
        
    if ind_a == 1: #north west edge 
        ind_piny=ind_piny+1 # move up only
        ind_a=2
        
    #if ind_a == 2: #south west edge
        #stay here! no remapping
        
    if ind_a == 3: #south east edge
        ind_pinx=ind_pinx+1 # move to the right only
        ind_a=2       
    
    return ind_pinx,ind_piny,ind_a
    
    
def FlatFuelMod(r,a):
    """
    modifies the indicators such that one single value of temperature and 
    power is assigned to fuel, and one for clad.
    """
    if r in [0,1,2]: #fuel
        r=0
        a=0
    if r in [3]:   #clad
        a=0
    return r,a    
        
    
def Preparer(pitch,owt,z_max,grid,num_R,num_angle,z_mesh2):
    # 1) generate z_mesh
    z_mesh=[0]          #generate the z meshing in absolute height
    for i in range(len(z_mesh2)):
        z_mesh.append(sum(z_mesh2[0:i+1]))
                            
    ## the following is a uniform z mesh                        
    #z_mesh=[]
    #for i in range(11):      # hardcode warning
    #z_mesh.append((i/10)*z_max)                        
                            
    # 2) misc
    num_Z       =len(z_mesh)-1  # number of z sections 
    num_pins    =len(grid)      # number pins in y direction (atm square grid assumed)
    num_pinsx   =num_pins+1     # could be used lated to define non square geometries
    num_pinsy   =num_pins+1     # the +1 is needed for the coarser subchanmesh,
                                # see ReMapper() for this
                                
    
    grid.reverse()    # turns the intuitive grid map into the numerical practical one
        
    pinmap= PinMapper(pitch,owt,num_pins) # marks the upper bound of each pin
    
    # 3) create lists for the average values    
    V=      Block(num_pinsx,num_pinsy,num_R,num_angle,num_Z)    # segment total Volume (consitency check)
    VT=     Block(num_pinsx,num_pinsy,num_R,num_angle,num_Z)    # segment V*T, will be volume weighted average temp
                                                                # used for T_mean=sum(V_i*T_i)/sum(V_i)
    VD=     Block(num_pinsx,num_pinsy,num_R,num_angle,num_Z)    # see VT
    VP=     Block(num_pinsx,num_pinsy,num_R,num_angle,num_Z)    # V times Power
    V_p=    Block(num_pinsx,num_pinsy,num_R,num_angle,num_Z)    # volume for power
   

    A=      Block(num_pinsx,num_pinsy,1,num_angle,num_Z)    # segment total Area (consitency check)
    AT=     Block(num_pinsx,num_pinsy,1,num_angle,num_Z)    # segment A*T, will be area weighted average temp
                                                            # used for T_mean=sum(V_i*T_i)/sum(V_i)
    AF=     Block(num_pinsx,num_pinsy,1,num_angle,num_Z)    # see AT, Flux
    

   
    q_max=[num_pinsx,num_pinsx,num_R,num_angle,num_Z]
    
    return A,AT,AF,V,VT,VD,VP,V_p,pinmap,grid,q_max,z_mesh
    
    
def BulkReader(ifile,ri_b,cntr_print_b,pinmap,grid,z_mesh,radii,num_angle,mode,V,VT,VD,V_p,VP,pitch):
              
    cntr_bad=0              # counts  bad line (e.g. if a cell is weird)
    f_in= open(ifile, 'rb')
    f_in.next()             # skip header for reading
    reader = csv.reader(f_in,delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
    for row in reader:      # pick the correct data colums from file
        try:
        
            T=row[ri_b[0]]
            d=row[ri_b[1]]
            v=row[ri_b[2]]
            p=row[ri_b[3]] # in case of processed tables, this is dummy data 
            x=row[ri_b[4]]
            y=row[ri_b[5]]
            z=row[ri_b[6]] # an error here might indicate wrong table column idx       
            
            if reader.line_num % cntr_print_b ==0:
                LinePrint(reader.line_num,0)
                
            #if reader.line_num==9794:  # once had a bug at this line
            #    pdb.set_trace()                
                
            q= FindBin(x,y,z,pinmap,grid,z_mesh,num_angle,mode,pitch,radii,None)
            
            # 'q' because a short name is nice here, see below
            # q contains the index set of a cell that maps to the according
            # averaging-region
            # q=[pinx,piny,r,a,z]
            
                        
            # some debug function, not used in operation 
            #debug1=0
            #if debug1==1: # debug mmode. care, outputspam!
            #    aa= '%.4f' % x
            #    cc= '%.4f' % z
            #    bb= '%.4f' % y 
            #    dd= '%.4f' % d
            #    #e= '%+.4f' %
            #    #f= '%+.4f' %
            #    print q, aa,bb,cc,dd
            # \end debug function    
                
            if -1 in q:  # if for whatever reason the indication did not work
                              # dont check for q[-1]  
                print 'line ' + str(reader.line_num) + ' bad: q=' + str(q)
                cntr_bad=cntr_bad+1
                aa=bb   # if the error points here, make sure in inputdeck.py, ri_b 
						# is set according to the file
                continue
            
            # here the cell values are added to thier according bin.
            # in case of fuel and clad, the density is ignored (its constant anyway)
            VT[q[0]][q[1]][q[2]][q[3]][q[4]]=VT[q[0]][q[1]][q[2]][q[3]][q[4]]+v*T
            V[q[0]][q[1]][q[2]][q[3]][q[4]] = V[q[0]][q[1]][q[2]][q[3]][q[4]]+v
            if d < 2000: # no need for density averaging in fuel &clad
                VD[q[0]][q[1]][q[2]][q[3]][q[4]]=VD[q[0]][q[1]][q[2]][q[3]][q[4]]+v*d
            if q[2]<=2: # radial indicator: no need to do treat power density outside of fuel
                VP[q[0]][q[1]][q[2]][q[3]][q[4]]=VP[q[0]][q[1]][q[2]][q[3]][q[4]]+v*p # inzwischen uberflussig?
                V_p[q[0]][q[1]][q[2]][q[3]][q[4]]=V_p[q[0]][q[1]][q[2]][q[3]][q[4]]+v
        except ZeroDivisionError:
            print 'ZeroDivision Error at line '+str(reader.line_num)
            print sys.exc_info()
            print reader.line_num,row
            raise
            
        except IndexError:    
            print 'Indexing Error at line '+str(reader.line_num)
            print 'possible reason: wrong table column index'
            print sys.exc_info()
            print reader.line_num,row     
            raise        
            
    print str(reader.line_num) + ' lines read; among them ' + str(cntr_bad)+ ' bad lines' 
    f_in.close()
    
    return V,VT,VD,V_p,VP
    

def SurfReader(ifile,ri_s,cntr_print_s,pinmap,grid,z_mesh,num_angle,A,AT,AF,pitch,ind_pin):
    # ----- 1) reading ------
    cntr_bad=0
    f_in= open(ifile, 'rb')
    f_in.next()           # skip header
    reader = csv.reader(f_in,delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
    for row in reader:
        T=row[ri_s[0]]
        f=row[ri_s[1]]
        a=row[ri_s[2]]
        x=row[ri_s[3]]
        y=row[ri_s[4]]
        z=row[ri_s[5]]
        
        if reader.line_num % cntr_print_s ==0:
            LinePrint(reader.line_num,0)
            
        q= FindBin(x,y,z,pinmap,grid,z_mesh,num_angle,[0,0],pitch,None,ind_pin) 
                        
        # 'q' because a short name is nice here, see below
        
        #debug1=0    
        #if debug1==1: # debug mmode. care, outputspam!
        #    aa= '%.4f' % x
        #    bb= '%.4f' % y 
        #    cc= '%.4f' % z
        #    dd= '%.4f' % d
        #    #e= '%+.4f' %
        #    #f= '%+.4f' %
        #    print q, aa,bb,cc,dd
        if -1 in q:  # if for whatever reason the indication did not work
            print 'line ' + str(reader.line_num) + ' bad: q=' + str(q)
            counter_bad=cntr_bad+1
            continue
            
            
        AT[q[0]][q[1]][q[2]][q[3]][q[4]]=AT[q[0]][q[1]][q[2]][q[3]][q[4]]+a*T
        A [q[0]][q[1]][q[2]][q[3]][q[4]]= A[q[0]][q[1]][q[2]][q[3]][q[4]]+a
        AF[q[0]][q[1]][q[2]][q[3]][q[4]]=AF[q[0]][q[1]][q[2]][q[3]][q[4]]+a*f

        
    print str(reader.line_num) + ' lines read; among them ' + str(cntr_bad)+ ' bad lines' 
    f_in.close()
    return A,AT,AF
    
       
    
def BulkAvg(V,VT,VD,V_p,VP,q_max):
    """
    takes the colllected data and creates  the averages by division
    """
    num_pinsx   =q_max[0]
    num_pinsy   =q_max[1]
    num_R       =q_max[2]
    num_angle   =q_max[3]
    num_Z       =q_max[4]
    
    Temp=   Block(num_pinsx,num_pinsy,num_R,num_angle,num_Z)    # segment Temperature (final averaged value)
    Dens=   Block(num_pinsx,num_pinsy,num_R,num_angle,num_Z)    # segment Density (final averaged value)
    Powr=   Block(num_pinsx,num_pinsy,num_R,num_angle,num_Z)    # segment Power Density (final averaged value)
    
    for i in range(num_pinsx):
        for j in range(num_pinsy):
            for k in range(num_R):
                for l in range(num_angle):
                    for m in range(num_Z):
                        if V[i][j][k][l][m] != 0: #avoid divide by 0 as fuel & clad isnt trated
                        #try:
                            Temp[i][j][k][l][m]=VT[i][j][k][l][m]/V[i][j][k][l][m]
                            Dens[i][j][k][l][m]=VD[i][j][k][l][m]/V[i][j][k][l][m]
                        #except ZeroDivisonError:
                        #    pass
                        if V_p[i][j][k][l][m]!=0:
                            Powr[i][j][k][l][m]=VP[i][j][k][l][m]/V_p[i][j][k][l][m]

    return Temp,Dens,Powr
 

def SurfAvg(A,AT,AF,q_max):
    """
    takes the colllected data and creates  the averages by division
    """
    num_pinsx   =q_max[0]
    num_pinsy   =q_max[1]
    num_R       =1          # only one radial value, at clad surface
    num_angle   =q_max[3]
    num_Z       =q_max[4]
    
    TCld=   Block(num_pinsx,num_pinsy,num_R,num_angle,num_Z)    # surface segment Temperature (final averaged value)
    Flux=   Block(num_pinsx,num_pinsy,num_R,num_angle,num_Z)    # surface segment Density (final averaged value)
    
    for i in range(num_pinsx):
        for j in range(num_pinsy):
            for k in range(num_R):
                for l in range(num_angle):
                    for m in range(num_Z):
                        if A[i][j][k][l][m] != 0:# when debugging with a part of the table,
                                # some of the volumes may be 0 => div0
                                # also, when the A-R-Z mesh is finer than the
                                # CFD mesh, this occurs
                            TCld[i][j][k][l][m]=AT[i][j][k][l][m]/A[i][j][k][l][m]
                            Flux[i][j][k][l][m]=AF[i][j][k][l][m]/A[i][j][k][l][m]
    return TCld,Flux            

def BulkWriter(ifile,ofile,ri_b,cntr_print,pinmap,grid,z_mesh,radii,radiinew,num_angle,mode,Temp,Dens,pitch):

    counter_bad=0
    
    f_in= open(ifile, 'rb')   
    reader = csv.reader(f_in,delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
    f_out= open(ofile, 'wb')   
    writer = csv.writer(f_out,delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
    # next 3 lines: write header 
    row=reader.next()
    newrow=[row[0],row[ri_b[0]],row[ri_b[1]],row[ri_b[2]],row[ri_b[4]],row[ri_b[5]],row[ri_b[6]]]
    writer.writerow(newrow)
    
    for row in reader:
    
        if reader.line_num % cntr_print ==0:
            LinePrint(reader.line_num,1)
        d=row[ri_b[1]]
        x=row[ri_b[4]]
        y=row[ri_b[5]]
        z=row[ri_b[6]]
        #ri_b=index for[Temp,Dens,Vol,Pow,X,Y,Z]    

            
        q = FindBin(x,y,z,pinmap,grid,z_mesh,num_angle,mode,pitch,radiinew,None)
    
        if -1 in q:  # if for whatever reason the indication did not work
            print 'line ' + str(reader.line_num) + ' bad: q=' + str(q)
            counter_bad=counter_bad+1
            writer.writerow(row)
            continue 
            
        row[ri_b[0]]=Temp[q[0],q[1],q[2],q[3],q[4]]
        # attenton, Temp is now np.array()
        
        
        if d < 2000: # no need for density averaging in fuel &clad
            q = FindBin(x,y,z,pinmap,grid,z_mesh,num_angle,[mode[0],5],pitch,radii,None)
    
            if -1 in q:  # if for whatever reason the indication did not work
                print 'line ' + str(reader.line_num) + ' bad: q=' + str(q)
                counter_bad=counter_bad+1
                writer.writerow(row)
                continue 
            row[ri_b[1]]=Dens[q[0]][q[1]][q[2]][q[3]][q[4]]
        
        newrow=[row[0],row[ri_b[0]],row[ri_b[1]],row[ri_b[2]],row[ri_b[4]],row[ri_b[5]],row[ri_b[6]]]
            #prostarID,Temp             ,Dens             ,Vol              ,X                ,Y                ,Z    
        # the format above is needed to make sure decart can reed the table
        
        writer.writerow(newrow)
        
    print str(reader.line_num) + ' lines written; among them ' + str(counter_bad)+ ' bad lines' 
    
    f_in.close()
    f_out.close()
    
    
def SurfWriter(ifile,ofile,ri_s,cntr_print,pinmap,grid,z_mesh,radii,num_angle,TCld,Flux,pitch,ind_pin):
    cntr_bad=0
    
    f_in= open(ifile, 'rb')   
    reader = csv.reader(f_in,delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
    f_out= open(ofile, 'wb')   
    writer = csv.writer(f_out,delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
    # next 3 lines: write header 
    row=reader.next()
    newrow=[row[ri_s[0]],row[ri_s[1]],row[ri_s[3]],row[ri_s[4]],row[ri_s[5]]]
    writer.writerow(newrow)

    for row in reader:

        
        if reader.line_num % cntr_print ==0:
            LinePrint(reader.line_num,1)
        x=row[ri_s[3]]
        y=row[ri_s[4]]
        z=row[ri_s[5]]
        
        q= FindBin(x,y,z,pinmap,grid,z_mesh,num_angle,[0,0],pitch,None,ind_pin)
    
        if -1 in q:  # if for whatever reason the indication did not work
            print 'line ' + str(reader.line_num) + ' bad: q=' + str(q)
            counter_bad=cntr_bad+1
            writer.writerow(row)
            continue 
            
        row[ri_s[0]]=TCld[q[0]][q[1]][q[2]][q[3]][q[4]]
        row[ri_s[1]]=Flux[q[0]][q[1]][q[2]][q[3]][q[4]]
        newrow=[row[ri_s[0]],row[ri_s[1]],row[ri_s[3]],row[ri_s[4]],row[ri_s[5]]]
        #     =[TClad,       Flux,         X,           Y,           Z]  
        # which is the format decart needs
        writer.writerow(newrow)
    
        
    print str(reader.line_num) + ' lines written; among them ' + str(cntr_bad)+ ' bad lines' 
    
    f_in.close()
    f_out.close()


    
    
# ---------- Debug functions----------#    
def ShowIndex(Temp,Temp2=None):
    """
    
    lists the entries of up to 2 Temp lists together with the indices.
    I mean Temp lists from nnpinavg.py. input should have 2 to 5 axes
    """

    if Temp2==None:
        Temp2=Temp
   
    cntr =0
    Tshape=np.shape(Temp)
    ll=len(Tshape)
    
    for i in range(Tshape[0]):
        for j in range(Tshape[1]):
            if ll>2:
                for k in range(Tshape[2]):
                    if ll>3:
                        for l in range(Tshape[3]):
                            if ll>4:
                                for m in range(Tshape[4]):
                                    if ll>5:
                                        print 'an array is bigger then 5d'
                                        return
                                    
                                    else:
                                        if (Temp[i][j][k][l][m] not in np.array([0.0])) or (Temp2[i][j][k][l][m] not in np.array([0.0])): #[0,np.nan,np.inf]
                                            a= Temp[i][j][k][l][m]== Temp2[i][j][k][l][m]
                                            print i,j,k,l,m, [], Temp[i][j][k][l][m],Temp2[i][j][k][l][m], a
                                            cntr=cntr+1
                            else:
                                if Temp[i][j][k][l]!=0 or Temp2[i][j][k][l]!=0:
                                    a= Temp[i][j][k][l]== Temp2[i][j][k][l]
                                    print i,j,k,l, [], Temp[i][j][k][l],Temp2[i][j][k][l], a
                                    cntr=cntr+1
                    else:
                        if Temp[i][j][k]!=0 or Temp2[i][j][k]!=0:
                            a= Temp[i][j][k]== Temp2[i][j][k]
                            print i,j,k, [], Temp[i][j][k],Temp2[i][j][k], a
                            cntr=cntr+1
            else:
                if Temp[i][j]!=0 or Temp2[i][j]!=0:
                    a= Temp[i][j]== Temp2[i][j]
                    print i,j, [], Temp[i][j],Temp2[i][j], a
                    cntr=cntr+1
    print np.shape(Temp)
    print str(cntr)+' elements printed'
                        
                        
def FD(Temp,TCld,Flux,Powr,radii,q_max,submode): 
    #Finite Difference 
    #### warning ##### hardcode at hand ####
    te=np.array(Temp)   #create numpy arrays
    tc=np.array(TCld)
    fx=np.array(Flux)
    p=np.array(Powr)
    coef=np.array(Block(q_max[0],q_max[1],1,q_max[3],q_max[4]))
    
    rmid=np.array([0.0]*(len(radii[0])-1))
    for i in range(len(radii[0])-1):
        rmid[i]=(radii[0][i]+radii[0][i+1])/2
        
    if submode==1:
        for i in range(q_max[0]-1):
            for j in range(q_max[1]-1):
                for l in range(q_max[3]):
                    
                    ii,jj,ll=ReMapper(i,j,l)
                    coef[i,j,0,l,:]=-fx[i,j,0,l,:]/(tc[i,j,0,l,:]-te[ii,jj,4,ll,:])
    else:
        coef=-fx/(tc-te[:,:,4:5,:,:])
        
    k_z     =17         # W/m2K    
    k_uo2   =6
    
    dr=[]   #from relap script
    dl=[]
    r=np.array(radii[0])
    for j in range(len(r)):
        if j!=0:
            dl.append(r[j]-r[j-1])
        if j!=range(len(r))[-1]:
            dr.append(r[j+1]-r[j])
    dl.insert(0,np.nan)
    dr.append(np.nan)
    dl=np.array(dl)
    dr=np.array(dr)
    
    kl=[np.nan] #from relap script
    kr=[]
    for j in range(len(r)-1):
        if r[j]<0.004025:
            kl.append(k_uo2)
            kr.append(k_uo2)
        else:
            kl.append(k_z)
            kr.append(k_z)
    kr.append(np.nan)    
    kr=np.array(kr)
    kl=np.array(kl)

    dlv=np.pi*dl*(r-dl/4)
    drv=np.pi*dr*(r+dr/4)
    
    dls=2*np.pi*(r-dl/2)/dl
    drs=2*np.pi*(r+dr/2)/dr
    
    db=2*np.pi*r
    
    
    
    
    Ql=np.array(Block(q_max[0],q_max[1],len(r),q_max[3],q_max[4]))
    Qr=np.array(Block(q_max[0],q_max[1],len(r),q_max[3],q_max[4]))
    
    Ql[:,:,0,:,:]=np.nan
    
    for i in range(len(r)-1):
        if r[i]<0.002324:
            Ql[:,:,i+1,:,:]=p[:,:,0,:,:]
            Qr[:,:,i,:,:]=p[:,:,0,:,:]
        elif r[i]<0.003286:
            Ql[:,:,i+1,:,:]=p[:,:,1,:,:]
            Qr[:,:,i,:,:]=p[:,:,1,:,:]            
        elif r[i]<0.004025:
            Ql[:,:,i+1,:,:]=p[:,:,2,:,:]
            Qr[:,:,i,:,:]=p[:,:,2,:,:]        
        else:
            Ql[:,:,i+1,:,:]=0.0
            Qr[:,:,i,:,:]=0.0    
        Qr[:,:,-1,:,:]=np.nan            

    
    
    b_m=np.array(Block(q_max[0],q_max[1],len(r),q_max[3],q_max[4]))
    d_m=np.array(Block(q_max[0],q_max[1],len(r),q_max[3],q_max[4]))
    
    
    # inner points (boundaries are set below)
    a_m=-kl*dls             # p335 ff relap5 manual
    c_m=-kr*drs
    # left boundaries
    c_m[0]=-kr[0]*drs[0]
    # right boundries
    a_m[-1]=-kl[-1]*dls[-1]
    
    num_pinsx=q_max[0]
    num_pinsx   =q_max[0]
    num_pinsy   =q_max[1]
    num_R       =q_max[2]
    num_angle   =q_max[3]
    num_Z       =q_max[4]    
    Temp2=   np.array(Block(num_pinsx,num_pinsy,num_R+1,num_angle,num_Z))    
    t=np.array(Block(q_max[0],q_max[1],len(r)+1,q_max[3],q_max[4]))
    # wee need len(r)+1 since the numbers of bins in fuel and clad
    # increases by one. why? because we will use the FD values at the
    # region edges and extrapolate them as step function. if you draw
    # that on paper, you immediately see why
    r1=radii[0][3]
    r2=radii[0][4]
    
    for i in range(q_max[0]-1):
        for j in range(q_max[1]-1):
            for l in range(q_max[3]):
                for m in range(q_max[4]):
                
                    if submode==1 :
                        ii,jj,ll=ReMapper(i,j,l)  
                    else:    
                        ii,jj,ll=i,j,l
                        
                    b_m[i,j,:,l,m]=-a_m-c_m
                    d_m[i,j,:,l,m]=Ql[i,j,:,l,m]*dlv+Qr[i,j,:,l,m]*drv
    
    # left boundaries
    
                    b_m[i,j,0,l,m]=-c_m[0]      #A_ln from p 336 should be zero, see p 330
                    d_m[i,j,0,l,m]=Qr[i,j,0,l,m]*drv[0]+kr[0]*db[0]/k_uo2
    
    #right boundary
                    
                    b_m[i,j,-1,l,m]=kl[-1]*-coef[i,j,0,l,m]*db[-1]/k_z -a_m[-1]    # Coef3[0,5] and 
                    
                    d_m[i,j,-1,l,m]=kl[-1]*db[-1]*-coef[i,j,0,l,m]*(te[ii,jj,4,ll,m])/k_z+Ql[i,j,-1,l,m]*dlv[-1]        
                    
                        
#    for i in range(q_max[0]-1):
#        for j in range(q_max[1]-1):
#            for l in range(q_max[3]):
#                for m in range(q_max[4]): 
                    
                    #Create matrix
                    
                    M=np.zeros((len(r),len(r)))
                    for k in range(len(r)-1):
                        M[k,k]=b_m[i,j,k,l,m]
                        M[k+1,k]=a_m[k+1]
                        M[k,k+1]=c_m[k]
                    M[-1,-1]=b_m[i,j,-1,l,m] 
                    #if i==1 and j==0 and m==20:
                        #print i,j,k,l,m,np.linalg.det(M)
                        #print M
                        #print d_m[i,j,:,l,m]
                    
                    try:
                        # assign all now-water temperatures to t
                        t[i,j,:-1,l,m]=np.linalg.solve(M,d_m[i,j,:,l,m])
                        
                        
                        
                        
                    except np.linalg.linalg.LinAlgError: # singular matrix
                        print 'singular matrix for i,j,k,l,m = '+str([i,j,k,l,m])
                        t[i,j,:-1,l,m]=0.0                      
                        # this exception rise f.e. because the brutal averaging 
						# (FlatFuelMode) in
						# FindBin is actitivated together with the FD (which 
						# makes no sense....)
						# another reason might be missing flux files
                    # fuel part
                    for k in [0,1,2]:
                        Temp2[i][j][k][l][m]=0.5*(t[i,j,k,l,m]+t[i,j,k+1,l,m])
                    #cladding part
                    t1=t[i,j,3,l,m]
                    t2=t[i,j,4,l,m]
                    Temp2[i][j][3][l][m]=(t2*r2**2-t1*r1**2)/(r2**2-r1**2)-(t2-t1)/(2*np.log(r2/r1))
                    # coolant part
                    Temp2[i][j][4][l][m]=Temp[i][j][4][l][m]
                        
    # calculate new radii

    
    return Temp,Temp2,coef,radii,t

    

    
    
    
    
    
    

def FindMaxValue(file,column,startvalue):
    """
    reads a csv file and gives the maximum of one column
    """

    f_in= open(file, 'rb')

    reader = csv.reader(f_in,delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
    print reader.next()[column]
    for row in reader:
        if row[column]>startvalue:
            startvalue=row[column]
            number=reader.line_num
    print str(startvalue) + ' is maximum'
    return startvalue
            
def LinTester(mesh):


    a=np.linspace(mesh[0],mesh[-1],100)
    for i in a:
        print i,FindLinear(i,mesh)
        

def ShowShape(a):

    """
    shows the shape of all elements in a
    """
    for i in range(len(a)):
        print np.shape(a[i])
    return


def DataSlicer(z1,z_mesh):
    """
    returns the temperature vs radius cell data for specified z regions
    """
        
    ifile2='G:\\powertables\\thdata.csv'
    r_thresh=[]
    t_thresh=[]
    f_in= open(ifile2, 'rb')
    f_in.next()           # skip header
    reader = csv.reader(f_in,delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
    for row in reader:
        
        if row[7]>z_mesh[z1] and row[7]<z_mesh[z1+1]:
            t_thresh.append(row[1])
            r_thresh.append(np.sqrt(row[5]**2+row[6]**2))
    
    f_in.close()
    return r_thresh,t_thresh
    
    #------------ \end debug functions ------------


        