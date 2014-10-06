'''
Created on Oct 6, 2014

@author: fran_re
'''
import math

c = 1.0
N = 35


for j in range(0,N):
    x = 0.5 * (1.0-math.cos((j * math.pi)/(N-1)))
    print x  
    
    
