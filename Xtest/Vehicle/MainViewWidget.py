'''
Created on Feb 4, 2015

@author: rene
'''
from PySide import QtGui, QtCore

from Xtest.Vehicle.vehicleData import VehicleData
from Xtest.Vehicle.Views.frontViewOGL import FrontViewWidget
from Xtest.Vehicle.Views.sideViewGL import SideViewGL
from Xtest.Vehicle.Views.threeDViewOGL import ThreeDViewOGL
from Xtest.Vehicle.Views.topViewOGL import TopViewWidget

class MainWidget(QtGui.QMainWindow):
    def __init__(self, tixi, tigl, parent = None):
        super(MainWidget, self).__init__(parent)    
        
        # data points
        self.data = VehicleData(tixi, tigl)
        
        self.plotWidgets = [FrontViewWidget("Front", tixi, tigl, self.data), SideViewGL("Side", tixi, tigl, self.data),
                            TopViewWidget("Top", tixi, tigl, self.data), ThreeDViewOGL("3D", tixi, tigl, self.data)]

        self.dockList = []
        
        for widget in self.plotWidgets :
            self.addSimpleWidget(widget.getTitle(), widget)

    def addSimpleWidget(self, name, widget):
        dock = QtGui.QDockWidget(name)
        dock.setWidget(widget)
        dock.setMinimumHeight(150)
        
        dock.setAllowedAreas(QtCore.Qt.AllDockWidgetAreas)
        dock.setFeatures(QtGui.QDockWidget.DockWidgetClosable |
                         QtGui.QDockWidget.DockWidgetMovable |
                         QtGui.QDockWidget.DockWidgetFloatable)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dock)
        
    def updateView(self):
        self.data.updateTixiTiglData()
        for plotWidget in self.plotWidgets :
            plotWidget.renderer.updateLists(self.data)
            
            