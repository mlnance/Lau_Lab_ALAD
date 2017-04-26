#!/usr/bin/python
__author__="morganlnance"


'''
Usage:

Take each image along a string, in sequence
Calculate the distance between each image
Ex) distance of 2 from 1 and 3, 5 from 4 and 6
Determine each image's nearest neighbors
Is image 4 closest to 3 and 5?
Or is it closest to 3 and 9?
If the latter is true, there is a knot
Then connect each image in terms of its nearest neighbors
If a knot is present, connect that image to its highest
nearest neighbor image number
This is how image numbers will be taken out of a string

Case for start and stop points:
Start needs to be closest to start+1 and start+2
Stop needs to be closest to stop-1 and stop-2
'''


###########
# IMPORTS #
###########
import sys, os
from math import sqrt
import numpy as np


####################
# HELPER FUNCTIONS #
####################
def calc_dist( p1, p2 ):
    '''
    Determine the distance between two points
    Points can have any number of components
    ( phi, psi ), ( x, y, z ), etc
    :param p1: list( or tuple( first point )
    :param p2: list( or tuple( second point )
    :return: float( distance )
    '''
    # ensure the points have the same number of components
    if not len( p1 ) == len( p2 ):
        return None

    # sqrt( i sum n( ( p2i - p1i )**2 ) )
    # with n components from i to n
    return sqrt(
        sum(
            [ ( p2[ii] - p1[ii] )**2
              for ii in range( len( p1 )) ]))


#####################
# READ-IN ARGUMENTS #
#####################
# read-in and check the string_<>.dat file
try:
    string_file = sys.argv[1]
    # ensure this is a valid path
    if not os.path.isfile( string_file ):
        print "\nI need a valid string_<>.dat file."
        print "\n%s is not a valid path.\n" %string_file
        sys.exit()
    # read the data from the string_file
    try:
        string_f = open( string_file, 'r' )
        string_data = string_f.readlines()
        string_f.close()
    except:
        print "\nI had an issue opening and reading your string file.\n"
        sys.exit()
# if no input argument was given
except IndexError:
    print "\nI need a string_<>.dat file.\n"
    sys.exit()


#############################
# PARSE THROUGH STRING DATA #
#############################
## collect the string phi,psi data from the file
# ignore commented lines in the string file (# Image n)
# phi,psi data is repeated in order per image
try:
    string_data = [ float( l.strip() ) for l in string_data
                    if not l.startswith( '#' ) ]
except:
    print "\nSomething is wrong with your string_<>.dat file."
    print "Are there lines in there that need to be commented out?\n"
    sys.exit()
# collect phi,psi data in tuples per image
string_phi_psi = zip( string_data[::2], 
                      string_data[1::2] )
# there are as many images as phi,psi tuples
nimages = len( string_phi_psi )


###############################
# DETERMINE NEAREST NEIGHBORS #
###############################
## go in sequential order through images and
## determine distance between image i and
## all other images in the string, all while
## keeping track of nearest neighbors to images
# iterate through each image number in the string
# nn means nearest neighbor
# nn_dict will contain each image number
# as the key, and its value will be a list of
# its two nearest neighbors
# ex) nn_dict[ 4 ] = [ 3, 5 ]
nn_dict = {}
for ii in range( nimages ):
    # pull out the phi,psi tuple for that image number
    ii_phi_psi = string_phi_psi[ ii ]

    # this keeps track of distances between image
    # ii and all other images jj
    # ignore the image number we are currently using (jj!=ii)
    # use image jj to pull out the phi,psi tuple from
    # the string_phi_psi data holder and use it to
    # calc_dist between image ii and image jj
    distances, image_numbers = zip( *[ (calc_dist( ii_phi_psi, 
                                                   string_phi_psi[ jj ] ), 
                                        jj )
                                       for jj in range( nimages )
                                       if not jj == ii ] )

    # pull out the indices associated with the nearest neighbors
    # np.argsort returns the indices that would sort the list
    # since distances and image_numbers were filled in the same
    # order, getting the indices for the two smallest values
    # from distances will give the same indices needed to
    # pull out the corresponding image numbers that are the
    # nearest neighbor images to image ii
    nn = [ image_numbers[ jj ]
           for jj in np.argsort( distances )[0:5] ]

    # store this nearest neighbor (nn) info in the dictionary
    nn_dict[ ii ] = nn
