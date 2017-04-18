#!/usr/bin/python
__author__="morganlnance"

'''
Usage: python <script>.py string_cycle#.dat

Using a string_<>.dat file, calculate the normal vector using three points.
Points a, b, c
Calculate vector from a to b, v1
Calculate normal vector to v1, n1
Calculate vector from c to b, v2
Calculate normal vector to v2, n2
Add vectors u1 and u2, push
Normalize the push vector, unit_push
Move points along the normalized unit_push vectors

Output: string.dat file Images 0-n pushed along unit_push vectors
'''

###########
# IMPORTS # 
###########
import sys, os
from math import sqrt, cos
from random import choice


####################
# HELPER FUNCTIONS #
####################
def angle_360( angle ):
    '''
    Change your angle (phi or psi) to be between 0 and 360
    :param angle: float( phi or psi value )
    '''
    while angle > 360:
        angle -= 360
    while angle < 0:
        angle += 360
    return angle

def angle_180( angle ):
    '''
    Change your angle (phi or psi) to be between -180 and 180
    :param angle: float( phi or psi value )
    '''
    while angle > 180:
        angle -= 360
    while angle < -180:
        angle += 360
    return angle
        
def vector_magnitude( v ):
    '''
    Get the magnitude of a vector tuple
    :param v: tuple( phi, psi )
    '''
    # sqrt( dx * dx + dy * dy )
    return sqrt( 
        sum( v[ii] * v[ii]
             for ii in range( len( v ))))

class Vector:
    '''
    Vector v is ( phi, psi ). Lets you hold the
    vector information in a more clear format
    '''
    def __init__( self, v ):
        self.phi = v[0]
        self.psi = v[1]
        self.vector = v


####################
# CHECK INPUT ARGS #
####################
# read-in and check string_file argument
try:
    string_file = sys.argv[1]
    # ensure this is a filepath
    if not os.path.isfile( string_file ):
        print "\nI need a valid string_cycle#.dat filepath.\n"
        sys.exit()
# if no string_file was given
except IndexError:
    print "\nI need a string_cycle#.dat file.\n"
    sys.exit()


##########################
# COLLECT IMAGES PHI,PSI #
##########################
# read and store the image number phis
# and psis from the string_cycle#.dat file
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
# and lines starting with '#' were skipped
phi_data = all_phi_psi_data[::2]
psi_data = all_phi_psi_data[1::2]
phi_psi_data = zip( phi_data, psi_data )
# the number of images is the number of
# phi,psi tuples from the file
nimages = len( phi_psi_data )


#########################
# DETERMINE PUSH VECTOR #
#########################
# since we want some randomness in this algorithm
# randomly decide which vector direction we will pick
# there will be two directions for each normal vector
# so pick the first or second direction calculated
direction = choice( [ 0, 1 ] )

# calculate vectors between sets of three points
# skip the first and last point (start and stop)
# start and stop points should never move
# store the unit push vectors
unit_push_vectors = []
for ii in range( 1, nimages - 1 ):
    # get points a, b, and c
    # these are successive points
    # data format: ( phi, psi )
    # so point[0] = phi, point[1] = psi
    # v = ( phi, psi )
    a = Vector( phi_psi_data[ii-1] )
    b = Vector( phi_psi_data[ii] )
    c = Vector( phi_psi_data[ii+1] )

    # calculate two vectors focused on point b
    # a to b vector v1. b to c vector v2
    # dx = phi2 - phi1
    # dy = psi2 - psi1
    # vector = ( (phi2 - phi1), (psi2 - psi1) )
    # v1
    dphi1 = (b.phi - a.phi)
    dpsi1 = (b.psi - a.psi)
    v1 = Vector( ( dphi1, dpsi1 ) )
    # v2
    dphi2 = (c.phi - b.phi)
    dpsi2 = (c.psi - b.psi)
    v2 = Vector( ( dphi2, dpsi2 ) )

    # calculate the normal to vectors v1 and v2
    # dx=phi2-phi1 and dy=phi2-psi1
    # then the normals are (-dy, dx) and (dy, -dx)
    # select the vector by using the predetermined direction
    n1 = Vector( [ ( -dpsi1, dphi1 ), 
                   ( dpsi1, -dphi1 ) ][ direction ] )
    n2 = Vector( [ ( -dpsi2, dphi2 ), 
                   ( dpsi2, -dphi2 ) ][ direction ] )

    # add the normal vectors together to get the push
    # vector (it should be somewhere between the two vectors)
    # add vectors component-wise
    # push = < n1.phi + n2.phi, n1.psi + n1.phi >
    push = Vector( ( n1.phi + n2.phi, 
                     n1.psi + n2.psi ) )

    # normalize the push vector
    # u = v / |v|
    push_mag = vector_magnitude( push.vector )
    # this multiplier is empirically chosen, for now it is a random choice
    multiplier = 10
    unit_push = Vector( tuple( [ multiplier * ( push.vector[jj] / push_mag )
                                 for jj in range( len( push.vector )) ] ))
    unit_push_vectors.append( unit_push )


##################
# PUSHING POINTS #
##################
# create a data holder for the pushed points
# add the first point (which is unmoved) to the list
# the last point will be added at the end of the loop
pushed_phi_psi_data = []
pushed_phi_psi_data.append( Vector( phi_psi_data[0] ) )
# now that unit_push_vectors have been collected
# move each phi,psi image along its unit_push vector
for ii, push in zip( range( 1, nimages - 1 ), 
                     unit_push_vectors ):
    # grab the image to move along the push vector
    point = Vector( phi_psi_data[ii] )

    # move the image according to its push vector
    # add it component wise (phi1 + phi2, psi1 + psi2)
    pushed_point = Vector( ( point.phi + push.phi, 
                             point.psi + push.psi ) )

    # add pushed phi,psi point to a list
    pushed_phi_psi_data.append( pushed_point )
# add the last point (which is unmoved) to the list
pushed_phi_psi_data.append( Vector( phi_psi_data[-1] ) )


###################
# CREATE DAT FILE #
###################
# convert the pushed_phi_psi_data into a .dat file
for ii in range( len( pushed_phi_psi_data ) ):
    # pull out the image
    image = pushed_phi_psi_data[ii]
    # print the format for this image
    print "# Image %s\n%s\n%s" %( ii, 
                                  image.phi, 
                                  image.psi )
