'''
Created on Sep 29, 2014

@author: fran_re
'''
import math














def createLineFunction(p1,p2):
    # m = (y2-y1) / (x2-x1) ;;; b = y2 - m-x2 
    m = ( p2[1] - p1[1] ) / ( p2[0] - p1[0] )
    b = p2[1] - m * p2[0]
    
    return lambda x : m * x + b

'''
@param p1: start of line
@param p2: end of line
@param p3: normal goes through this point
'''
def createPerpendicular(p1, p2, p3):
    m = ( p2[1] - p1[1] ) / ( p2[0] - p1[0] )
    m_per = -1/m
    b = p3[1] - m_per * p3[0]
    
    return lambda x : m_per * x + b

def createPerpendicular2(p1, p2, p3):
    m = ( p2[1] - p1[1] ) / ( p2[0] - p1[0] )
    b = p3[1] - m * p3[0]
    
    return lambda x : m * x + b

def getIntersectionPoint(m1, b1, m2, b2):
    m = m1 - m2
    b = b2 - b1
    x = b / m
    y = m1 * x + b1
    return [x,y,1]

'''
@param p1: first point
@param p2: second point
@return: distance between p1 and p2 
'''    
def getDistanceBtwPoints(p1, p2):
    x = p1[0] - p2[0] 
    y = p1[1] - p2[1] 
    z = p1[2] - p2[2] 
    return math.sqrt(x*x + y*y + z*z)





l = [1,-4,0]
t = [4,3,0]

res = createLineFunction(l, t)
res2 = createPerpendicular2(l,t,[1.3,0])
print res(0)
print res2(0)

print getIntersection(-3,3,3,-9)