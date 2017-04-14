#!/usr/bin/python
__author__="morganlnance"

# open input argument file
# read in the phi, psi, and third variable data
# third variable can be energy (pmf) or count (bia)
import sys
try:
    with open( sys.argv[1], "r" ) as fh:
        data = fh.readlines()
except IndexError:
    print "\nI need a .dat file. Should be a pmf or bia file."
    print "Run the program like this: %s filename_bia.dat\n" %__file__.split('/')[-1]
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


# determine if the third value is an energy (pmf) or a count (bia)
# this is for adding a proper legend to the heatmap graph
if "bia" in sys.argv[1]:
    val = "Count"
elif "pmf" in sys.argv[1]:
    val = "Energy"
else:
    val = "Val"


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
             c = data_dict[ "val" ] )
plt.xlim( [ -180, 180 ] )
plt.xticks( range( -180, 180 + 1, 60 ) )
plt.xlabel( "Phi", fontsize=16 )
plt.ylim( [ -180, 180 ] )
plt.ylabel( "Psi", fontsize=16 )
plt.yticks( range( -180, 180 + 1, 60 ) )
plt.colorbar( label=val )
plt.title( "Psi vs Phi vs %s Heatmap" %val, fontsize=16 )
plt.show(block=False)
