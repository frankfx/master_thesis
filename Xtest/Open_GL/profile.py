'''
Created on Oct 9, 2014

@author: rene
'''

class Profile:
    def __init__(self, name, plist, parent = None):    
        self.__name      = name
        self.__pointList = plist

    def setName(self, value):
        self.__name = value

    def setPointList(self, plist):
        self.__pointList = plist

    def getName(self):
        return self.__name
    
    def getPointList(self):
        return self.__pointList

    def setPointToPointListAtIdx(self, idx, val):
        self.__pointList[idx] = val

    def insertToPointList(self, idx, val):
        self.__pointList.insert(idx, val)
    
    def removeFromPointList(self, idx):
        del self.__pointList[idx] 

    def __str__(self):
        return str(self.__name) + " --> " + str(self.__pointList)