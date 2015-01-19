'''
Created on Jan 14, 2015

@author: fran_re
'''

from PySide import QtGui
from popUp_tool import PopUpTool
from Xtest.XML_Editor.externTools import difficultTestTool
from Xtest.Open_GL import utility
from pylab import *
import os

class ToolX(PopUpTool):
    '''
    This class represents a new file dialog widget. It will be used to create an empty cpacs file
    '''
    def __init__(self, name, width=500, height=300):
        '''
        constructs five input text fields and two buttons to for submitting the input or cancel the event
        '''
        super(ToolX, self).__init__(name, width, height)          
        
        self.setupWidget()
        
        layout = QtGui.QFormLayout()
        layout.addRow("&name"   , self.textName)
        layout.addRow("&version", self.textVers)
        layout.addRow("&aircraftModelUID", self.textUID)
        layout.addRow("&datasetName", self.textDSet)
        layout.addRow("&choise", self.groupBox)
        layout.addRow(self.labelLoadCaseUID, self.textLoadCaseUID)
        layout.addRow(self.labelLoadCase, self.textLoadCase)
        layout.addRow(self.labelMachNumber, self.textMachNumber)
        layout.addRow(self.labelReynoldsNumber, self.textReynoldsNumber)
        
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addLayout(layout)
        mainLayout.addWidget(self.buttonBox)
        
        self.setLayout(mainLayout)

    @utility.overrides(PopUpTool)    
    def setupWidget(self):
        # tool
        self.textName = QtGui.QLineEdit()
        self.textVers = QtGui.QLineEdit()
        # aircraftModelUID
        self.textUID  = QtGui.QLineEdit()
        # datasetName
        self.textDSet = QtGui.QLineEdit()
        # referenceValues
        self.textArea = QtGui.QLineEdit()        
        self.textLengthCmx = QtGui.QLineEdit()        
        self.textLengthCmy = QtGui.QLineEdit()        
        self.textLengthCmz = QtGui.QLineEdit()        
        self.textMomentReferencePoint = QtGui.QLineEdit()        
        
        # loadCases vs performanceMap
        self.groupBox = QtGui.QGroupBox()
        radio1 = QtGui.QRadioButton("&loadCases")
        radio2 = QtGui.QRadioButton("&performanceMap")
        grid = QtGui.QGridLayout()
        grid.addWidget(radio1,0,1)
        grid.addWidget(radio2,0,2)
        self.groupBox.setLayout(grid)
        
        radio1.setChecked(True)
        radio2.setChecked(False)
        
        radio1.toggled.connect(self.__clickkedstate)

        # loadCase
        self.textLoadCaseUID = QtGui.QLineEdit()
        self.textLoadCase = QtGui.QLineEdit()
        self.labelLoadCaseUID = QtGui.QLabel("labelLoadCaseUID")
        self.labelLoadCase = QtGui.QLabel("labelLoadCase")
        
        # performanceMap
        self.textMachNumber     = QtGui.QLineEdit()
        self.textReynoldsNumber = QtGui.QLineEdit()
        self.labelMachNumber= QtGui.QLabel("MachNumber")
        self.labelReynoldsNumber = QtGui.QLabel("ReynoldsNumber")

        self.textName.setToolTip("name of tool")        
        self.textVers.setToolTip("version of tool")
        self.textUID.setToolTip("reference to aircraft model")
        self.textDSet.setToolTip("name of the dataset for LIFTING_LINE calculation")
        
        
        self.buttonBox = QtGui.QDialogButtonBox()
        self.buttonBox.addButton("ok", QtGui.QDialogButtonBox.AcceptRole)
        self.buttonBox.addButton("cancel", QtGui.QDialogButtonBox.RejectRole)
        
        self.buttonBox.accepted.connect(self.submitInput)        

        self.__setLoadCase(True)
        self.__setPerformanceMap(False)

    def __clickkedstate(self, b):
        self.__setLoadCase(b)
        self.__setPerformanceMap(not b)
        
        
        
    def __setPerformanceMap(self, b):
        if b :
            self.textMachNumber.show()
            self.textReynoldsNumber.show()
            self.labelMachNumber.show()
            self.labelReynoldsNumber.show()            
        else:
            self.textMachNumber.hide()
            self.textReynoldsNumber.hide()
            self.labelMachNumber.hide()
            self.labelReynoldsNumber.hide()
            

    def __setLoadCase(self, b):
        if b :
            self.textLoadCaseUID.show()
            self.textLoadCase.show()
            self.labelLoadCaseUID.show()
            self.labelLoadCase.show()            
        else:
            self.textLoadCaseUID.hide()
            self.textLoadCase.hide()
            self.labelLoadCaseUID.hide()
            self.labelLoadCase.hide()

    @utility.overrides(PopUpTool)    
    def setConnection(self):
        retvalue = os.system("xsltproc -o ../cpacs_files/test.xml ../cpacs_files/mappingInputRaw.xsl ../cpacs_files/D150_CPACS2.0_valid2.xml")
        print "rer" ,retvalue

        
        #self.tool = difficultTestTool.init()

    @utility.overrides(PopUpTool)    
    def submitInput(self):
        '''
        returns the input values from the new file dialog form
        '''     
        
        self.setConnection()
           
        try :
            a = int(self.text1.text())
            b = int(self.text2.text())
            self.tool = difficultTestTool.doSomething(a, b)
        except :
            print "error"
            self.tool = np.arange(2.0, 0.1)
        s = sin(2*pi*self.tool)
        plot(self.tool, s)

        xlabel('time (s)')
        ylabel('voltage (mV)')
        title('About as simple as it gets, folks')
        grid(True)
        savefig("test.png")
        show()


if __name__ == "__main__":
    app = QtGui.QApplication([])
    test = ToolX("name")
    test.show()
    app.exec_()       