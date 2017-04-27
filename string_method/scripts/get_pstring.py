#!/usr/bin/python

"""compute_pstring.py: A simple script for extracting the pushed string from
                       the .var files 

     Usage: python compute_string.py <nimgs> <cycle>
                                                                             """

import numpy as np
import os, sys

#------------------#
# Helper Functions #
#------------------# 

def write_img(img_file, string_file, image):
  
  string_file.write('# Image %s\n' %image)

  for line in img_file:
    line = line.split()
    try:
      # Write the CV to the string file
      string_file.write('%s\n' %line[0])

    except IndexError:
      pass        # Do nothing, probably header info.

#------#
# Main #
#------#

nimgs = int(sys.argv[1])
cycle = int(sys.argv[2])

stringfile = open('string_pushed_%s.dat' % cycle, 'w')

for image in range(nimgs):

  if image == 0 or image == (nimgs-1):
    imgfile = open('img_%s_cycle_1.var' % image, 'r')
  else:
    imgfile = open('img_%s_cycle_%s_pushed.var' %(image, cycle), 'r')
  write_img(imgfile, stringfile, image)
  imgfile.close()

stringfile.close()
