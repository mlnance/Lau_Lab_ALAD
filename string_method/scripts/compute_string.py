#!/usr/bin/python

""" compute_string.py: A simple program to compute the unparametrized string
                       values for each image

      Usage: python compute_string.py <nvars> <nimg> <cycle> <ntraj>

      Description:
      
      Input:

      Output: string_unparam_<cycle>.dat 
                                                                            """

import numpy as np
import os, sys

#------------------#
# Helper Functions #
#------------------#

def compute_strimg(sdata, nvars):  
  """Computes the average of the swarm of trajectories from a flattened array"""

  ntraj = sdata.size / nvars
  swarm = np.reshape(sdata, (nvars, ntraj), order='F') # Reshape column major
  strimg = np.zeros(nvars)

  for i in range(nvars):
   
    # Compute Arithmetic Mean:
    strimg[i] = np.sum(swarm[i,:]) / ntraj

  return strimg

def get_colvars(imgfile):
  """Gives a flattened array of col vars"""
  
  image_array = np.loadtxt(imgfile)
  return image_array.flatten() 
   
def get_swarm(img, cycle, nvars, ntraj):
  """Appends col vars in each trajectory to a swarm array"""

  # Preallocate memory
  swarm = np.zeros(ntraj *nvars)  

  for traj in range(ntraj):

    imgfile = open('img_%s_cycle_%s.swm%s' %(img, cycle, traj), 'r')
    colvars = get_colvars(imgfile)
 
    start = traj * nvars 
    end   = (traj + 1) * nvars 

    swarm[start:end] = colvars

  return swarm
  
#--------#
#  MAIN  #
#--------#

nvars = int(sys.argv[1])
nimg  = int(sys.argv[2])
cycle = int(sys.argv[3])
ntraj = int(sys.argv[4])

output = open('string_unparam_%s.dat' %cycle, 'w')

for img in range(nimg):

  # Fixed images, set ntraj = 1 and copy over swarm from initial .var
  if img == 0 or img == (nimg-1):
    os.system('cp img_%s_cycle_1.var img_%s_cycle_%s.swm0' %(img, img, cycle))
    swarm = get_swarm(img, cycle, nvars, 1)
  else: 
    swarm = get_swarm(img, cycle, nvars, ntraj)
    
  strimg = compute_strimg(swarm, nvars)

#  DEBUGGING:
#  print "=============== SWARM %s ===============" %i
#  print np.reshape(swarm, (nvars,10), order = 'F')
#  print "============ String Image %s ===========" %i
#  print strimg

  # Write out the string:
  output.write('# Image %s\n' %img)  # Header
  for j in strimg:
    output.write('%s\n' %j)
