#!/usr/bin/python
__author__="morganlnance"

'''
Usage: python <script>.py string_cycle#.dat

Using a string_<>.dat file, calculate the normal vector using three points.
Points a, b, c
Calculate vector from a to b, v1
Calculate normal vector to v1, n1
Normalize n1, now u1
Calculate vector from c to b, v2
Calculate normal vector to v2, n2
Normalize n2, now u2
Add vectors u1 and u2, push
Move point b along push vector
'''

# imports
import sys, os
from math import sqrt, cos
from random import choice

# helper functions
def vector_magnitude( v ):
    # sqrt( dx * dx + dy * dy )
    return sqrt( 
        sum( v[ii] * v[ii]
             for ii in range( len( v ))))


# read-in and check input argument
try:
    string_file = sys.argv[1]
    # ensure this is a filepath
    if not os.path.isfile( string_file ):
        print "\nI need a valid string_cycle#.dat filepath.\n"
        sys.exit()
# if no argument was given
except IndexError:
    print "\nI need a string_cycle#.dat file.\n"
    sys.exit()


# read and store the image number phis
# and psis from the string_cycle#.dat file
try:
    with open( string_file, 'r' ) as fh:
        lines = fh.readlines()
except IOError:
    print "\nI couldn't open your string_cycle#.dat file.\n" \
        "Is there something wrong with %s ?\n" %string_file
    sys.exit()
# parse the file, storing phi,psi info
all_phi_psi_data = [ float( line.strip() ) # phi and psi
                     for line in lines
                     if not line.startswith( '#' ) ] # if not '# Image n'
# string_cycle#.dat file looks like
'''
# Image n
phi
psi
# Image n+1
phi
psi
'''
# so phi comes first, then psi, then repeat
phi_data = all_phi_psi_data[::2]
psi_data = all_phi_psi_data[1::2]
phi_psi_data = zip( phi_data, psi_data )
# the number of images is the number of
# phi,psi tuples from the file
nimages = len( phi_psi_data )


# since we want some randomness in this algorithm
# randomly decide which vector direction we will pick
# there will be two directions for each normal vector
# so pick the first or second direction calculated
direction = choice( [ 0, 1 ] )


# calculate vectors between sets of three points
# skip the first and last point (start and stop)
# start and stop points should never move
for ii in range( nimages - 2 ):
    # get points a, b, and c
    # these are successive points
    # data format: ( phi, psi )
    # so point[0] = phi, point[1] = psi
    # v = ( phi, psi )
    a = phi_psi_data[ii]
    b = phi_psi_data[ii+1]
    c = phi_psi_data[ii+2]

    # calculate two vectors focused on point b
    # a to b vector v1. c to b vector v2
    # dx = phi2 - phi1
    # dy = psi2 - psi1
    # vector = ( (phi2 - phi1), (psi2 - psi1) )
    # v1
    dx1 = (b[0] - a[0])
    dy1 = (b[1] - a[1])
    v1 = ( dx1, dy1 )
    # v2
    dx2 = (b[0] - c[0])
    dy2 = (b[1] - c[1])
    v2 = ( dx2, dy2 )

    # calculate the normal to vectors v1 and v2
    # dx=phi2-phi1 and dy=phi2-psi1
    # then the normals are (-dy, dx) and (dy, -dx)
    # select the vector by using the predetermined direction
    n1 = [ ( -dy1, dx1 ), ( dy1, -dx1 ) ][ direction ]
    n2 = [ ( -dy2, dx2 ), ( dy2, -dx2 ) ][ direction ]

    # normalize the vectors
    # u = v / |v|
    # v1
    v1mag = vector_magnitude( v1 )
    u1 = tuple( [ v1[jj] / v1mag
                  for jj in range( len( v1 )) ] )
    # v2
    v2mag = vector_magnitude( v2 )
    u2 = tuple( [ v2[jj] / v2mag
                  for jj in range( len( v2 )) ] )

