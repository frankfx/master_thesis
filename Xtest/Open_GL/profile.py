'''
Created on Oct 9, 2014

@author: rene
'''

class Profile(object):
    def __init__(self, name, tigl, plist, parent = None):    
        self.pointList = plist
        self.__name      = name
        self.__tigl = tigl

    def setName(self, value):
        self.__name = value

    def setPointList(self, plist):
        self.pointList = plist

    def getName(self):
        return self.__name
    
    def getTigl(self):
        return self.__tigl

    def getPointList(self):
        return self.pointList

    def setPointToPointListAtIdx(self, idx, val):
        self.pointList[idx] = val

    def insertToPointList(self, idx, val):
        self.pointList.insert(idx, val)
    
    def removeFromPointList(self, idx):
        del self.pointList[idx] 

    def __str__(self):
        return str(self.__name) + " --> " + str(self.pointList)