#!/usr/bin/python
__author__="morganlnance"

'''
coords_<steps>steps.csv to string_1.dat file. Assumes that there is a header, so ensure there is a "phi,psi" header.
You must direct the output of this file to a filename of your own choosing!

Usage: python <script>.py file.csv
Output: properly formated lines for a string_1.dat file
'''

# imports
import sys, os

# read-in arguments
try:
    csv_file = sys.argv[1]
except IndexError:
    print "\nI need a coords_<steps>steps.csv file.\n"
    sys.exit()
if not os.path.isfile( csv_file ):
    print "\nYou did not give me a valid filepath.\n"
    sys.exit()

# open and read csv file
# start at second line because need to skip header
with open( csv_file, 'r' ) as fh:
    lines = fh.readlines()[1:]

# create a string_1.dat file lines
# the line format should be "phi,psi" or "phi,psi,step"
# so split on comma
for line, ii in zip( lines, range(len(lines) ) ):
    line = line.strip()
    print "# Image %s" %ii
    print line.split(',')[0]
    print line.split(',')[1]
