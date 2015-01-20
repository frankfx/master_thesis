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
    
    def setupToolTips(self):
        self.textName.setToolTip("name of tool")        
        self.textVers.setToolTip("version of tool")
        self.textAMUID.setToolTip("reference to aircraft model")
        self.textDSet.setToolTip("name of the dataset for LIFTING_LINE calculation")    
    
    def setupLabels(self):
        # longest label word
        labelNames = ["name", "version", "aircraftModelUID", "datasetName", "area", "lengthCMX", "lengthCMY", "lengthCMZ", "momentReferencePoint",
                      "loadCaseUID", "loadCase", "controlSurfaceUID", "MachNumber", "ReynoldsNumber", "angleOfYaw", "angleOfAttack", 
                      "positiveQuasiSteadyRotation", "negativeQuasiSteadyRotation", "controlSurfaces"]
        
        maxlength = max(len(s) for s in labelNames)
        nameList  = map(lambda x : x.rjust(maxlength), labelNames)
        
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
        layout.addRow(self.butOpenTool)
        layout.addRow(self.labelName, self.textName)
        layout.addRow(self.labelVers, self.textVers)
        layout.addRow(self.butOpenAircraftModelUID)        
        layout.addRow(self.__getSeperator())
        layout.addRow(self.labelAMUID, self.textAMUID)
        layout.addRow(self.butOpenDataSetName)
        layout.addRow(self.labelDSet, self.textDSet)
        layout.addRow(self.__getSeperator())
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
        
        #self.listWidget = QtGui.QListWidget()
        #self.listWidget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        #self.listWidget.addItem(QtGui.QListWidgetItem("Oak"))
        
        #mainLayout.addWidget(self.listWidget)
        
        self.setLayout(mainLayout)
        self.layout().setSizeConstraint(QtGui.QLayout.SetFixedSize)

    @utility.overrides(PopUpTool)    
    def setupWidget(self):
        self.setupLabels()
        self.setupInputFields()
        self.setupGroupBoxes()
        self.setupButtons()
        self.setupToolTips()

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

    def setupButtons(self):
        self.buttonBox = QtGui.QDialogButtonBox()
        self.buttonBox.addButton("ok", QtGui.QDialogButtonBox.AcceptRole)
        self.buttonBox.addButton("cancel", QtGui.QDialogButtonBox.RejectRole)        
        
        self.butOpenTool             = QtGui.QPushButton("Tool")
        self.butOpenAircraftModelUID = QtGui.QPushButton("aircraftModelUID")        
        self.butOpenDataSetName      = QtGui.QPushButton("datasetName")        
        self.butOpenReferenceValues  = QtGui.QPushButton("referenceValues")        
        self.butOpenLCasesAndPerMap  = QtGui.QPushButton("loadCases & performanceMap") 
        
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
      #  self.butOpenLCasesAndPerMap.clicked.connect(self.__button_visibility_case_map)       

        #self.butOpenAircraftModelUID.click()
        #self.butOpenDataSetName.click()
        #self.butOpenReferenceValues.click()
        #self.butOpenLCasesAndPerMap.click()

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


        self.radioCaseVsPerMap1.toggled.connect(self.__setCaseVisible)
        self.radioCaseVsPerMap2.toggled.connect(self.__setPerMapVisible)
        
        self.radioLoadCases1.toggled.connect(self.__setLoadCaseUIDVisible)
        self.radioLoadCases2.toggled.connect(self.__setLoadCaseVisible)
        
        self.radioPerMap1.toggled.connect(self.__setPerMapFSTVisible)        
        self.radioPerMap2.toggled.connect(self.__setPerMapSNDVisible)        



    def __setCaseVisible(self, b):
        self.groupBoxLoadCases.setVisible(b)
        if b == False :
            self.__setLoadCase_1(b)
            self.__setLoadCase_2(b) 
        elif self.radioLoadCases1.isChecked() :
            self.__setLoadCase_1(b)
        elif self.radioLoadCases2.isChecked() :
            self.__setLoadCase_2(b) 
        else :
            print "toggled"
            self.radioLoadCases1.toggle()

    def __setPerMapVisible(self, b):
        self.groupBoxPerMap.setVisible(b) 
        if self.radioPerMap1.isChecked() :
            self.__setPerMapFSTVisible(b)
        elif self.radioPerMap2.isChecked() :
            self.__setPerMapSNDVisible(b) 
        else :
            print "toggled"
            self.radioPerMap1.toggle()        
        
        
    def __setLoadCaseUIDVisible(self, b):
        self.__setLoadCase_1(b)
    
    def __setLoadCaseVisible(self, b):  
        self.__setLoadCase_2(b)
        
    def __setPerMapFSTVisible(self, b):   
        pass 
        #self.__setPerMapFSTVisible(b)

    def __setPerMapSNDVisible(self, b):
        pass
        
        #self.radioCaseVsPerMap1.toggle()


    #----------------------------------- def __button_visibility_case_map(self):
        #------------------------------- self.flagButCase = not self.flagButCase
#------------------------------------------------------------------------------ 
        #---------------- self.groupBoxCaseVsPerMap.setVisible(self.flagButCase)
#------------------------------------------------------------------------------ 
        #------------------------------------------------- if self.flagButCase :
            #-------------------------- if self.radioCaseVsPerMap1.isChecked() :
                #------------------------------- self.__setCaseVsPerMapVisible(True)
            #------------------------ elif self.radioCaseVsPerMap2.isChecked() :
                #----------------------------- self.__setLoadPerMapVisible(True)
            #------------------------------------------------------------ else :
                #------------------------------ self.radioCaseVsPerMap1.toggle()
        #---------------------------------------------------------------- else :
            #---------------------------------------- self.__hideCaseAndPerMap()
        
     

     
        
    def __hideCaseAndPerMap(self):
        self.groupBoxLoadCases.hide()
        self.groupBoxPerMap.hide()
        
        self.__setLoadCase_1(False)
        self.__setLoadCase_2(False)
        self.__setVisiblePerMap_1(False)
        self.__setVisiblePerMap_2(False)
        







    def setLoadCase(self, b):
        self.__setLoadCase_1(b)
        self.__setLoadCase_2(not b)

    def setVisiblePerMap(self, b):
        self.__setVisiblePerMap_1(b)
        self.__setVisiblePerMap_2(not b)






    def __setLoadCase_1(self, b):
        self.labelLoadCaseUID.setVisible(b)
        self.textLoadCaseUID.setVisible(b)

    def __setLoadCase_2(self, b):        
        self.labelLoadCase.setVisible(b)
        self.textLoadCase.setVisible(b)        

    def __setVisiblePerMap_1(self, b):
        self.labelPositiveSteadi.setVisible(b)
        self.labelNegativeSteadi.setVisible(b)
        self.labelCtrlSurUID.setVisible(b)

        self.textPositiveSteadi.setVisible(b)
        self.textNegativeSteadi.setVisible(b)
        self.textCtrlSurUID.setVisible(b)

    def __setVisiblePerMap_2(self, b):
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
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    def __getSeperator(self):
        line = QtGui.QFrame()
        line.setFrameShape(QtGui.QFrame.HLine)
        line.setFrameShadow(QtGui.QFrame.Sunken)        
        return line
        

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