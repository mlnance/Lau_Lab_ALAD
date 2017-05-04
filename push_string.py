#!/usr/bin/python
__author__="morganlnance"


## period used for simulated annealing function
period = 25

'''
Usage: python <script>.py string_cycle#.dat nvars cycle_number
Arguments: string_cycle#.dat (/path/to/the string.dat file)
           nvars             (the number of variables defining one image)
           cycle_number      (the number of the current cycle of the algorithm)

Using a string_<>.dat file, calculate the normal vector using two images.
Points a and b
Calculate vector from a to b, v1
Calculate tangent vector to v1, tangent_push
Normalize the tangent_push vector
Collect all tangent_push vectors for each image, except start and stop
Adjust all unit_push vectors according to a multiplier and 
a simulated annealing calculation
Then, iteratively, 
Add normalized tangent_push to the position vector of the corresponding image

Output: string.dat file Images 0-n pushed along unit_push vectors
'''

###########
# IMPORTS # 
###########
import sys, os
from math import sqrt, cos, pi
from random import choice, sample, uniform
import numpy as np



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

def add_vectors( v1, v2 ):
    '''
    Add components of v1 and v2
    :param v1: tuple( vector 1 )
    :param v2: tuple( vector 2 )
    :return: tuple( v1 + v2 )
    '''
    # ensure the vectors are the same size
    if len( v1 ) != len( v2 ):
        print "\nThe vectors you gave me for calculating distance do not have the same number of points.\n"
        sys.exit()
    # add the vectors together component-wise
    v_len = len( v1 )
    return tuple( [ v1[ii] + v2[ii] 
                    for ii in range( v_len ) ] )
        
def subtract_vectors( v1, v2 ):
    '''
    Subtract components of v1 from v2
    :param v1: tuple( vector 1 )
    :param v2: tuple( vector 2 )
    :return: tuple( v2 - v1 )
    '''
    # ensure the vectors have the same number of points
    if len( v1 ) != len( v2 ):
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
    ## dimensional - 1 space and
    ## randomly choose nvars-1 random points between [-1, 1]
    # we have a range of choices from 0 to nvars
    choices = range( nvars )
    # pick nvars-1 points of these choices
    random_picks = sample( choices, nvars-1 )
    # find the point that was not randomly picked
    # this is the one we will need to calculate
    # using the random_picks points that are set to values
    # subtracting the set of random_picks (size nvars-1)
    # from the set of choices (size nvars), will leave
    # the value in choices that is not present in random_picks
    # taking the first element because the difference between
    # set( choices ) and set( random_picks ) should only be
    # one value
    # ex) choices = [ 0, 1, 2 ]
    # ex) random_picks = [ 0, 2 ]
    # ex) --> calc_pt = 1
    calc_pt = list( set( choices ) - set( random_picks ) )[0]

    # we need nvars number of random values between -1 and 1
    # so that the can be parsed according to random_picks
    random_coords = [ uniform( -1, 1 ) for ii in range( nvars ) ]

    # solve the system of equations by calculating the appropriate
    # last variable
    # ex) 3D space, nvars = 3, so we randomly chose two variables (random_coords)
    # ex) equation: nx( x2 - x1 ) + ny( y2 - y1 ) + nz( z2 - z1 ) = 0
    # ex) we randomly chose nx and ny (we know (x1, y1, z1) and (x2, y2, z2))
    # ex) so now we calculate what nz needs to be so the equation is 0
    # so we multiply our randomly chosen random_coords[ii] variable
    # with the difference between v2[ii] and v1[ii] for
    # nvars-1 points of difference vectors v2 and v1
    randomly_chosen_points = [ random_coords[ii] * ( v2[ii] - v1[ii] ) 
                               for ii in random_picks ]
    # random_coords contained nvars values between -1 and 1, 
    # but we need only nvars-1, so adjust the contents of this list
    # ensuring that you are only picking the values that were
    # selected in random_picks
    random_coords = [ random_coords[ii] for ii in random_picks ]

    # with this information, we need to use the last points of
    # v2 and v1 and a now calculated value (instead of random)
    # to get that last portion of the system of equations
    # to equal to zero
    # ex) in 3D case, we need nz( z2 - z1 ) = 0 and calculate nz
    # ex) we calculated nx( x2 - x1 ) and ny( y2 - y1 ), 
    # ex) let's call those values X and Y, respectively and
    # ex) call (z2 - z1) Z
    # ex) so we would have X + Y + nz( Z ) = 0, or, 
    # ex) nz = (-( X + Y )) / Z
    # so we take the sum of what we calculated using random points
    calc_sum = sum( randomly_chosen_points )
    # multiply that by negative one
    calc_sum *= -1
    # and divide that by z2 - z1
    # which in this case is the left over point
    # the one that was not randomly selected and assigned
    last_points_diff = v2[calc_pt] - v1[calc_pt]
    calc_last_coord = calc_sum / last_points_diff

    # so our final point vector that is tangent to v2 and v1
    # is random_coords and calc_last_coord
    # add this calc_last_coord to the list of random_coords
    # so that random_coords now has nvars values (instead of nvars-1)
    # and the random_coords have the selected values and calculated
    # values in the same order that was established
    random_coords.append( calc_last_coord )
    # we chose randomly the points we were going to selected values
    # for and the last point we would calculate, which means that
    # the random_coords data holder of nvars values is not necessarily
    # in the same order as the actual data given in the input vectors
    # so start with the random_picks, they are the first nvars-1 points
    unordered_order = random_picks
    # then add the last point which was the that needed to be calculated
    unordered_order.append( calc_pt )
    # sort this list based on the indices
    # i.e. get the list of indices that would put unordered_order
    # in a sorted order 
    # ex) unordered_order = [ 2, 0, 1 ]
    # ex) np.argsort( unordered_order ) --> [ 1, 2, 0 ]
    # ex) giving order = [ 0, 1, 2 ]
    order = list(np.argsort( unordered_order ))
    # now put the coord values that were randomly selected
    # and calculated (random_coords) in the correct order
    # because prior to this, random_coords was in the same
    # order as random_picks with calc_pt being last
    random_coords = [ random_coords[ii] for ii in order ]
    # finally, turn this into a tuple
    tangent_v = tuple( random_coords )

    # normalize this tangent vector
    normalized_tangent_v = normalize_vector( tangent_v )
    return normalized_tangent_v



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
## where phi came first then psi after each
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



#########################
# DETERMINE PUSH VECTOR #
#########################
# estimate normal vectors between sets of two points
# skip the first and last point (start and stop)
# start and stop points should never move
# store the tangent push vectors
tangent_push_vectors = []
for ii in range( 1, 2 ):
#for ii in range( 1, nimages - 1 ):
    # get points a, b, and c
    # these are successive points
    # data format: ( var1, var2, var3, ..., var_nvars )
    # v = ( var1, var2, ... )
    a = all_images[ii-1]
    b = all_images[ii]

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

    # calculate a normal vector between points a and b
    # this function introduces randomness in direction and
    # normalizes the returned tangent_push vector
    # the tangent_push vector will eventually be added to point b
    tangent_push = calculate_tangent( a, b, nvars )

    # adjust the tangent_push vector according to a simulated
    # annealing equation as defined in a helper function
    # period remains constant (currently an arbitrary value)
    # chosen with the intent to use 100 cycles
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
    #tangent_push = tuple( 
    #        [ tangent_push[jj] * sim_anneal * multiplier 
    #          for jj in range( nvars ) ] )
    tangent_push_vectors.append( tangent_push )
    print ','.join( [ str(tangent_push[0]+b[0]), str(tangent_push[1]+b[1]), str(tangent_push[2]+b[2]) ] )



##################
# PUSHING POINTS #
##################
# now that all the tangent_push vectors have been
# calculated for images 1 to nimages-1, 
# create a data holder for the pushed points
# add the first point (which is unmoved) to the list
# then the last point will be added at the end of this loop
pushed_images = []
pushed_images.append( all_images[0] )
# now that tangent_push_vectors have been collected
# move each phi,psi image along its tangent_push vector
# there is either no push, max push, or in between
for ii, tangent_push in zip( range( 1, nimages - 1 ), 
                     tangent_push_vectors ):
    # grab the image to move along the tangent_push vector
    point = all_images[ii]

    #####
    ## NOT ADJUSTED FOR USING NVARS ARGUMENT
    ## only for strings whose phi,psi cross barrier
    # our unit tangent_push vectors were calculated for images
    # between phi,psi values of 0,360
    # so convert the image phi,psi to 0,360
    # this is to fix periodicity problems
    #point = Vector( ( angle_360( point.phi ),
    #                  angle_360( point.psi ) ) )
    #####

    # move the image according to its tangent_push vector
    # adding them component wise
    pushed_point = add_vectors( point, tangent_push )

    #####
    ## NOT ADJUSTED FOR USING NVARS ARGUMENT
    ## only for strings whose phi,psi cross barrier
    # now move the pushed point back between -180 and 180
    # phi,psi point was adjusted to 0,360 previously
    # this is to fix periodicity problems
    #pushed_point = Vector( ( angle_180( pushed_point.phi ),
    #                         angle_180( pushed_point.psi ) ) )
    #####

    # add pushed image point to the pushed_images list
    pushed_images.append( pushed_point )
# add the last image point (which is also unmoved) to the list
pushed_images.append( all_images[-1] )



###################
# CREATE DAT FILE #
###################
# convert the pushed_images into a .dat file
for ii in range( len( pushed_images ) ):
    # pull out the image
    image = pushed_images[ii]
    # print the format for this image
#    print "# Images %s" %ii
    # print all the data describing this image
    # len( image ) should == nvars
#    for jj in image:
#        print jj
