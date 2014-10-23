'''
Created on Oct 8, 2014

@author: fran_re
'''
from profile import Profile

class Fuselage(Profile):
    def __init__(self, name, tigl, plist, parent = None):
        super(Fuselage, self).__init__(name, tigl, plist, parent)
