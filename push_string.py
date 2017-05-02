#!/usr/bin/python
__author__="morganlnance"

'''
Usage: python <script>.py string_cycle#.dat nvars cycle_number
Arguments: string_cycle#.dat (/path/to/the string.dat file)
           nvars             (the number of variables defining one image)
           cycle_number      (the number of the current cycle of the algorithm)

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
from random import choice, uniform



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
        
def vector_difference( v1, v2 ):
    '''
    Get the difference between vector v1 and vector v2
    :param v1: tuple( 1p1, 1p2, ..., 1pn )
    :param v2: tuple( 2p1, 2p2, ..., 2pn )
    :return: tuple( 2p1 - 1p1, 2p2 - 1p2, ... )
    '''
    # ensure the vectors have the same number of points
    if not len( v1 ) == len( v2 ):
        print "\nThe vectors you gave me for calculating distance do not have the same number of points.\n"
        sys.exit()
    # calculate distance
    v_len = len( v1 )
    return tuple( [ v2[ii] - v1[ii] for ii in range( v_len ) ] )

def vector_magnitude( v ):
    '''
    Get the magnitude of a vector tuple
    :param v: tuple( p1, p2, ..., pn )
    :return: float( magnitude )
    '''
    return sqrt( 
        sum( v[ii]**2
             for ii in range( len( v ))))

def normalize_vector( v ):
    '''
    Normalize the vector v_hat = v / |v|
    :param v: tuple( vector )
    :return: tuple( normalized vector )
    '''
    return tuple( [ v[ii] / vector_magnitude( v ) 
                    for ii in range( len( v ) ) ] )

def calculate_tangent( v1, v2, nvars ):
    '''
    Calculate the tangent vector between position vectors v1 and v2
    Both v1 and v2 are described by nvars number of points
    :param v1: tuple( position vector 1 )
    :param v2: tuple( position vector 2 )
    :param nvars: int( number of variables describing an image point )
    :return: tuple( tangent vector )
    '''
    ## solve a system of equations to find a point in nvars-
    ## dimensional -1 space
    # choose nvars -1 random points between [-1, 1]
    random_coords = [ uniform( -1, 1 ) for ii in range( nvars - 1 ) ]

    # solve the system of equations by calculating the appropriate
    # last variable
    # ex) 3D space, nvars = 3, so we choose two variables (random_coords)
    # ex) equation: nx( x2 - x1 ) + ny( y2 - y1 ) + nz( z2 - z1 ) = 0
    # ex) we randomly chose nx and ny (we know (x1, y1, z1) and (x2, y2, z2))
    # ex) so now we calculate what nz needs to be so the equation is 0
    # so we multiply our randomly chosen random_coords[ii] variable
    # with the difference between v2[ii] and v1[ii] for
    # nvars-1 points of difference vectors v2 and v1
    randomly_chosen_points = [ random_coords[ii] 
                               * ( v2[ii] - v1[ii] ) 
                               for ii in range( nvars - 1 ) ]
    # with this information, we need to use the last points of
    # v2 and v1 and a now calculated value (instead of random)
    # to get that last portion of the system of equations
    # to equal to zero
    # ex) in 3D case, we need nz( z2 - z1 ) = 0 and calculate nz
    # ex) we calculated nx( x2 - x1 ) and ny( y2 - y1 ), 
    # ex) let's call those values X and Y, respectively and
    # ex) call (z2 - z1) Z
    # ex) so we would have X + Y + nz( Z ) = 0, or, 
    # ex) nz * Z = -( X + Y )
    # so we take the sum of what we calculated using random points
    calc_sum = sum( randomly_chosen_points )
    # multiply that by negative one
    calc_sum *= -1
    # and divide that by z2 - z1
    # minus one because python is 0-indexed
    last_points_diff = v2[nvars-1] - v1[nvars-1]
    calc_last_coord = calc_sum / last_points_diff

    # so our final point vector that is tangent to v2 and v1
    # is random_coords and calc_last_coord
    random_coords.append( calc_last_coord )
    tangent_v = tuple( random_coords )

    # normalize this vector
    unit_normal_v = normalize_vector( tangent_v )
    return unit_normal_v



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
# read-in and check nvars argument
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
# read-in and check cycle_number argument
try:
    cycle_num = sys.argv[3]
    # ensure it is a number
    try:
        cycle_num = int(float( cycle_num ))
    # if not a number
    except ValueError:
        print "\nYou did not give me a number as your cycle_number argument.\n"
        sys.exit()
# if no cycle_number was given
except IndexError:
    print "\nYou did not give me a cycle_number argument.\n"
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
all_phi_psi_data = [ float( line.strip() ) # phi and psi
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
## where phi came first then psi after each
## '# Image n' line
# so loop over the data according to how
# many variables describe the data (nvars)
all_data = []
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
    all_data.append( all_phi_psi_data[ii::nvars] )
# unpack and organize the data appropriately
# each tuple in the data list are the variables associated
# with that particular image number (by index)
data = zip( *all_data )

# the number of images is the number of
# data point tuples from the file
nimages = len( data )



#########################
# DETERMINE PUSH VECTOR #
#########################
# estimate normal vectors between sets of two points
# skip the first and last point (start and stop)
# start and stop points should never move
# store the unit push vectors
unit_push_vectors = []
for ii in range( 1, 2 ):
#for ii in range( 1, nimages ):
    # get points a, b, and c
    # these are successive points
    # data format: ( var1, var2, var3, ..., var_nvars )
    # v = ( var1, var2, ... )
    a = data[ii-1]
    b = data[ii]

    #####
    ## NOT ADJUSTED FOR USING NVARS ARGUMENT
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
    '''
    # calculate the difference between points
    # a and b (could b in n dimensional space)
    # each vector has nvars points to it
    diff_a_b = vector_difference( a, b )

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
    '''
    # calculate a normal vector between points a and b
    # this function introduces randomness
    tangent = calculate_tangent( a, b, nvars )
    print tangent
    '''

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
    # the multiplier is empirically chosen, for now it is a random choice
    # this is to ensure that the push is significant enough
    multiplier = 20.0
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
'''
