'''
Created on Sep 2, 2014

@author: rene
'''
import sys
import math
import utility
from airfoilWidget import AirfoilWidget
from airfoilDetectWidget import AirfoilDetectWidget
from Xtest.Open_GL.airfoilNacaWidget import AirfoilNacaWidget
from PySide import QtGui, QtCore

try:
    from OpenGL import GL
except ImportError:
    app = QtGui.QApplication(sys.argv)
    QtGui.QMessageBox.critical(None, "OpenGL hellogl",
                              "PyOpenGL must be installed to run this example.",
                            QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default,
                            QtGui.QMessageBox.NoButton)
    sys.exit(1)

class AirfoilMainWidget(QtGui.QWidget):
    def __init__(self, plist, parent = None):
        super(AirfoilMainWidget, self).__init__(parent)

        utility.debug('call ProfileWidget__init__')

        grid = QtGui.QGridLayout()
        
        self.ogl_widget          = AirfoilWidget(plist)
        self.ogl_widget_naca     = AirfoilNacaWidget(self.ogl_widget) 
        self.ogl_widget_detector = AirfoilDetectWidget(self.ogl_widget)
       
        self.ogl_widget_naca.naca4.butCreate.clicked.connect(self.updateEvalList)
        self.ogl_widget_naca.naca5.butCreate.clicked.connect(self.updateEvalList)
        self.ogl_widget_detector.butCreate.clicked.connect(self.updateEvalList)
        
        grid.addLayout(self.createTopOfWidget(),0,1)
        grid.addWidget(self.ogl_widget, 1,1)

        self.setLayout(grid)
        self.updateEvalList()
        
        self.setWindowTitle('Airfoil-Widget')    
        self.resize(560,520)
        #self.setFixedSize(QtCore.QSize(400,400))
        self.show()
    
    
    def createTopOfWidget(self):
        vboxLayout  = QtGui.QVBoxLayout()
        vboxLayout.addWidget(self.createEvalView())
        vboxLayout.addWidget(self.createViewingElements())    
        return vboxLayout
        
    def createEvalView(self):
        groupEval    = QtGui.QGroupBox("Evaluation")
        gridEval    = QtGui.QGridLayout()
        
        labelName               = QtGui.QLabel("Name")
        labelLength             = QtGui.QLabel("Length")
        labelAngle              = QtGui.QLabel("Angle of attack")
        labelThickness          = QtGui.QLabel("Thickness")
        labelCamber             = QtGui.QLabel("Arch")
        self.textName           = QtGui.QLineEdit()
        self.textLength         = QtGui.QLineEdit()
        self.textAngle          = QtGui.QLineEdit()
        self.textThickness      = QtGui.QLineEdit()
        self.textCamber         = QtGui.QLineEdit()
        
        gridEval.addWidget(labelName                , 0, 0)
        gridEval.addWidget(labelLength              , 1, 0)
        gridEval.addWidget(labelAngle               , 2, 0)
        gridEval.addWidget(labelThickness           , 0, 3)
        gridEval.addWidget(labelCamber              , 1, 3)
        gridEval.addWidget(self.textName            , 0, 1)
        gridEval.addWidget(self.textLength          , 1, 1)
        gridEval.addWidget(self.textAngle           , 2, 1)
        gridEval.addWidget(self.textThickness       , 0, 4)
        gridEval.addWidget(self.textCamber          , 1, 4)
        
        self.textName.setReadOnly(True)
        self.textLength.setReadOnly(True)
        self.textAngle.setReadOnly(True)
        self.textThickness.setReadOnly(True)
        self.textCamber.setReadOnly(True)

        groupEval.setLayout(gridEval) 
        return groupEval    
        
    def createViewingElements(self):    
        groupView  = QtGui.QGroupBox("View") 
        gridView    = QtGui.QGridLayout()  
        
        checkShowPoints         = QtGui.QCheckBox("Show points")
        checkFitToPage          = QtGui.QCheckBox("Fit to page")
        checkCloseTrailingedge  = QtGui.QCheckBox("Close Trailing edge")
        checkChaikinCurve       = QtGui.QCheckBox("Chaikin curve ")
        checkDrawCamber         = QtGui.QCheckBox("Camber")
        checkDrawChord          = QtGui.QCheckBox("Chord")
        
        self.butNaca            = QtGui.QPushButton("NacaCreator")
        self.butImgDetect       = QtGui.QPushButton("ImgDetect")
        
        labelSpin_rot = QtGui.QLabel("Rotation")
        self.spin_rot = QtGui.QDoubleSpinBox() 
        self.spin_rot.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.spin_rot.setRange(-45,45)
        self.spin_rot.valueChanged.connect(self.fireSetRotValue)        
        
        labelSpin_zoom = QtGui.QLabel("Zoom")        
        self.spin_zoom = QtGui.QSpinBox()
        self.spin_zoom.setRange(1, 100)
        self.spin_zoom.setSingleStep(5)
        self.spin_zoom.setSuffix('%')
        self.spin_zoom.setValue(50)        
        self.spin_zoom.valueChanged[int].connect(self.ogl_widget.setScale) 
        
        gridView.addWidget(checkDrawChord           , 1, 0)
        gridView.addWidget(checkDrawCamber          , 2, 0)
        gridView.addWidget(checkCloseTrailingedge   , 3, 0)        
        gridView.addWidget(checkChaikinCurve        , 1, 1)                
        gridView.addWidget(checkShowPoints          , 2, 1)
        gridView.addWidget(checkFitToPage           , 3, 1)
        gridView.addWidget(self.spin_zoom           , 1, 2)
        gridView.addWidget(self.spin_rot            , 2, 2)
        gridView.addWidget(labelSpin_zoom           , 1, 3)
        gridView.addWidget(labelSpin_rot            , 2, 3)         
        gridView.addWidget(self.butNaca             , 1, 4)
        gridView.addWidget(self.butImgDetect        , 2, 4)  
         
        checkShowPoints.toggled.connect(self.fireShowPoints)
        checkFitToPage.toggled.connect(self.fireFitToPage)
        checkCloseTrailingedge.toggled.connect(self.fireCloseTrailingEdge)
        checkChaikinCurve.toggled.connect(self.fireChaikinCurve)
        checkDrawCamber.toggled.connect(self.fireDrawCamber)
        checkDrawChord.toggled.connect(self.fireDrawChord)

        self.butNaca.clicked.connect(self.fireNacaWidget)
        self.butImgDetect.clicked.connect(self.fireDetectWidget)    
    
        groupView.setLayout(gridView)     
        return groupView
    
    def updateEvalList(self):      
        self.textName.setText(self.ogl_widget.getName())
        self.textLength.setText(str(self.ogl_widget.getLenChord()))
        self.textAngle.setText(str(self.ogl_widget.getWorkAngle()))
        self.textThickness.setText(str(self.ogl_widget.getAirfoilThickness()))
        self.textCamber.setText(str(self.ogl_widget.getAirfoilArch()))

    def fireSetRotValue(self, value):
        self.ogl_widget.setRotate(-value)
        self.updateEvalList()
   
    def fireShowPoints(self, value):
        self.ogl_widget.setDrawPointsOption(value)   

    def fireFitToPage(self, value):
        if value:
            self.spin_zoom.setValue(51) 
            self.spin_zoom.setEnabled(False)
        else:
            self.spin_zoom.setEnabled(True)
        self.ogl_widget.fitToPage(value)  
    
    def fireCloseTrailingEdge(self, value):
        self.ogl_widget.setFlagCloseTrailingEdge(value)
    
    def fireChaikinCurve(self, value):
        self.ogl_widget.setFlagChaikinCurve(value)
    
    def fireDrawCamber(self, value):
        self.ogl_widget.setFlagDrawCamber(value)
        
    def fireDrawChord(self, value):    
        self.ogl_widget.setFlagDrawChord(value)
    
    def fireNacaWidget(self):
        self.ogl_widget_naca.show()

    def fireDetectWidget(self):
        self.ogl_widget_detector.show()

    def closeEvent(self, event):
        self.ogl_widget_naca.close()
        self.ogl_widget_detector.close()
        event.accept() # let the window close


