#!/usr/bin/python

from math import sin, cos

n = 2
coords = {}
num_sins = 0
for ii in range( 1, n+1 ):
    if ii == n:
        coords[ii] = [ sin for jj in range(n-1) ]
    else:
        coords[ii] = [ sin for jj in range(num_sins) ]
        num_sins += 1
        if not ii in coords.keys():
            coords[ii] = [cos]
        else:
            coords[ii].append( cos )
'''
# Image 0
79.5
-55.5
# Image 1
74.663
-50.969
'''
A = 74.663 - 79.5
B = -50.969 - -55.5
dat = [ A, B ]
