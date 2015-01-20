'''
Created on Jan 14, 2015

@author: fran_re
'''

from PySide import QtGui, QtCore
from popUp_tool import PopUpTool
from Xtest.XML_Editor.externTools import difficultTestTool
from Xtest.Open_GL import utility
from pylab import *
import os

class ToolX(PopUpTool):
    def __init__(self, name, width=300, height=700):
        super(ToolX, self).__init__(name, width, height)          
        
        self.setupWidget()
                
        layout = QtGui.QFormLayout()
        layout.addRow(self.butOpenTool)
        layout.addRow(self.labelName, self.textName)
        layout.addRow(self.labelVers, self.textVers)
        layout.addRow(self.butOpenAircraftModelUID)        
        layout.addRow(self.labelAMUID, self.textAMUID)
        layout.addRow(self.butOpenDataSetName)
        layout.addRow(self.labelDSet, self.textDSet)
        layout.addRow(self.butOpenReferenceValues)
        layout.addRow(self.labelArea,self.textArea)
        layout.addRow(self.labelLenCmx,self.textLenCmx)
        layout.addRow(self.labelLenCmy,self.textLenCmy)
        layout.addRow(self.labelLenCmz,self.textLenCmz)
        layout.addRow(self.labelMomRefPnt,self.textMomRefPnt)
        layout.addRow(self.butOpenLCasesAndPerMap)
        layout.addRow(self.groupBoxCaseVsPerMap)
        layout.addRow(self.groupBoxLoadCases)
        layout.addRow(self.labelLoadCaseUID, self.textLoadCaseUID)
        layout.addRow(self.labelLoadCase, self.textLoadCase)
        layout.addRow(self.groupBoxPerMap)        
        layout.addRow(self.labelMachNum, self.textMachNum)
        layout.addRow(self.labelReynNum, self.textReynNum)
        layout.addRow(self.labelAngleYaw, self.textAngleYaw)
        layout.addRow(self.labelAngleAtt, self.textAngleAtt)
        layout.addRow(self.labelPositiveSteadi, self.textPositiveSteadi)
        layout.addRow(self.labelNegativeSteadi, self.textNegativeSteadi)
        layout.addRow(self.labelCtrlSurfaces, self.textCtrlSurfaces)
        layout.addRow(self.labelCtrlSurUID, self.textCtrlSurUID)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addLayout(layout)
        mainLayout.addWidget(self.buttonBox)
        
        self.setLayout(mainLayout)
        

    def setupInputFields(self):
        # tool
        self.textName = QtGui.QLineEdit()
        self.textVers = QtGui.QLineEdit()
        
        # aircraftModelUID
        self.textAMUID  = QtGui.QLineEdit()

        # datasetName
        self.textDSet = QtGui.QLineEdit()
        
        # referenceValues
        self.textArea      = QtGui.QLineEdit()        
        self.textLenCmx    = QtGui.QLineEdit()        
        self.textLenCmy    = QtGui.QLineEdit()        
        self.textLenCmz    = QtGui.QLineEdit()        
        self.textMomRefPnt = QtGui.QLineEdit()        

        # loadCase
        self.textLoadCaseUID  = QtGui.QLineEdit()
        self.textLoadCase     = QtGui.QLineEdit()
        
        # performanceMap one
        # - positiveQuasiSteadyRotation --> see performanceMap two
        # - negativeQuasiSteadyRotation --> see performanceMap two
        self.textCtrlSurUID = QtGui.QLineEdit()
        
        # performanceMap two
        self.textMachNum  = QtGui.QLineEdit()
        self.textReynNum  = QtGui.QLineEdit()
        self.textAngleYaw = QtGui.QLineEdit()
        self.textAngleAtt = QtGui.QLineEdit()
        self.textPositiveSteadi = QtGui.QLineEdit()
        self.textNegativeSteadi = QtGui.QLineEdit()
        self.textCtrlSurfaces   = QtGui.QLineEdit()

    def setupLabels(self):
        # longest label word
        labelNames = ["name", "version", "aircraftModelUID", "datasetName", "area", "lengthCMX", "lengthCMY", "lengthCMZ", "momentReferencePoint",
                      "loadCaseUID", "loadCase", "controlSurfaceUID", "MachNumber", "ReynoldsNumber", "angleOfYaw", "angleOfAttack", 
                      "positiveQuasiSteadyRotation", "negativeQuasiSteadyRotation", "controlSurfaces"]
        
        maxlength = max(len(s) for s in labelNames)
        nameList  =  labelNames #map(lambda x : x.rjust(maxlength), labelNames)
        
        # tool
        self.labelName = QtGui.QLabel(nameList[0])
        self.labelVers   = QtGui.QLabel(nameList[1])
        
        # aircraftModelUID
        self.labelAMUID = QtGui.QLabel(nameList[2])         
        # datasetName
        self.labelDSet = QtGui.QLabel(nameList[3])        
        
        # referenceValues 
        self.labelArea      = QtGui.QLabel(nameList[4])        
        self.labelLenCmx    = QtGui.QLabel(nameList[5])        
        self.labelLenCmy    = QtGui.QLabel(nameList[6])        
        self.labelLenCmz    = QtGui.QLabel(nameList[7])        
        self.labelMomRefPnt = QtGui.QLabel(nameList[8])         

        # loadCase
        self.labelLoadCaseUID = QtGui.QLabel(nameList[9])
        self.labelLoadCase    = QtGui.QLabel(nameList[10])

        # performanceMap two
        self.labelCtrlSurUID = QtGui.QLabel(nameList[11]) 

        # performanceMap two
        self.labelMachNum = QtGui.QLabel(nameList[12])
        self.labelReynNum = QtGui.QLabel(nameList[13])
        self.labelAngleYaw = QtGui.QLabel(nameList[14])
        self.labelAngleAtt = QtGui.QLabel(nameList[15])
        self.labelPositiveSteadi = QtGui.QLabel(nameList[16])
        self.labelNegativeSteadi = QtGui.QLabel(nameList[17])
        self.labelCtrlSurfaces = QtGui.QLabel(nameList[18])

    def setupToolTips(self):
        self.textName.setToolTip("name of tool")        
        self.textVers.setToolTip("version of tool")
        self.textAMUID.setToolTip("reference to aircraft model")
        self.textDSet.setToolTip("name of the dataset for LIFTING_LINE calculation") 

    def setupButtons(self):
        self.buttonBox = QtGui.QDialogButtonBox()
        self.buttonBox.addButton("ok", QtGui.QDialogButtonBox.AcceptRole)
        self.buttonBox.addButton("cancel", QtGui.QDialogButtonBox.RejectRole)        
        
        self.butOpenTool             = QtGui.QPushButton("Tool")
        self.butOpenAircraftModelUID = QtGui.QPushButton("aircraftModelUID")        
        self.butOpenDataSetName      = QtGui.QPushButton("datasetName")        
        self.butOpenReferenceValues  = QtGui.QPushButton("referenceValues")        
        self.butOpenLCasesAndPerMap  = QtGui.QPushButton("loadCase performanceMap") 

        self.butOpenTool.setStyleSheet("background-color:#98AFC7; border-style: outset; border-width: 2px; border-radius: 10px;border-color: beige;font: bold 14px;min-width: 10em; padding: 2px;")
        self.butOpenAircraftModelUID.setStyleSheet("background-color:#98AFC7; border-style: outset; border-width: 2px; border-radius: 10px;border-color: beige;font: bold 14px;min-width: 10em; padding: 2px;")
        self.butOpenDataSetName.setStyleSheet("background-color:#98AFC7; border-style: outset; border-width: 2px; border-radius: 10px;border-color: beige;font: bold 14px;min-width: 10em; padding: 2px;")
        self.butOpenReferenceValues.setStyleSheet("background-color:#98AFC7; border-style: outset; border-width: 2px; border-radius: 10px;border-color: beige;font: bold 14px;min-width: 10em; padding: 2px;")
        self.butOpenLCasesAndPerMap.setStyleSheet("background-color:#98AFC7; border-style: outset; border-width: 2px; border-radius: 10px;border-color: beige;font: bold 14px;min-width: 10em; padding: 2px;")
        
        self.flagButTool = True
        self.flagButAir  = True
        self.flagButData = True
        self.flagButRef  = True
        self.flagButCase = True
        
        self.buttonBox.accepted.connect(self.submitInput) 
        self.buttonBox.rejected.connect(self.close)          
        self.butOpenTool.clicked.connect(self.__visibilityTool)       
        self.butOpenAircraftModelUID.clicked.connect(self.__visibilityAircraftModelUID)       
        self.butOpenDataSetName.clicked.connect(self.__visibilityDataSetName)       
        self.butOpenReferenceValues.clicked.connect(self.__visibilityReferenceValues)       
        self.butOpenLCasesAndPerMap.clicked.connect(self.__visibilityLoadCasePerMap)       

        self.butOpenAircraftModelUID.click()
        self.butOpenDataSetName.click()
        self.butOpenReferenceValues.click()
        self.butOpenLCasesAndPerMap.click()

    def setupGroupBoxes(self):
        # loadCases vs performanceMap
        self.groupBoxCaseVsPerMap = QtGui.QGroupBox()
        grid   = QtGui.QGridLayout()
        self.radioCaseVsPerMap1 = QtGui.QRadioButton("&loadCases")
        self.radioCaseVsPerMap2 = QtGui.QRadioButton("&performanceMap")
        grid.addWidget(self.radioCaseVsPerMap1,0,1)
        grid.addWidget(self.radioCaseVsPerMap2,0,2)
        self.groupBoxCaseVsPerMap.setLayout(grid)
        self.groupBoxCaseVsPerMap.setFlat(True)        

        # loadCases
        self.groupBoxLoadCases = QtGui.QGroupBox()
        grid = QtGui.QGridLayout()
        self.radioLoadCases1 = QtGui.QRadioButton("&loadCaseUID")
        self.radioLoadCases2 = QtGui.QRadioButton("&loadCase")
        grid.addWidget(self.radioLoadCases1,0,1)
        grid.addWidget(self.radioLoadCases2,0,2)
        self.groupBoxLoadCases.setLayout(grid)
        self.groupBoxLoadCases.setFlat(True)   

        # performanceMap
        self.groupBoxPerMap = QtGui.QGroupBox()
        grid   = QtGui.QGridLayout()
        self.radioPerMap1 = QtGui.QRadioButton("performanceMap one")
        self.radioPerMap2 = QtGui.QRadioButton("performanceMap two")
        grid.addWidget(self.radioPerMap1,0,1)
        grid.addWidget(self.radioPerMap2,0,2)
        self.groupBoxPerMap.setLayout(grid)
        self.groupBoxPerMap.setFlat(True)  


        self.__hideCaseAndPerMap()

        self.radioCaseVsPerMap1.toggled.connect(self.showLoadCase)
        self.radioCaseVsPerMap2.toggled.connect(self.showPerMap)
        
        self.radioLoadCases1.toggled.connect(self.__showLoadCaseUID)
        self.radioLoadCases2.toggled.connect(self.__showLoadCase)
        
        self.radioPerMap1.toggled.connect(self.__setPerMap_1)        
        self.radioPerMap2.toggled.connect(self.__setPerMap_2)        


    def showLoadCase(self, b):
        self.groupBoxLoadCases.setVisible(b)
        self.__setPerMap_1(False)
        self.__setPerMap_2(False)

        if self.radioLoadCases1.isChecked() :
            self.__setLoadCase_1(True)
        elif self.radioLoadCases2.isChecked() :
            self.__setLoadCase_2(True)

    def showPerMap(self, b):
        self.groupBoxPerMap.setVisible(b) 
        self.__setLoadCase_1(False)
        self.__setLoadCase_2(False)
        
        if self.radioPerMap1.isChecked() :
            self.__setPerMap_1(True)
        elif self.radioPerMap2.isChecked() :
            self.__setPerMap_2(True)
        
    def __showLoadCaseUID(self, b):
        self.__setLoadCase_1(b)
    
    def __showLoadCase(self, b):  
        self.__setLoadCase_2(b)

    def __setLoadCase_1(self, b):
        self.labelLoadCaseUID.setVisible(b)
        self.textLoadCaseUID.setVisible(b)

    def __setLoadCase_2(self, b):        
        self.labelLoadCase.setVisible(b)
        self.textLoadCase.setVisible(b) 

    def __setPerMap_1(self, b):
        self.labelPositiveSteadi.setVisible(b)
        self.labelNegativeSteadi.setVisible(b)
        self.labelCtrlSurUID.setVisible(b)

        self.textPositiveSteadi.setVisible(b)
        self.textNegativeSteadi.setVisible(b)
        self.textCtrlSurUID.setVisible(b)

    def __setPerMap_2(self, b):
        self.labelMachNum.setVisible(b)
        self.labelReynNum.setVisible(b)         
        self.labelAngleYaw.setVisible(b)
        self.labelAngleAtt.setVisible(b)
        self.labelPositiveSteadi.setVisible(b)
        self.labelNegativeSteadi.setVisible(b)
        self.labelCtrlSurfaces.setVisible(b)

        self.textMachNum.setVisible(b)
        self.textReynNum.setVisible(b)         
        self.textAngleYaw.setVisible(b)
        self.textAngleAtt.setVisible(b)
        self.textPositiveSteadi.setVisible(b)
        self.textNegativeSteadi.setVisible(b)
        self.textCtrlSurfaces.setVisible(b)  

    def __visibilityTool(self):
        self.flagButTool = not self.flagButTool
        self.labelName.setVisible(self.flagButTool)
        self.labelVers.setVisible(self.flagButTool)
        self.textName.setVisible(self.flagButTool)
        self.textVers.setVisible(self.flagButTool)

    def __visibilityAircraftModelUID(self):
        self.flagButAir = not self.flagButAir
        self.labelAMUID.setVisible(self.flagButAir)
        self.textAMUID.setVisible(self.flagButAir)

    def __visibilityDataSetName (self):
        self.flagButData = not self.flagButData
        self.labelDSet.setVisible(self.flagButData)
        self.textDSet.setVisible(self.flagButData)

    def __visibilityReferenceValues(self):
        self.flagButRef = not self.flagButRef
        self.labelArea.setVisible(self.flagButRef)
        self.labelLenCmx.setVisible(self.flagButRef)
        self.labelLenCmy.setVisible(self.flagButRef)
        self.labelLenCmz.setVisible(self.flagButRef)
        self.labelMomRefPnt.setVisible(self.flagButRef)
        self.textArea.setVisible(self.flagButRef)
        self.textLenCmx.setVisible(self.flagButRef)
        self.textLenCmy.setVisible(self.flagButRef)
        self.textLenCmz.setVisible(self.flagButRef)
        self.textMomRefPnt.setVisible(self.flagButRef)    
    
    def __visibilityLoadCasePerMap(self):
        self.flagButCase = not self.flagButCase
        self.groupBoxCaseVsPerMap.setVisible(self.flagButCase)
        if not self.flagButCase :
            self.__hideCaseAndPerMap()   
        elif self.radioCaseVsPerMap1.isChecked():
            self.showLoadCase(True)
        elif self.radioCaseVsPerMap2.isChecked():
            self.showPerMap(True)


    def __hideCaseAndPerMap(self):
        self.groupBoxLoadCases.hide()
        self.groupBoxPerMap.hide()
        
        self.__setLoadCase_1(False)
        self.__setLoadCase_2(False)
        self.__setPerMap_1(False)
        self.__setPerMap_2(False)
        
    def __getSeperator(self):
        line = QtGui.QFrame()
        line.setFrameShape(QtGui.QFrame.HLine)
        line.setFrameShadow(QtGui.QFrame.Sunken)        
        return line
    
    def getValuesTool(self):
        return self.textName.text() , self.textVers.text()
    
    def getValuesAircraftModelUID(self):
        return self.textAMUID.text()
    
    def getValuesDatasetName(self):
        return self.textDSet.text()
    
    def getValuesReferenceValues(self):
        return self.textArea.text() , self.textLenCmx.text() ,self.textLenCmy.text(), self.textLenCmz.text()
    
    def getValuesLoadCasesLoadCaseUID(self):
        return self.textLoadCaseUID.text()
    
    def getValuesLoadCasesLoadCase(self):
        return self.textLoadCase.text()

    def getValuesPerformanceMap_1(self):
        return self.textPositiveSteadi.text() , self.textNegativeSteadi.text(), self.textCtrlSurUID.text()

    def getValuesPerformanceMap_2(self):
        return self.textMachNum.text(), self.textReynNum.text(), self.textAngleYaw.text(), self.textAngleAtt.text(), self.textPositiveSteadi.text(), self.textNegativeSteadi.text(), self.textCtrlSurfaces.text()
        

    def keyPressEvent(self, event):
        if event.modifiers() & QtCore.Qt.ControlModifier:
            if event.key() == QtCore.Qt.Key_1:
                self.layout().setSizeConstraint(QtGui.QLayout.SetFixedSize)
            if event.key() == QtCore.Qt.Key_2:
                self.layout().setSizeConstraint(QtGui.QLayout.SetMinAndMaxSize)

    @utility.overrides(PopUpTool)    
    def setupWidget(self):
        self.setupLabels()
        self.setupInputFields()
        self.setupGroupBoxes()
        self.setupButtons()
        self.setupToolTips() 
        

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