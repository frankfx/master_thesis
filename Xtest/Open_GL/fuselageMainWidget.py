'''
Created on Oct 8, 2014

@author: fran_re
'''

from fuselageWidget import FuselageWidget
from PySide import QtGui


class FuselageMainWidget(QtGui.QWidget):
    def __init__(self, plist, parent = None):
        super(FuselageMainWidget, self).__init__(parent)

        grid = QtGui.QGridLayout()
        
        self.ogl_widget = FuselageWidget(plist)
        
        grid.addWidget(self.ogl_widget,1,1)
        self.setLayout(grid)
        self.setWindowTitle('Airfoil-Widget')    
        self.resize(560,520)
        #self.setFixedSize(QtCore.QSize(400,400))
        self.show()    