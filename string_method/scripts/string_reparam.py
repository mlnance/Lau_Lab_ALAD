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

nimg_old = count / nvar
pts.resize(nimg_old, nvar)
# we now may have cases where we are getting strings that
# are smaller than the number of images we told it we want
#pts.resize(nimg, nvar)

#print pts

## ------------------ Compute Gradient/String Length --------------- ##

slength = np.zeros(nimg_old)                  # String Length
grad = np.zeros((nimg_old-1, nvar))           # FD between img (n+1, n)

# Projection parameters
for i in range(nimg_old-1):

#  diff_v = pts[i + 1, :] - pts[i,:]
  diff_v = np.zeros(nvar)

  # Take care of angle variables
  for j in range(nvar):
    
    if j < ang_var:
      # the differences between image i+1 and image i
      diff_v[j] = pts[i+1, j] - pts[i, j]
    else:
      diff_v[j] = adiff( pts[i+1,j] ,pts[i,j] ) 

  # magnitude of the difference vector
  # equivalent to math.sqrt(sum(i**2 for i in diff_v))
  dist = np.linalg.norm(diff_v)

  grad[i, :] = diff_v / dist
  # the distance between image i and image i+1 of the whole string
  slength[i+1] = slength[i] + dist

## -------------------- Reparametrize the string ------------------- ##

# the average distance between each image in the string
# slength[-1] is the total length of the string
# there are nimg - 1 lines connecting nimg images
img_dist   = slength[-1] / float(nimg - 1)
new_string = np.zeros(nimg * nvar)
new_string.resize( nimg, nvar )
# the new string is now not a copy of the old string
# because we may want more images than we started with
# so we need to create a fresh new_string variable
#new_string = np.copy(pts)

#print "Gradient"
#print grad
#print "slength"
#print slength
#print 

for i in range(nimg):

  tot_dist = img_dist * i
  
  # First and last points, Project 0 distance.
  #   Careful - Floating Point rounding errors
  if tot_dist == 0:
    # first point
    start_pt = pts[i,:]
    new_pt = start_pt                       
  elif round(tot_dist, 5) == round(slength[-1], 5):
    # last point
    start_pt = pts[-1,:]
    new_pt = start_pt

#    print tot_dist
#    print 'ITER = %s' %i
#    print 'START_PT = %s, NEW_PT = %s \n' %(start_pt, new_pt)

  else:
    # the link point is the point that is a good starting point to
    # use to make a new point along the string in an ideal fashion
    # it is the point chosen to then move along its gradient to
    # the next point
    # it's found by having the actual point of a string (meaning
    # how far you've gone down the string distance wise) and comparing
    # it to how far an ideal string would be by this same image point
    link = np.searchsorted(slength, tot_dist) - 1    # nth link of string

#    print tot_dist
#    print 'ITER = %s LINK = %s' % (i, link)
   
    # Compute the new points
    start_pt = pts[link]
    # gradient is the slope connecting the link point
    # and the point following the link
    # this is the line on which you would take the link point
    # move it along the gradient to some point where
    # the ideal point would fall
    gradient  = grad[link, :]
    # this is how far you need to move the link point along the
    # gradient to get the point of the string on which the ideal
    # image of this image number would sit
    proj_dist = tot_dist - slength[link]

    # your new point is the starting point that is projected along
    # the gradient connecting this point and the following point in
    # the string as far as determined by the proj_dist
    # this ensures your new string looks like your old string,
    # but the images (points) along the string are separated in
    # an equidistant fashion (the avg dist between the starting images)
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


