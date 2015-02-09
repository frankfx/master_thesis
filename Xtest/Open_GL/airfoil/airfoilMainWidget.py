'''
Created on Sep 2, 2014

@author: rene
'''
from Xtest.Open_GL.Renderer.airfoilRenderer import AirfoilRenderer
from Xtest.Open_GL.airfoil.airfoilDetectWidget import AirfoilDetectWidget
from Xtest.Open_GL.airfoil.airfoilNacaWidget import AirfoilNacaWidget
from PySide import QtGui

class AirfoilMainWidget(QtGui.QWidget):
    def __init__(self, profile, parent = None):
        super(AirfoilMainWidget, self).__init__(parent)

        self.ogl_widget          = AirfoilRenderer(profile)
        self.ogl_widget_naca     = AirfoilNacaWidget(self.ogl_widget) 
        self.ogl_widget_detector = AirfoilDetectWidget(self.ogl_widget)
       
        grid = QtGui.QGridLayout()        
        grid.addLayout(self.createTopOfWidget(),0,1)
        grid.addWidget(self.ogl_widget, 1,1)
        
        # updates the input fields on the top of the widget
        self.updateEvalFields()
        
        self.setWindowTitle('Airfoil-Widget')   
        self.setLayout(grid)
        self.resize(560,520)              
        self.show()

        # actions
        self.ogl_widget_naca.naca4.btnCreate.clicked.connect(self.updateEvalFields)
        self.ogl_widget_naca.naca5.btnCreate.clicked.connect(self.updateEvalFields)
        self.ogl_widget_detector.btnCreate.clicked.connect(self.updateEvalFields)        
    
    def createTopOfWidget(self):
        vboxLayout = QtGui.QVBoxLayout()
        vboxLayout.addWidget(self.createEvalView())
        vboxLayout.addWidget(self.createViewElements())    
        return vboxLayout
        
    def createEvalView(self):
        groupEval = QtGui.QGroupBox("Evaluation")
        
        self.textName      = QtGui.QLineEdit()
        self.textLength    = QtGui.QLineEdit()
        self.textAngle     = QtGui.QLineEdit()
        self.textThickness = QtGui.QLineEdit()
        self.textCamber    = QtGui.QLineEdit()
        
        self.textName.setReadOnly(True)
        self.textLength.setReadOnly(True)
        self.textAngle.setReadOnly(True)
        self.textThickness.setReadOnly(True)
        self.textCamber.setReadOnly(True)        
        
        formLeft = QtGui.QFormLayout()
        formLeft.addRow("Name",   self.textName)
        formLeft.addRow("Length", self.textLength)
        formLeft.addRow("Arch",   self.textCamber)  

        formRight = QtGui.QFormLayout()
        formRight.addRow("Thickness",       self.textThickness)
        formRight.addRow("Angle of attack", self.textAngle)
        
        gridEval  = QtGui.QGridLayout()
        gridEval.addLayout(formLeft, 0,0)
        gridEval.addLayout(formRight, 0,1)
        
        groupEval.setLayout(gridEval) 
        return groupEval    
        
    def createViewElements(self):    
        groupView  = QtGui.QGroupBox("View") 
        
        checkShowPoints        = QtGui.QCheckBox("Show points")
        checkFitToPage         = QtGui.QCheckBox("Fit to page")
        checkCloseTrailingedge = QtGui.QCheckBox("Close Trailing edge")
        checkDrawCamber        = QtGui.QCheckBox("Camber")
        checkDrawChord         = QtGui.QCheckBox("Chord")
        
        comboBoxSpline = QtGui.QComboBox()
        comboBoxSpline.addItem("default")       
        comboBoxSpline.addItem("Chaikin-Spline")
        comboBoxSpline.addItem("B-Spline")

        self.buttonNaca      = QtGui.QPushButton("NacaCreator")
        self.buttonImgDetect = QtGui.QPushButton("ImgageDetect")
        
        self.spin_rot = QtGui.QDoubleSpinBox() 
        self.spin_rot.setRange(-45,45)
        
        self.spin_zoom = QtGui.QSpinBox()
        self.spin_zoom.setRange(1, 100)
        self.spin_zoom.setSingleStep(1)
        self.spin_zoom.setSuffix('%')
        self.spin_zoom.setValue(50)        
        
        gridView = QtGui.QGridLayout()          
        gridView.addWidget(checkDrawChord           , 1, 0)
        gridView.addWidget(checkDrawCamber          , 2, 0)
        gridView.addWidget(checkCloseTrailingedge   , 3, 0)        
        gridView.addWidget(comboBoxSpline           , 1, 1)                
        gridView.addWidget(checkShowPoints          , 2, 1)
        gridView.addWidget(checkFitToPage           , 3, 1)
        gridView.addWidget(self.spin_zoom           , 1, 2)
        gridView.addWidget(self.spin_rot            , 2, 2)
        gridView.addWidget(QtGui.QLabel("Zoom")     , 1, 3)
        gridView.addWidget(QtGui.QLabel("Rotation") , 2, 3)         
        gridView.addWidget(self.buttonNaca          , 1, 4)
        gridView.addWidget(self.buttonImgDetect     , 2, 4)  
         
    
        # actions
        self.spin_rot.valueChanged.connect(self.fireSetRotValue)          
        
        checkShowPoints.toggled.connect(self.fireShowPoints)
        checkFitToPage.toggled.connect(self.fireFitToPage)
        checkCloseTrailingedge.toggled.connect(self.fireCloseTrailingEdge)
        checkDrawCamber.toggled.connect(self.fireDrawCamber)
        checkDrawChord.toggled.connect(self.fireDrawChord)

        comboBoxSpline.activated[str].connect(self.fireActivatedSpline) 

        self.spin_zoom.valueChanged[int].connect(self.fireScaleProfile)
        
        self.buttonNaca.clicked.connect(self.fireNacaWidget)
        self.buttonImgDetect.clicked.connect(self.fireDetectWidget) 
        # end actions
    
        groupView.setLayout(gridView)     
        return groupView
    
    def updateEvalFields(self):      
        self.textName.setText(self.ogl_widget.profile.getName())
        self.textLength.setText(str(self.ogl_widget.profile.getLenChord()))
        self.textAngle.setText(str(self.ogl_widget.profile.getWorkAngle()))
        self.textThickness.setText(str(self.ogl_widget.profile.getAirfoilThickness()))
        self.textCamber.setText(str(self.ogl_widget.profile.getAirfoilArch()))


    def fireSetRotValue(self, value):
        self.ogl_widget.setRotAngle(value)
        self.updateEvalFields()
        self.ogl_widget.updateGL()  
   
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
    
    def fireCloseTrailingEdge(self, value):
        self.ogl_widget.setFlagCloseTrailingEdge(value)
        self.ogl_widget.updateGL()
    
    def fireActivatedSpline(self, value):
        if value == 'B-Spline' :
            self.__setSplineType(True, False)
        elif value == 'Chaikin-Spline' :
            self.__setSplineType(False, True)
        else :
            self.__setSplineType(False, False)
            print ("<airfoilMainWidget> : no spline activated")
        self.ogl_widget.updateGL()
    
    def __setSplineType(self, flagB, flagC):
        self.ogl_widget.setFlagBSpline(flagB)
        self.ogl_widget.setFlagChaikinSpline(flagC)
    
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


