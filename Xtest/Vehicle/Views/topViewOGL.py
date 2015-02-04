'''
Created on Jul 30, 2014

@author: fran_re
'''
from Xtest.Vehicle.Views.widget import Widget
    
class TopViewWidget(Widget):
    def __init__(self,name, tixi, tigl, data, parent = None):
        super(TopViewWidget, self).__init__(name, tixi, tigl, data, parent)
        self.setTopView()
