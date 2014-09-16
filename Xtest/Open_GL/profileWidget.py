'''
Created on Sep 2, 2014

@author: rene
'''
from PySide.QtGui import QPushButton
from Xtest.Open_GL import TestSimpleOpenGL
from Xtest.Open_GL import profile_ogl_image_detector
from Xtest.Open_GL import porfile_ogl_view
from Xtest.Open_GL.profile_ogl import Profile
import logging
import datetime
'''
Created on Jul 30, 2014

@author: fran_re
'''
import sys
import math
from PySide import QtOpenGL, QtGui, QtCore

try:
    from OpenGL import GL, GLU, GLUT
except ImportError:
    app = QtGui.QApplication(sys.argv)
    QtGui.QMessageBox.critical(None, "OpenGL hellogl",
                              "PyOpenGL must be installed to run this example.",
                            QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default,
                            QtGui.QMessageBox.NoButton)
    sys.exit(1)

logging.basicConfig(filename='example.log',level=logging.DEBUG)
logging.info('\n#####################################################\nstart\n#####################################################')
logging.info(datetime.datetime.now().time())

class ProfileWidget(QtGui.QWidget):
    def __init__(self, parent = None):
        super(ProfileWidget, self).__init__(parent)

        # ################################################
        logging.debug('call ProfileWidget__init__')
        # ################################################
        
        grid = QtGui.QGridLayout()
        self.ogl_widget          = porfile_ogl_view.MyProfileWidget()
        self.ogl_widget_naca     = NacaWidget(self.ogl_widget) 
        self.ogl_widget_detector = ProfileDetectWidget(self.ogl_widget)
       
        self.ogl_widget_naca.butCreate.clicked.connect(self.updateEvalList)
        self.ogl_widget_detector.butCreate.clicked.connect(self.updateEvalList)
        
        grid.addLayout(self.createEvalView(),0,1)
        grid.addWidget(self.ogl_widget, 1,1)

        self.setLayout(grid)
        
        self.setWindowTitle('Calculator')    
        self.resize(560,520)
        #self.setFixedSize(QtCore.QSize(400,400))
        self.show()
        
        
    def createEvalView(self):
        groupEval    = QtGui.QGroupBox("Evaluation")
        groupDetect   = QtGui.QGroupBox("View")
        
        vboxLayout  = QtGui.QVBoxLayout()
        gridEval    = QtGui.QGridLayout()
        gridView    = QtGui.QGridLayout()
        
        labelName               = QtGui.QLabel("Name")
        labelLength             = QtGui.QLabel("Length")
        labelAngle              = QtGui.QLabel("Angle of attack")
        labelThickness          = QtGui.QLabel("Thickness")
        labelCamber             = QtGui.QLabel("Camber")
        self.textName           = QtGui.QLineEdit()
        self.textLength         = QtGui.QLineEdit()
        self.textAngle          = QtGui.QLineEdit()
        self.textThickness      = QtGui.QLineEdit()
        self.textCamber         = QtGui.QLineEdit()
        checkShowPoints         = QtGui.QCheckBox("Show points")
        checkFitToPage          = QtGui.QCheckBox("Fit to page")
        checkCloseTrailingedge  = QtGui.QCheckBox("Close Trailing edge")
        checkCosineSpacing      = QtGui.QCheckBox("Cosine spacing")
        self.butNaca            = QtGui.QPushButton("NacaCreator")
        self.butImgDetect       = QtGui.QPushButton("ImgDetect")
        self.dial_rot           = QtGui.QDial()
        self.spinBoxRot         = QtGui.QDoubleSpinBox() 
        self.slider_zoom        = QtGui.QSlider(QtCore.Qt.Horizontal, self)        
  
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
        
        gridView.addWidget(self.slider_zoom         , 0, 1,1,2)
        gridView.addWidget(checkShowPoints          , 1, 0)
        gridView.addWidget(checkCloseTrailingedge   , 1, 1)        
        gridView.addWidget(checkFitToPage           , 2, 0)
        gridView.addWidget(checkCosineSpacing       , 2, 1)
        gridView.addWidget(self.spinBoxRot          , 1, 2, 2, 1) 
        
        gridView.addWidget(self.butNaca             , 1, 4)
        gridView.addWidget(self.butImgDetect        , 2, 4)

        self.textName.setReadOnly(True)
        self.textLength.setReadOnly(True)
        self.textAngle.setReadOnly(True)
        self.textThickness.setReadOnly(True)
        self.textCamber.setReadOnly(True)

        self.spinBoxRot.setStyleSheet("QDoubleSpinBox { border: 3px inset grey; } \
            QDoubleSpinBox::up-button { subcontrol-position: left; width: 30px; height: 25px;} \
            QDoubleSpinBox::down-button { subcontrol-position: right; width: 30px; height: 25px;}")
       
        #self.dial_rot.setFocusPolicy(QtCore.Qt.StrongFocus)
        #self.dial_rot.setRange(0,90)
        #self.dial_rot.valueChanged.connect(self.fireSetRotValue)

        self.spinBoxRot.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.spinBoxRot.setRange(0,90)
        self.spinBoxRot.valueChanged.connect(self.fireSetRotValue)

        self.slider_zoom.setMinimum(1)
        self.slider_zoom.setValue(51)
        self.slider_zoom.setFocusPolicy(QtCore.Qt.NoFocus)
        self.slider_zoom.valueChanged[int].connect(self.ogl_widget.slider_zoom) 
        
        checkShowPoints.toggled.connect(self.fireShowPoints)
        checkFitToPage.toggled.connect(self.fireFitToPage)
        checkCloseTrailingedge.toggled.connect(self.fireCloseTrailingEdge)
        checkCosineSpacing.toggled.connect(self.fireCosineSpacing)
        self.butNaca.clicked.connect(self.fireNacaWidget)
        self.butImgDetect.clicked.connect(self.fireDetectWidget)

        groupEval.setLayout(gridEval) 
        groupDetect.setLayout(gridView)     
        
        vboxLayout.addWidget(groupEval)
        vboxLayout.addWidget(groupDetect)    
        
        self.updateEvalList()    
        return vboxLayout
        
    def updateEvalList(self):      
        self.textName.setText(self.ogl_widget.get_name())
        self.textLength.setText(str(self.ogl_widget.get_len_chord()))
        self.textAngle.setText(str(self.ogl_widget.get_work_angle()))
        self.textThickness.setText(str(self.ogl_widget.get_profile_thickness()))
        self.textCamber.setText(str(self.ogl_widget.get_profile_arch()))

    def fireSetRotValue(self, value):
        self.ogl_widget.set_rotate(-value)
        self.updateEvalList() ##### Loeschen!!!!!!!!!!!!
   
    def fireShowPoints(self, value):
        self.ogl_widget.setDrawPointsOption(value)   

    def fireFitToPage(self, value):
        if value:
            self.slider_zoom.setValue(51) 
            self.slider_zoom.setEnabled(False)
        else:
            self.slider_zoom.setEnabled(True)
        self.ogl_widget.fitToPage(value)  
    
    def fireCloseTrailingEdge(self, value):
        self.ogl_widget.setCloseTrailingEdge(value)
    
    def fireCosineSpacing(self, value):
        self.ogl_widget.setCosineSpacing(value)
    
    def fireNacaWidget(self):
        self.ogl_widget_naca.show()

    def fireDetectWidget(self):
        self.ogl_widget_detector.show()

    def closeEvent(self, event):
        self.ogl_widget_naca.close()
        self.ogl_widget_detector.close()
        event.accept() # let the window close

class NacaWidget(QtGui.QWidget):
    def __init__(self, ogl_widget, parent = None):
        super(NacaWidget, self).__init__(parent)
        grid = QtGui.QGridLayout()
        self.setSizePolicy ( QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        
        label1 = QtGui.QLabel("Name")
        label2 = QtGui.QLabel("Length")
        label3 = QtGui.QLabel("Max. Camber")
        label4 = QtGui.QLabel("Pos. max. Camber")
        label5 = QtGui.QLabel("Thickness")
        label6 = QtGui.QLabel("Number of points")
        
        label3_1 = QtGui.QLabel("First digit. %d to %s%%:" % (0, "9.5"))
        label4_1 = QtGui.QLabel("Second digit. %d to %d%%:" % (0, 90))
        label5_1 = QtGui.QLabel("Third & fourth digit. %d to %d%%:" % (1, 40))
        label6_1 = QtGui.QLabel("%d to %d" % (20, 200))
        
        self.text1Name = QtGui.QLineEdit()
        self.text1Name.setText('NACA 00xx')
        self.text1Name.setReadOnly(True)
        self.text2Length = QtGui.QLineEdit()
        self.text2Length.setText('1.0')        
        self.text3MaxCamber = QtGui.QLineEdit()
        self.text3MaxCamber.setText('2')
        self.text4PosCamber = QtGui.QLineEdit()
        self.text4PosCamber.setText('4')
        self.text5Thickness = QtGui.QLineEdit()
        self.text5Thickness.setText('12') 
        
        self.countSpinBox = QtGui.QSpinBox()
        self.countSpinBox.setRange(20, 200)
        self.countSpinBox.setSingleStep(5)
        self.countSpinBox.setSuffix('pts')
        self.countSpinBox.setSpecialValueText("Automatic")
        self.countSpinBox.setValue(10)
        
        self.butCreate = QtGui.QPushButton("create")
        self.butCreate.clicked.connect(self.fireButtonCreate)
        self.ogl_widget = ogl_widget
        
        grid.addWidget(label1, 1, 1)
        grid.addWidget(label2, 2, 1)
        grid.addWidget(label3, 3, 1)
        grid.addWidget(label4, 4, 1)
        grid.addWidget(label5, 5, 1)
        grid.addWidget(label6, 6, 1)
        grid.addWidget(self.text1Name,      1, 3)
        grid.addWidget(self.text2Length,    2, 3)        
        grid.addWidget(self.text3MaxCamber, 3, 3)
        grid.addWidget(self.text4PosCamber, 4, 3)        
        grid.addWidget(self.text5Thickness, 5, 3)
        grid.addWidget(self.countSpinBox,   6, 3)
        grid.addWidget(label3_1, 3, 4)
        grid.addWidget(label4_1, 4, 4)
        grid.addWidget(label5_1, 5, 4)
        grid.addWidget(label6_1, 6, 4)
        
        grid.addWidget(self.butCreate, 7, 1)
        self.setLayout(grid)        

    def fireButtonCreate(self):
        
        length      = self.text2Length.text()
        maxCamber   = self.text3MaxCamber.text()
        posCamber   = self.text4PosCamber.text()        
        thick       = self.text5Thickness.text()
        pcnt        = self.countSpinBox.value()
        
        try : 
            length      = float(length)
            maxCamber   = float(maxCamber)
            posCamber   = float(posCamber)
            thick       = float(thick)
               
            if maxCamber > 9.5 or maxCamber < 0 :
                self.text3MaxCamber.selectAll() 
                return
            elif posCamber > 90 or posCamber < 0 :
                self.text4PosCamber.selectAll()
                return
            elif thick > 40 or thick < 1 : 
                self.text5Thickness.selectAll()
                return
             
            if thick < 10 :
                self.text1Name.setText('NACA ' + str(int(maxCamber)) + str(int(posCamber)) + '0' + str(int(thick)))    
            else :
                self.text1Name.setText('NACA ' + str(int(maxCamber)) + str(int(posCamber)) + str(int(thick)))
        except ValueError:
            print "fireButtonCreate in profileWidget (NACA Creator)" , length, thick
            return
        
        if maxCamber > 0 or posCamber > 0 :
            self.ogl_widget.createCambered_Naca(length, thick/100.0, maxCamber/100.0, posCamber/10.0, pcnt)
        else :
            self.ogl_widget.createSym_Naca(length, thick/100.0, pcnt)
        
        self.ogl_widget.set_name(self.text1Name.text())


class ProfileDetectWidget(QtGui.QWidget): 
    def __init__(self, ogl_widget, parent = None):
        super(ProfileDetectWidget, self).__init__(parent)
        
        grid                     = QtGui.QGridLayout()
        label1                   = QtGui.QLabel("Name")
        self.text1Name           = QtGui.QLineEdit()       
        self.butCreate           = QtGui.QPushButton("create")
        self.butCancel           = QtGui.QPushButton("cancel")        
        self.ogl_widget          = ogl_widget
        self.ogl_detector_widget = profile_ogl_image_detector.MyProfileWidget()
        #self.ogl_widget.setFixedSize(200,200)
        
        grid.addWidget(self.ogl_detector_widget, 1,1,1,4)
        grid.addWidget(label1,                       2,1)
        grid.addWidget(self.text1Name,               2,2)
        grid.addWidget(self.butCreate,               2,3)
        grid.addWidget(self.butCancel,               2,4)
        
        self.butCreate.clicked.connect(self.fireButtonCreate)
        self.butCancel.clicked.connect(self.close)
        
        self.createActions()
        self.createMenus()
        
        self.setLayout(grid) 
        self.resize(320,320)
        
    def fireButtonCreate(self):
        self.ogl_widget.set_name(self.text1Name)
        self.ogl_widget.set_pointList_top(self.ogl_detector_widget.getPointList_top)
        self.ogl_widget.set_pointList_bot(self.ogl_detector_widget.getPointList_bot)
        print "dummy function"


    def open(self) :
        (fileName, _) = QtGui.QFileDialog.getOpenFileName(self,
                                     "Open File", QtCore.QDir.currentPath())
        
        if (fileName) :
            print fileName
            #---------------------------------------------- if (image is None) :
                #----------- QtGui.QMessageBox.information(self, "Image Viewer",
                                         #------ "Cannot load " + str(fileName))
                #-------------------------------------------------------- return
    
            #self.imageLabel.setPixmap(QtGui.QPixmap.fromImage(image))
           # self.scaleFactor = 1.0
    
            #self.printAct.setEnabled(True)
           # self.fitToWindowAct.setEnabled(True)
            #self.updateActions()

           # if (not self.fitToWindowAct.isChecked()) :
            #   self.imageLabel.adjustSize()
            self.ogl_detector_widget.drawImage(fileName)

    def createActions(self):
        self.openAct = QtGui.QAction('Open...', self)
        self.openAct.triggered.connect(self.open)    
        
        self.exitAct = QtGui.QAction("E&xit", self);
        self.exitAct.triggered.connect(self.close)
        
    def createMenus(self):
        fileMenu = QtGui.QMenu("File", self)
        fileMenu.addAction(self.openAct)
        fileMenu.addSeparator()
        fileMenu.addAction(self.exitAct)

        menubar = QtGui.QMenuBar(self)
        menubar.addMenu(fileMenu)



if __name__ == '__main__':
    app = QtGui.QApplication(["PyQt OpenGL"])
    widget = ProfileWidget()
    widget.show()
    app.exec_()    