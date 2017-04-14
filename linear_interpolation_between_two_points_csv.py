#!/usr/bin/python
__author__="morganlnance"

'''
Give me two points( phi1, psi1 ) and ( phi2, psi2 ) and a number of steps to get between these points and this will print to screen a set of phi,psi steps to be written to a coords_<steps>steps.csv file

Usage: python <script>.py phi1, psi1, phi2, psi2, steps
Args:  python <script>.py float, float, float, float, int
'''

# imports
import sys

# get the right input arguments
# phi1
try:
    phi1 = float( sys.argv[1] )
except IndexError:
    print "\nGive me a phi value for your first point.\n"
    sys.exit()
except ValueError:
    print "\nI need a float for phi of the first point.\n"
    sys.exit()
# psi1
try:
    psi1 = float( sys.argv[2] )
except IndexError:
    print "\nGive me a psi value for your first point.\n"
    sys.exit()
except ValueError:
    print "\nI need a float for psi of the first point.\n"
    sys.exit()
# phi2
try:
    phi2 = float( sys.argv[3] )
except IndexError:
    print "\nGive me a phi value for your second point.\n"
    sys.exit()
except ValueError:
    print "\nI need a float for phi of the second point.\n"
    sys.exit()
# psi2
try:
    psi2 = float( sys.argv[4] )
except IndexError:
    print "\nGive me a psi value for your second point.\n"
    sys.exit()
except ValueError:
    print "\nI need a float for psi of the second point.\n"
    sys.exit()
# steps
try:
    steps = int( sys.argv[5] )
except IndexError:
    print "\nGive me the number of steps to get from point 1 to 2.\n"
    sys.exit()
except ValueError:
    print "\nI need an integer for the number of steps between point 1 to 2.\n"
    sys.exit()


# get the distance between each step
phi_step = ( phi2 - phi1 ) / steps
psi_step = ( psi2 - psi1 ) / steps

# linear interpolation to get the coords
# plus one for steps because the first point should be phi1/psi1
phi_coords = [ round( phi1 + ( ii * phi_step ), 3 ) for ii in range( steps + 1 ) ]
psi_coords = [ round( psi1 + ( ii * psi_step ), 3 ) for ii in range( steps + 1) ]
phi_psi_coords = zip( phi_coords, psi_coords )

print "phi,psi,step"
for ii in range( steps + 1 ):
    phi = phi_psi_coords[ii][0]
    psi = phi_psi_coords[ii][1]
    while phi > 180:
        phi -= 360
    while phi < -180:
        phi += 360
    while psi > 180:
        psi -= 360
    while psi < -180:
        psi += 360
    print "%s,%s,%s" %( phi, psi, ii )
