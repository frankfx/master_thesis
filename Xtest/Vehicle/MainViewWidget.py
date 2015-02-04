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
        self.plotWidgets[0].renderer.before_indexGenerated.triggered.connect(self.setRenderContext0)
        self.plotWidgets[1].renderer.before_indexGenerated.triggered.connect(self.setRenderContext1)
        self.plotWidgets[2].renderer.before_indexGenerated.triggered.connect(self.setRenderContext2)
        self.plotWidgets[3].renderer.before_indexGenerated.triggered.connect(self.setRenderContext3)

        for widget in self.plotWidgets :
            self.addSimpleWidget(widget.getTitle(), widget)


    def setRenderContext0(self):
        self.index0 = GL.glGenLists(10)
        print "hier0" , self.index0
        self.plotWidgets[0].renderer.setRenderIndex(self.index0)
            
    def setRenderContext1(self):
        self.index1 = GL.glGenLists(10)
        print "hier1" ,self.index1
        self.plotWidgets[1].renderer.setRenderIndex(self.index1)

    def setRenderContext2(self):
        self.index2 = GL.glGenLists(10)
        print "hier2" ,self.index2
        self.plotWidgets[2].renderer.setRenderIndex(self.index2)
        
    def setRenderContext3(self):
        self.index3 = GL.glGenLists(10)
        print "hier3" ,self.index3
        self.plotWidgets[3].renderer.setRenderIndex(self.index3)            

    #===========================================================================
    # def setRenderContext(self):
    #     idx = self.plotWidgets[0].renderer.getRenderIndex()
    #     print idx
    #     self.plotWidgets[1].renderer.setRenderIndex(idx)
    #     self.plotWidgets[2].renderer.setRenderIndex(idx)
    #     self.plotWidgets[3].renderer.setRenderIndex(idx)
    #===========================================================================
    

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
            print plotWidget.getTitle()
        
        for plotWidget in self.plotWidgets :
            plotWidget.renderer.update()
        
            #break
           # plotWidget.renderer.updateGL()
            
            