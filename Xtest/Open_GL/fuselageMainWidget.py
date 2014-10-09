'''
Created on Oct 8, 2014

@author: fran_re
'''

from fuselageWidget import FuselageWidget
from PySide import QtGui, QtCore


class FuselageMainWidget(QtGui.QWidget):
    def __init__(self, profile, parent = None):
        super(FuselageMainWidget, self).__init__(parent)

        self.ogl_widget = FuselageWidget(profile)

        grid = QtGui.QGridLayout() 
        grid.addWidget(self.createViewElements(), 0,0)       
        grid.addWidget(self.ogl_widget,1,0)
        
        self.setLayout(grid)
        self.setWindowTitle('Airfoil-Widget')    
        self.resize(560,520)
        self.show()    
 
    def createViewElements(self):    
        groupView = QtGui.QGroupBox("View") 
        gridView  = QtGui.QGridLayout()  

        labelSpin_zoom = QtGui.QLabel("Zoom")
        
        checkShowPoints   = QtGui.QCheckBox("Show points")
        checkFitToPage    = QtGui.QCheckBox("Fit to page")
        checkChaikinCurve = QtGui.QCheckBox("Chaikin curve ")
        
        self.spin_zoom = QtGui.QSpinBox()
        self.spin_zoom.setRange(1, 100)
        self.spin_zoom.setSingleStep(5)
        self.spin_zoom.setSuffix('%')
        self.spin_zoom.setValue(50)        
        
        gridView.addWidget(checkChaikinCurve, 0, 0)                
        gridView.addWidget(checkShowPoints  , 0, 1)
        gridView.addWidget(checkFitToPage   , 0, 2)
        gridView.addWidget(self.spin_zoom   , 1, 0)
        gridView.addWidget(labelSpin_zoom   , 1, 1)

        checkShowPoints.toggled.connect(self.fireShowPoints)
        checkFitToPage.toggled.connect(self.fireFitToPage)
        checkChaikinCurve.toggled.connect(self.fireChaikinCurve)
        self.spin_zoom.valueChanged[int].connect(self.fireScaleProfile) 
        
        groupView.setLayout(gridView)     
        return groupView

    def fireScaleProfile(self, value):
        self.ogl_widget.setScale(value)
        self.ogl_widget.updateGL()

    def fireShowPoints(self, value):
        self.ogl_widget.setDrawPointsOption(value)   
        self.ogl_widget.updateGL()

    def fireFitToPage(self, value):
        if value:
            self.spin_zoom.setValue(51)
            self.spin_zoom.setEnabled(False)
        else:
            self.spin_zoom.setEnabled(True)
        self.ogl_widget.fitToPage(value)  
        self.ogl_widget.updateGL()
    
    def fireChaikinCurve(self, value):
        self.ogl_widget.setFlagSplineCurve(value)
        self.ogl_widget.updateGL()
