'''
Created on Oct 8, 2014

@author: fran_re
'''
import sys
import math
import utility
from airfoil import Airfoil
from airfoilDetectWidget import AirfoilDetectWidget
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


class AirfoilNacaWidget(QtGui.QWidget):
    def __init__(self, ogl_main_widget, parent = None):
        super(AirfoilNacaWidget, self).__init__(parent)
        self.setSizePolicy ( QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        
        self.naca4 = Naca4Tab(ogl_main_widget)
        self.naca5 = Naca5Tab(ogl_main_widget)
        tabWidget = QtGui.QTabWidget()
        tabWidget.addTab(self.naca4, self.tr("Naca4"))
        tabWidget.addTab(self.naca5, self.tr("Naca5"))
        
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(tabWidget)
        self.setLayout(mainLayout)
        self.setWindowTitle(self.tr("Tab Dialog"))        
        
class Naca4Tab(QtGui.QWidget):
    def __init__(self, ogl_widget, parent = None):        
        QtGui.QWidget.__init__(self, parent)
        
        grid = QtGui.QGridLayout()
        
        label1 = QtGui.QLabel("Name")
        label2 = QtGui.QLabel("Length")
        label3 = QtGui.QLabel("Max. Camber")
        label4 = QtGui.QLabel("Pos. max. Camber")
        label5 = QtGui.QLabel("Thickness")
        label6 = QtGui.QLabel("Number of points")
        
        label3_1 = QtGui.QLabel("First digit. %d to %s%%:" % (0, "9.5"))
        label4_1 = QtGui.QLabel("Second digit. %d to %d%%:" % (1, 9))
        label5_1 = QtGui.QLabel("Third & fourth digit. %d to %d%%:" % (1, 40))
        label6_1 = QtGui.QLabel("%d to %d" % (20, 200))
        
        self.text1Name = QtGui.QLineEdit()
        self.text1Name.setText('NACA 00xx')
        self.text1Name.setReadOnly(True)
        self.text2Length = QtGui.QLineEdit()
        self.text2Length.setText('1.0') 
        self.text2Length.setReadOnly(True)               
        self.text3MaxCamber = QtGui.QLineEdit()
        self.text3MaxCamber.setText('0')
        self.text4PosCamber = QtGui.QLineEdit()
        self.text4PosCamber.setText('0')
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
            
            if maxCamber == 0 :
                posCamber = 0 
                self.text4PosCamber.setText('0')
               
            if maxCamber > 9.5 or maxCamber < 0 :
                self.text3MaxCamber.selectAll() 
                return
            elif posCamber > 9 :
                self.text4PosCamber.selectAll()
                return
            elif maxCamber != 0 and posCamber < 1 :
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
            self.ogl_widget.createCambered_Naca(length, maxCamber/100.0, posCamber/10.0, thick/100.0, pcnt)
        else :
            self.ogl_widget.createSym_Naca(length, thick/100.0, pcnt)
        
        self.ogl_widget.profile.setName(self.text1Name.text())



class Naca5Tab(QtGui.QWidget):
    def __init__(self, ogl_widget, parent = None):        
        QtGui.QWidget.__init__(self, parent)
        
        grid = QtGui.QGridLayout()
        
        label1 = QtGui.QLabel("Name")
        label2 = QtGui.QLabel("Design coefficient of lift")
        label3 = QtGui.QLabel("Pos. max. Camber")
        label4 = QtGui.QLabel("Reflex")
        label5 = QtGui.QLabel("Thickness")
        label6 = QtGui.QLabel("Number of points")
        
        label2_1 = QtGui.QLabel("First digit: %s to %s:" % ("0", "9"))
        label3_1 = QtGui.QLabel("Second & third digits.")
        label5_1 = QtGui.QLabel("Fourth & fifth digits. %d to %d%%:" % (1, 30))
        label6_1 = QtGui.QLabel("%d to %d" % (20, 200))
        
        self.text1Name = QtGui.QLineEdit()
        self.text1Name.setText('NACA xxxxx')
        self.text1Name.setReadOnly(True)
        
        self.text2Cl = QtGui.QLineEdit()
        clvalidator = QtGui.QIntValidator(1,9 ,self)
        self.text2Cl.setValidator(clvalidator)
        self.text2Cl.setText('1')        
        
        self.combosCamberReflex = QtGui.QComboBox()
        self.combosCamberReflex.addItem("0")
        self.combosCamberReflex.addItem("1")
        
        self.combosCamberPos = QtGui.QComboBox()
        self.combosCamberPos.addItem("1")
        self.combosCamberPos.addItem("2")
        self.combosCamberPos.addItem("3")
        self.combosCamberPos.addItem("4")
        self.combosCamberPos.addItem("5")
        
        self.text4Thickness = QtGui.QLineEdit()
        self.text4Thickness.setText('12')
        
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
        grid.addWidget(self.text2Cl,        2, 3)        
        grid.addWidget(self.combosCamberPos, 3, 3)
        grid.addWidget(self.combosCamberReflex, 4, 3)
        grid.addWidget(self.text4Thickness, 5, 3)        
        grid.addWidget(self.countSpinBox,   6, 3)
        grid.addWidget(label2_1, 2, 4)
        grid.addWidget(label3_1, 3, 4)
        grid.addWidget(label5_1, 5, 4)
        grid.addWidget(label6_1, 6, 4)
        
        grid.addWidget(self.butCreate, 7, 1)
        self.setLayout(grid)        

    def fireButtonCreate(self):
        
        cl          = self.text2Cl.text()
        posCamber   = self.combosCamberPos.currentText()  
        reflex      = self.combosCamberReflex.currentText()      
        thick       = self.text4Thickness.text()
        pcnt        = self.countSpinBox.value()
        
        try : 
            cl          = float(cl)
            posCamber   = float(posCamber)
            thick       = float(thick)
            reflex      = reflex == "1"
            if posCamber == 1 and reflex:
                # reflex not possible at posCamber 1
                self.reflex = False           
            elif thick > 30 or thick < 1 : 
                self.text5Thickness.selectAll()
                return            
            
        except ValueError:
            print "Exception fireButtonCreate in profileWidget (NACA Creator)" ,  thick
            return
        
        self.ogl_widget.createCambered_Naca5(cl, posCamber, reflex, thick, pcnt)        
        self.ogl_widget.setName(self.text1Name.text())