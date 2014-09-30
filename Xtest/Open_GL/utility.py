'''
Created on Sep 29, 2014

@author: fran_re
'''

import math

'''
@param p: first point
@param plist: point list 
@return: Point of plist with minimum distance to p
'''  
def computePointWithMinDistance(p, plist):
    dist = -1.0
    pnt = None
    for p1 in plist :
        cur_dist = getDistanceBtwPoints(p, p1)
        if dist < 0.0 or cur_dist < dist :
            dist = cur_dist
            pnt = p1
    return pnt

'''
@param p: first point
@param plist: point list 
@return: Point of plist with minimum distance to p
'''  
def computeIdxOfPointWithMinDistance1(p, plist):
    dist = -1.0
    idx = None
    for i in range(0, len(plist)) :
        cur_dist = getDistanceBtwPoints(p, plist[i])
        if dist < 0.0 or cur_dist < dist :
            dist = cur_dist
            idx = i
    return idx

'''
@param p: first point
@param plist: point list 
@param cnt: count of result values 
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
@return: Point on Line of Points p1 to p2
'''
def computePointOnLine(x, p1, p2):
    fst = p1 if p1[0] <= p2[0] else p2
    snd = p2 if p1[0] <= p2[0] else p1

    # m = (y2-y1) / (x2-x1) ;;; b = y2 - m-x2 
    m = ( snd[1] - fst[1] ) / ( snd[0] - fst[0] )
    b = snd[1] - m * snd[0]

    y = m * x + b
    return [x, y, p1[2]]   
   
'''
@param p1: first point
@param p2: second point
@return: center point of p1 and p2 
'''    
def getCenterPoint(p1, p2):
    return [0.5 * (p1[0] + p2[0]), 0.5 * (p1[1] + p2[1]), 0.5 * (p1[2] + p2[2])]    
    
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
@return: index of searched point 
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
    m = ( p2[1] - p1[1] ) / ( p2[0] - p1[0] )
    if m == 0 :
        return None , p3[0]
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
    for i in range (1, len(plist),1) :
        if plist[id_max][dim] < plist[i][dim] :
            id_max = i
        if plist[id_min][dim] > plist[i][dim] :
            id_min = i
    return plist[id_min], plist[id_max] 


def normalize(plist):
    x_min , x_max = plist[get_min_max_of_List(plist, 0)]
    y_min , y_max = plist[get_min_max_of_List(plist, 1)]
    