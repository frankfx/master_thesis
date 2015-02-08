'''
Created on Oct 9, 2014

@author: rene
'''

from Xtest.Open_GL.utils.chaikinSpline import Chaikin
from Xtest.Open_GL.utils.bSpline import BSplineCurve

class Profile(object):
    """This is the parent class for all specific profiles (airfoil, fuselage).

    Attributes:
      pointList (list of 3dim float lists): contains the profile points.
      name (str): name of the profile given by uID.

    """    
    def __init__(self, uid, tigl, plist, parent = None):    
        self.name      = uid
        self.pointList = plist

        self.__tigl = tigl
        
    def setPointList(self, plist):
        self.pointList = plist

    def setName(self, name):
        self.name = name

    def getPointList(self):
        return self.pointList

    def getName(self):
        return self.name

    def getLength(self):
        """Abstract method which should be implemented by the childs.

        Returns:
          NotImplemented.

        """        
        return NotImplemented
 
    def computeChaikinSplineCurve(self):
        """returns the point list as chaikin spline """           
        spline = Chaikin(self.pointList)
        spline.IncreaseLod()
        spline.IncreaseLod()
        return spline.getPointList()

    def computeBSplineCurve(self):
        """returns the point list as b-spline"""
        spline = BSplineCurve(self.name ,self.__tigl)
        return spline.getPointList()

    def __str__(self):
        return str(self.__name) + " --> " + str(self.pointList)