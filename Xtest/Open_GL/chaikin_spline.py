'''
Created on Sep 23, 2014

@author: fran_re
'''


class Chaikin_Spline:
    def __init__(self, plist):
        self.pList = plist
        self.flag_DecreaseIsPossible = False

    @classmethod
    def initPLists(cls, plistX, plistY, pListZ):
        res = []
        for i in range(0, len(plistX), 1) :
            res.append([plistX[i], plistY[i], pListZ[i]-0.5])
        return cls(res)

# IncreaseLod()
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
        new_pList = []
        len_pList = len(self.pList)

        print "\n\n"
        print self.pList

        #keep the first point
        new_pList.append(self.pList[0])
        for i in range(0, len_pList-1) :

            # get 2 original points
            p0 = self.pList[i]
            p1 = self.pList[i+1]
            Q = [0,0,0]
            R = [0,0,0]

            # average the 2 original points to create 2 new points. For each
            # CV, another 2 verts are created.
            Q[0] = 0.75 * p0[0] + 0.25 * p1[0]
            Q[1] = 0.75 * p0[1] + 0.25 * p1[1]
            Q[2] = 0.75 * p0[2] + 0.25 * p1[2]

            R[0] = 0.25 * p0[0] + 0.75 * p1[0]
            R[1] = 0.25 * p0[1] + 0.75 * p1[1]
            R[2] = 0.25 * p0[2] + 0.75 * p1[2]

            new_pList.append(Q)
            new_pList.append(R)

        #keep the last point
        new_pList.append(self.pList[len_pList-1])

        # update the points array
        self.pList = new_pList
        self.flag_DecreaseIsPossible = True

 # ------------------------------------------------------------    DecreaseLod()
# When we decrease the LOD, we can rather niftily get back
# to exactly what we had before. Since the original subdivision
# simply required a basic ratio of both points, we can simply
# reverse the ratio's to get the previous point...
#
    def DecreaseLod(self) :
        len_pList = len(self.pList)

        # make sure we dont loose any points!!
        if len_pList <= 4 or not self.flag_DecreaseIsPossible :
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
            Q = [0,0,0]

            # calculate the original point
            Q[0] = p0[0] - 0.75 * pLast[0]
            Q[1] = p0[1] - 0.75 * pLast[1]
            Q[2] = p0[2] - 0.75 * pLast[2]

            Q[0] *= 4.0
            Q[1] *= 4.0
            Q[2] *= 4.0

            #add to new curve
            new_pList.append(Q)

        # copy over points
        self.pList = new_pList
        self.flag_DecreaseIsPossible = False

    def getPointList(self):
        return self.pList

    def __str__(self):
        return self.pList

if __name__ == '__main__':
    ()

#--------------------------------------------------------------------------- """
#------------------- A cubic spline interpolation on a given set of points (x,y)
# Recalculates everything on every call which is far from efficient but does the job for now
#--------------------- should eventually be replaced by an external helper class
#--------------------------------------------------------------------------- """
#------------------------------------------- def Interpolate(xa,ya,queryPoints):
    #--------------------------------------------------------- #number of points
    #--------------------------------------------------------------- n = len(xa)
    #----------------------------------------------------------------- u = [0]*n
    #---------------------------------------------------------------- y2 = [0]*n
#------------------------------------------------------------------------------ 
    #----------------------------------------------------------------- u[0] = 0;
    #---------------------------------------------------------------- y2[0] = 0;
#------------------------------------------------------------------------------ 
    #---------------------------------------------------- for i in range(1,n-1):
#------------------------------------------------------------------------------ 
        #-------- # This is the decomposition loop of the tridiagonal algorithm.
        #-- # y2 and u are used for temporary storage of the decomposed factors.
#------------------------------------------------------------------------------ 
        #-------------------------------------------- wx = xa[i + 1] - xa[i - 1]
        #---------------------------------------- sig = (xa[i] - xa[i - 1]) / wx
        #--------------------------------------------- p = sig * y2[i - 1] + 2.0
#------------------------------------------------------------------------------ 
        #----------------------------------------------- y2[i] = (sig - 1.0) / p
#------------------------------------------------------------------------------ 
        # ddydx = (ya[i + 1] - ya[i]) / (xa[i + 1] - xa[i]) - (ya[i] - ya[i - 1]) / (xa[i] - xa[i - 1])
#------------------------------------------------------------------------------ 
        #----------------------- u[i] = (6.0 * ddydx / wx - sig * u[i - 1]) / p;
#------------------------------------------------------------------------------ 
#------------------------------------------------------------------------------ 
    #------------------------------------------------------------ y2[n - 1] = 0;
#------------------------------------------------------------------------------ 
    #---------- # This is the backsubstitution loop of the tridiagonal algorithm
    #------------------------------------------- #((int i = n - 2; i >= 0; --i):
    #------------------------------------------------ for i in range(n-2,-1,-1):
        #------------------------------------- y2[i] = y2[i] * y2[i + 1] + u[i];
#------------------------------------------------------------------------------ 
    #------------ # Interpolate() adapted from Paint Mono which in turn adapted:
    #----------------- # NUMERICAL RECIPES IN C: THE ART OF SCIENTIFIC COMPUTING
    #------------------------------ # ISBN 0-521-43108-5, page 113, section 3.3.
    # # http://paint-mono.googlecode.com/svn/trunk/src/PdnLib/SplineInterpolator.cs
#------------------------------------------------------------------------------ 
    #---------------------------------------------------------- results = [0]*n;
#------------------------------------------------------------------------------ 
    #----------------------------------------------- #loop over all query points
    #----------------------------------------- for i in range(len(queryPoints)):
        #-------------- # bisection. This is optimal if sequential calls to this
        #-------------- # routine are at random values of x. If sequential calls
        #--------------- # are in order, and closely spaced, one would do better
        #----------------- # to store previous values of klo and khi and test if
#------------------------------------------------------------------------------ 
        #-------------------------------------------------------------- klo = 0;
        #---------------------------------------------------------- khi = n - 1;
#------------------------------------------------------------------------------ 
        #------------------------------------------------ while (khi - klo > 1):
            #--------------------------------------------- k = (khi + klo) >> 1;
            #-------------------------------------- if (xa[k] > queryPoints[i]):
                #------------------------------------------------------ khi = k;
            #------------------------------------------------------------- else:
                #------------------------------------------------------ klo = k;
#------------------------------------------------------------------------------ 
        #------------------------------------------------ h = xa[khi] - xa[klo];
        #----------------------------------- a = (xa[khi] - queryPoints[i]) / h;
        #----------------------------------- b = (queryPoints[i] - xa[klo]) / h;
#------------------------------------------------------------------------------ 
        #--------------------------- # Cubic spline polynomial is now evaluated.
        # results[i] = a * ya[klo] + b * ya[khi] + ((a * a * a - a) * y2[klo] + (b * b * b - b) * y2[khi]) * (h * h) / 6.0;
#------------------------------------------------------------------------------ 
    #----------------------------------------------------------- return results;
#------------------------------------------------------------------------------ 
