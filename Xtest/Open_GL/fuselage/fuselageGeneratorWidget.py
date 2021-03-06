'''
Created on Oct 20, 2014

@author: fran_re
'''

from PySide import QtGui

class FuselageGeneratorWidget(QtGui.QWidget):
    def __init__(self, parent = None):
        super(FuselageGeneratorWidget, self).__init__(parent)
        self.setSizePolicy ( QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        
        self.widget1 = SuperEllipse()
        tabWidget = QtGui.QTabWidget()
        tabWidget.addTab(self.widget1, self.tr("SuperEllipse"))
        
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(tabWidget)
        self.setLayout(mainLayout)
        self.setWindowTitle(self.tr("Tab Dialog"))        
        
class SuperEllipse(QtGui.QWidget):
    def __init__(self, parent = None):        
        QtGui.QWidget.__init__(self, parent)

        horizontalLine     =  QtGui.QFrame()
        horizontalLine.setFrameStyle(QtGui.QFrame.HLine)
        horizontalLine.setSizePolicy(QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        
        # sends signal to fuselageMainWidget
        self.btnCreate = QtGui.QPushButton("Create")

        self.textName = QtGui.QLineEdit()              
        self.widthSpinBox_t = self.__createDoubleSpinBox(value=1.0)
        self.heightSpinBox_t = self.__createDoubleSpinBox(value=1.0)        
        self.curveSpinBox1_t = self.__createDoubleSpinBox(value=2.0)       
        self.curveSpinBox2_t = self.__createDoubleSpinBox(value=2.0)       
        self.pcntSpinBox_t = self.__createSpinBox()       

        self.widthSpinBox_b = self.__createDoubleSpinBox(value=1.0)
        self.heightSpinBox_b = self.__createDoubleSpinBox(value=1.0)        
        self.curveSpinBox1_b = self.__createDoubleSpinBox(value=2.0)       
        self.curveSpinBox2_b = self.__createDoubleSpinBox(value=2.0)       
        self.pcntSpinBox_b = self.__createSpinBox()
        
        self.widthSpinBox_t.setEnabled(False)
        self.heightSpinBox_t.setEnabled(False)
        self.widthSpinBox_b.setEnabled(False)
        self.heightSpinBox_b.setEnabled(False)
        
        layout = QtGui.QFormLayout()
        
        layout.addRow("Name", self.textName )
                
        layout.addRow(QtGui.QLabel("TopSide"))
        layout.addRow("a : half-axes", self.widthSpinBox_t)
        layout.addRow("b : half-axes", self.heightSpinBox_t)
        layout.addRow("m : exp of a", self.curveSpinBox1_t)
        layout.addRow("n : exp of b", self.curveSpinBox2_t)
        layout.addRow("point count", self.pcntSpinBox_t)
        
        layout.addRow(QtGui.QLabel(""))
        
        layout.addRow(QtGui.QLabel("BotSide"))
        layout.addRow("a : half-axes", self.widthSpinBox_b)
        layout.addRow("b : half-axes", self.heightSpinBox_b)
        layout.addRow("m : exp of a", self.curveSpinBox1_b)
        layout.addRow("n : exp of b", self.curveSpinBox2_b)
        layout.addRow("point count", self.pcntSpinBox_b)

        layout.addRow(self.btnCreate)
        
        self.setLayout(layout)        

    def __createSpinBox(self, start=4, end=200, step=1, suffix='pts', value=100):
        spinBox = QtGui.QDoubleSpinBox()
        spinBox.setRange(start, end)
        spinBox.setSingleStep(step)
        spinBox.setValue(value)   
        return spinBox 
    
    def __createDoubleSpinBox(self, start=1, end=10, step=1, value=4):
        spinBox = QtGui.QDoubleSpinBox()
        spinBox.setRange(start, end)
        spinBox.setSingleStep(step)
        spinBox.setValue(value)   
        return spinBox     
        
    def getSuperEllipseParameter(self):
        topSide = [self.widthSpinBox_t.value(), self.heightSpinBox_t.value(), 
                   self.curveSpinBox1_t.value(), self.curveSpinBox2_t.value(), self.pcntSpinBox_t.value()]
        
        botSide = [self.widthSpinBox_b.value(), self.heightSpinBox_b.value(), self.curveSpinBox1_b.value(), 
                   self.curveSpinBox2_b.value(), self.pcntSpinBox_b.value()]

        return topSide, botSide, self.textName.text()
    