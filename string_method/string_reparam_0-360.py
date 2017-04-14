#!/usr/bin/python

# A simple script to reparametrize the string
#  Usage: python string_reparam.py [nvar] [nimg] [fname]

import os, sys, math
import numpy as np

## ------------------------ Helper Functions ----------------------- ##

# Projection
def project(start_point, gradient, dist):
  return start_point + gradient * dist

def angle (a):
  while a > 360:
    a -= 360
  while a < 0:
    a += 360
  return a

## ------------------------- Read in the data ---------------------- ##

nvar     = int(sys.argv[1])
nimg     = int(sys.argv[2])
fname    = sys.argv[3]

string = open(fname, 'r').readlines() 

# Allocate memory for storing points
pts = np.zeros(nimg * nvar)
count = 0

for line in string:
  
  line = line.strip()
  
  # Remove comments
  if line[0] != '#': 
    pts[count] = float(line)
    count += 1

pts.resize(nimg, nvar)

#print pts

## ------------------ Compute Gradient/String Length --------------- ##

slength = np.zeros(nimg)                  # String Length
grad = np.zeros((nimg-1, nvar))           # FD between img (n+1, n)

# Projection parameters
for i in range(nimg-1):

  diff_v = np.zeros(nvar)

  # Take care of angle variables
  for j in range(nvar):
    diff_v[j] = angle(pts[i+1, j]) - angle(pts[i,j])
    
  dist = np.linalg.norm(diff_v)

  grad[i, :] = diff_v / dist
  slength[i+1] = slength[i] + dist

## -------------------- Reparametrize the string ------------------- ##

img_dist   = slength[-1] / float(nimg - 1)
new_string = np.copy(pts)

#print "Gradient"
#print grad
#print "slength"
#print slength
#print 

for i in range(nimg):

  tot_dist = img_dist * i
  
  # First and last points, Project 0 distance.
  #   Careful - Floating Point rounding errors
  if tot_dist == 0 or round(tot_dist, 5) == round(slength[-1], 5):

    start_pt = [angle(pts[i,:][0]), angle(pts[i,:][1])]
    new_pt = start_pt                       

#    print tot_dist
#    print 'ITER = %s' %i
#    print 'START_PT = %s, NEW_PT = %s \n' %(start_pt, new_pt)

  else:
    link = np.searchsorted(slength, tot_dist) - 1    # nth link of string

#    print tot_dist
#    print 'ITER = %s LINK = %s' % (i, link)
   
    # Compute the new points
    start_pt = [angle(pts[link][0]), angle(pts[link][1])]
    gradient  = grad[link, :]
    proj_dist = tot_dist - slength[link]

    new_pt = project(start_pt, gradient, proj_dist)

#    print 'START_PT = %s   PROJ DIST = %s   GRADIENT = %s' %(start_pt, proj_dist, gradient)
#    print 'NEW_PT = %s \n' % new_pt

  new_string[i, :] = new_pt

## ----------------------- Print out the data ---------------------- ##

for i in range(nimg):
  
  print '# Image %s' % i

  for j in range(nvar):

    # Check angle vars are: -180 < theta < 180
    theta = new_string[i,j]
    while (theta > 180):
      theta -= 360
    while (theta < -180):
      theta += 360

    print theta

#    print new_string[i, j]
