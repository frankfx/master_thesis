'''
Created on Jul 29, 2014

@author: fran_re
'''
class ShapeNames:
    dict = {0:"dreieck", 1:"viereck", 2:"stern"}
       
    def getKey(self, key):
        return self.dict.get(key)
    
    def getValue(self, value):
        try:
            return self.dict.keys()[self.dict.values().index(value)]
        except ValueError:
            return None

#print ShapeNames.values.get(0)
#print ShapeNames.values.keys()[ShapeNames.values.values().index("dreieck")]

s = ShapeNames()
print ShapeNames().getKey(24)
print ShapeNames().getValue("dreizeck")
