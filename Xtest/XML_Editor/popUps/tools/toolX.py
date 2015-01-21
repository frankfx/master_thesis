'''
Created on Jan 14, 2015

@author: fran_re
'''

from PySide import QtGui, QtCore
from popUp_tool import PopUpTool
from Xtest.XML_Editor.externTools import difficultTestTool
from Xtest.Open_GL import utility
from pylab import *
from Xtest.XML_Editor.configuration.config import Config
import os

from tixiwrapper   import Tixi, TixiException

class ToolX(PopUpTool):
    def __init__(self, name, width=300, height=700):
        super(ToolX, self).__init__(name, width, height)          
        
        self.setupWidget()
        self.initTixi()
                
        layout = QtGui.QFormLayout()
        layout.addRow(self.butOpenTool)
        layout.addRow(self.labelName, self.textName)
        layout.addRow(self.labelVers, self.textVers)
        layout.addRow(self.butOpenAircraftModelUID)        
        layout.addRow(self.gridAMUID)
        layout.addRow(self.butOpenDataSetName)
        layout.addRow(self.labelCheckDSet, self.checkDataset)
        layout.addRow(self.labelDSet, self.textDSet)
        layout.addRow(self.butOpenLCasesAndPerMap)
        layout.addRow(self.groupBoxCaseVsPerMap)
        layout.addRow(self.labelLoadCaseUID, self.textLoadCaseUID)
        layout.addRow(self.labelPositiveSteadi, self.textPositiveSteadi)
        layout.addRow(self.labelNegativeSteadi, self.textNegativeSteadi)
        layout.addRow(self.labelCtrlSurUID, self.textCtrlSurUID)
        layout.addRow(self.butOpenToolParameters)
        layout.addRow(self.labelUsePOLINT, self.textUsePOLINT)
        layout.addRow(self.labelArchiveMode, self.textArchiveMode)
        layout.addRow(self.labelParallelComputation, self.textParallelComputation)
        layout.addRow(self.labelCheckWingUID, self.checkWingUID)
        layout.addRow(self.labelWingUID, self.textWingUID)
        layout.addRow(self.labelSpanwise, self.textSpanwise)
        layout.addRow(self.labelchordwise, self.textChordwise)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addLayout(layout)
        mainLayout.addWidget(self.buttonBox)
        
        self.setLayout(mainLayout)
        
    def enableTextDatasetName(self, n):
        self.textDSet.setEnabled(n)

    def enableTextWingUID(self, n):
        self.textWingUID.setEnabled(n)


    def setupInputFields(self):
        # tool
        self.textName = QtGui.QLineEdit()
        self.textVers = QtGui.QLineEdit()
        
        # aircraftModelUID
        self.listAMUID1 = QtGui.QListWidget()
        self.listAMUID2 = QtGui.QListWidget()
        self.butLeft    = QtGui.QPushButton()
        self.butRight   = QtGui.QPushButton()
        self.gridAMUID  = QtGui.QGridLayout()

        self.butLeft.setIcon(QtGui.QIcon(Config.path_but_left_icon))
        self.butLeft.setIconSize(QtCore.QSize(10,10))
        self.butLeft.clicked.connect(self.modelUIDSwitchLeft) 

        self.butRight.setIcon(QtGui.QIcon(Config.path_but_right_icon))
        self.butRight.setIconSize(QtCore.QSize(10,10))   
        self.butRight.clicked.connect(self.modelUIDSwitchRight)

        self.gridAMUID.addWidget(self.labelAMUID1, 0,0)
        self.gridAMUID.addWidget(self.labelAMUID2, 0,3)
        self.gridAMUID.addWidget(self.listAMUID1, 1,0, 2, 1)
        self.gridAMUID.addWidget(self.butLeft, 1,1)
        self.gridAMUID.addWidget(self.butRight, 2,1)
        self.gridAMUID.addWidget(self.listAMUID2, 1,3, 2, 1)


        # datasetName
        self.textDSet = QtGui.QLineEdit()
        self.textDSet.setDisabled(True)
        self.checkDataset = QtGui.QCheckBox()
        self.checkDataset.stateChanged.connect(self.enableTextDatasetName)
        
        # loadCase
        self.textLoadCaseUID  = QtGui.QListWidget()
        self.textLoadCaseUID.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        
        # performanceMap 
        self.textPositiveSteadi = QtGui.QLineEdit()
        self.textNegativeSteadi = QtGui.QLineEdit()
        self.textCtrlSurUID = QtGui.QLineEdit()
        
        # tool parameters
        self.textUsePOLINT = QtGui.QComboBox()
        self.textUsePOLINT.addItem("True")
        self.textUsePOLINT.addItem("False")
        
        self.textArchiveMode = QtGui.QComboBox()
        self.textArchiveMode.addItem("0=logfile")
        self.textArchiveMode.addItem("1=log+inputfiles")
        self.textArchiveMode.addItem("2=all results")
        
        self.textParallelComputation = QtGui.QLineEdit()
        self.textParallelComputation.setValidator(QtGui.QIntValidator(0, 10000, self) )       
        

        self.textSpanwise  = QtGui.QLineEdit()        
        self.textChordwise = QtGui.QLineEdit()        
        self.textWingUID   = QtGui.QLineEdit()
        self.textWingUID.setDisabled(True)        
        self.checkWingUID  = QtGui.QCheckBox()
        self.checkWingUID.stateChanged.connect(self.enableTextWingUID)

        

    def initTixi(self, path = Config.path_cpacs_D150_2):
        self.tixi = Tixi() 
        self.tixi.openDocument(path)
        
        if self.tixiValidateXPath("/cpacs/toolspecific/liftingLine") :
            self.tixiSetAircraftModelUID() 
        else:
            QtGui.QMessageBox.about(self, "error", "no toolspecific found in the given file path : %s" % path)
            sys.exit()
        
        
    def tixiValidateXPath(self, xpath):
        try:
            return self.tixi.xPathEvaluateNodeNumber(xpath)
        except Exception :
            return False
        
    
    def tixiSetToolName(self):
        self.textName.setText(self.tixi.getTextElement("/cpacs/toolspecific/liftingLine/tool/name"))

    def tixiSetToolVersion(self):
        self.textVers.setText(self.tixi.getTextElement("/cpacs/toolspecific/liftingLine/tool/name[1]"))
        
    def tixiSetAircraftModelUID(self):
        tmp_list = []
        for j in range(1, self.tixi.getNamedChildrenCount("/cpacs/toolspecific/liftingLine", "aircraftModelUID") + 1) :
            item = self.tixi.getTextElement("/cpacs/toolspecific/liftingLine/aircraftModelUID["+str(j)+"]")
            self.listAMUID2.addItem(item)
            tmp_list.append(item)
       
        for i in range(1, self.tixi.getNamedChildrenCount("/cpacs/vehicles/aircraft", "model") + 1) :
            item = self.tixi.getTextAttribute("/cpacs/vehicles/aircraft/model[" + str(i) +"]" , 'uID')
            if not item in tmp_list:
                self.listAMUID1.addItem(item)


    def tixiSetDatasetName(self):
        if self.tixiValidateXPath("/cpacs/toolspecific/liftingLine/datasetName"):
            self.textDSet.setText(self.tixi.getTextElement("/cpacs/toolspecific/liftingLine/datasetName"))        
    
    def tixiSetLoadCaseUID(self):
        for i in range(1, self.tixi.getNamedChildrenCount("/cpacs/vehicles/aircraft/model/analyses/loadAnalysis/loadCases", "flightLoadCase") + 1) :
            print "available"
            print self.tixi.getTextAttribute("/cpacs/vehicles/aircraft/model/analyses/loadAnalysis/loadCases/flightLoadCase["+str(i)+"]" , 'uID')
        
        for i in range(1, self.tixi.getNamedChildrenCount("/cpacs/toolspecific/liftingLine/loadCases", "loadCaseUID") + 1) :
            print "chosen uids"
            print self.tixi.getTextElement("/cpacs/toolspecific/liftingLine/loadCases/loadCaseUID["+str(i)+"]")
        
   
        

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
        self.labelAMUID1 = QtGui.QLabel("available uids")
        self.labelAMUID2 = QtGui.QLabel("chosen uids")
        
        # datasetName
        self.labelDSet = QtGui.QLabel(nameList[3])               
        self.labelCheckDSet= QtGui.QLabel("set")

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
        
        # tool parameters
        self.labelUsePOLINT      = QtGui.QLabel("usePOLINT")
        self.labelArchiveMode    = QtGui.QLabel("archiveMode")
        self.labelParallelComputation = QtGui.QLabel("parallelComputation")
        self.labelCheckWingUID   = QtGui.QLabel("set wingUID")
        self.labelWingUID        = QtGui.QLabel("wingUID")
        self.labelSpanwise       = QtGui.QLabel("spanwise")
        self.labelchordwise      = QtGui.QLabel("chordwise")

    def setupToolTips(self):
        self.textName.setToolTip("name of tool")        
        self.textVers.setToolTip("version of tool")
        self.textDSet.setToolTip("name of the dataset for LIFTING_LINE calculation") 
        self.textParallelComputation.setToolTip("0=parallel computation on all available cores\n1=sequencial computation\nn=parallel computation on n cores")

    def setupButtons(self):
        # create buttons
        self.buttonBox = QtGui.QDialogButtonBox()
        self.buttonBox.addButton("ok", QtGui.QDialogButtonBox.AcceptRole)
        self.buttonBox.addButton("cancel", QtGui.QDialogButtonBox.RejectRole)        
        
        self.butOpenTool             = QtGui.QPushButton("Tool")
        self.butOpenAircraftModelUID = QtGui.QPushButton("aircraftModelUID")        
        self.butOpenDataSetName      = QtGui.QPushButton("datasetName*")        
        self.butOpenLCasesAndPerMap  = QtGui.QPushButton("loadCase performanceMap") 
        self.butOpenToolParameters   = QtGui.QPushButton("toolParameters")

        # style buttons
        self.butOpenTool.setStyleSheet("background-color:#98AFC7; border-style: outset; border-width: 2px; border-radius: 10px;border-color: beige;font: bold 14px;min-width: 10em; padding: 2px;")
        self.butOpenAircraftModelUID.setStyleSheet("background-color:#98AFC7; border-style: outset; border-width: 2px; border-radius: 10px;border-color: beige;font: bold 14px;min-width: 10em; padding: 2px;")
        self.butOpenDataSetName.setStyleSheet("background-color:#98AFC7; border-style: outset; border-width: 2px; border-radius: 10px;border-color: beige;font: bold 14px;min-width: 10em; padding: 2px;")
        self.butOpenLCasesAndPerMap.setStyleSheet("background-color:#98AFC7; border-style: outset; border-width: 2px; border-radius: 10px;border-color: beige;font: bold 14px;min-width: 10em; padding: 2px;")
        self.butOpenToolParameters.setStyleSheet("background-color:#98AFC7; border-style: outset; border-width: 2px; border-radius: 10px;border-color: beige;font: bold 14px;min-width: 10em; padding: 2px;")
        
        # connect buttons
        self.flagButTool = True
        self.flagButAir  = True
        self.flagButData = True
        self.flagButCase = True
        self.flagButTPar = True
        
        self.buttonBox.accepted.connect(self.submitInput) 
        self.buttonBox.rejected.connect(self.close)       
        self.butOpenTool.clicked.connect(self.__visibilityTool)       
        self.butOpenAircraftModelUID.clicked.connect(self.__visibilityAircraftModelUID)       
        self.butOpenDataSetName.clicked.connect(self.__visibilityDataSetName)       
        self.butOpenLCasesAndPerMap.clicked.connect(self.__visibilityLoadCasePerMap)       
        self.butOpenToolParameters.clicked.connect(self.__visibilityToolParameters)       

        self.butOpenAircraftModelUID.click()
        self.butOpenDataSetName.click()
        self.butOpenLCasesAndPerMap.click()
        self.butOpenToolParameters.click()

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

        #self.__hideCaseAndPerMap()

        self.radioCaseVsPerMap1.toggled.connect(self.showLoadCase)
        self.radioCaseVsPerMap2.toggled.connect(self.showPerMap)
        

    def showLoadCase(self, b):
        self.labelLoadCaseUID.setVisible(b)
        self.textLoadCaseUID.setVisible(b)

    def showPerMap(self, b):
        self.labelPositiveSteadi.setVisible(b)
        self.labelNegativeSteadi.setVisible(b)
        self.labelCtrlSurUID.setVisible(b)

        self.textPositiveSteadi.setVisible(b)
        self.textNegativeSteadi.setVisible(b)
        self.textCtrlSurUID.setVisible(b)        

    def __visibilityTool(self):
        self.flagButTool = not self.flagButTool
        self.labelName.setVisible(self.flagButTool)
        self.labelVers.setVisible(self.flagButTool)
        self.textName.setVisible(self.flagButTool)
        self.textVers.setVisible(self.flagButTool)

    def __visibilityAircraftModelUID(self):
        self.flagButAir = not self.flagButAir
        self.labelAMUID1.setVisible(self.flagButAir)
        self.labelAMUID2.setVisible(self.flagButAir)
        self.listAMUID1.setVisible(self.flagButAir)
        self.listAMUID2.setVisible(self.flagButAir)
        self.butLeft.setVisible(self.flagButAir)
        self.butRight.setVisible(self.flagButAir)

    def __visibilityDataSetName (self):
        self.flagButData = not self.flagButData
        self.labelDSet.setVisible(self.flagButData)
        self.labelCheckDSet.setVisible(self.flagButData)
        self.textDSet.setVisible(self.flagButData)
        self.checkDataset.setVisible(self.flagButData)

    def __visibilityLoadCasePerMap(self):
        self.flagButCase = not self.flagButCase
        self.groupBoxCaseVsPerMap.setVisible(self.flagButCase)
        
        if not self.flagButCase :
            self.showLoadCase(False)
            self.showPerMap(False)
        elif self.radioCaseVsPerMap1.isChecked():
            self.showLoadCase(True)
        elif self.radioCaseVsPerMap2.isChecked():
            self.showPerMap(True)
        else:
            self.showLoadCase(False)
            self.showPerMap(False)

    def __visibilityToolParameters(self):
        self.flagButTPar = not self.flagButTPar
        self.labelUsePOLINT.setVisible(self.flagButTPar)
        self.labelArchiveMode.setVisible(self.flagButTPar)
        self.labelParallelComputation.setVisible(self.flagButTPar)
        self.labelCheckWingUID.setVisible(self.flagButTPar)
        self.labelWingUID.setVisible(self.flagButTPar)
        self.labelSpanwise.setVisible(self.flagButTPar)
        self.labelchordwise.setVisible(self.flagButTPar)
        
        self.textUsePOLINT.setVisible(self.flagButTPar)
        self.textArchiveMode.setVisible(self.flagButTPar)
        self.textParallelComputation.setVisible(self.flagButTPar)
        self.checkWingUID.setVisible(self.flagButTPar)
        self.textWingUID.setVisible(self.flagButTPar)
        self.textSpanwise.setVisible(self.flagButTPar)
        self.textChordwise.setVisible(self.flagButTPar)

        
    def __getSeperator(self):
        line = QtGui.QFrame()
        line.setFrameShape(QtGui.QFrame.HLine)
        line.setFrameShadow(QtGui.QFrame.Sunken)        
        return line
    
    def getValuesTool(self):
        return self.textName.text() , self.textVers.text()
    
    def getValuesAircraftModelUID(self):
        print "not implemented yet"
        
    def getValuesDatasetName(self):
        return self.textDSet.text()
    
    def getValuesLoadCasesLoadCaseUID(self):
        return self.textLoadCaseUID.text()

    def getValuesPerformanceMap_1(self):
        return self.textPositiveSteadi.text() , self.textNegativeSteadi.text(), self.textCtrlSurUID.text()

    def getValuesPerformanceMap_2(self):
        return self.textMachNum.text(), self.textReynNum.text(), self.textAngleYaw.text(), self.textAngleAtt.text(), self.textPositiveSteadi.text(), self.textNegativeSteadi.text(), self.textCtrlSurfaces.text()
        

    def modelUIDSwitchLeft(self):
        self.switchBetweenLists(self.listAMUID2, self.listAMUID1, False)
      
    def modelUIDSwitchRight(self):
        self.switchBetweenLists(self.listAMUID1, self.listAMUID2, True)      
        
    def switchBetweenLists(self, list1, list2, swap):
        item = list1.currentItem()
        list1.setCurrentItem(None)
        if item is not None :
            if swap and list2.count()>0:
                tmp = list2.takeItem(0)
                list1.takeItem(list1.row(item))
                list2.addItem(item)
                list1.addItem(tmp)                  
            else: 
                list1.takeItem(list1.row(item))
                list2.addItem(item)
      
        


    def modelUIDSwitchLeft2(self):
        self.switchBetweenLists(self.listAMUID2, self.listAMUID1)
      
    def modelUIDSwitchRight2(self):
        self.switchBetweenLists(self.listAMUID1, self.listAMUID2)  

    def switchBetweenLists2(self, list1, list2):
        item = list1.currentItem()
        list1.setCurrentItem(None)
        if item is not None :
            list1.takeItem(list1.row(item))
            list2.addItem(item)
            
            

    
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
        os.system("xsltproc -o " + Config.path_cpacs_test + " " + Config.path_cpacs_inputMapping + " " + Config.path_cpacs_D150_2)
        #os.system("xsltproc -o test.xml mappingInputRaw.xsl D150_CPACS2.0_valid2.xml")

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
            print "error in submitInput"
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