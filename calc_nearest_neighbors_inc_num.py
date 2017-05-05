#!/usr/bin/python
__author__="morganlnance"


'''
Usage: python <script>.py string_cycle#.dat nvars
Arguments: string_cycle#.dat (/path/to/the string.dat file)
           nvars             (the number of variables defining one image)

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
neighbors AND if the nearest neighbor image is larger
in value (higher image number) than iamge ii
This is how image numbers will be taken out of a string
and how to remove knots
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
# 1) read-in and check the string_<>.dat file
try:
    string_file = sys.argv[1]
    # ensure this is a valid path
    if not os.path.isfile( string_file ):
        print "\nI need a valid string_cycle#.dat file."
        print "'%s' is not a valid path.\n" %string_file
        sys.exit()
# if no input argument was given
except IndexError:
    print "\nI need a string_cycle#.dat file.\n"
    sys.exit()
# 2) read-in and check nvars argument
try:
    nvars = sys.argv[2]
    # ensure it is a number
    try:
        nvars = int(float( nvars ))
    # if not a number        
    except ValueError:
        print "\nYou did not give me a number as your nvars argument.\n"
        sys.exit()
# if no nvars was given
except IndexError:
    print "\nYou did not give me an nvars argument.\n"
    sys.exit()


#######################
# COLLECT IMAGES VARS #
#######################
# read and store the image number vars
# from the string_cycle#.dat file
try:
    # nucleus cluster runs on older python
    # no with open statements allowed
    fh = open( string_file, 'r' )
    lines = fh.readlines()
    fh.close()
except IOError:
    print "\nI couldn't open your string_cycle#.dat file.\n" \
        "Is there something wrong with %s ?\n" %string_file
    sys.exit()
# parse the file, storing vars info
all_images_raw = [ float( line.strip() )
                   for line in lines
                   if not line.startswith( '#' ) ] # if not '# Image n'
# string_cycle#.dat file looks like
'''
# Image n
phi
psi
dist
length
...
# Image n+1
phi
psi
dist
length
...
'''
## each image is described by nvars variables
## so each variable associated with each image
## is repeated in a predictable manner
## ex) alad project described by phi,psi
## ex) where phi came first then psi after each
## '# Image n' line
# so loop over the all_images_raw data according to how
# many variables describe the data (nvars)
all_images = []
for ii in range( nvars ):
    # each var that describes the image repeats in
    # a predictable manner
    # so by sorting through all the info from the dat
    # file in a way that parses through it in repeating
    # chunks means that all variables can be pulled out
    # in their corresponding manner
    # reminder: list[start_at:end_before:skip]
    # so start_at should iterate from 0 to nvars
    # and nvars should be skipped each time
    all_images.append( all_images_raw[ii::nvars] )
# unpack and organize the data appropriately
# each tuple in the data list are the variables associated
# with that particular image number (by index)
all_images = zip( *all_images )

# the number of images is the number of
# data point tuples from the file
nimages = len( all_images )



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
    # pull out the variables for that image number
    image_vars = all_images[ii]

    # this keeps track of distances between image ii
    # and all other images jj
    # ignore the image number we are currently using (jj!=ii)
    # use image jj to pull out the image variables from
    # the all_images data holder and use it to
    # calc_dist between image ii and image jj
    distances, image_numbers = zip( *[ (calc_dist( image_vars, 
                                                   all_images[jj] ), 
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
    # only if it is a larger number than ii
    # once we find our next image, we update ii
    # and move to finding the next nearest neighbor
    # that increases in image number up until we
    # get to image number nimages-1
    for nn in neighbors:
        if nn > ii:
            ii = nn
            break

    # add this nearest neighbor to the list
    # this is our new, growing string
    nn_list.append( nn )


###################
# CREATE DAT FILE #
###################
# convert the nearest neighbors data to a new string
for ii in range( len( nn_list ) ):
    # get the corresponding nearest-neighbor image number
    image_num = nn_list[ii]
    # pull out the image
    image = all_images[ image_num ]
    # print the format for this image
    print "# Images %s" %ii
    # print all the data describing this image
    # len( image ) should == nvars
    for jj in image:
        print jj
