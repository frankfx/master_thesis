'''
Created on Jan 12, 2015

@author: fran_re
'''

class SelectionList():
    def __init__(self):
        self.fuselist  = []
        self.wing_up   = []
        self.wing_lo   = []
        self.wing_up_r = []
        self.wing_lo_r = []
    
    def addPointToFuse(self, p):
        self.fuselist.append(p)

    def addPointToWingUp(self, p):
        self.wing_up.append(p)
        
    def addPointToWingLo(self, p):
        self.wing_lo.append(p)        

    def addPointToWingUpRefl(self, p):
        self.wing_up_r.append(p)
        
    def addPointToWingLoRefl(self, p):
        self.wing_lo_r.append(p) 

    def fuseIsEmpty(self):
        return self.fuselist == []

    def wingUpIsEmpty(self):
        return self.wing_up == []
    
    def wingLoIsEmpty(self):
        return self.wing_lo == []
    
    def wingUpRIsEmpty(self):
        return self.wing_up_r == []
    
    def wingLoRIsEmpty(self):
        return self.wing_lo_r == []       

    def removeAtIndexFuse(self, i):
        del self.fuselist[i]

    def removeAtIndexWingUp(self, i):
        del self.wing_up[i]
        
    def removeAtIndexWingLo(self, i):
        del self.wing_lo[i]
        
    def removeAtIndexWingUpR(self, i):
        del self.wing_up_r[i]
        
    def removeAtIndexWingLoR(self, i):
        del self.wing_lo_r[i]                        

    def isEmpty(self):
        return self.fuseIsEmpty() and self.wingUpIsEmpty() and self.wingLoIsEmpty() \
                                  and self.wingUpRIsEmpty() and self.wingLoRIsEmpty() 
        
    def removeAll(self):
        self.fuselist  = []
        self.wing_up   = []
        self.wing_lo   = []
        self.wing_up_r = []
        self.wing_lo_r = []  


    def  __str__(self):
        return "Shape[" # + str(self.shaIdx) + "] . Segment[" + str(self.segIdx) + "]" + " with point " + str(self.coordinates)      
 
