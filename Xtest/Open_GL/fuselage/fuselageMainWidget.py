'''
Created on Oct 8, 2014

@author: fran_re
'''

from Xtest.Open_GL.Renderer.fuseRenderer import FuseRenderer
from Xtest.Open_GL.fuselage.fuselageGeneratorWidget import FuselageGeneratorWidget

from PySide import QtGui, QtCore


class FuselageMainWidget(QtGui.QWidget):
    def __init__(self, profile, parent = None):
        super(FuselageMainWidget, self).__init__(parent)

        self.ogl_widget = FuseRenderer(profile)
        self.superEllipse_widget = FuselageGeneratorWidget()

        self.superEllipse_widget.widget1.btnCreate.clicked.connect(self.createSuperEllipse)
        
        grid = QtGui.QGridLayout() 
        grid.addWidget(self.createViewElements(), 0,0)       
        grid.addWidget(self.ogl_widget,1,0)
        
        self.setLayout(grid)
        self.setWindowTitle('Fuselage-Widget')    
        self.resize(560,520)
        self.show()    
 
    def createSuperEllipse(self):
        topSide, botSide, profName = self.superEllipse_widget.widget1.getSuperEllipseParameter()
        self.ogl_widget.createSuperEllipse(topSide, botSide)
        self.ogl_widget.profile.setName(profName)        
 
    def createViewElements(self):    
        groupView = QtGui.QGroupBox("View") 
        gridView  = QtGui.QGridLayout()  

        labelSpin_zoom = QtGui.QLabel("Zoom")
        
        checkShowPoints   = QtGui.QCheckBox("Show points")
        checkFitToPage    = QtGui.QCheckBox("Fit to page")
        checkSplineCurve = QtGui.QCheckBox("B-Spline")
    
        self.xSlider = self.createSlider(QtCore.SIGNAL("xRotationChanged(int)"),
                                         self.ogl_widget.setXRotation)
        self.ySlider = self.createSlider(QtCore.SIGNAL("yRotationChanged(int)"),
                                         self.ogl_widget.setYRotation)
        self.zSlider = self.createSlider(QtCore.SIGNAL("zRotationChanged(int)"),
                                         self.ogl_widget.setZRotation)    
    
        
        butGenerator = QtGui.QPushButton("SuperEllipse")
        
        self.spin_zoom = QtGui.QSpinBox()
        self.spin_zoom.setRange(1, 100)
        self.spin_zoom.setSingleStep(5)
        self.spin_zoom.setSuffix('%')
        self.spin_zoom.setValue(50)        
        
        gridView.addWidget(checkSplineCurve, 0, 0)                
        gridView.addWidget(checkShowPoints  , 0, 1)
        gridView.addWidget(checkFitToPage   , 0, 2)
        gridView.addWidget(self.spin_zoom   , 1, 0)
        gridView.addWidget(labelSpin_zoom   , 1, 1)
        gridView.addWidget(self.xSlider     , 2, 0)
        gridView.addWidget(self.ySlider     , 2, 1)
        gridView.addWidget(self.zSlider     , 2, 2)
        gridView.addWidget(butGenerator, 3, 2)

        butGenerator.clicked.connect(self.fireSuperEllipseWidget)
        checkShowPoints.toggled.connect(self.fireShowPoints)
        checkFitToPage.toggled.connect(self.fireFitToPage)
        checkSplineCurve.toggled.connect(self.fireSplineCurve)
        self.spin_zoom.valueChanged[int].connect(self.fireScaleProfile) 
        
        groupView.setLayout(gridView)     
        return groupView

    def createSlider(self, changedSignal, setterSlot):
        slider = QtGui.QSlider(QtCore.Qt.Horizontal)

        slider.setRange(0, 360 * 2)
        slider.setSingleStep(2)
        slider.setPageStep(15 * 2)
        slider.setTickInterval(15 * 2)
        slider.setTickPosition(QtGui.QSlider.TicksRight)

        self.ogl_widget.connect(slider, QtCore.SIGNAL("valueChanged(int)"), setterSlot)
        self.connect(self.ogl_widget, changedSignal, slider, QtCore.SLOT("setValue(int)"))

        return slider

    def fireSuperEllipseWidget(self):
        self.superEllipse_widget.show()

    def fireScaleProfile(self, value):
        self.ogl_widget.setScale(value)
        self.ogl_widget.updateGL()

    def fireShowPoints(self, value):
        self.ogl_widget.setFlagDrawPoints(value)   
        self.ogl_widget.updateGL()

    def fireFitToPage(self, value):
        if value:
            self.spin_zoom.setValue(51)
            self.spin_zoom.setEnabled(False)
        else:
            self.spin_zoom.setEnabled(True)
        self.ogl_widget.fitToPage(value)  
        self.ogl_widget.updateGL()
    
    def fireSplineCurve(self, value):
        self.ogl_widget.setFlagBSpline(value)
        self.ogl_widget.updateGL()
