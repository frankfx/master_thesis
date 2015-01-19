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
        layout.addRow("", self.groupBox)
        layout.addRow(self.labelLoadCaseUID, self.textLoadCaseUID)
        layout.addRow(self.labelLoadCase, self.textLoadCase)
        layout.addRow(self.labelMachNum, self.textMachNum)
        layout.addRow(self.labelReynNum, self.textReynNum)
        
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addLayout(layout)
        mainLayout.addWidget(self.buttonBox)
        
        
        self.listWidget = QtGui.QListWidget()
        self.listWidget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.listWidget.addItem(QtGui.QListWidgetItem("Oak"))
        
        mainLayout.addWidget(self.listWidget)
        
        
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
        self.textArea      = QtGui.QLineEdit()        
        self.textLenCmx    = QtGui.QLineEdit()        
        self.textLenCmy    = QtGui.QLineEdit()        
        self.textLenCmz    = QtGui.QLineEdit()        
        self.textMomRefPnt = QtGui.QLineEdit()        
        
        # loadCases vs performanceMap
        self.groupBox = QtGui.QGroupBox()
        grid   = QtGui.QGridLayout()
        radio1 = QtGui.QRadioButton("&loadCases")
        radio2 = QtGui.QRadioButton("&performanceMap")
        grid.addWidget(radio1,0,1)
        grid.addWidget(radio2,0,2)
        self.groupBox.setLayout(grid)
        
        # loadCase
        self.textLoadCaseUID  = QtGui.QLineEdit()
        self.textLoadCase     = QtGui.QLineEdit()
        self.labelLoadCaseUID = QtGui.QLabel("labelLoadCaseUID")
        self.labelLoadCase    = QtGui.QLabel("labelLoadCase")
        
        # performanceMap
        self.textMachNum  = QtGui.QLineEdit()
        self.textReynNum  = QtGui.QLineEdit()
        self.labelMachNum = QtGui.QLabel("MachNumber")
        self.labelReynNum = QtGui.QLabel("ReynoldsNumber")



        # #################################################
        # set tool tips
        # #################################################
        self.textName.setToolTip("name of tool")        
        self.textVers.setToolTip("version of tool")
        self.textUID.setToolTip("reference to aircraft model")
        self.textDSet.setToolTip("name of the dataset for LIFTING_LINE calculation")

        # #################################################
        # set buttons
        # #################################################        
        self.buttonBox = QtGui.QDialogButtonBox()
        self.buttonBox.addButton("ok", QtGui.QDialogButtonBox.AcceptRole)
        self.buttonBox.addButton("cancel", QtGui.QDialogButtonBox.RejectRole)

        # #################################################
        # set actions
        # #################################################
        radio1.toggle()   
        radio1.toggled.connect(self.__clickkedstate)     
        self.buttonBox.accepted.connect(self.submitInput) 
        self.buttonBox.rejected.connect(self.close)       

    def __clickkedstate(self, b):
        self.textMachNum.setVisible(b)
        self.textReynNum.setVisible(b)
        self.labelMachNum.setVisible(b)
        self.labelReynNum.setVisible(b)         

        self.textLoadCaseUID.setVisible(not b)
        self.textLoadCase.setVisible(not b)
        self.labelLoadCaseUID.setVisible(not b)
        self.labelLoadCase.setVisible(not b) 
        
        
        
        
        

    @utility.overrides(PopUpTool)    
    def setConnection(self):
        os.system("xsltproc -o ../cpacs_files/test.xml ../cpacs_files/mappingInputRaw.xsl ../cpacs_files/D150_CPACS2.0_valid2.xml")

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