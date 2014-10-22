'''
Created on Sep 2, 2014

@author: rene
'''
import sys
import utility
from airfoilWidget import AirfoilWidget
from airfoilDetectWidget import AirfoilDetectWidget
from Xtest.Open_GL.airfoilNacaWidget import AirfoilNacaWidget
from PySide import QtGui, QtCore

class AirfoilMainWidget(QtGui.QWidget):
    def __init__(self, profile, parent = None):
        super(AirfoilMainWidget, self).__init__(parent)

        self.ogl_widget          = AirfoilWidget(profile)
        self.ogl_widget_naca     = AirfoilNacaWidget(self.ogl_widget) 
        self.ogl_widget_detector = AirfoilDetectWidget(self.ogl_widget)
       
        self.ogl_widget_naca.naca4.butCreate.clicked.connect(self.updateEvalList)
        self.ogl_widget_naca.naca5.butCreate.clicked.connect(self.updateEvalList)
        self.ogl_widget_detector.butCreate.clicked.connect(self.updateEvalList)
        
        grid = QtGui.QGridLayout()        
        grid.addLayout(self.createTopOfWidget(),0,1)
        grid.addWidget(self.ogl_widget, 1,1)

        self.updateEvalList()
        self.setLayout(grid)
        self.setWindowTitle('Airfoil-Widget')   
        self.resize(560,520)              
        #self.setFixedSize(QtCore.QSize(400,400))
        self.show()
    
    def createTopOfWidget(self):
        vboxLayout = QtGui.QVBoxLayout()
        vboxLayout.addWidget(self.createEvalView())
        vboxLayout.addWidget(self.createViewElements())    
        return vboxLayout
        
    def createEvalView(self):
        groupEval = QtGui.QGroupBox("Evaluation")
        gridEval  = QtGui.QGridLayout()
        
        labelName          = QtGui.QLabel("Name")
        labelLength        = QtGui.QLabel("Length")
        labelAngle         = QtGui.QLabel("Angle of attack")
        labelThickness     = QtGui.QLabel("Thickness")
        labelCamber        = QtGui.QLabel("Arch")
        self.textName      = QtGui.QLineEdit()
        self.textLength    = QtGui.QLineEdit()
        self.textAngle     = QtGui.QLineEdit()
        self.textThickness = QtGui.QLineEdit()
        self.textCamber    = QtGui.QLineEdit()
        
        gridEval.addWidget(labelName         , 0, 0)
        gridEval.addWidget(labelLength       , 1, 0)
        gridEval.addWidget(labelAngle        , 2, 0)
        gridEval.addWidget(labelThickness    , 0, 3)
        gridEval.addWidget(labelCamber       , 1, 3)
        gridEval.addWidget(self.textName     , 0, 1)
        gridEval.addWidget(self.textLength   , 1, 1)
        gridEval.addWidget(self.textAngle    , 2, 1)
        gridEval.addWidget(self.textThickness, 0, 4)
        gridEval.addWidget(self.textCamber   , 1, 4)
        
        self.textName.setReadOnly(True)
        self.textLength.setReadOnly(True)
        self.textAngle.setReadOnly(True)
        self.textThickness.setReadOnly(True)
        self.textCamber.setReadOnly(True)

        groupEval.setLayout(gridEval) 
        return groupEval    
        
    def createViewElements(self):    
        groupView  = QtGui.QGroupBox("View") 
        gridView    = QtGui.QGridLayout()  
        
        checkShowPoints        = QtGui.QCheckBox("Show points")
        checkFitToPage         = QtGui.QCheckBox("Fit to page")
        checkCloseTrailingedge = QtGui.QCheckBox("Close Trailing edge")
        checkChaikinCurve      = QtGui.QCheckBox("Chaikin curve")
        checkBSpline           = QtGui.QCheckBox("B-Spline")
        checkDrawCamber        = QtGui.QCheckBox("Camber")
        checkDrawChord         = QtGui.QCheckBox("Chord")
        
        self.butNaca      = QtGui.QPushButton("NacaCreator")
        self.butImgDetect = QtGui.QPushButton("ImgDetect")
        
        labelSpin_rot  = QtGui.QLabel("Rotation")
        labelSpin_zoom = QtGui.QLabel("Zoom")
        
        self.spin_rot = QtGui.QDoubleSpinBox() 
        self.spin_rot.setRange(-45,45)
        self.spin_rot.valueChanged.connect(self.fireSetRotValue)        
        
        self.spin_zoom = QtGui.QSpinBox()
        self.spin_zoom.setRange(1, 100)
        self.spin_zoom.setSingleStep(5)
        self.spin_zoom.setSuffix('%')
        self.spin_zoom.setValue(50)        
        
        gridView.addWidget(checkDrawChord        , 1, 0)
        gridView.addWidget(checkDrawCamber       , 2, 0)
        gridView.addWidget(checkCloseTrailingedge, 3, 0)        
        gridView.addWidget(checkChaikinCurve     , 1, 1)                
        gridView.addWidget(checkShowPoints       , 2, 1)
        gridView.addWidget(checkFitToPage        , 3, 1)
        gridView.addWidget(self.spin_zoom        , 1, 2)
        gridView.addWidget(self.spin_rot         , 2, 2)
        gridView.addWidget(labelSpin_zoom        , 1, 3)
        gridView.addWidget(labelSpin_rot         , 2, 3)         
        gridView.addWidget(self.butNaca          , 1, 4)
        gridView.addWidget(self.butImgDetect     , 2, 4)  
        gridView.addWidget(checkBSpline          , 3, 4) 
         
         
        checkShowPoints.toggled.connect(self.fireShowPoints)
        checkFitToPage.toggled.connect(self.fireFitToPage)
        checkCloseTrailingedge.toggled.connect(self.fireCloseTrailingEdge)
        checkChaikinCurve.toggled.connect(self.fireSplineCurve)
        checkBSpline.toggled.connect(self.fireBSpline)
        checkDrawCamber.toggled.connect(self.fireDrawCamber)
        checkDrawChord.toggled.connect(self.fireDrawChord)

        self.spin_zoom.valueChanged[int].connect(self.fireScaleProfile)
        
        self.butNaca.clicked.connect(self.fireNacaWidget)
        self.butImgDetect.clicked.connect(self.fireDetectWidget)    
    
        groupView.setLayout(gridView)     
        return groupView
    
    def updateEvalList(self):      
        self.textName.setText(self.ogl_widget.profile.getName())
        self.textLength.setText(str(self.ogl_widget.profile.getLenChord()))
        self.textAngle.setText(str(self.ogl_widget.profile.getWorkAngle()))
        self.textThickness.setText(str(self.ogl_widget.profile.getAirfoilThickness()))
        self.textCamber.setText(str(self.ogl_widget.profile.getAirfoilArch()))

    def fireSetRotValue(self, value):
        self.ogl_widget.setRotAngle(value)
        self.updateEvalList()
        self.ogl_widget.updateGL()  
   
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
    
    def fireCloseTrailingEdge(self, value):
        self.ogl_widget.setFlagCloseTrailingEdge(value)
        self.ogl_widget.updateGL()
    
    def fireSplineCurve(self, value):
        self.ogl_widget.setFlagChaikinSpline(value)
        self.ogl_widget.updateGL()
        
    def fireBSpline(self, value):
        self.ogl_widget.setFlagBSpline(value)
        self.ogl_widget.updateGL()
    
    def fireDrawCamber(self, value):
        self.ogl_widget.setFlagDrawCamber(value)
        self.ogl_widget.updateGL()
        
    def fireDrawChord(self, value):    
        self.ogl_widget.setFlagDrawChord(value)
        self.ogl_widget.updateGL()
    
    def fireNacaWidget(self):
        self.ogl_widget_naca.show()

    def fireDetectWidget(self):
        self.ogl_widget_detector.show()

    def closeEvent(self, event):
        self.ogl_widget_naca.close()
        self.ogl_widget_detector.close()
        event.accept() # let the window close


