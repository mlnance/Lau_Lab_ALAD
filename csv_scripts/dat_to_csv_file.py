#!/usr/bin/python
__author__="morganlnance"

'''
You must direct the output of this file to a filename of your own choosing!

Usage: python <script>.py file.dat
Output: properly formated lines for a coords.csv
'''

# imports
import sys, os

# read-in arguments
try:
    dat_file = sys.argv[1]
except IndexError:
    print "\nI need a string_n.dat file.\n"
    sys.exit()
if not os.path.isfile( dat_file ):
    print "\nYou did not give me a valid filepath.\n"
    sys.exit()

# open and read csv file
# start at second line because need to skip header
with open( dat_file, 'r' ) as fh:
    lines = fh.readlines()[1:]

# create a coods.csv file
# the line format should be "phi,psi"
lines = [ line.strip() for line in lines if not line.startswith( '#' ) ]
phi = [ line for line in lines[::2] ]
psi = [ line for line in lines[1::2] ]

print "phi,psi,step"
for ii in range( len( phi ) ):
    print "%s,%s,%s" %( phi[ii], psi[ii], ii )
