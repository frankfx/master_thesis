'''
Created on Sep 23, 2014

@author: fran_re
'''


# ------------------------------------------------------------
# file    Main.cpp
# author  Rob Bateman
# date    9-feb-2005
# brief   The Chaikin curve is one of the simplest subdivison
#         curves around. It uses a very simple ratio method
#         to determine the new points on the curve. It can be
#         shown mathmatically that this curve is the same as
#         a quadratic b-spline.
# ------------------------------------------------------------

''' a strcture to hold a curve point'''
class Point :
    # ctor
    def __init__(self, a=0, b=0, c=0):
        # the position
        self.x = a
        self.y = b
        self.z = c
        
    # copy ctor
    @classmethod
    def copyPoint(cls, point):
        return cls(point.x, point.y, point.z)       
        
    def __str__(self):
        return "Point(" + str(self.x) + ", " + str(self.y) + ", " + str(self.z) + ")" 



''' a dynamic array of all points in the curve'''
class Chaikin:
    # ctor
    def __init__(self, plist):
        self.pList = plist   
        self.incCount = 0

    @classmethod
    def initPLists(cls, plistX, plistY, pListZ):
        res = []
        for i in range(0, len(plistX), 1) :
            res.append(Point(plistX[i], plistY[i], pListZ[i]-0.5))
        return cls(res) 

# ------------------------------------------------------------    IncreaseLod()
# When we increase the LOD we will have to re-create the points
# array inserting the new intermediate points into it.
#
#    Basically the subdivision works like this. each line,
#
#            A  *------------*  B
#
#    will be split into 2 new points, Q and R.
#
#                   Q    R
#            A  *---|----|---*  B
#
#    Q and R are given by the equations :
#
#         Q = 3/4*A + 1/4*B
#         R = 3/4*B + 1/4*A
#

    def IncreaseLod(self) : 
        if self.incCount > 3 :
            return
        new_pList = []
        len_pList = len(self.pList)

        #keep the first point
        new_pList.append(self.pList[0])
        for i in range(0, len_pList-1) :
        
            # get 2 original points
            p0 = self.pList[i]
            p1 = self.pList[i+1]
            Q = Point()
            R = Point()
    
            # average the 2 original points to create 2 new points. For each
            # CV, another 2 verts are created.
            Q.x = 0.75 * p0.x + 0.25 * p1.x
            Q.y = 0.75 * p0.y + 0.25 * p1.y
            Q.z = 0.75 * p0.z + 0.25 * p1.z
    
            R.x = 0.25 * p0.x + 0.75 * p1.x
            R.y = 0.25 * p0.y + 0.75 * p1.y
            R.z = 0.25 * p0.z + 0.75 * p1.z

            new_pList.append(Q)
            new_pList.append(R)

        new_pList.append(self.pList[len_pList-1])

        self.echo( self.pList)
        self.echo( new_pList)

        # update the points array
        self.pList = new_pList
        self.incCount += 1

# ------------------------------------------------------------    DecreaseLod()
# When we decrease the LOD, we can rather niftily get back
# to exactly what we had before. Since the original subdivision
# simply required a basic ratio of both points, we can simply
# reverse the ratio's to get the previous point...
#
    def DecreaseLod(self) :
        len_pList = len(self.pList)

        # make sure we dont loose any points!!
        if len_pList <= 4 : 
            return

        new_pList = []

        # keep the first point
        new_pList.append(self.pList[0])

        # step over every 2 points
        for i in range(1, len_pList-1, 2) :
            # get last point found in reduced array
            pLast = new_pList[len(new_pList)-1]

            # get 2 original point
            p0 = self.pList[i]
            Q = Point()

            # calculate the original point
            Q.x = p0.x - 0.75 * pLast.x
            Q.y = p0.y - 0.75 * pLast.y
            Q.z = p0.z - 0.75 * pLast.z

            Q.x *= 4.0
            Q.y *= 4.0
            Q.z *= 4.0

            #add to new curve
            new_pList.append(Q)

        self.echo( self.pList)
        self.echo( new_pList)
        # copy over points
        self.pList = new_pList


    def getPointList(self):
        return self.pList

    def __str__(self):
        return self.pList

    def echo(self, plist):
        s = ""
        for p in plist:
            s = s + str(p) + ", "
        print s


if __name__ == '__main__':
    p = Point(1)
    c = Point.copyPoint(p)
    print p
    print c 





