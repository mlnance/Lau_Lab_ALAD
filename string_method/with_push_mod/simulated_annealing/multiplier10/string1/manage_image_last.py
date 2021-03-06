#!/usr/bin/python

"""manage_image_last.py: A simple wrapper for launching the last CHARMM job in
                         the string method.

     Usage: manage_image_last.py <image> <cycle> <nvars> <nimages> <ntraj>

     Description: manage_image.py submits the last CHARMM job in the cycle,
                  computes the average trajectories in the swarm, and
                  reparametrizes the string. Lastly, it cleans up the
                  directory.

                  This is taken care of in separate python scripts. See
                  compute_string.py, wstring_reparam.py, run_string.inp for
                  more information.

     Input: image - the image number
            cycle - the iteration of the string method
            nvars - the number of col vars
            nimages - the number of images
            ntraj - the number of trajectories in the swarm

     Output: See scripts above for more information.

                                                                             """
#----------------#
# Initialization #
#----------------#

import os, sys, random

image   = int(sys.argv[1])
cycle   = int(sys.argv[2])
nvars   = int(sys.argv[3])
nimages = int(sys.argv[4])
ntraj   = int(sys.argv[5])

prev = cycle-1

#----------------------------#
# Launch the last CHARMM job #
#----------------------------#

while 1:  # wait for string file to be written
  if os.path.isfile('string_%s.dat' % prev):
    os.system('sleep 1s')
    break
  else:
    os.system('sleep 10s')

while 1: # Re-run if ABNORMAL termination

  isee1 = random.randint(100,1000000)
  isee2 = random.randint(100,1000000)
  isee3 = random.randint(100,1000000)    
  isee4 = random.randint(100,1000000)
    
  os.system('c36b1_large cycle=%s image=%s isee1=%s isee2=%s isee3=%s isee4=%s < run_string.inp > img_%s_cycle_%s.out' % \
           (cycle, image, isee1, isee2, isee3, isee4, image, cycle))
       
  output = open('img_%s_cycle_%s.out' % (image, cycle), 'r')
  output.seek(-5000,2)  # Go to 5000 bytes from end of file.
  outtail = output.read()
  if outtail.find('ABNORMAL') == -1:
    break

#-----------------------------------------------#
# Reparametrize the string and analyze the data #
#-----------------------------------------------#

while 1:  # wait for cycle to finish (.o files to be written)
  os.system('sleep 5s')
  img_done = 0
  for img in range(1, nimages - 2):  # Count only evolved images:1-41
    if os.path.isfile('as.%s.%s.o' % (img, cycle)):
      img_done += 1
  if img_done == (nimages-3):
    break

os.system('./get_pstring.py %s %s' %(nimages, cycle))
os.system('./compute_string.py %s %s %s %s ' %(nvars, nimages, cycle, ntraj))
# for general, -180,180 strings
os.system('./string_reparam.py %s %s string_unparam_%s.dat > string_%s.dat' % (nvars, nimages, cycle, cycle))
# for strings that cross the boundary
#os.system('./string_reparam_0-360.py %s %s string_unparam_%s.dat > string_%s.dat' % (nvars, nimages, cycle, cycle))

#-------------------------#
# Algorithm modifications #
#-------------------------#
# pushing string testing - Morgan Nance
# simulated annealing approach, pushing along normal to string
# simulated annealing is sinusoidal, so push each cycle
# for general, -180,180 strings
os.system('./push_string.py string_%s.dat %s > string_normal_%s.dat'
          %( cycle, cycle, cycle ) )
#
##
### NEED TO EDIT FIRST BEFORE USING 0-360 ONE
##
#
# for strings that cross the boundary
#os.system('./push_string_0-360.py string_%s.dat > string_normal_%s.dat'
#          %( cycle, cycle ) )
# reparamertize the pushed string
# for general, -180,180 strings
os.system('./string_reparam.py %s %s string_normal_%s.dat > string_%s.dat'
          %(nvars, nimages, cycle, cycle))
# for strings that cross the boundary
#os.system('./string_reparam_0-360.py %s %s string_normal_%s.dat > string_%s.dat'
#          %(nvars, nimages, cycle, cycle))


#------------------------#
# Clean up the directory #
#------------------------#

os.system('/bin/rm img_*_cycle_%s.dcd' % cycle)
os.system('/bin/rm img_*_cycle_%s_pushed.var' %cycle)

os.system('mv img_*_cycle_%s.cor 0cor/' % prev)
os.system('mv img_*_cycle_%s.str 0str/' % prev)
os.system('mv string_%s.dat 0dat/' %prev)

os.system('mv img_*_cycle_%s.out 0out/' % cycle)
os.system('mv img_*_cycle_%s.swm* 0swm/' % cycle)

# These files aren't generated in cycle 1.
if prev > 1:
  os.system('mv string_unparam_%s.dat 0dat/' % prev)
  os.system('mv string_pushed_%s.dat 0dat/' % prev)
  # move files from modifications to algorithm
  if "string_normal_%s.dat" %prev in os.listdir( os.getcwd() ):
    os.system('mv string_normal_%s.dat 0dat/' % prev)
    

# Generate stream files for next iteration
os.system('./gen-img-stream.py %s %s %s' %(nimages, nvars, cycle))
