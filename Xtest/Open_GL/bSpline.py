'''
Created on Oct 22, 2014

@author: fran_re
'''

import numpy as np
from Xtest.Open_GL import bspline


class BSpline:
    def __init__(self, uid, tigl):
        self.tigl = tigl
        self.uid = uid
    
    def getSplineList(self):
        res = []
        uid = self.uid
        # get number of curves of the current profile
        ncurves = self.tigl.profileGetBSplineCount(uid)
        
        for icurve in range(ncurves):
            # get size of knot vector and number of control points
            (degree, ncp, nk) = self.tigl.profileGetBSplineDataSizes(uid, icurve+1)
            # now get the data
            (cpx, cpy, cpz, knots) = self.tigl.profileGetBSplineData (uid, icurve+1, ncp, nk)
    
            # and visualize the spline using my b-spline class
            cp = np.vstack([cpx, cpy, cpz])
            kn = np.array(knots)
            
            spline = bspline.BSpline(cp, kn, degree)
            t = np.linspace(kn[0], kn[-1], 1000)
            tmp = spline.eval(t)
            
            res = res + self.__convertToPList(tmp[0], tmp[1], tmp[2])
            
        return res
            
    def __convertToPList(self, xList, yList, zList):
        res = []
        for i in range(len(xList)) :
            res.append([xList[i], yList[i], zList[i]]) 
        return res

