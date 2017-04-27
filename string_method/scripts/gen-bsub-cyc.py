#!/usr/bin/python

"""gen-bsub-cyc.py: A simple program to generate the LSF submission scripts to i
                    nucleus.

     Usage: python gen-bsub-cyc.py <startcycle> <endcycle>
  
     Description: - 

     Input: startcycle - the starting iteration
            endcycle - the last iteration      
          
     Output: as.<image>.<cycle>.sh - the submission script.
                                                                            """
import os, re, random, sys

#-------------------#
# Initial Variables #
#-------------------#

startcycle = int(sys.argv[1])
endcycle   = int(sys.argv[2])

nvars   = 2  # number of collective variables
nimages = 39  # number of images in string
ntraj   = 100

#----------------------------------#
# Write out the Submission scripts #
#----------------------------------#

for cycle in range(startcycle, endcycle+1):
  for image in range(1, nimages-1): 

    # Evolved images(1-40) excluding last
    if image != (nimages-2):
      output = open('as.%s.%s.sh' % (image, cycle), 'w')
      output.write("""\
#!/bin/sh

#BSUB-q normal           # queue
##BSUB-c 7200            # time limit in minutes
#BSUB-J as.%s.%s         # name of the job
#BSUB-o as.%s.%s.o       # LSF output file

./manage_image.py %s %s %s   #(img, cycle, nvars)
""" % (image, cycle, image, cycle, image, cycle, nvars)) 
      output.close()

    # Last evolved image 41
    else:
      output = open('as.%s.%s.sh' % (image, cycle), 'w')
      output.write("""\
#!/bin/sh

#BSUB-q normal           # queue
##BSUB-c 7200            # time limit in minutes
#BSUB-J as.%s.%s         # name of the job
#BSUB-o as.%s.%s.o       # LSF output file

./manage_image_last.py %s %s %s %s %s   #(img, cycle, nvars, nimgs, ntraj)
""" % (image, cycle, image, cycle, image, cycle, nvars, nimages, ntraj))
      output.close()

os.system('chmod +x *.sh')
