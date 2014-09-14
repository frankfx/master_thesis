'''
Created on Sep 2, 2014

@author: rene
'''
from PySide.QtGui import QPushButton
from Xtest.Open_GL import TestSimpleOpenGL, ImageViewer
from Xtest.Open_GL import porfile_widget
from profile import Profile
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



class Tab1(QtGui.QWidget):
    def __init__(self, parent = None):
        super(Tab1, self).__init__(parent)
        
        grid = QtGui.QGridLayout()
        self.ogl_widget = porfile_widget.MyProfileWidget()
        self.ogl_widget_creater = Tab2(self.ogl_widget) 
        self.ogl_widget_detect  = Tab3(self.ogl_widget)
        self.ogl_widget_creater.but1.clicked.connect(self.refreshDataList)
        self.ogl_widget_detect.but1.clicked.connect(self.refreshDataList)
        
        grid.addLayout(self.createEvalLayout(),0,1)
        grid.addWidget(self.ogl_widget, 1,1)

        self.setLayout(grid)
        
        
    def createEvalLayout(self):
        groupBox    = QtGui.QGroupBox("Evaluation")
        groupBox2   = QtGui.QGroupBox("View")
        
        vboxLayout  = QtGui.QVBoxLayout()
        gridEval    = QtGui.QGridLayout()
        gridView    = QtGui.QGridLayout()
        
        labelName               = QtGui.QLabel("Name")
        labelProfiltiefe        = QtGui.QLabel("Profiltiefe")
        labelAnstellwinkel      = QtGui.QLabel("Anstellwinkel")
        labelProfildicke        = QtGui.QLabel("Profildicke")
        labelProfilwoelbung     = QtGui.QLabel("Profilwoelbung")
        self.textName           = QtGui.QLineEdit()
        self.textProfiltiefe    = QtGui.QLineEdit()
        self.textAnstellWinkel  = QtGui.QLineEdit()
        self.textProfildicke    = QtGui.QLineEdit()
        self.textProfilWoelbung = QtGui.QLineEdit()
        labelZoomIn             = QtGui.QLabel("+")
        labelZoomOut            = QtGui.QLabel("-")
        checkShowPoints         = QtGui.QCheckBox("show points")
        checkFitToPage          = QtGui.QCheckBox("fit to page")
        self.butNaca            = QtGui.QPushButton("NacaCreator")
        self.butImgDetect       = QtGui.QPushButton("ImgDetect")
        dial                    = QtGui.QDial()
        self.sld                = QtGui.QSlider(QtCore.Qt.Horizontal, self)        
        
        gridEval.addWidget(labelName                , 0, 0)
        gridEval.addWidget(labelProfiltiefe         , 1, 0)
        gridEval.addWidget(labelAnstellwinkel       , 2, 0)
        gridEval.addWidget(labelProfildicke         , 0, 3)
        gridEval.addWidget(labelProfilwoelbung      , 1, 3)
        gridEval.addWidget(self.textName            , 0, 1)
        gridEval.addWidget(self.textProfiltiefe     , 1, 1)
        gridEval.addWidget(self.textAnstellWinkel   , 2, 1)
        gridEval.addWidget(self.textProfildicke     , 0, 4)
        gridEval.addWidget(self.textProfilWoelbung  , 1, 4)
        
        gridView.addWidget(labelZoomIn              , 0, 0)
        gridView.addWidget(self.sld                 , 0, 1)
        gridView.addWidget(labelZoomOut             , 0, 2)
        gridView.addWidget(checkShowPoints          , 1, 0, 1, 2)
        gridView.addWidget(checkFitToPage           , 2, 0, 1, 2)
        gridView.addWidget(self.butNaca             , 1, 3)
        gridView.addWidget(self.butImgDetect        , 2, 3)
        gridView.addWidget(dial                     , 1, 1, 2, 2)        
        
        self.refreshDataList()
        
        dial.setFocusPolicy(QtCore.Qt.StrongFocus)
        dial.setRange(0,90)
        dial.valueChanged.connect(self.fireSetRotValue)
        checkShowPoints.toggled.connect(self.fireShowPoints)
        checkFitToPage.toggled.connect(self.fireFitToPage)
        self.butNaca.clicked.connect(self.fireEvalWidget)
        self.butImgDetect.clicked.connect(self.fireDetectWidget)

        self.sld.setMinimum(1)
        self.sld.setValue(51)
        self.sld.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sld.valueChanged[int].connect(self.ogl_widget.zoom) 
        
        groupBox.setLayout(gridEval) 
        groupBox2.setLayout(gridView)     
        
        vboxLayout.addWidget(groupBox)
        vboxLayout.addWidget(groupBox2)    
            
        return vboxLayout
        
    def refreshDataList(self):
        print self.ogl_widget.get_name()
        print self.ogl_widget.get_len_chord()
        print self.ogl_widget.get_work_angle()
        print self.ogl_widget.get_profile_thickness()
        print self.ogl_widget.get_profile_arch()
        
        self.textName.setText(self.ogl_widget.get_name())
        self.textProfiltiefe.setText(str(self.ogl_widget.get_len_chord()))
        self.textAnstellWinkel.setText(str(self.ogl_widget.get_work_angle()))
        self.textProfildicke.setText(str(self.ogl_widget.get_profile_thickness()))
        self.textProfilWoelbung.setText(str(self.ogl_widget.get_profile_arch()))
        

    def fireSetRotValue(self, value):
        print value
        self.ogl_widget.set_rotate(-value)
        
    def fireShowPoints(self):
        self.ogl_widget.setFlagDrawPoints(not self.ogl_widget.getFlagDrawPoints())
    
    def fireFitToPage(self, value):
        if value:
            self.sld.setValue(51) 
            self.sld.setEnabled(False)
        else:
            self.sld.setEnabled(True)
        self.ogl_widget.fitToPage(value)
    
    def fireEvalWidget(self):
        self.ogl_widget_creater.show()

    def fireDetectWidget(self):
        self.ogl_widget_detect.show()

class Tab2(QtGui.QWidget):
    def __init__(self, ogl_widget, parent = None):
        super(Tab2, self).__init__(parent)
        grid = QtGui.QGridLayout()
        self.setSizePolicy ( QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        
        label1 = QtGui.QLabel("Name")
        label2 = QtGui.QLabel("max CamberLine (%)")
        label3 = QtGui.QLabel("pos max Camberline (%)")
        label4 = QtGui.QLabel("Laenge Sehne")
        label5 = QtGui.QLabel("max Profildicke (%)")
        label6 = QtGui.QLabel("Punkt [%d, %d]:" % (10, 100))
        
       # checkBox = QtGui.QCheckBox("symmetrical 4-digit NACA airfoil")
        
        self.text1Name = QtGui.QLineEdit()
        self.text1Name.setText('NACA 00xx')
        self.text1Name.setReadOnly(True)
        self.text2MaxCamber = QtGui.QLineEdit()
        self.text2MaxCamber.setText('2')
        self.text3PosCamber = QtGui.QLineEdit()
        self.text3PosCamber.setText('4')
        self.text4Length = QtGui.QLineEdit()
        self.text4Length.setText('1.0')
        self.text5Thickness = QtGui.QLineEdit()
        self.text5Thickness.setText('12')
        
        self.countSpinBox = QtGui.QSpinBox()
        self.countSpinBox.setRange(90, 200)
        self.countSpinBox.setSingleStep(5)
        self.countSpinBox.setSuffix('pts')
        self.countSpinBox.setSpecialValueText("Automatic")
        self.countSpinBox.setValue(10)
        
        self.but1 = QtGui.QPushButton("create")
        self.but1.clicked.connect(self.fireButtonCreate)
        self.ogl_widget = ogl_widget
        
        grid.addWidget(label1, 1, 1)
        grid.addWidget(label2, 2, 1)
        grid.addWidget(label3, 3, 1)
        grid.addWidget(label4, 4, 1)
        grid.addWidget(label5, 5, 1)
        grid.addWidget(label6, 6, 1)
        grid.addWidget(self.text1Name,      1, 3)
        grid.addWidget(self.text2MaxCamber, 2, 3)
        grid.addWidget(self.text3PosCamber, 3, 3)        
        grid.addWidget(self.text4Length,    4, 3)
        grid.addWidget(self.text5Thickness, 5, 3)
        grid.addWidget(self.countSpinBox,   6, 3)
        
        
        grid.addWidget(self.but1, 7, 1)
        #grid.addWidget(self.ogl_widget, 6, 1, 2, 3)
        self.setLayout(grid)        

    def fireButtonCreate(self):
        
        length = self.text4Length.text()
        thick = self.text5Thickness.text()
        maxCamber = self.text2MaxCamber.text()
        posCamber = self.text3PosCamber.text()
        pcnt = self.countSpinBox.value()
        
        try : 
            length = float(length)
            thick = float(thick)
            maxCamber = float(maxCamber)
            posCamber = float(posCamber)
            if thick >= 100 or thick < 0 : 
                return
            if thick < 10 :
                self.text1Name.setText('NACA ' + str(int(maxCamber)) + str(int(posCamber)) + '0' + str(int(thick)))    
            else :
                self.text1Name.setText('NACA ' + str(int(maxCamber)) + str(int(posCamber)) + str(int(thick)))
        except ValueError:
            print length, thick
            return
        
        if maxCamber > 0 or posCamber > 0 :
            print "dfsfs"
            print length
            self.ogl_widget.createCambered_Naca(length, thick/100.0, maxCamber/100.0, posCamber/10.0, pcnt)
        else :
            self.ogl_widget.createSym_Naca(length, thick/100.0, pcnt)
        
        self.ogl_widget.set_name(self.text1Name.text())


class Tab3(QtGui.QWidget): 
    def __init__(self, ogl_widget, parent = None):
        super(Tab3, self).__init__(parent)
        
        grid = QtGui.QGridLayout()
        img_widget = ImageViewer.ImageViewer()
        self.ogl_widget = TestSimpleOpenGL.MyProfileWidget()
        #self.ogl_widget.setFixedSize(200,200)
        
        self.but1 = QtGui.QPushButton("ok")
        but2 = QtGui.QPushButton("cancel")
        grid.addWidget(self.but1, 1,1,1,1)
        grid.addWidget(but2, 1,2,1,1)
        grid.addWidget(img_widget,2,1,1,1)
        grid.addWidget(self.ogl_widget,2,2,1,1)
        
    
        self.setLayout(grid)
        

class TabWidget(QtGui.QTabWidget):
    def __init__(self, parent = None):
        super(TabWidget, self).__init__(parent)
        self.setWindowTitle("Tab")
        tab1 = Tab1()
        tab2 = Tab2(None)
        tab3 = Tab3(None)
        self.addTab(tab1, "tab1")
        self.addTab(tab2, "tab2")
        self.addTab(tab3, "tab3")


class MyProfileWidget(QtGui.QWidget):
    def __init__(self, parent = None):
        super(MyProfileWidget, self).__init__(parent)
        
        grid = QtGui.QGridLayout()
        but = TabWidget()
        grid.addWidget(but,1,1)
        self.setLayout(grid)   
        
        self.setWindowTitle('Calculator')    
        self.resize(560,520)
        #self.setFixedSize(QtCore.QSize(400,400))
        self.show()


        

if __name__ == '__main__':
    app = QtGui.QApplication(["PyQt OpenGL"])
    widget = MyProfileWidget()
    widget.show()
    app.exec_()    