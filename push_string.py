#!/usr/bin/python
__author__="morganlnance"

'''
Usage: python <script>.py string_cycle#.dat cycle_number

Using a string_<>.dat file, calculate the normal vector using three points.
Points a, b, c
Calculate vector from a to b, v1
Calculate normal vector to v1, n1
Calculate vector from c to b, v2
Calculate normal vector to v2, n2
Add vectors u1 and u2, push
Normalize the push vector, unit_push
Collect all unit_push vectors for each image
Adjust all unit_push vectors according to a multiplier and 
a simulated annealing calculation
Then
Move all images along the adjusted unit_push vectors

Output: string.dat file Images 0-n pushed along unit_push vectors
'''

###########
# IMPORTS # 
###########
import sys, os
from math import sqrt, cos, pi
from random import choice



####################
# HELPER FUNCTIONS #
####################
def simulated_annealing( cycle, period ):
    '''
    Depending on which cycle number you are on, 
    calculate the level of pushing based on a 
    simulated annealing approach utilizing a 
    cycle number and a period
    :param cycle: int( cycle number of string method )
    :param period: float( length of one period of simulated annealing curve )
    :return: float( amount of "push" to give to image )
    '''
    # (1/2) * cos( 2*pi * (cycle/period) - pi ) + 1/2
    return 0.5 * cos((( 2 * pi ) * ( float( cycle ) / float( period ))) - pi ) + 0.5

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
        
def image_distance( p1, p2 ):
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

def vector_magnitude( v ):
    '''
    Get the magnitude of a vector tuple
    :param v: tuple( phi, psi )
    '''
    # sqrt( dx**2 + dy**2 )
    return sqrt( 
        sum( v[ii]**2
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
# read-in and check cycle_number argument
try:
    cycle_num = sys.argv[2]
    # ensure it is a number
    try:
        cycle_num = float( cycle_num )
    # if not a number
    except ValueError:
        print "\nYou did not give me a number as your cycle_number argument.\n"
        sys.exit()
# if no cycle_number was given
except IndexError:
    print "\nYou did not give me a cycle_number argument.\n"
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



###########################
# DETERMINE MAX PUSH SIZE #
###########################
## max push size is determined by the average 
## distance between successive phi,psi images
# collect the distances between each point of the string
# if there are nimages, there are nimages - 1 lines
# connecting each image together (ie distances to calculate)
# start with one point and get distance to the next point
distances = [ image_distance( phi_psi_data[ii], 
                              phi_psi_data[ii+1] ) 
              for ii in range( nimages - 1 ) ]
# calculate the average distance
avg_img_dist = sum( distances ) / float( len( distances ) )
# the max_push is the average distance between the images
# it will be adjusted later by the simulated annealing stage
max_push = avg_img_dist



#########################
# DETERMINE PUSH VECTOR #
#########################
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

    #####
    ## only for strings whose phi,psi cross barrier
    # keep the phi,psi values of vectors a,b,c
    # between 0 and 360
    # this is to fix periodicity problems
    #a = Vector( ( angle_360( a.phi ),
    #              angle_360( a.psi ) ) )
    #b = Vector( ( angle_360( b.phi ),
    #              angle_360( b.psi ) ) )
    #c = Vector( ( angle_360( c.phi ),
    #              angle_360( c.psi ) ) )
    #####

    # calculate two vectors focused on point b
    # a to b vector v1. b to c vector v2
    # dx = phi2 - phi1
    # dy = psi2 - psi1
    # vector = ( dx, dy )
    # v1
    dphi1 = (b.phi - a.phi)
    dpsi1 = (b.psi - a.psi)
    v1 = Vector( ( dphi1, dpsi1 ) )
    # v2
    dphi2 = (c.phi - b.phi)
    dpsi2 = (c.psi - b.psi)
    v2 = Vector( ( dphi2, dpsi2 ) )

    # since we want some randomness in this algorithm
    # randomly decide which vector direction we will pick
    # there will be two directions for each normal vector
    # so pick the first or second direction calculated
    # if a sufficient number of images are in the string,
    # then the average "push" of the normal vectors sums
    # to zero because about half will be up and half
    # will be down. Meaning we don't affect our algorithm
    # in a polar/directed manner. It is random and equal
    direction = choice( [ 0, 1 ] )

    # calculate the normal to vectors v1 and v2
    # since dx=phi2-phi1 and dy=psi2-psi1
    # then the normals are (-dy, dx) and (dy, -dx)
    # select the vector by using a randomly-selected direction
    # both normals should point in the same direction
    # otherwise they cancel each other out
    n1 = Vector( [ ( -dpsi1, dphi1 ), 
                   ( dpsi1, -dphi1 ) ][ direction ] )
    n2 = Vector( [ ( -dpsi2, dphi2 ), 
                   ( dpsi2, -dphi2 ) ][ direction ] )

    # add the normal vectors together to get the push vector
    # (it should be somewhere in between the two vectors)
    # add vectors component-wise
    # push = ( n1.phi + n2.phi, n1.psi + n1.phi )
    push = Vector( ( n1.phi + n2.phi, 
                     n1.psi + n2.psi ) )

    ## normalize the push vector to a unit vector: u = v / |v|
    ## then adjust the unit vector in a simulated annealing approach
    # determine the magnitude of the push vector
    push_mag = vector_magnitude( push.vector )
    # unit_push = ( phi, psi ) from u = v / |v|
    unit_push = Vector( tuple( 
            [ push.vector[jj] / push_mag
              for jj in range( len( push.vector )) ] ))
    # adjust the unit_push vector according to a simulated
    # annealing equation as defined in a helper function
    # period remains constant (currently an arbitrary value)
    # chosen with the intent to use 100 cycles
    period = 25
    # cycle depends on which cycle number the algorithm is on
    # (1/2) * cos( 2*pi * (cycle/period) - pi ) + 1/2
    sim_anneal = simulated_annealing( cycle_num, period )
    # the multiplier is a factor of the max_push calculated earlier
    # the simulated annealing function and the cycle_num
    # sim_anneal can be between 0 and 1 given the function
    # so the multiplier will be a factor of max_push times
    # the 1 plus the sim_anneal value (so, now it's between 1 and 2)
    # meaning the multiplier is either the max_push or twice max_push
    # this is to ensure that the push is significant enough
    multiplier = max_push * ( sim_anneal + 1 )
    # each component of the vector needs to be multiplied
    # hence using a list comprehension approach to isolate
    # each phi,psi component of the vector (like above normalization)
    # when sim_anneal = 0, there is no push. You are at the
    # bottom of the simulated annealing cosine curve
    # when sim_anneal = max, there is max push. You are at the 
    # top of the simulated annealing cosine curve
    # the simulated annealing function is a periodic one
    # with multiple mins and maxs and heating and cooling cycles
    unit_push = Vector( tuple( 
            [ unit_push.vector[jj] * sim_anneal * multiplier 
              for jj in range( len( unit_push.vector ) ) ] ) )
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
# there is either no push, max push, or in between
for ii, unit_push in zip( range( 1, nimages - 1 ), 
                     unit_push_vectors ):
    # grab the image to move along the unit_push vector
    point = Vector( phi_psi_data[ii] )

    #####
    ## only for strings whose phi,psi cross barrier
    # our unit unit_push vectors were calculated for images
    # between phi,psi values of 0,360
    # so convert the image phi,psi to 0,360
    # this is to fix periodicity problems
    #point = Vector( ( angle_360( point.phi ),
    #                  angle_360( point.psi ) ) )
    #####

    # move the image according to its unit_push vector
    # add it component wise (phi1 + phi2, psi1 + psi2)
    pushed_point = Vector( ( point.phi + unit_push.phi, 
                             point.psi + unit_push.psi ) )

    #####
    ## only for strings whose phi,psi cross barrier
    # now move the pushed point back between -180 and 180
    # phi,psi point was adjusted to 0,360 previously
    # this is to fix periodicity problems
    #pushed_point = Vector( ( angle_180( pushed_point.phi ),
    #                         angle_180( pushed_point.psi ) ) )
    #####

    # add pushed phi,psi point to the data list
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
