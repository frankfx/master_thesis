'''
Created on Jan 12, 2015

@author: fran_re
'''

class Point():
    def __init__(self, shaIdx=-1, segIdx=-1, coorinates=[]):
        self.shaIdx = shaIdx
        self.segIdx = segIdx
        self.coordinates = coorinates
    
    def setShapeIdx(self, shaIdx):
        self.shaIdx = shaIdx
        
    def setSegmentIdx(self, segIdx):
        self.segIdx = segIdx   

    def setCoord(self, coorinates):
        self.coordinates = coorinates

    def getShapeIdx(self):
        return self.shaIdx
        
    def getSegmentIdx(self):
        return self.segIdx  
 
    def getCoord(self):
        return self.coordinates
    
    def pointIsInitialized(self):
        return self.segIdx != -1
    
    def  __str__(self):
        return "Shape[" + str(self.shaIdx) + "] . Segment[" + str(self.segIdx) + "]" + " with point " + str(self.coordinates)      
 
