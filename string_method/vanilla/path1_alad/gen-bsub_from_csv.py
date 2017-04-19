#!/usr/bin/python

import os, re, sys, csv

syst   = 'alad'
cycle  = 1
prev   = cycle-1

# read input args, if given
# input should be a coords.csv file
# variable step number for each coord set
# phi, psi, step
# phi1, psi1, 1
# phi2, psi2, 2
try:
  in_file = sys.argv[1]
  # make sure input is a file
  if not os.path.isfile( in_file ):
    print "\nYou gave me an input, but it is not a file. Check your commandline.\n"
    sys.exit()
  # make sure input is a .csv file
  if not in_file.endswith( ".csv" ):
    print "\nYou gave me an input coords file, but it does not have a .csv extension. I need a .csv file.\n"
    sys.exit()
except IndexError:
  print "\nI need a .csv file of coordinate steps.\n"
  sys.exit()

# prepare out file
outsub = open('submit_bsubs.sh', 'w')
outsub.write("#!/bin/bash\n\n")

# just for organization
alad_dir = os.getcwd() + '/'
alad_bsubs_dir = alad_dir + "bsubs/"
alad_out_dir = alad_dir + "data/out/"
alad_o_files_dir = alad_dir + "data/o_files/"
if not os.path.isdir( alad_bsubs_dir ):
  os.mkdir( alad_bsubs_dir )
if not os.path.isdir( alad_out_dir ):
  os.mkdir( alad_out_dir )
if not os.path.isdir( alad_o_files_dir ):
  os.mkdir( alad_o_files_dir )

# get the phi, psi, step data from the .csv file
try:
  f = open( in_file, "r" )
  phi_psi_step_reader = csv.reader( f )
  # there is a header, so skip the first entry
  phi_psi_step_data = [ ( l[0], l[1], l[2] ) for l in phi_psi_step_reader ][1:]
  f.close()
except:
  print "\nI could not open or read your file in Python's csv module.\n"
  sys.exit()

# write out the bsub file
for line in phi_psi_step_data:
  phi = line[0]
  psi = line[1]
  step = line[2]
  # the actual submit script
  output = open('%salad_%s,%s_%s.sh' %(alad_bsubs_dir, phi, psi, step), 'w')
  # this output file needs an extra 'step' input file
  # so phi= psi= cycle= step=
  output.write("""\
#!/bin/sh

#BSUB-q normal             # queue
##BSUB-c 7200              # time limit in minutes
#BSUB-J alad_%s,%s_%s      # name of the job
#BSUB-o %salad_%s,%s_%s.o  # LSF output file

c36b1_large phi=%s psi=%s image=%s < %salad_vac.inp > %salad_phi%s_psi%s_vac_%s.out
""" %(phi, psi, step, alad_o_files_dir, phi, psi, step, phi, psi, step, alad_dir, alad_out_dir, phi, psi, step))

  # for the single file that contains the commands to
  # run each individual submit script made
  # goes to the submit_bsubs script
  outsub.write("bsub < %salad_%s,%s_%s.sh\n" %(alad_bsubs_dir, phi, psi, step))
    
  output.close()

outsub.close()
