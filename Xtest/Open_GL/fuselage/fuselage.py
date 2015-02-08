'''
Created on Oct 8, 2014

@author: fran_re
'''
from profile import Profile

class Fuselage(Profile):
    def __init__(self, name, tigl, plist, parent = None):
        super(Fuselage, self).__init__(name, tigl, plist, parent)

    def getLength(self):
        """Implements the abstract method of the parent class 
        
        Returns:
            the length of the profile
        """ 
        return 3.0