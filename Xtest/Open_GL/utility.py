'''
Created on Sep 29, 2014

@author: fran_re
'''

import math

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

'''
@param p: point
@param plist: point list 
@return: Point of plist with minimum distance to p
'''  
def computePointWithMinDistance(p, plist):
    return plist[ computeIdxOfPointWithMinDistance(p, plist)[0] ]

'''
@param p: first point
@param plist: point list 
@param cnt: count of results 
@return: indexes of Points of plist with minimum distance to p, beginning with smallest distance
'''  
def computeIdxOfPointWithMinDistance(p, plist, cnt = 1):
    # idx = list of indexes and there distances
    # idx = [ [i1, i2, i3, ...] , [d1, d2, d3, ...] ]
    idx = [cnt*[-1],cnt*[-1]]
    for i in range(0, len(plist)) :
        cur_dist = getDistanceBtwPoints(p, plist[i])
        for j in range (0, cnt) :
            if idx[1][j] < 0.0 or cur_dist < idx[1][j] :
                idx[1].insert(j, cur_dist)
                idx[0].insert(j, i)
                break
    return idx[0][:cnt]
  
'''
@param x: x-value of result point
@param p1: point one of line (p1, p2)
@param p2: point two of line (p1, p2)
@return: Point on Line (p1, p2)
'''
def computePointOnLine(x, p1, p2):
    # m = (y2-y1) / (x2-x1) ;;; b = y2 - m-x2 
    m = ( p2[1] - p1[1] ) / ( p2[0] - p1[0] )
    b = p2[1] - m * p2[0]

    y = m * x + b
    return [x, y, p1[2]]   
   
'''
@param p1: first point
@param p2: second point
@return: point between p1 and p2 
'''    
def getCenterPoint(p1, p2):
    return [0.5 * (p1[0] + p2[0]), 0.5 * (p1[1] + p2[1]), 0.5 * (p1[2] + p2[2])]    
    
'''
@param p: first point
@param plist: point list 
@return: minimum radius of p in plist
'''  
def computeMinDistance(p, plist):
    dist = -1.0
    for p1 in plist :
        cur_dist = getDistanceBtwPoints(p, p1)
        if dist < 0.0 or cur_dist < dist :
            dist = cur_dist
    return dist
 
'''
@param val: search value
@param plist: point list
@param dim: dimension
@return: index of searched value 
'''     
def searchPointByDimension(val, plist, dim=0):
    i = 0
    for p in plist :
        if p[dim] == val : 
            return i
        i += 1
    return -1       

'''
@param p: search point
@param plist: point list
@return: index of p in plist 
'''      
def searchPoint(p, plist):
    for i in range(0, len(plist)) :
        if plist[i] == p :
            return i
    return -1

'''
@param m1: gradient of first line
@param b1: y-intercept of first line
@param m2: gradient of second line
@param b2: y-intercept of second line
@return: the intersection point of the two lines
'''
def getIntersectionPoint(m1, b1, m2, b2):
    m = m1 - m2
    b = b2 - b1
    x = 0 if m == 0 else b / m
    y = m1 * x + b1
    return [x,y,1]

'''
@param p1: first point of line
@param p2: second point of line
@param p3: line goes through this point p3
@param return: gradient and y-intercept of line
'''
def createLineFunction(p1,p2,p3):
    # m = (y2-y1) / (x2-x1) ;;; b = y2 - m-x2 
    m = ( p2[1] - p1[1] ) / ( p2[0] - p1[0] )
    b = p3[1] - m * p3[0]
    
    return m , b

'''
@param p1: start of line
@param p2: end of line
@param p3: normal goes through this point p3
@return: gradient and y-intercept of line
'''
def createPerpendicular(p1, p2, p3):
    if p2[0] - p1[0] == 0 :
        return (None,"x") , p3[1]
    m = ( p2[1] - p1[1] ) / ( p2[0] - p1[0] )
    if m == 0 :
        return (None,"y") , p3[0]
    m_per = -1/m
    b = p3[1] - m_per * p3[0]
    
    return m_per , b

    '''
@param plist: format [ [x0,y0,z0] , [x1,y1,z1] , ...  ]
@param dim: dimension e.g. 0==x, 1==y, 2==z 
@return: minimum and maximum point compared by dim 
'''
def get_min_max_of_List(plist, dim=0):
    id_max = 0 
    id_min = 0
    for i in range (1, len(plist)) :
        if plist[id_max][dim] < plist[i][dim] :
            id_max = i
        if plist[id_min][dim] > plist[i][dim] :
            id_min = i
    return plist[id_min], plist[id_max] 


def equalFloats(a, b):
    return abs(a - b) <= 10**-9

def equalFloats2(a, b):
    return str(a) == str(b)




plist = [[1.0, 0.00095, 0.0], [0.95, 0.00605, 0.0], [0.9, 0.01086, 0.0], [0.8, 0.01967, 0.0], [0.7, 0.02748, 0.0], [0.6, 0.03423, 0.0], [0.5, 0.03971, 0.0], [0.4, 0.04352, 0.0], [0.3, 0.04501, 0.0], [0.25, 0.04456, 0.0], [0.2, 0.04303, 0.0], [0.15, 0.04009, 0.0], [0.1, 0.03512, 0.0], [0.075, 0.0315, 0.0], [0.05, 0.02666, 0.0], [0.025, 0.01961, 0.0], [0.0125, 0.0142, 0.0], [0.005, 0.0089, 0.0], [0.0, 0.0, 0.0], [0.005, -0.0089, 0.0], [0.0125, -0.0142, 0.0], [0.025, -0.01961, 0.0], [0.05, -0.02666, 0.0], [0.075, -0.0315, 0.0], [0.1, -0.03512, 0.0], [0.15, -0.04009, 0.0], [0.2, -0.04303, 0.0], [0.25, -0.04456, 0.0], [0.3, -0.04501, 0.0], [0.4, -0.04352, 0.0], [0.5, -0.03971, 0.0], [0.6, -0.03423, 0.0], [0.7, -0.02748, 0.0], [0.8, -0.01967, 0.0], [0.9, -0.01086, 0.0], [0.95, -0.00605, 0.0], [1.0, -0.00095, 0.0]]
p = [1.0, 0.00095, 0.0]
assert(computeIdxOfPointWithMinDistance(p, plist, 10) == [0, 36, 1, 35, 2, 34, 3, 33, 4, 32])
assert(computePointWithMinDistance(p, plist) == [1.0, 0.00095, 0.0])