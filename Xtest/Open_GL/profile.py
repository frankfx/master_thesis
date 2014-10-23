'''
Created on Oct 9, 2014

@author: rene
'''
from chaikinSpline import Chaikin
from Xtest.Open_GL.bSpline import BSplineCurve

class Profile(object):
    def __init__(self, uid, tigl, plist, parent = None):    
        self.pointList = plist
        self.__name    = uid
        self.__tigl = tigl

    def setPointList(self, plist):
        self.pointList = plist

    def setName(self, value):
        self.__name = value

    def setTigl(self, value):
        self.__tigl = value

    def getPointList(self):
        return self.pointList

    def getName(self):
        return self.__name
    
    def getTigl(self):
        return self.__tigl

    def setPointToPointListAtIdx(self, idx, val):
        self.pointList[idx] = val

    def insertToPointList(self, idx, val):
        self.pointList.insert(idx, val)
    
    def removeFromPointList(self, idx):
        del self.pointList[idx] 

    '''
    @return: chaikin spline of point list
    '''  
    def computeChaikinSplineCurve(self):
        spline = Chaikin(self.pointList)
        spline.IncreaseLod()
        spline.IncreaseLod()
        return spline.getPointList()

    def computeBSplineCurve(self):
        spline = BSplineCurve(self.__name ,self.__tigl)
        return spline.getPointList()

    def __str__(self):
        return str(self.__name) + " --> " + str(self.pointList)