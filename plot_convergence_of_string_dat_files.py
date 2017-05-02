#!/usr/bin/python
__author__="morganlnance"

'''
Uses the /path/to/dat files to construct a graph. Ensure the format of the dat files are as "string_<n>.dat" where n is the cycle number, 1 through n. Assumes all files in sequential order. If you have 1, 2, 3, 5, but not 4, then there will be an issue
'''

# imports
import sys, os
from math import ceil, floor
try:
    import matplotlib
except ImportError:
    print "\nI need matplotlib to work\n"
    sys.exit()
# setting to ensure plot pops up on a Mac
matplotlib.use( "TKAgg" )
import matplotlib.pyplot as plt
plt.rcParams.update( { "font.size" : 14 } )


# input arguments
# dat_file dir
try:
    dat_dir = sys.argv[1]
except IndexError:
    print "\nI need a directory where I can find .dat files\n"
    sys.exit()
# string number, for use in naming the graph
try:
    string_num = sys.argv[2]
except IndexError:
    print "\nWhat number is this string? For plotting purposes.\n"
    sys.exit()
# check input args validity
# ensure dat_dir is a dir
if not os.path.isdir( dat_dir ):
    print "\nI need a directory where I can find .dat files\n"
    sys.exit()
# add trailing /
if not dat_dir.endswith( '/' ):
    dat_dir += '/'
# get all the dat files from the dir
dat_files = [ dat_dir + dat_file for dat_file in os.listdir( dat_dir ) if dat_file.endswith( ".dat" ) ]
# for use in setting a range to open all the dat files
# should be 1 through len( dat_files )
last_dat_file_num = len( dat_files )


############
# GET DATA #
############
# data holder. Diffs between phi and psi from
# each dat file vs its previous dat file
total_changes = []

# for each dat file in the dir
# skip the first dat file
# string_1.dat has no previous dat file
for ii in range( 2, last_dat_file_num + 1 ):
    # open this dat file
    with open( dat_dir + "string_%s.dat" %ii , 'r' ) as fh:
        cur_dat_file = fh.readlines()
    # open the previous dat file
    with open( dat_dir + "string_%s.dat" %( ii - 1 ), 'r' ) as fh:
        prev_dat_file = fh.readlines()
    # get the phi and psi values from each dat file
    # dat file looks like below, so phis come first, then psi
    '''
    # Image n
    phi
    psi
    '''
    # cur phi
    cur_dat_phi = [ float( l.strip() ) for l in cur_dat_file
                    if not l.startswith( '#' ) ][::2]
    # cur psi
    cur_dat_psi = [ float( l.strip() ) for l in cur_dat_file
                    if not l.startswith( '#' ) ][1::2]
    # prev phi
    prev_dat_phi = [ float( l.strip() ) for l in prev_dat_file
                     if not l.startswith( '#' ) ][::2]
    # prev psi
    prev_dat_psi = [ float( l.strip() ) for l in prev_dat_file
                     if not l.startswith( '#' ) ][1::2]
    # count the number of images as lines that start with #
    nimages = len( [ jj for jj in cur_dat_file
                     if jj.startswith( '#' ) ] )
    # ensure they're the same between current and previous
    nimages_prev = len( [ jj for jj in prev_dat_file
                          if jj.startswith( '#' ) ] )
    if not nimages_prev == nimages:
        print "\nThe number of images between string_%s.dat and string_%s.dat are not the same. What happened here?\n" %( nimages_prev, nimages )
        sys.exit()

    # make comparisons between prev and cur
    # first and last image should always be the same, so skip
    # first and last images are the start and end points
    diff_phi = [ abs( prev_dat_phi[jj] - cur_dat_phi[jj] ) 
                 for jj in range( 1, nimages - 1 ) ]
    diff_psi = [ abs( prev_dat_psi[jj] - cur_dat_psi[jj] ) 
                 for jj in range( 1, nimages - 1 ) ]

    # sum the differences and that is the total change
    # between the current cycle and the last
    total_changes.append( sum( diff_phi ) + sum( diff_psi ) )


#############
# PLOT DATA #
#############
# plot the total_changes collected between
# each cycle of the string method run on this path
plt.scatter( x=range( 2, last_dat_file_num + 1 ), y=total_changes )
plt.xlim( [ 0, last_dat_file_num ] )
plt.xticks( range( 0, last_dat_file_num+1, 10 ) )
plt.xlabel( "Cycle Number" )
max_delta = int( ceil( max( total_changes ) ) )
min_delta = int( ceil( min( total_changes ) ) )
plt.ylim( [ 0, max_delta ] )
plt.ylabel( "Abs( Phi,Psi Diffs b/w Cycles )" )
diff = 50
#plt.yticks( range( 0, max_delta+diff, 30 ) )
plt.title( "Convergence of String %s" %string_num )
plt.show(block=False)
