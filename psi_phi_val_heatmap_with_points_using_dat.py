#!/usr/bin/python
__author__="morganlnance"

'''
Plots a landscape using .bia or .pmf data and adds multiples strings by reading all .dat files in a given directory or if given a single file

Usage: python psi_phi_val_heatmap_with_points_using_dat_files.py <bia.dat or pmf.dat file> </path/to/string_<>.dat file(s)>
Example: python psi_phi_val_heatmap_with_points_using_dat_files.py alad_2d_pmf.dat /path/to/dat_file(s)
'''

# open input argument file
# read in the phi, psi, and third variable data
# third variable can be energy (pmf) or count (bia)
import sys, os
try:
    with open( sys.argv[1], "r" ) as fh:
        data = fh.readlines()
except IndexError:
    print "\nI need a .dat file. Should be a pmf or bia file."
    print "Run the program like this: %s filename_bia.dat\n" %__file__.split('/')[-1]
    sys.exit()

# check the .dat file (directory) to get all .dat files
# read in a string_<>.dat file with the points of interest
try:
    # get the points to add from the csv file
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


# determine if the third value is an energy (pmf) or a count (bia)
# this is for adding a proper legend to the heatmap graph
if "bia" in sys.argv[1]:
    title = "Count"
elif "pmf" in sys.argv[1]:
    title = "Energy"
else:
    title = "Val"

# extract the three sets of data from the file
# phi, psi, val (energy or count or something)
data_dict = { "phi": [], "psi": [], "val": []}
# there should be three columns in the data file
# so catch an error if there is not
try:
    [ ( data_dict[ "phi" ].append( line.split()[0] ), 
        data_dict[ "psi" ].append( line.split()[1] ), 
        data_dict[ "val" ].append( line.split()[2] ) ) for line in data ]
except IndexError:
    print "\nI need a file that has three columns of data. Are you sure that's what you gave me?\n"
    sys.exit()


# plot the data in a heatmap fashion
# x = psi, y = phi, z = val (energy, count, something)
plt.scatter( x = data_dict[ "phi" ], 
             y = data_dict[ "psi" ], 
             c = data_dict[ "val" ], zorder=1 )
plt.xlim( [ -180, 180 ] )
plt.xticks( range( -180, 180 + 1, 60 ) )
plt.xlabel( "Phi", fontsize=16 )
plt.ylim( [ -180, 180 ] )
plt.ylabel( "Psi", fontsize=16 )
plt.yticks( range( -180, 180 + 1, 60 ) )
plt.colorbar( label=title )


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

# format of dat_filename should be string_<cycle number>.dat
# so make a dictionary for each cycle based on this info
dat_dict_phi = {}
dat_dict_psi = {}
keys = []
# get phi and psi information from each string_<>.dat file
for dat_file in dat_filenames:
    # prepare the dat_dict
    # split on slashes, then split on .dat then on _
    # ex. goes from /path/to/string_1.dat to string_1.dat to
    # string_1 to 1
    # entries should range from 1 to number of cycles
    key = int( dat_file.split('/')[-1].split(".dat")[0].split('_')[-1] )
    keys.append( key )
    # make an empty phi_psi_coords holder
    # will hold phi and psi data as it comes, like
    # phi1, psi1, phi2, psi2, ..., phin, psin
    # then phi and psi will be passed to the dat_dict
    # final form as dat_dict[ key ] = [ [phi1, psi1], [phi2, psi2], etc ]
    phi_psi_coords = []
    # open the file
    with open( dat_file, "r" ) as fh:
        lines = fh.readlines()
        # format of a string_<>.dat file is
        '''
        # Image 0
        phi
        psi
        # Image 1
        phi
        psi
        etc...
        '''
        for line in lines:
            line = line.strip()
            # skip lines that start with a comment
            if not line.startswith( '#' ):
                phi_psi_coords.append( line )
        # add the [ phi, psi ] data for each dat_file entry
        # [ phi1, psi1, phi2, psi2, ..., phin, psin ]
        # you have to pull out every other element for phi and for psi
        dat_dict_phi[ key ] = phi_psi_coords[::2]
        dat_dict_psi[ key ] = phi_psi_coords[1::2]
        # a bit too fancy of a way to do it
        #dat_dict[ key ] = [ [x,y] for x, y in zip( phi_psi_coords[::2], phi_psi_coords[1::2] ) ]


# sort the keys to plot dat files in order so that
# the last dat file plotted is actually the last string
keys.sort()
## plot the dat files depending on how many there are
## and, if more than one, if it's the last dat file
# x is phi, which is the first set
# y is psi, which is the second set
# if there is only one single dat file to plot, 
# color each scatter point differently
if len( keys ) == 1:
    # store the key and get the number of points along
    # this particular string in the dat file
    key = keys[0]
    num_points = len( dat_dict_phi[key] )
    # each point on the single string has a different color
    color_idx = np.linspace(0, 1, num_points)
    for ii, jj in zip( range( num_points ), color_idx ):
        x = dat_dict_phi[key][ii]
        y = dat_dict_psi[key][ii]
        plt.scatter( x=x, y=y, 
                     s=14, marker='D', zorder=10, 
                     color=plt.cm.Greys(jj), label=key )
        # if you want each scatter point to have its
        # associated point number
        # works because the dat_dicts were filled in
        # image order from the dat phi,psi file
        #plt.annotate( ii, (x, y), color="white", size=8 )
# otherwise, if there are two or more dat files to plot
# plot so that each dat file string is a different color
else:
    # each dat file string plotted has a different color
    color_idx = np.linspace(0, 1, len(keys))
    for ii, jj in zip( range( len( keys ) ), color_idx ):
        key = keys[ii]
        # if this is the last string_#.dat file
        # give it a biger marker and a different color
        if ii == len( keys ) - 1:
            plt.scatter( x = dat_dict_phi[key], 
                         y = dat_dict_psi[key], 
                         s=14, marker='D', color="purple", 
                         zorder=10, label=key )
        # otherwise this is string 1 through nstrings - 1
        # give it a color along the chosen spectrum
        else:
            plt.scatter( x = dat_dict_phi[key], 
                         y = dat_dict_psi[key], 
                         s=10, marker='.', 
                         color=plt.cm.Greys(jj), zorder=10, label=key )
# http://stackoverflow.com/questions/4700614/how-to-put-the-legend-out-of-the-plot
#plt.legend(loc='center left', bbox_to_anchor=(0.5, -0.05), 
#           fancybox=True, shadow=True, ncol=len(keys) )

# title and show the graph
plt.title( "Psi vs Phi vs %s Heatmap" %title, fontsize=16 )
plt.show(block=False)
