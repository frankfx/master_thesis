'''
Created on Oct 20, 2014

@author: fran_re
'''

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


class FuselageGeneratorWidget(QtGui.QWidget):
    def __init__(self, ogl_main_widget, parent = None):
        super(FuselageGeneratorWidget, self).__init__(parent)
        self.setSizePolicy ( QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        
        self.widget1 = SuperEllipse(ogl_main_widget)
        tabWidget = QtGui.QTabWidget()
        tabWidget.addTab(self.naca4, self.tr("SuperEllipse"))
        
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(tabWidget)
        self.setLayout(mainLayout)
        self.setWindowTitle(self.tr("Tab Dialog"))        
        
class SuperEllipse(QtGui.QWidget):
    def __init__(self, ogl_widget, parent = None):        
        QtGui.QWidget.__init__(self, parent)

        self.ogl_widget = ogl_widget

        horizontalLine     =  QtGui.QFrame()
        horizontalLine.setFrameStyle(QtGui.QFrame.HLine)
        horizontalLine.setSizePolicy(QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        
        labelTopSide         = QtGui.QLabel("TopSide")        
        labelBotSide         = QtGui.QLabel("BotSide")  
        labelName            = QtGui.QLabel("Name: ")  
        butCreate            = QtGui.QPushButton("Create")
        butCreate.clicked.connect(self.fireButtonCreate)

        self.textName        = QtGui.QLineEdit()              
        self.widthSpinBox_t  = self.__createDoubleSpinBox()
        self.heightSpinBox_t = self.__createDoubleSpinBox()        
        self.curveSpinBox_t  = self.__createSpinBox()       
        self.pcntSpinBox_t   = self.__createSpinBox()       

        self.widthSpinBox_b  = self.__createDoubleSpinBox()
        self.heightSpinBox_b = self.__createDoubleSpinBox()        
        self.curveSpinBox_b  = self.__createSpinBox()       
        self.pcntSpinBox_b   = self.__createSpinBox()

        grid = QtGui.QGridLayout() 
        grid.addWidget(labelTopSide,0,0)       
        grid.addWidget(self.widthSpinBox_t, 1,0)
        grid.addWidget(self.heightSpinBox_t, 1,1)
        grid.addWidget(self.curveSpinBox_t, 1,2)
        grid.addWidget(self.pcntSpinBox_t, 1,3)   

        grid.addWidget(horizontalLine,1, 0, 2, 2)

        grid.addWidget(labelBotSide,3,0)
        grid.addWidget(self.widthSpinBox_b, 4,0)
        grid.addWidget(self.heightSpinBox_b, 4,1)
        grid.addWidget(self.curveSpinBox_b, 4,2)
        grid.addWidget(self.pcntSpinBox_b, 4,3) 
        
        grid.addWidget(labelName, 5,0) 
        grid.addWidget(self.textName, 5,1) 
        grid.addWidget(butCreate, 5,2) 
        
        grid.addWidget(self.butCreate, 7, 1)
        self.setLayout(grid)        


    def __createSpinBox(self, start=20, end=200, step=5, suffix='pts', value=10):
        spinBox = QtGui.QDoubleSpinBox()
        spinBox.setRange(start, end)
        spinBox.setSingleStep(step)
        spinBox.setSuffix(suffix)
        spinBox.setValue(value)   
        return spinBox 
    
    def __createDoubleSpinBox(self, start=20, end=200, step=5, suffix='pts', value=10):
        spinBox = QtGui.QDoubleSpinBox()
        spinBox.setRange(start, end)
        spinBox.setSingleStep(step)
        spinBox.setSuffix(suffix)
        spinBox.setValue(value)   
        return spinBox     

    def fireButtonCreate(self):
        topSide = [self.widthSpinBox_t.value(), self.heightSpinBox_t.value(), self.curveSpinBox_t.value(), self.pcntSpinBox_t.value()]
        botSide = [self.widthSpinBox_b.value(), self.heightSpinBox_b.value(), self.curveSpinBox_b.value(), self.pcntSpinBox_b.value()]
        

        self.ogl_widget.createSuperEllipse(topSide, botSide)

        self.ogl_widget.profile.setName(self.text1Name.text())


