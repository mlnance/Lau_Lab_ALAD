#!/usr/bin/python

# A simple script to reparametrize the string
#  Usage: python string_reparam.py [nvar] [nimg] [fname]

import os, sys, math
import numpy as np

## ------------------------ Helper Functions ----------------------- ##

# Projection
def project(start_point, gradient, dist):
  return start_point + gradient * dist

# Periodicity in Angles 
def adiff(a, b):
  diff = a - b      # Modular Arithmetic: a + b +(m+n)z
  
  # Sign the angle, - 180 < theta < 180
  while abs(diff) > 180:
    if   (diff >   180):
      diff -= 2 * 180
    elif (diff < - 180):
      diff += 2 * 180

  return diff

## ------------------------- Read in the data ---------------------- ##

nvar     = int(sys.argv[1])
nimg     = int(sys.argv[2])
fname    = sys.argv[3]
ang_var  = 14           # Index from 0
uang_var = 17

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

#  diff_v = pts[i + 1, :] - pts[i,:]
  diff_v = np.zeros(nvar)

  # Take care of angle variables
  for j in range(nvar):
    
    if j < ang_var:
      diff_v[j] = pts[i+1, j] - pts[i, j]
    else:
      diff_v[j] = adiff( pts[i+1,j] ,pts[i,j] ) 

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

    start_pt = pts[i,:]
    new_pt = start_pt                       

#    print tot_dist
#    print 'ITER = %s' %i
#    print 'START_PT = %s, NEW_PT = %s \n' %(start_pt, new_pt)

  else:
    link = np.searchsorted(slength, tot_dist) - 1    # nth link of string

#    print tot_dist
#    print 'ITER = %s LINK = %s' % (i, link)
   
    # Compute the new points
    start_pt = pts[link]
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
    if j < ang_var:
      print new_string[i, j]
    elif ang_var <= j and j < uang_var:
      phi = new_string[i,j]

      while abs(phi) > 180:
        if   (phi > 180):
          phi -= 2 * 180
        elif (phi < -180):
          phi += 2 * 180
  
      print phi
    
    else:
      theta = new_string[i,j]

      while abs(theta) > 180:
        if   (theta > 180):
          theta -= 2 * 180
        elif (theta < -180):
          theta += 2 * 180
  
      print abs(theta)


