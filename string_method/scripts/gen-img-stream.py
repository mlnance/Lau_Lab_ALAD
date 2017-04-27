#!/usr/bin/python

""" gen-img-stream.py: A simple program for generating image specific CHARMM
                       code for the string method.

      Usage: python gen-img-stream.py <nimg> <nvars> <cycle>

      Description: Reads string_<cycle>.dat and outputs the CHARMM commands for
                   restraints into a stream file img_<img>_cycle_<cycle>.str
                   to be called by run_string.inp

                   See run_string.inp for more details.

      Input: nimgs - the number of images
             nvars - the number of collective variables
             cycle - the iteration cycle of the string method
  
             string_<cycle>.dat - the parametrized (target) 

      Output: img_<img>_cycle_<cycle>.str - stream file containing restraints
                   
                                                                         """
import os, sys

#----------------#
# Initialization #
#----------------#

nimgs = int(sys.argv[1])
nvars = int(sys.argv[2])
cycle = int(sys.argv[3])

string = open('string_%s.dat' %cycle).readlines()

#----------------------------#
# Generate the stream files  #
#----------------------------#

for img in range(nimgs):

  # Make stream files only for evolved images:1-41
  if img != 0 and img != (nimgs-1):
    outfile = open('img_%s_cycle_%s.str' %(img, cycle), 'w')

    for coors in range(nvars/2):

      # Indices of the Collective Variables in the string
      phiInd = nvars * img + (img + 1) + 2 * coors
      psiInd = nvars * img + (img + 1) + 2 * coors + 1
    
      # Get the coor and resid values 
      phiVal = string[phiInd].strip()
      psiVal = string[psiInd].strip()

      # Write out PHI/PSI restraints
      outfile.write("""\
mmfp
geo sphere dihedral - 
  harmonic symmetric force 200.0 tref %s dtoff 0.0 - 
  select type CLP end   select type NL  end -
  select type CA  end   select type CRP end
end

mmfp
geo sphere dihedral - 
  harmonic symmetric force 200.0 tref %s dtoff 0.0 - 
  select type NL  end   select type CA  end -
  select type CRP end   select type NR  end
end

""" %(phiVal, psiVal))
 
    outfile.close()
