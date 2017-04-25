#!/usr/bin/python
__author__="morganlnance"


'''
Usage:

Take each image along a string, in sequence
Calculate the distance between each image
Ex) distance of 2 from 1 and 3, 5 from 4 and 6
Determine each image's nearest neighbors
Is image 4 closest to 3 and 5?
Or is it closest to 3 and 9?
If the latter is true, there is a knot
Then connect each image in terms of its nearest neighbors
If a knot is present, connect that image to its highest
nearest neighbor image number
This is how image numbers will be taken out of a string
'''
