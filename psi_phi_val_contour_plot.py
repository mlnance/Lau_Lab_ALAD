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
import numpy as np
import scipy.interpolate


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
    [ ( data_dict[ "phi" ].append( float( line.split()[0] ) ), 
        data_dict[ "psi" ].append( float( line.split()[1] ) ), 
        data_dict[ "val" ].append( float( line.split()[2] ) ) )
      for line in data ]
except IndexError:
    print "\nI need a file that has three columns of data. Are you sure that's what you gave me?\n"
    sys.exit()


# rearrange the data to prepare for a contour plot
# http://stackoverflow.com/questions/9008370/python-2d-contour-plot-from-3-lists-x-y-and-rho
# steps taken from above link
# x = psi, y = phi, z = val (energy, count, something)
x = np.array( data_dict["phi"] )
y = np.array( data_dict["psi"] )
z = np.array( data_dict["val"] )
# Set up a regular grid of interpolation points
xi, yi = np.linspace(x.min(), x.max()), np.linspace(y.min(), y.max())
xi, yi = np.meshgrid(xi, yi)
# Interpolate
rbf = scipy.interpolate.Rbf(x, y, z, function="linear")
zi = rbf(xi, yi)
# plot the data in a contour plot fashion
plt.imshow(zi, vmin=z.min(), vmax=z.max(), origin="lower",
           extent=[x.min(), x.max(), y.min(), y.max()])
plt.xlim( [ -180, 180 ] )
plt.xticks( range( -180, 180 + 1, 60 ) )
plt.xlabel( "Phi", fontsize=16 )
plt.ylim( [ -180, 180 ] )
plt.ylabel( "Psi", fontsize=16 )
plt.yticks( range( -180, 180 + 1, 60 ) )
plt.colorbar( label=val )
plt.title( "Psi vs Phi vs %s Heatmap" %val, fontsize=16 )
plt.show(block=False)
