#!/usr/bin/python
__author__="morganlnance"

'''
This script needs an alad_2d_pmf.dat file and a string_100.dat file or a /path/to/dat files
'''

# open input argument file
# read in the phi, psi, and third variable data
# third variable is energy (pmf)
import sys, os
try:
    with open( sys.argv[1], "r" ) as fh:
        data = fh.readlines()
except IndexError:
    print "\nI need a .dat file. Should be a pmf file.\n"
    sys.exit()
# check the .dat file (directory) to get all .dat files
# read in a string_<>.dat file with the points of interest
try:
    # get the points to add from the dat file
    dat_path = sys.argv[2]
    if os.path.isdir( dat_path ):
        is_dir = True
    elif os.path.isfile( dat_path ):
        is_dir = False
    else:
        print "\nYou did not give me a valid .dat file or directory path."
        print "%s is not a valid path.\n" %dat_path
        sys.exit()
    # remove a trailing / if needed, for clarity later
    if dat_path.endswith( '/' ):
        dat_path = dat_path[:-1]
except IndexError:
    print "\nI need a valid path to a directory full of string_<>.dat files\n"
    sys.exit()
try:
    string_num = sys.argv[3]
except IndexError:
    print "\nGive me the string number for this path. For the graph.\n"
    sys.exit()


# import needed functions now that file is read in
try:
    import matplotlib
except ImportError:
    print "\nI need matplotlib to work\n"
    sys.exit()
# setting to ensure plot pops up on a Mac
matplotlib.use( "TKAgg" )
import matplotlib.pyplot as plt
plt.rcParams.update( { "font.size" : 14 } )
import numpy as np


#######
# PMF #
#######
# extract the three sets of data from the pmf file
# ( phi, psi ) = energy
pmf_data_dict = {}
# there should be three columns in the data file
# pmf_data_dict[ ( phi, psi ) ] = energy
for line in data:
    pmf_data_dict[ ( float( line.split()[0] ) ), 
               float( line.split()[1] ) ] = float( line.split()[2] )
pmf_phi_psi = pmf_data_dict.keys()


#######
# DAT #
#######
# handle the dat file(s) depending if a file or directory was given
# if a directory was given
if is_dir is True:
    # read in the string_<>.dat files from the given directories
    dat_filenames = [ dat_path + '/' + dat_file
                      for dat_file in os.listdir( dat_path )
                      # if this is a file (not a directory or something)
                      if os.path.isfile( dat_path + '/' + dat_file )
                      # if it ends with .dat
                      and dat_file.endswith( ".dat" ) ]
    print "\nPlotting %s strings from .dat files\n" %len( dat_filenames )
# otherwise, if a single file was given
if is_dir is False:
    dat_filenames = [ dat_path ]

# round the phi,psi coordinates to the nearest value
# that is found in the input pmf file
# this will be the best estimate
color_idx = np.linspace(0, 1, len(dat_filenames))
max_energy = None
for dat_file, ii in zip( dat_filenames, color_idx ):
    # open and read the data from the string_<>.dat file
    with open( dat_file, 'r' ) as fh:
        dat_data = fh.readlines()
    # extract the data from the string_<>.dat file
    all_dat_phi_psi = [ round( float( line.strip() ), 1 ) 
                        for line in dat_data if not line.startswith( '#' ) ]
    dat_phi_psi = zip( all_dat_phi_psi[::2], all_dat_phi_psi[1::2] )

    # compare all phi,psi for each dat file
    # to the phi,psi combos from the pmf file
    energies = []
    for phi_psi in dat_phi_psi:
        # initiate holders for this round
        min_diff = None
        energy = None
        close_match = None
        # for each phi,psi combo from the pmf file
        for pmf_pp in pmf_phi_psi:
            # sum( abs((pmf_phi - dat_phi)), abs((pmf_psi - dat_psi)) )
            diff = sum( ( abs((pmf_pp[0]-phi_psi[0])), 
                          abs((pmf_pp[1]-phi_psi[1])) ) )
            # keep track of the min_diff and the corresponding
            # phi,psi combo from the pmf file
            if min_diff is None or diff < min_diff:
                min_diff = diff
                energy = pmf_data_dict[ pmf_pp ]
                close_match = pmf_pp
        energies.append( energy )
        # for y-lim in plot
        if max_energy is None or energy > max_energy:
            max_energy = energy

    # now that all energies for each phi,psi in
    # all the images associated with this string_<>.dat file
    # are collected, plot the data
    # energy of image number phi,psi vs image number
    plt.plot( range( len( energies ) ), 
              energies, linestyle="-", 
              color=plt.cm.rainbow(ii) )
    plt.scatter( x=range( len( energies ) ), 
                 y=energies, 
                 color=plt.cm.rainbow(ii) )

# finish the plot
plt.xlim( [ 0, len( dat_phi_psi ) ] )
plt.xlabel( "Image Number" )
plt.ylim( [ 0, round( max_energy ) + 1 ] )
plt.ylabel( "(Phi,Psi) Energy" )
plt.title( "String %s" %string_num )
plt.show(block=False)
