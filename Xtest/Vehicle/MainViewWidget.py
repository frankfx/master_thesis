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




import sys
from PySide import QtOpenGL, QtGui, QtCore

from Xtest.Vehicle.selectionList import SelectionList
from Xtest.Plotting import plotWidget

try:
    from OpenGL import GL
except ImportError:
    app = QtGui.QApplication(sys.argv)
    QtGui.QMessageBox.critical(None, "OpenGL hellogl",
                              "PyOpenGL must be installed to run this example.",
                            QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default,
                            QtGui.QMessageBox.NoButton)
    sys.exit(1)


class MainWidget(QtGui.QMainWindow):
    def __init__(self, tixi, tigl, parent = None):
        super(MainWidget, self).__init__(parent)    
        
        # data points
        self.data = VehicleData(tixi, tigl)
        
        front = FrontViewWidget("Front", tixi, tigl, self.data)
        side  = SideViewGL("Front", tixi, tigl, self.data)
        top   = TopViewWidget("Top", tixi, tigl, self.data)
        three = ThreeDViewOGL("3D", tixi, tigl, self.data)

        self.plotWidgets = [front, side, three, top]
        # 
        self.plotWidgets[0].renderer.indexGenerated.triggered.connect(self.setRenderContext)

        for widget in self.plotWidgets :
            self.addSimpleWidget(widget.getTitle(), widget)
          
    def setRenderContext(self):
        idx = self.plotWidgets[0].renderer.getRenderIndex()
        self.plotWidgets[1].renderer.setRenderIndex(idx)
        self.plotWidgets[2].renderer.setRenderIndex(idx)
        self.plotWidgets[3].renderer.setRenderIndex(idx)
    

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
            plotWidget.renderer.update()
            