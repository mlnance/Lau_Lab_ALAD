#!/usr/bin/python
__author__="morganlnance"


# use argparse to get file and basin phi psi cutoffs
import sys
import argparse
# parse and store input arguments
parser = argparse.ArgumentParser(description="Use Python to determine the min value of two different basins given phi and psi cutoffs")
parser.add_argument("in_file", type=str, help="the *bia.dat or *pmf.dat file")
parser.add_argument("b1_phi_min", type=float, help="the min phi value defining the lower x (phi) value of the first basin")
parser.add_argument("b1_phi_max", type=float, help="the max phi value defining the upper x (phi) value of the first basin")
parser.add_argument("b1_psi_min", type=float, help="the min psi value defining the low y (psi) value of the first basin")
parser.add_argument("b1_psi_max", type=float, help="the max psi value defining the upper x (psi) value of the first basin")
input_args = parser.parse_args()

# example basin 1
'''
b1_psi_max ----------------
           |              |
           |              |
           |              |
           |              |
           |              |
           |              |
b1_psi_min ----------------
          b1_phi_min      b1_phi_max
'''


# open input argument file
# read in the phi, psi, and third variable data
# third variable can be energy (pmf) or count (bia)
try:
    with open( input_args.in_file, "r" ) as fh:
        data = fh.readlines()
except:
    print "\nI need a .dat file. Should be a pmf or bia file. What did you give me?\n"
    sys.exit()


# extract the three sets of data from the file
# phi, psi, val (energy or count or something)
# data_dict = { ( phi, psi ) : val }
# there should be three columns in the data file
# so catch an error if there is not
try:
    data_dict = { ( float( line.split()[0] ) , float( line.split()[1] ) ) : float( line.split()[2] ) for line in data }
except IndexError:
    print "\nI need a file that has three columns of data. Are you sure that's what you gave me?\n"
    sys.exit()


# parse the data_dict using the input basin
# min and max phi and psi values
# this should create a dict of both basins
# each key is a ( phi, psi ) tuple
# so key[0] is phi, and key[1] is psi
basin1 = { key : data_dict[ key ] for key in data_dict.keys()
           if input_args.b1_phi_max >= key[0] >= input_args.b1_phi_min and 
           input_args.b1_psi_max >= key[1] >= input_args.b1_psi_min }


# find the tuple ( phi, psi ) corresponding to
# the min val of the tuple key
# magic function from internet, but I don't understand it
#min( basin1, key=basin1.get )
#http://stackoverflow.com/questions/3282823/get-key-with-the-least-value-from-a-dictionary
basin1_min_phi_psi = None
basin1_min_val = None
for key, val in basin1.items():
    if basin1_min_val is None:
        basin1_min_phi_psi = key
        basin1_min_val = val
    elif val < basin1_min_val:
        basin1_min_val = val
        basin1_min_phi_psi = key

#print "\nbasin1_min_phi_psi:", basin1_min_phi_psi, "\n"
print "phi,psi"
print "%s,%s" %( basin1_min_phi_psi[0],
                 basin1_min_phi_psi[1] )
