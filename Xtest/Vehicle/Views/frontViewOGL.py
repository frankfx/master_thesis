'''
Created on Jul 30, 2014

@author: fran_re
'''

from Xtest.Vehicle.Views.widget import Widget
from Xtest.Vehicle.Renderer.defaultRenderer import DefaultRenderer    
    
class FrontViewWidget(Widget):
    def __init__(self,name, tixi, tigl, data, parent = None):
        super(FrontViewWidget, self).__init__(name, tixi, tigl, data, parent)
        self.setFrontView()
