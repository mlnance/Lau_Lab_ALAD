#!/usr/bin/python
__author__="morganlnance"


'''
NOT AS OPTIMIZED OF A SOLUTION TO THE NEAREST-NEIBHOR, KNOT-FIXING PROBLEM

Usage: python <script.py> /path/to/string_<>.dat

Take each image ii along a string, in sequence
Calculate the distance between ii and every other image
in the string that is not the same as image ii
Ex) image 1 to image 0, 2, 3, 4, ..., n
Rank images in terms of how close they are to image ii
( this is determining image iis nearest neighbors )
If image ii is closest to another image that is not ii+1
or ii-1, then there is likely a knot
Iterate through each image number (starting at 0) and
connect these images in order in terms of their nearest
neighbors AND if this nearest neighbor has not been seen before
( this method allows images to connect in an order that does
not necessarily have to be increasing order )
This is how image numbers will be taken out of a string, if
it is necessary, and how to remove knots
Move through each image number until string start (image 0)
is connected to the string end (image n)
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
# nn_list starts from the first image (0)
# and grows until nimages-1 in increasing order
# depending on which images are nearest neighbors
nn_list = [ 0 ]
ii = 0
while ii != ( nimages - 1 ):
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
    neighbors = [ image_numbers[ jj ]
                  for jj in np.argsort( distances ) ]

    # find the nearest neighbor to current image ii
    # only if it is an image that has not been used before
    # once we find our next image, we update ii
    # and move to finding the next nearest neighbor
    # until we get the image number nimages-1
    for nn in neighbors:
        if nn not in nn_list:
            # add this nearest neighbor to the list
            # this is our new, growing string
            nn_list.append( nn )

            # update our new starting image to find
            # the next nearest neighbor
            ii = nn
            break


# write out the new string
# string_phi_psi = ( phi, psi )
# so phi is the first element and psi is the second
for img, ii in zip( nn_list, range( len( nn_list ) )):
    print "# Image %s\n%s\n%s" %( ii,
                                  string_phi_psi[img][0], 
                                  string_phi_psi[img][1] )
