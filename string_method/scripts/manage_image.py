#!/usr/bin/python

"""manage_image.py: A simple wrapper for launching the CHARMM job to submit the
                    string method                           

    Usage: manage_image.py <image> <cycle> <nvars>
    
    Description: manage_image.py generates random seeds for different initial
                 for the IC of the trajectories. This script simply passes
                 a few variables to the CHARMM script run_string.inp and calls
                 run_string.inp

                 See run_string.inp for more details.
    
    Input: image - the image number
           cycle - the iteration of the string
           nvars - the number of col vars
    
    Output: See run_string.inp
                                                                            """

import os, sys, random

image   = int(sys.argv[1])
cycle   = int(sys.argv[2])
nvars   = int(sys.argv[3])

prev = cycle-1

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
