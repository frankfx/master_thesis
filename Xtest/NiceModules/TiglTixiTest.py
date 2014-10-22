'''
Created on Oct 21, 2014

@author: fran_re
'''
#import tixi-nightly
#from .tigl import tiglExtension, tiglwrapper
from cpacsPy.tixi import tixiwrapper
from cpacsPy.tigl import tiglwrapper
#import tiglwrapper
#import tixiwrapper
class CPACS_Handler():
    
    def __init__ (self):
        self.tixi = tixiwrapper.Tixi()
        self.tigl = tiglwrapper.Tigl()
        
t = CPACS_Handler()
print "c"