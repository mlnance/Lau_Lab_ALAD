#!/usr/bin/python
__author__="morganlnance"


'''
Used to play with the math and form of the simulated annealing function used in the push_string.oy code
'''


# imports
try:
    import matplotlib
except ImportError:
    print "\nI need matplotlib to work\n"
    sys.exit()
# setting to ensure plot pops up on a Mac
matplotlib.use( "TKAgg" )
import matplotlib.pyplot as plt
plt.rcParams.update( { "font.size" : 14 } )
# simulated annealing math
from math import cos, pi, ceil


# simulated annealing function
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


# calculate simulated annealing data
# period of 25 with the intent of using 100 cycles
# meaning 5 points of no push, 4 points of max push
period = 25
cycles = range( 100 )
multiplier = 1
data = [ multiplier * simulated_annealing( cycle, period ) 
         for cycle in cycles ]


# plot
plt.scatter( cycles, data )
plt.plot( cycles, data, '--' )
plt.xlim( [ 0, len(cycles) ] )
plt.xlabel( "Cycles" )
plt.ylim( [ 0, ceil(max(data)) ] )
plt.ylabel( "Simulated Annealing Push" )
title = "(1/2) * cos( 2*pi * (cycle/period) - pi ) + 1/2"
plt.title( title, fontsize=16, y=1.02 )
plt.show(block=False)
