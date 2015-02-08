'''
Created on Jan 14, 2015

@author: fran_re
'''
import os, sys
from PySide import QtGui, QtCore
from Xtest.XML_Editor.popUps.tools.popUp_tool import PopUpTool
from Xtest.XML_Editor.popUps.tools.popUp_FileSettings import PopUpFileSettings
from Xtest import utility
from Xtest.config import Config
from tixiwrapper import Tixi


class ToolX(PopUpTool):
    def __init__(self, name, tixi, width=900, height=900):
        super(ToolX, self).__init__(name, width, height)          
        
        self.setupWidget()
        self.initTixi(tixi)
                
        layout = QtGui.QFormLayout()
        layout.addRow(self.butOpenTool)
        layout.addRow(self.labelName, self.textName)
        layout.addRow(self.labelVers, self.textVers)
        layout.addRow(self.butOpenAircraftModelUID)        
        layout.addRow(self.gridAMUID)
        layout.addRow(self.butOpenDataSetName)
        layout.addRow(self.labelCheckDSet, self.checkDataset)
        layout.addRow(self.labelDataset, self.textDataset)
        layout.addRow(self.butOpenLCasesAndPerMap)
        layout.addRow(self.grid)
        layout.addRow(self.gridLoadCaseUID)
        layout.addRow(self.gridCtrlSurUID)
        layout.addRow(self.gridQuasiSteadyRotation)
        layout.addRow(self.butOpenToolParameters)
        layout.addRow(self.labelUsePOLINT, self.comboUsePOLINT)
        layout.addRow(self.labelArchiveMode, self.comboArchiveMode)
        layout.addRow(self.labelParallelComputation, self.textParallelComputation)
        layout.addRow(self.labelCheckWingUID, self.checkWingUID)
        layout.addRow(self.labelWingUID, self.listWingUID)
        layout.addRow(self.labelSpanwise, self.textSpanwise)
        layout.addRow(self.labelchordwise, self.textChordwise)
        layout.addRow(self.buttonBox)
        
        self.setLayout(layout)
        self.layout().setSizeConstraint(QtGui.QLayout.SetFixedSize)

    ## ========================================================================================================================================================
    ## ========================================================================================================================================================
    ## abstract functions
    ## ========================================================================================================================================================
    ## ========================================================================================================================================================
        
    @utility.overrides(PopUpTool)    
    def setupWidget(self):
        self.setupLabels()
        self.setupInputFields()
        self.setupToolTips()  
        self.setupButtons()
       
    @utility.overrides(PopUpTool)    
    def setConnection(self):
        inMap, outMap, cpacs4lili, xsltproc = self.path_settings.getPathValues()
        
        operation_sys = sys.platform 
        flag = "linux" in operation_sys
        
        self.startInputMapping(flag, Config.path_cpacs_D150_3, Config.path_cpacs_inputMapping)
        self.startCpacs4Lili(flag)
        self.startOutputMapping(flag, Config.path_cpacs_D150_3, Config.path_cpacs_outputMapping)        
      
    def startInputMapping(self, linux, initFile, inputMapping):
        if linux:
            os.system("xsltproc -o " + Config.path_cpacs_test + " " + inputMapping + " " + initFile)
        else :
            os.system("java -Xms512M -Xmx512M -jar " + Config.path_saxon9he +" -s:" + initFile + " -xsl:" + inputMapping + " -o:" + Config.path_cpacs_test2)
    
    def startCpacs4Lili(self, linux):
        if linux:
            return NotImplemented
        else :
            return NotImplemented #os.system("cpacs4Lili -o " + "mapped File", "outfilename")
    
    def startOutputMapping(self, linux, initFile, outputMapping):
        print ("outputmapping" , "init file" , "outputMapping.xsl"  ) 
        
        if linux:
            os.system("xsltproc -o " + Config.path_cpacs_test3 + " " + outputMapping + " " + initFile)
        else :
            os.system("java -Xms512M -Xmx512M -jar " + Config.path_saxon9he +" -s:" + initFile + " -xsl:" + outputMapping + " -o:" + Config.path_cpacs_test3)
          

    def openConfig(self):
        self.path_settings = PopUpFileSettings("path to .. settings")
        self.path_settings.buttonBox.button(QtGui.QDialogButtonBox.Ok).clicked.connect(self.setConnection)
    
    @utility.overrides(PopUpTool)    
    def fire_submitInput(self):
        if not self.tixi.checkElement("/cpacs/toolspecific/liftingLine") :
            print("create new lifting line")
            self.tixiCreateEmptyLiftingLine()
        self.tixiSetToolName()
        self.tixiSetToolVersion()
        self.tixiSetAircraftModelUID()
        self.tixiSetDatasetName()
        self.tixiSetToolParameters()
        wasChosen = self.tixiSetLoadCaseOrPerformanceMap()
        if wasChosen :
            self.tixi.saveDocument("text.xml")
            self.tixi.openDocument("text.xml")
            # self.close()
            return True
        else:
            QtGui.QMessageBox.about(self, "error", "please choose load case or performance map") 
            self.fire_setVisibilityAll(True, True, True, False, True)
            return False

    @utility.overrides(PopUpTool)            
    def fire_submitInputAndStartTool(self):
        if self.fire_submitInput():
            self.setConnection()
    

    ## ========================================================================================================================================================
    ## ========================================================================================================================================================
    ## gui elements
    ## ========================================================================================================================================================
    ## ========================================================================================================================================================

    def setupLabels(self):
        # tool
        self.labelName = QtGui.QLabel("name")
        self.labelVers   = QtGui.QLabel("version")
        
        # aircraftModelUID
        self.labelAMUID1 = QtGui.QLabel("available uids")
        self.labelAMUID2 = QtGui.QLabel("chosen uids")
        
        # datasetName
        self.labelDataset = QtGui.QLabel("aircraftModelUID")               
        self.labelCheckDSet= QtGui.QLabel("set")

        # loadCase
        self.labelLoadCaseUID1 = QtGui.QLabel("available uids")
        self.labelLoadCaseUID2 = QtGui.QLabel("chosen uids")
        
        # performanceMap two
        self.labelCtrlSurUID1 = QtGui.QLabel("available uids")
        self.labelCtrlSurUID2 = QtGui.QLabel("chosen uids")
        
        self.labelCheckCtrlSurUID = QtGui.QLabel("setCtrlSurfaceUIDs")

        # performanceMap two
        self.labelPositiveQuasiSteadyRotation = QtGui.QLabel("positiveQuasiSteadyRotation")
        self.labelPositiveSteadi_pstar = QtGui.QLabel("pstar")
        self.labelPositiveSteadi_qstar = QtGui.QLabel("qstar")
        self.labelPositiveSteadi_rstar = QtGui.QLabel("rstar")

        self.labelNegativeQuasiSteadyRotation = QtGui.QLabel("negativeQuasiSteadyRotation")        
        self.labelNegativeSteadi_pstar = QtGui.QLabel("pstar")
        self.labelNegativeSteadi_qstar = QtGui.QLabel("qstar")
        self.labelNegativeSteadi_rstar = QtGui.QLabel("rstar")
        
        # tool parameters
        self.labelUsePOLINT           = QtGui.QLabel("usePOLINT")
        self.labelArchiveMode         = QtGui.QLabel("archiveMode")
        self.labelParallelComputation = QtGui.QLabel("parallelComputation")
        self.labelCheckWingUID        = QtGui.QLabel("set wingUID")
        self.labelWingUID             = QtGui.QLabel("wingUID")
        self.labelSpanwise            = QtGui.QLabel("spanwise")
        self.labelchordwise           = QtGui.QLabel("chordwise")

    def setupInputFields(self):
        # tool
        self.textName = QtGui.QLineEdit()
        self.textVers = QtGui.QLineEdit()
        
        # aircraftModelUID
        self.listAMUID1    = QtGui.QListWidget()
        self.listAMUID2    = QtGui.QListWidget()
        self.butAMUIDLeft  = QtGui.QPushButton()
        self.butAMUIDRight = QtGui.QPushButton()
        self.gridAMUID     = QtGui.QGridLayout()

        self.listAMUID1.setFixedSize(300,100)
        self.listAMUID2.setFixedSize(300,100)
        self.listAMUID1.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        self.listAMUID1.setSortingEnabled(True)

        self.butAMUIDLeft.setIcon(QtGui.QIcon(Config.path_but_left_icon))
        self.butAMUIDLeft.setIconSize(QtCore.QSize(10,10))
        self.butAMUIDLeft.clicked.connect(self.fire_modelUIDSwitchLeft) 

        self.butAMUIDRight.setIcon(QtGui.QIcon(Config.path_but_right_icon))
        self.butAMUIDRight.setIconSize(QtCore.QSize(10,10))   
        self.butAMUIDRight.clicked.connect(self.fire_modelUIDSwitchRight)

        self.gridAMUID.addWidget(self.labelAMUID1, 0,0)
        self.gridAMUID.addWidget(self.labelAMUID2, 0,3)
        self.gridAMUID.addWidget(self.listAMUID1, 1,0, 2, 1)
        self.gridAMUID.addWidget(self.butAMUIDLeft, 1,1)
        self.gridAMUID.addWidget(self.butAMUIDRight, 2,1)
        self.gridAMUID.addWidget(self.listAMUID2, 1,3, 2, 1)

        # datasetName
        self.textDataset = QtGui.QLineEdit()
        self.textDataset.setDisabled(True)
        self.checkDataset = QtGui.QCheckBox()
        self.checkDataset.stateChanged.connect(self.fire_enableTextDatasetName)
        
        # set up fork between loadCases and performanceMap
        self.grid   = QtGui.QGridLayout()
        self.radioCaseVsPerMap1 = QtGui.QRadioButton("&loadCases")
        self.radioCaseVsPerMap2 = QtGui.QRadioButton("&performanceMap")
        self.grid.addWidget(self.radioCaseVsPerMap1,0,1)
        self.grid.addWidget(self.radioCaseVsPerMap2,0,2)

        self.radioCaseVsPerMap1.toggled.connect(self.fire_showLoadCase)
        self.radioCaseVsPerMap2.toggled.connect(self.fire_showPerMap)        
        
        # loadCase
        self.listLoadCaseUID1    = QtGui.QListWidget()
        self.listLoadCaseUID2    = QtGui.QListWidget()
        self.butLoadCaseUIDLeft  = QtGui.QPushButton()
        self.butLoadCaseUIDRight = QtGui.QPushButton()
        self.gridLoadCaseUID     = QtGui.QGridLayout()


        self.listLoadCaseUID1.setFixedSize(300,100)
        self.listLoadCaseUID2.setFixedSize(300,100)
        self.listLoadCaseUID1.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        self.listLoadCaseUID2.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        self.listLoadCaseUID1.setSortingEnabled(True)
        self.listLoadCaseUID2.setSortingEnabled(True)

        self.butLoadCaseUIDLeft.setIcon(QtGui.QIcon(Config.path_but_left_icon))
        self.butLoadCaseUIDLeft.setIconSize(QtCore.QSize(10,10))
        self.butLoadCaseUIDLeft.clicked.connect(self.fire_loadCaseUIDSwitchLeft) 

        self.butLoadCaseUIDRight.setIcon(QtGui.QIcon(Config.path_but_right_icon))
        self.butLoadCaseUIDRight.setIconSize(QtCore.QSize(10,10))   
        self.butLoadCaseUIDRight.clicked.connect(self.fire_loadCaseUIDSwitchRight)

        self.gridLoadCaseUID.addWidget(self.labelLoadCaseUID1, 0,0)
        self.gridLoadCaseUID.addWidget(self.labelLoadCaseUID2, 0,3)
        self.gridLoadCaseUID.addWidget(self.listLoadCaseUID1, 1,0, 2, 1)
        self.gridLoadCaseUID.addWidget(self.butLoadCaseUIDLeft, 1,1)
        self.gridLoadCaseUID.addWidget(self.butLoadCaseUIDRight, 2,1)
        self.gridLoadCaseUID.addWidget(self.listLoadCaseUID2, 1,3, 2, 1)

        # performanceMap 
        self.gridQuasiSteadyRotation = QtGui.QGridLayout()
        
        self.textPositiveSteadi_pstar = QtGui.QLineEdit()
        self.textPositiveSteadi_qstar = QtGui.QLineEdit()
        self.textPositiveSteadi_rstar = QtGui.QLineEdit()

        self.textNegativeSteadi_pstar = QtGui.QLineEdit()
        self.textNegativeSteadi_qstar = QtGui.QLineEdit()
        self.textNegativeSteadi_rstar = QtGui.QLineEdit()
        
        self.textPositiveSteadi_pstar.setEnabled(False)
        self.textPositiveSteadi_qstar.setEnabled(False)
        self.textPositiveSteadi_rstar.setEnabled(False)
        self.textNegativeSteadi_pstar.setEnabled(False)
        self.textNegativeSteadi_qstar.setEnabled(False)
        self.textNegativeSteadi_rstar.setEnabled(False)
        
        self.textPositiveSteadi_pstar.setValidator(QtGui.QDoubleValidator())
        self.textPositiveSteadi_qstar.setValidator(QtGui.QDoubleValidator())
        self.textPositiveSteadi_rstar.setValidator(QtGui.QDoubleValidator())
        self.textNegativeSteadi_pstar.setValidator(QtGui.QDoubleValidator())
        self.textNegativeSteadi_qstar.setValidator(QtGui.QDoubleValidator())
        self.textNegativeSteadi_rstar.setValidator(QtGui.QDoubleValidator())
                
        self.checkPos_pstar = QtGui.QCheckBox()
        self.checkPos_qstar = QtGui.QCheckBox()
        self.checkPos_rstar = QtGui.QCheckBox()
        
        self.checkNeg_pstar = QtGui.QCheckBox()
        self.checkNeg_qstar = QtGui.QCheckBox()
        self.checkNeg_rstar = QtGui.QCheckBox()

        self.gridQuasiSteadyRotation.addWidget(self.labelPositiveQuasiSteadyRotation,0 ,0, 1, 3)
        self.gridQuasiSteadyRotation.addWidget(self.checkPos_pstar, 1, 0)        
        self.gridQuasiSteadyRotation.addWidget(self.checkPos_qstar, 2, 0)        
        self.gridQuasiSteadyRotation.addWidget(self.checkPos_rstar, 3, 0)        
        self.gridQuasiSteadyRotation.addWidget(self.labelPositiveSteadi_pstar, 1, 1)        
        self.gridQuasiSteadyRotation.addWidget(self.labelPositiveSteadi_qstar, 2, 1)
        self.gridQuasiSteadyRotation.addWidget(self.labelPositiveSteadi_rstar, 3, 1)
        self.gridQuasiSteadyRotation.addWidget(self.textPositiveSteadi_pstar,  1, 2)
        self.gridQuasiSteadyRotation.addWidget(self.textPositiveSteadi_qstar,  2, 2)
        self.gridQuasiSteadyRotation.addWidget(self.textPositiveSteadi_rstar,  3, 2)
        
        self.gridQuasiSteadyRotation.addWidget(self.labelNegativeQuasiSteadyRotation, 0, 3, 1, 3)   
        self.gridQuasiSteadyRotation.addWidget(self.checkNeg_pstar, 1, 3)        
        self.gridQuasiSteadyRotation.addWidget(self.checkNeg_qstar, 2, 3)        
        self.gridQuasiSteadyRotation.addWidget(self.checkNeg_rstar, 3, 3)              
        self.gridQuasiSteadyRotation.addWidget(self.labelNegativeSteadi_pstar,  1, 4)
        self.gridQuasiSteadyRotation.addWidget(self.labelNegativeSteadi_qstar,  2, 4)
        self.gridQuasiSteadyRotation.addWidget(self.labelNegativeSteadi_rstar,  3, 4)
        self.gridQuasiSteadyRotation.addWidget(self.textNegativeSteadi_pstar,  1, 5)
        self.gridQuasiSteadyRotation.addWidget(self.textNegativeSteadi_qstar,  2, 5)
        self.gridQuasiSteadyRotation.addWidget(self.textNegativeSteadi_rstar,  3, 5)

        self.listCtrlSurUID1    = QtGui.QListWidget()
        self.listCtrlSurUID2    = QtGui.QListWidget()
        self.butCtrlSurUIDLeft  = QtGui.QPushButton()
        self.butCtrlSurUIDRight = QtGui.QPushButton()
        self.gridCtrlSurUID     = QtGui.QGridLayout()

        self.listCtrlSurUID1.setFixedSize(300,100)
        self.listCtrlSurUID2.setFixedSize(300,100)
        self.listCtrlSurUID1.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        self.listCtrlSurUID2.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        self.listCtrlSurUID1.setSortingEnabled(True)
        self.listCtrlSurUID2.setSortingEnabled(True)

        self.butCtrlSurUIDLeft.setIcon(QtGui.QIcon(Config.path_but_left_icon))
        self.butCtrlSurUIDLeft.setIconSize(QtCore.QSize(10,10))
        self.butCtrlSurUIDLeft.clicked.connect(self.fire_ctrlSurUIDSwitchLeft) 

        self.butCtrlSurUIDRight.setIcon(QtGui.QIcon(Config.path_but_right_icon))
        self.butCtrlSurUIDRight.setIconSize(QtCore.QSize(10,10))   
        self.butCtrlSurUIDRight.clicked.connect(self.fire_ctrlSurUIDSwitchRight)

        self.gridCtrlSurUID.addWidget(self.labelCtrlSurUID1,   0,0)
        self.gridCtrlSurUID.addWidget(self.labelCtrlSurUID2,   0,2)
        self.gridCtrlSurUID.addWidget(self.listCtrlSurUID1,    1,0, 2, 1)
        self.gridCtrlSurUID.addWidget(self.butCtrlSurUIDLeft,  1,1)
        self.gridCtrlSurUID.addWidget(self.butCtrlSurUIDRight, 2,1)
        self.gridCtrlSurUID.addWidget(self.listCtrlSurUID2,    1,2, 2, 1)

        # tool parameters
        self.comboUsePOLINT = QtGui.QComboBox()
        self.comboUsePOLINT.addItem("True")
        self.comboUsePOLINT.addItem("False")
        
        self.comboArchiveMode = QtGui.QComboBox()
        self.comboArchiveMode.addItem("0")
        self.comboArchiveMode.addItem("1")
        self.comboArchiveMode.addItem("2")
        
        self.textParallelComputation = QtGui.QLineEdit()
        self.textParallelComputation.setValidator(QtGui.QIntValidator() )       
        
        self.textSpanwise  = QtGui.QLineEdit()        
        self.textChordwise = QtGui.QLineEdit()  
        self.checkWingUID  = QtGui.QCheckBox()      
        self.listWingUID   = QtGui.QListWidget()
        self.listWingUID.setFixedSize(300,100)
        self.listWingUID.setVisible(False)  
        # =========================================
        # help save wingUIDS with spanwise und chordwise
        self.listWingUIDALL = dict()
        self.__cur_wing_uid = ""
        # =========================================
        
        self.checkWingUID.stateChanged.connect(self.fire_enableTextWingUID)
        self.checkPos_pstar.stateChanged.connect(self.fire_enableTextPosPStar)
        self.checkPos_qstar.stateChanged.connect(self.fire_enableTextPosQStar)
        self.checkPos_rstar.stateChanged.connect(self.fire_enableTextPosRStar)
        self.checkNeg_pstar.stateChanged.connect(self.fire_enableTextNegPStar)
        self.checkNeg_qstar.stateChanged.connect(self.fire_enableTextNegQStar)
        self.checkNeg_rstar.stateChanged.connect(self.fire_enableTextNegRStar)
        self.listWingUID.itemSelectionChanged.connect(self.fire_updateWingPanelingData)
        

    def setupToolTips(self):
        self.textName.setToolTip("name of tool")        
        self.textVers.setToolTip("version of tool")
        self.textDataset.setToolTip("name of the dataset for LIFTING_LINE calculation") 
        self.textParallelComputation.setToolTip("0=parallel computation on all available cores\n1=sequencial computation\nn=parallel computation on n cores")
        self.comboArchiveMode.setToolTip("0 = logfile\n1 = log+inputfiles\n2 = all results")    

    def setupButtons(self):
        # create buttons
        self.buttonBox = QtGui.QDialogButtonBox()
        self.buttonBox.addButton(QtGui.QDialogButtonBox.Ok)
        self.buttonBox.addButton(QtGui.QDialogButtonBox.Apply)
        self.buttonBox.addButton(QtGui.QDialogButtonBox.Cancel) 
        button_config = self.buttonBox.addButton("config", QtGui.QDialogButtonBox.HelpRole) 
               
        
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

        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).clicked.connect(self.fire_submitInputAndStartTool)
        self.buttonBox.button(QtGui.QDialogButtonBox.Apply).clicked.connect(self.fire_submitInput)
        self.buttonBox.button(QtGui.QDialogButtonBox.Cancel).clicked.connect(self.close)
        button_config.clicked.connect(self.openConfig)


        self.butOpenTool.clicked.connect(self.fire_setVisibilityTool)       
        self.butOpenAircraftModelUID.clicked.connect(self.fire_setVisibilityAircraftModelUID)       
        self.butOpenDataSetName.clicked.connect(self.fire_setVisibilityDatasetName)       
        self.butOpenLCasesAndPerMap.clicked.connect(self.fire_setVisibilityLoadCasePerMap)       
        self.butOpenToolParameters.clicked.connect(self.fire_setVisibilityToolParameters)       

        # unless first button click all buttons at init to collapse their elements. 
        self.butOpenAircraftModelUID.click()
        self.butOpenDataSetName.click()
        self.butOpenLCasesAndPerMap.click()
        self.butOpenToolParameters.click()

    def __getSeperator(self):
        line = QtGui.QFrame()
        line.setFrameShape(QtGui.QFrame.HLine)
        line.setFrameShadow(QtGui.QFrame.Sunken)        
        return line

    ## ========================================================================================================================================================
    ## ========================================================================================================================================================
    ## Tixi actions
    ## ========================================================================================================================================================
    ## ========================================================================================================================================================

    def initTixi(self, tixi):
        self.tixi = tixi 
        
        if self.tixi.checkElement("/cpacs/toolspecific/liftingLine") :
            print ("has LiftingListe")
            self.tixiGetToolName()
            self.tixiGetToolVersion()
            self.tixiGetAircraftModelUID()
            self.tixiGetDatasetName()
            self.tixiGetLoadCaseUID()
            self.tixiGetPositiveQuasiSteadyRotation()
            self.tixiGetNegativeQuasiSteadyRotation()
            self.tixiGetControlSurfaceUID()
            self.tixiGetToolParameters()
        else:
            print ("no lifting list")
            self.tixiGetAircraftModelUID()
            self.tixiGetLoadCaseUID()            
            self.tixiGetControlSurfaceUID()            
            self.__tixiGetToolParametersWingSpaneling()
                    
                    
    def tixiCreateEmptyLiftingLine(self):
        parentPath = "/cpacs/toolspecific"
        self.tixi.createElement(parentPath, "liftingLine")
        self.tixi.createElement(parentPath + "/liftingLine", "tool")
        self.tixi.createElement(parentPath + "/liftingLine", "aircraftModelUID")
        self.tixi.createElement(parentPath + "/liftingLine", "toolParameters")

        self.tixi.createElement(parentPath + "/liftingLine/tool", "name")
        self.tixi.createElement(parentPath + "/liftingLine/tool", "version")        

        self.tixi.createElement(parentPath + "/liftingLine/toolParameters", "usePOLINT")
        self.tixi.createElement(parentPath + "/liftingLine/toolParameters", "archiveMode")
        self.tixi.createElement(parentPath + "/liftingLine/toolParameters", "parallelComputation")
        self.tixi.createElement(parentPath + "/liftingLine/toolParameters", "wingPanelings")
        self.tixi.createElement(parentPath + "/liftingLine/toolParameters/wingPanelings", "wingPaneling")
        self.tixi.createElement(parentPath + "/liftingLine/toolParameters/wingPanelings/wingPaneling", "spanwise")
        self.tixi.createElement(parentPath + "/liftingLine/toolParameters/wingPanelings/wingPaneling", "chordwise")
        
    
    def tixiGetToolName(self):
        if self.tixi.checkElement("/cpacs/toolspecific/liftingLine/tool/name"):
            self.textName.setText(self.tixi.getTextElement("/cpacs/toolspecific/liftingLine/tool/name"))

    def tixiGetToolVersion(self):
        if self.tixi.checkElement("/cpacs/toolspecific/liftingLine/tool/version"):
            self.textVers.setText(self.tixi.getTextElement("/cpacs/toolspecific/liftingLine/tool/version"))
        
    def tixiGetAircraftModelUID(self):
        # get all model uids of aircraft node
        uids = []
        for i in range(1, self.tixi.getNamedChildrenCount("/cpacs/vehicles/aircraft", "model") + 1) :
            uids.append( self.tixi.getTextAttribute("/cpacs/vehicles/aircraft/model[" + str(i) +"]" , 'uID') )
            
        # set all model uids of toolspecific in the second list if they are a part of aircraft node
        if self.tixi.checkElement("/cpacs/toolspecific/liftingLine/aircraftModelUID"):
            for j in range(1, self.tixi.getNamedChildrenCount("/cpacs/toolspecific/liftingLine", "aircraftModelUID") + 1) :
                uid = self.tixi.getTextElement("/cpacs/toolspecific/liftingLine/aircraftModelUID["+str(j)+"]")
                if uid in uids :
                    self.listAMUID2.addItem(uid)
                    uids.remove(uid)
        
        # set remaining model uids of aircraft node in the first list if they are not a part of toolspecific aircraft model uids
        for uid in uids :
            self.listAMUID1.addItem( uid )


    def tixiGetDatasetName(self):
        if self.tixi.checkElement("/cpacs/toolspecific/liftingLine/datasetName"):
            self.textDataset.setText(self.tixi.getTextElement("/cpacs/toolspecific/liftingLine/datasetName"))        

    def tixiGetControlSurfaceUID(self):
        # AircraftModelUID has changed, current available ControlSurfaces (list 1) must be cleared
        if self.listCtrlSurUID1.count() > 0 :
            self.listCtrlSurUID1.clear()
        
        # save current ControlSurface selection and remove them from list2
        uids = set()
        for _ in range(0, self.listCtrlSurUID2.count()):
            uids.add(self.listCtrlSurUID2.takeItem(0).text())
            
        # check if AircraftModelUID was selected (AMUID list 2)
        if self.listAMUID2.count() > 0:
            # get selected model (only one is possible)
            model_uid  = self.listAMUID2.item(0).text()
            # read available ControlSurfaces for this model and save them in list 1
            uids_avail = set()
            for j in range(1, self.tixi.getNumberOfChilds('/cpacs/vehicles/aircraft/model[@uID="' + model_uid + '"]/analyses/aeroPerformanceMap/controlSurfaces') + 1) :
                item = self.tixi.getTextElement('/cpacs/vehicles/aircraft/model[@uID="' + model_uid + '"]/analyses/aeroPerformanceMap/controlSurfaces/controlSurface['+str(j)+']/controlSurfaceUID')
                uids_avail.add(item)

            # set items of old ControlSurface selection back to list 2 if they are available for this model
            uids = uids.intersection(uids_avail)
            
            # read given ControlSurfaces
            if self.tixi.checkElement("/cpacs/toolspecific/liftingLine/performanceMap/controlSurfaceUID"):
                for i in range(1, self.tixi.getNamedChildrenCount("/cpacs/toolspecific/liftingLine/performanceMap", "controlSurfaceUID") + 1) :
                    item = self.tixi.getTextElement("/cpacs/toolspecific/liftingLine/performanceMap/controlSurfaceUID["+str(i)+"]")
                    # check if given ControlSurfaces available for given AircraftModel
                    if item in uids_avail :
                        # set them to ControlSurfaces Set
                        uids.add(item)
            # set them to list
            for item in uids:
                self.listCtrlSurUID2.addItem(item)
            
            for item in uids_avail.difference(uids):
                self.listCtrlSurUID1.addItem(item)

    
    def tixiGetLoadCaseUID(self):
        
        # AircraftModelUID has changed, we must clear current available LoadCases (list 1)
        if self.listLoadCaseUID1.count() > 0 :
            self.listLoadCaseUID1.clear()
        
        # save current LoadCase selection and remove them from list2
        uids_LoadCases = set()
        for _ in range(0, self.listLoadCaseUID2.count()):
            uids_LoadCases.add(self.listLoadCaseUID2.takeItem(0).text())
            
        # check if AircraftModelUID was selected (AMUID list 2)
        if self.listAMUID2.count() > 0:
            # get selected model
            model_uid  = self.listAMUID2.item(0).text()
            
            # read available LoadCases for this model and save in list 1
            uids_avail = set()
            for j in range(1, self.tixi.getNamedChildrenCount('/cpacs/vehicles/aircraft/model[@uID="' + model_uid + '"]/analyses/loadAnalysis/loadCases', 'flightLoadCase') + 1) :
                item = self.tixi.getTextAttribute('/cpacs/vehicles/aircraft/model[@uID="' + model_uid + '"]/analyses/loadAnalysis/loadCases/flightLoadCase['+str(j)+']' , 'uID')
                uids_avail.add(item)

            # set items of old LoadCase selection back to list 2 if they are available for this model
            uids_LoadCases = uids_LoadCases.intersection(uids_avail)
            
            if self.tixi.checkElement("/cpacs/toolspecific/liftingLine/loadCases/loadCaseUID"):
                # read given loadCases
                for i in range(1, self.tixi.getNamedChildrenCount("/cpacs/toolspecific/liftingLine/loadCases", "loadCaseUID") + 1) :
                    item = self.tixi.getTextElement("/cpacs/toolspecific/liftingLine/loadCases/loadCaseUID["+str(i)+"]")
                    # check if given loadCase available for given AircraftModel
                    if item in uids_avail :
                        # set them to LoadCase Set
                        uids_LoadCases.add(item)
            # set them to list
            for item in uids_LoadCases:
                self.listLoadCaseUID2.addItem(item)
            
            for item in uids_avail.difference(uids_LoadCases):
                self.listLoadCaseUID1.addItem(item)


    def tixiGetPositiveQuasiSteadyRotation(self):
        path = "/cpacs/toolspecific/liftingLine/performanceMap/positiveQuasiSteadyRotation"
        if self.tixi.checkElement(path + "/pstar") :
            self.textPositiveSteadi_pstar.setText(self.tixi.getTextElement(path + "/pstar"))

        if self.tixi.checkElement(path + "/qstar") :
            self.textPositiveSteadi_qstar.setText(self.tixi.getTextElement(path + "/qstar"))
        
        if self.tixi.checkElement(path + "/rstar") :
            self.textPositiveSteadi_rstar.setText(self.tixi.getTextElement(path + "/rstar"))
        

    def tixiGetNegativeQuasiSteadyRotation(self):
        path = "/cpacs/toolspecific/liftingLine/performanceMap/negativeQuasiSteadyRotation"
        if self.tixi.checkElement(path + "/pstar") :
            self.textNegativeSteadi_pstar.setText(self.tixi.getTextElement(path + "/pstar"))

        if self.tixi.checkElement(path + "/qstar") :
            self.textNegativeSteadi_qstar.setText(self.tixi.getTextElement(path + "/qstar"))
        
        if self.tixi.checkElement(path + "/rstar") :
            self.textNegativeSteadi_rstar.setText(self.tixi.getTextElement(path + "/rstar"))        


    def tixiGetToolParameters(self):
        self.__tixiGetToolParametersConfig()
        self.__tixiGetToolParametersWingSpaneling()

    def __tixiGetToolParametersConfig(self):
        b = self.tixi.getBooleanElement("/cpacs/toolspecific/liftingLine/toolParameters/usePOLINT")
        self.comboUsePOLINT.setCurrentIndex(0 if b else 1)
        print (self.comboUsePOLINT.currentText())
        b = self.tixi.getIntegerElement("/cpacs/toolspecific/liftingLine/toolParameters/archiveMode")
        self.comboArchiveMode.setCurrentIndex(b)
        b = self.tixi.getIntegerElement("/cpacs/toolspecific/liftingLine/toolParameters/parallelComputation")
        self.textParallelComputation.setText(str(b))
        
    def __tixiGetToolParametersWingSpaneling(self):

        # if AircraftModelUID has changed, we must clear current available wingUIDs)
        if self.listWingUID.count() > 0 :
            self.listWingUID.clear()
            self.listWingUIDALL.clear()

        # check if AircraftModelUID was selected (AMUID list 2)
        if self.listAMUID2.count() > 0:
            # get selected model (list has only 0 or 1 items)
            model_uid  = self.listAMUID2.item(0).text()
            path = '/cpacs/vehicles/aircraft/model[@uID="' + model_uid + '"]/wings'
        
            if self.tixi.checkElement(path) :
                # get all wing uids
                for i in range(1, self.tixi.getNamedChildrenCount(path, "wing")+1): 
                    uID = self.tixi.getTextAttribute(path + "/wing[" + str(i) +"]" , "uID")
                    self.listWingUID.addItem(uID)
                    self.listWingUIDALL.update({uID : ("", "")})

            # get all given wing uids in tool block
            path = "/cpacs/toolspecific/liftingLine/toolParameters/wingPanelings"
            cnt_wingPaneling = self.tixi.getNamedChildrenCount(path, "wingPaneling") 
            
            for i in range(1, cnt_wingPaneling+1):
                if self.tixi.checkElement(path + "/wingPaneling[" + str(i) +"]/wingUID") :
                    uid = self.tixi.getTextElement(path + "/wingPaneling[" + str(i) +"]/wingUID")
                    span  = self.tixi.getIntegerElement(path + "/wingPaneling[" + str(i) +"]/spanwise")
                    chord = self.tixi.getIntegerElement(path + "/wingPaneling[" + str(i) +"]/chordwise")
                    self.listWingUIDALL.update({uid:(str(span), str(chord))})              
                elif cnt_wingPaneling > 1 :
                    print ("ERROR!!!!!!!! more than one wingPaneling available but no uids")
                    break
            
            if not self.checkWingUID.isChecked() :
                self.textSpanwise.setText( str(self.tixi.getIntegerElement(path + "/wingPaneling[" + str(i) +"]/spanwise")) )
                self.textChordwise.setText( str(self.tixi.getIntegerElement(path + "/wingPaneling[" + str(i) +"]/chordwise")) )

                
    ## ========================================================================================================================================================
    ## ========================================================================================================================================================
    ## checkbox fired functions
    ## ========================================================================================================================================================
    ## ========================================================================================================================================================

    def fire_enableTextDatasetName(self, n):
        self.textDataset.setEnabled(n)          

    def fire_enableTextWingUID(self, n):
        self.labelWingUID.setVisible(n)
        self.listWingUID.setVisible(n)
        
        if not n :
            # ATTENTION!!! clearSelection sends signal list item changed --> call fire_updateWingPanelingData
            self.listWingUID.clearSelection()
            self.__cur_wing_uid = ""
        self.textSpanwise.clear()
        self.textChordwise.clear()
        
    def fire_enableTextPosPStar(self, n):
        self.textPositiveSteadi_pstar.setEnabled(n)
    
    def fire_enableTextPosQStar(self, n):
        self.textPositiveSteadi_qstar.setEnabled(n)
    
    def fire_enableTextPosRStar(self, n):
        self.textPositiveSteadi_rstar.setEnabled(n)
    
    def fire_enableTextNegPStar(self, n):
        self.textNegativeSteadi_pstar.setEnabled(n)
    
    def fire_enableTextNegQStar(self, n):
        self.textNegativeSteadi_qstar.setEnabled(n)
    
    def fire_enableTextNegRStar(self, n):
        self.textNegativeSteadi_rstar.setEnabled(n)
        
    ## ========================================================================================================================================================
    ## ========================================================================================================================================================
    ## list selection changed fired functions
    ## ========================================================================================================================================================
    ## ========================================================================================================================================================

    def fire_updateWingPanelingData(self):
        # get span and chord of last selection
        span  = self.textSpanwise.text()
        chord = self.textChordwise.text()

        # update values for last selected uid
        if self.__cur_wing_uid != "" :        
            self.listWingUIDALL.update({self.__cur_wing_uid : (span, chord)})
        
        # update selected wing uid
        self.__cur_wing_uid = self.listWingUID.currentItem().text()
        
        # set text fields with content of selected wing uid
        (span, chord) = self.listWingUIDALL[self.__cur_wing_uid] 
        self.textSpanwise.setText(span)
        self.textChordwise.setText(chord)
        
        
    ## ========================================================================================================================================================
    ## ========================================================================================================================================================
    ## collapse button functions
    ## ========================================================================================================================================================
    ## ========================================================================================================================================================    

    def fire_setVisibilityTool(self):
        self.flagButTool = not self.flagButTool
        self.labelName.setVisible(self.flagButTool)
        self.labelVers.setVisible(self.flagButTool)
        self.textName.setVisible(self.flagButTool)
        self.textVers.setVisible(self.flagButTool)

    def fire_setVisibilityAircraftModelUID(self):
        self.flagButAir = not self.flagButAir
        self.labelAMUID1.setVisible(self.flagButAir)
        self.labelAMUID2.setVisible(self.flagButAir)
        self.listAMUID1.setVisible(self.flagButAir)
        self.listAMUID2.setVisible(self.flagButAir)
        self.butAMUIDLeft.setVisible(self.flagButAir)
        self.butAMUIDRight.setVisible(self.flagButAir)

    def fire_setVisibilityDatasetName (self):
        self.flagButData = not self.flagButData
        self.labelDataset.setVisible(self.flagButData)
        self.labelCheckDSet.setVisible(self.flagButData)
        self.textDataset.setVisible(self.flagButData)
        self.checkDataset.setVisible(self.flagButData)

    def fire_setVisibilityLoadCasePerMap(self):
        self.flagButCase = not self.flagButCase
        
        self.radioCaseVsPerMap1.setVisible(self.flagButCase)
        self.radioCaseVsPerMap2.setVisible(self.flagButCase)
        
        if not self.flagButCase :
            self.fire_showLoadCase(False)
            self.fire_showPerMap(False)
        elif self.radioCaseVsPerMap1.isChecked():
            self.fire_showLoadCase(True)
        elif self.radioCaseVsPerMap2.isChecked():
            self.fire_showPerMap(True)
        else:
            self.fire_showLoadCase(False)
            self.fire_showPerMap(False)

    def fire_showLoadCase(self, b):
        self.labelLoadCaseUID1.setVisible(b)
        self.labelLoadCaseUID2.setVisible(b)
        self.listLoadCaseUID1.setVisible(b)
        self.listLoadCaseUID2.setVisible(b)
        self.butLoadCaseUIDLeft.setVisible(b)
        self.butLoadCaseUIDRight.setVisible(b)

    def fire_showPerMap(self, b):
        self.labelPositiveQuasiSteadyRotation.setVisible(b)
        self.labelPositiveSteadi_pstar.setVisible(b)
        self.labelPositiveSteadi_qstar.setVisible(b)
        self.labelPositiveSteadi_rstar.setVisible(b)
        
        self.labelNegativeQuasiSteadyRotation.setVisible(b)
        self.labelNegativeSteadi_pstar.setVisible(b)
        self.labelNegativeSteadi_qstar.setVisible(b)
        self.labelNegativeSteadi_rstar.setVisible(b)

        self.checkPos_pstar.setVisible(b)
        self.checkPos_qstar.setVisible(b)
        self.checkPos_rstar.setVisible(b)
    
        self.checkNeg_pstar.setVisible(b)
        self.checkNeg_qstar.setVisible(b)
        self.checkNeg_rstar.setVisible(b)

        self.textPositiveSteadi_pstar.setVisible(b)
        self.textPositiveSteadi_qstar.setVisible(b)
        self.textPositiveSteadi_rstar.setVisible(b)
        
        self.textNegativeSteadi_pstar.setVisible(b)
        self.textNegativeSteadi_qstar.setVisible(b)
        self.textNegativeSteadi_rstar.setVisible(b)

        self.labelCtrlSurUID1.setVisible(b)
        self.labelCtrlSurUID2.setVisible(b)
        self.listCtrlSurUID1.setVisible(b)
        self.listCtrlSurUID2.setVisible(b)
        self.butCtrlSurUIDLeft.setVisible(b)
        self.butCtrlSurUIDRight.setVisible(b)

    def fire_setVisibilityToolParameters(self):
        self.flagButTPar = not self.flagButTPar
        self.labelUsePOLINT.setVisible(self.flagButTPar)
        self.labelArchiveMode.setVisible(self.flagButTPar)
        self.labelParallelComputation.setVisible(self.flagButTPar)
        self.labelCheckWingUID.setVisible(self.flagButTPar)
        self.labelWingUID.setVisible(self.flagButTPar and self.checkWingUID.isChecked())
        self.labelSpanwise.setVisible(self.flagButTPar)
        self.labelchordwise.setVisible(self.flagButTPar)
        
        self.comboUsePOLINT.setVisible(self.flagButTPar)
        self.comboArchiveMode.setVisible(self.flagButTPar)
        self.textParallelComputation.setVisible(self.flagButTPar)
        self.checkWingUID.setVisible(self.flagButTPar)
        self.listWingUID.setVisible(self.flagButTPar and self.checkWingUID.isChecked())
        self.textSpanwise.setVisible(self.flagButTPar)
        self.textChordwise.setVisible(self.flagButTPar)

    def fire_setVisibilityAll(self, flagTool, flagAircraftModel, flagDatasetName, flagLoadCasePerMap, flagToolParameters):
        self.flagButTool = flagTool
        self.flagButAir  = flagAircraftModel
        self.flagButData = flagDatasetName
        self.flagButCase = flagLoadCasePerMap
        self.flagButTPar = flagToolParameters
        
        self.fire_setVisibilityTool()
        self.fire_setVisibilityAircraftModelUID()
        self.fire_setVisibilityDatasetName()
        self.fire_setVisibilityLoadCasePerMap()
        self.fire_setVisibilityToolParameters()

    ## ========================================================================================================================================================
    ## ========================================================================================================================================================
    ## get values
    ## ========================================================================================================================================================
    ## ========================================================================================================================================================          
 
    def __tixiCreateNode(self, path, child, idx):
        if not self.tixi.checkElement(path + "/" + child) :
            self.tixi.createElementAtIndex(path, child, idx)  
    
    def tixiSetToolName(self):
        self.__tixiCreateNode("/cpacs/toolspecific/liftingLine", "tool", 1)
        self.__tixiCreateNode("/cpacs/toolspecific/liftingLine/tool", "name", 1)
        self.__tixiUpdateTextElement("/cpacs/toolspecific/liftingLine/tool/name", self.textName.text())
    
    def tixiSetToolVersion(self):
        self.__tixiCreateNode("/cpacs/toolspecific/liftingLine/tool", "version", 2)
        self.__tixiUpdateTextElement("/cpacs/toolspecific/liftingLine/tool/version", self.textVers.text())

    def tixiSetAircraftModelUID(self):
        self.__tixiCreateNode("/cpacs/toolspecific/liftingLine", "aircraftModelUID", 2)
        item = self.listAMUID2.item(0)
        self.__tixiUpdateTextElement("/cpacs/toolspecific/liftingLine/aircraftModelUID", "" if item is None else item.text())        

    def tixiSetDatasetName(self):
        isAvailNodeDatasetName = self.tixi.checkElement("/cpacs/toolspecific/liftingLine/datasetName")
        
        if self.checkDataset.isChecked() :
            if not isAvailNodeDatasetName :
                self.tixi.createElementAtIndex("/cpacs/toolspecific/liftingLine", "datasetName", 3) 
            self.__tixiUpdateTextElement("/cpacs/toolspecific/liftingLine/datasetName", self.textDataset.text()) 
        elif isAvailNodeDatasetName :
            self.tixi.removeElement("/cpacs/toolspecific/liftingLine/datasetName")

    
    def tixiSetLoadCaseOrPerformanceMap(self):
        # if loadCase
        if self.radioCaseVsPerMap1.isChecked() :
            self.__tixiSetLoadCaseOrPerformanceMap("/cpacs/toolspecific/liftingLine", "loadCases", "performanceMap")
            self.__tixiUpdateListElement("/cpacs/toolspecific/liftingLine/loadCases", "loadCaseUID", self.listLoadCaseUID2)
            return True
        elif self.radioCaseVsPerMap2.isChecked() :
            self.__tixiSetLoadCaseOrPerformanceMap("/cpacs/toolspecific/liftingLine", "performanceMap", "loadCases")
            # to comply with the xml sequence condition the PositiveQuasiSteadyRotation must be called before NegativeQuasiSteadyRotation 
            self.__tixiSetPositiveQuasiSteadyRotation()
            self.__tixiSetNegativeQuasiSteadyRotation()
            self.__tixiSetControlSurfaceUID()            
            return True
        else :
            return False
    
    def __tixiSetLoadCaseOrPerformanceMap(self, path, used_child, unused_child):
        if not self.tixi.checkElement(path + "/" + used_child) :
            n = 4 if self.tixi.checkElement("/cpacs/toolspecific/liftingLine/datasetName") else 3
            self.tixi.createElementAtIndex(path, used_child, n)
            
        if self.tixi.checkElement(path + "/" + unused_child) :
            self.tixi.removeElement(path + "/" + unused_child)
        
    def __tixiSetControlSurfaceUID(self):
        #self.__tixiCreateNode("/cpacs/toolspecific/liftingLine/performanceMap", "controlSurfaceUID" , 2)
        start_idx = self.tixi.getNumberOfChilds("/cpacs/toolspecific/liftingLine/performanceMap") +1
        self.__tixiUpdateListElement("/cpacs/toolspecific/liftingLine/performanceMap", "controlSurfaceUID", self.listCtrlSurUID2, start_idx)        
        
    def __tixiCreateQuasiSteadyRotation(self, path, child, idx=None):
        if not self.tixi.checkElement(path + "/" + child) :
            if idx is not None:
                self.tixi.createElementAtIndex(path, child, idx)
            else:
                self.tixi.createElement(path, child)

    def __tixiRemoveQuasiSteadyRotation(self, path):
        if self.tixi.checkElement(path) :
            self.tixi.removeElement(path)        
        
        
    def __tixiSetPositiveQuasiSteadyRotation(self):
        path = "/cpacs/toolspecific/liftingLine/performanceMap/positiveQuasiSteadyRotation"
        
        # check parent node positiveQuasiSteadyRotation
        if self.checkPos_pstar.isChecked() or self.checkPos_qstar.isChecked() or self.checkPos_rstar.isChecked() : 
            self.__tixiCreateQuasiSteadyRotation("/cpacs/toolspecific/liftingLine/performanceMap" ,"positiveQuasiSteadyRotation", 1)
        else:
            self.__tixiRemoveQuasiSteadyRotation("/cpacs/toolspecific/liftingLine/performanceMap/positiveQuasiSteadyRotation")

        # check childs pstar, qstar, rstar
        if self.checkPos_pstar.isChecked():
            self.__tixiCreateQuasiSteadyRotation("/cpacs/toolspecific/liftingLine/performanceMap/positiveQuasiSteadyRotation", "pstar")
            self.__tixiUpdateTextElement(path + "/pstar", self.textPositiveSteadi_pstar.text())
        else:
            self.__tixiRemoveQuasiSteadyRotation("/cpacs/toolspecific/liftingLine/performanceMap/positiveQuasiSteadyRotation/pstar")            
        
        if self.checkPos_qstar.isChecked():        
            self.__tixiCreateQuasiSteadyRotation("/cpacs/toolspecific/liftingLine/performanceMap/positiveQuasiSteadyRotation", "qstar")        
            self.__tixiUpdateTextElement(path + "/qstar", self.textPositiveSteadi_qstar.text())        
        else:
            self.__tixiRemoveQuasiSteadyRotation("/cpacs/toolspecific/liftingLine/performanceMap/positiveQuasiSteadyRotation/qstar")            
        
        if self.checkPos_rstar.isChecked():
            self.__tixiCreateQuasiSteadyRotation("/cpacs/toolspecific/liftingLine/performanceMap/positiveQuasiSteadyRotation", "rstar")
            self.__tixiUpdateTextElement(path + "/rstar", self.textPositiveSteadi_rstar.text())
        else:
            self.__tixiRemoveQuasiSteadyRotation("/cpacs/toolspecific/liftingLine/performanceMap/positiveQuasiSteadyRotation/rstar") 
    
    
    def __tixiSetNegativeQuasiSteadyRotation(self):
        path = "/cpacs/toolspecific/liftingLine/performanceMap/negativeQuasiSteadyRotation"
             
        if self.checkNeg_pstar.isChecked() or self.checkNeg_qstar.isChecked() or self.checkNeg_rstar.isChecked() : 
            n = 2 if self.checkPos_pstar.isChecked() or self.checkPos_qstar.isChecked() or self.checkPos_rstar.isChecked() else 1
            # check parent node negativeQuasiSteadyRotation  
            self.__tixiCreateQuasiSteadyRotation("/cpacs/toolspecific/liftingLine/performanceMap" ,"negativeQuasiSteadyRotation", n)
        else:
            self.__tixiRemoveQuasiSteadyRotation("/cpacs/toolspecific/liftingLine/performanceMap/negativeQuasiSteadyRotation")        
        
        # check childs pstar, qstar, rstar        
        if self.checkNeg_pstar.isChecked():
            self.__tixiCreateQuasiSteadyRotation("/cpacs/toolspecific/liftingLine/performanceMap/negativeQuasiSteadyRotation", "pstar")
            self.__tixiUpdateTextElement(path + "/pstar", self.textNegativeSteadi_pstar.text())
        else:
            self.__tixiRemoveQuasiSteadyRotation("/cpacs/toolspecific/liftingLine/performanceMap/negativeQuasiSteadyRotation/pstar")         
        
        if self.checkNeg_qstar.isChecked():        
            self.__tixiCreateQuasiSteadyRotation("/cpacs/toolspecific/liftingLine/performanceMap/negativeQuasiSteadyRotation", "qstar")        
            self.__tixiUpdateTextElement(path + "/qstar", self.textNegativeSteadi_qstar.text())        
        else:
            self.__tixiRemoveQuasiSteadyRotation("/cpacs/toolspecific/liftingLine/performanceMap/negativeQuasiSteadyRotation/qstar") 
        
        if self.checkNeg_rstar.isChecked():
            self.__tixiCreateQuasiSteadyRotation("/cpacs/toolspecific/liftingLine/performanceMap/negativeQuasiSteadyRotation", "rstar")
            self.__tixiUpdateTextElement(path + "/rstar", self.textNegativeSteadi_rstar.text())      
        else:
            self.__tixiRemoveQuasiSteadyRotation("/cpacs/toolspecific/liftingLine/performanceMap/negativeQuasiSteadyRotation/rstar")
        
    
    # if first wingPaneling has an uid then the following wingPanelings have to have one too
    def tixiSetToolParameters(self):
        n = 5 if self.tixi.checkElement("/cpacs/toolspecific/liftingLine/datasetName") else 4
        self.__tixiCreateNode("/cpacs/toolspecific/liftingLine", "toolParameters", n)
        
        self.__tixiCreateNode("/cpacs/toolspecific/liftingLine/toolParameters", "usePOLINT", 1)
        self.__tixiCreateNode("/cpacs/toolspecific/liftingLine/toolParameters", "archiveMode", 2)
        self.__tixiCreateNode("/cpacs/toolspecific/liftingLine/toolParameters", "parallelComputation", 3)
        self.__tixiCreateNode("/cpacs/toolspecific/liftingLine/toolParameters", "wingPanelings", 4)
        
        self.__tixiUpdateTextElement("/cpacs/toolspecific/liftingLine/toolParameters/usePOLINT", self.comboUsePOLINT.currentText())
        self.__tixiUpdateTextElement("/cpacs/toolspecific/liftingLine/toolParameters/archiveMode", self.comboArchiveMode.currentText())
        self.__tixiUpdateTextElement("/cpacs/toolspecific/liftingLine/toolParameters/parallelComputation", self.textParallelComputation.text())
        
        path = "/cpacs/toolspecific/liftingLine/toolParameters/wingPanelings"

        if self.checkWingUID.isChecked() :
            # remove all
            for j in range(self.tixi.getNamedChildrenCount(path, "wingPaneling"), 0, -1) :
                self.tixi.removeElement(path + "/wingPaneling[" + str(j) +"]") 
                
            keys = self.listWingUIDALL.keys()
            vals = self.listWingUIDALL.values()
                
            for i in range(0, len(keys)) :
                (span, chord) = vals[i]
                self.tixi.createElement(path, "wingPaneling")
                self.tixi.addTextElement(path + "/wingPaneling[" + str(i+1) +"]" , "wingUID", keys[i])
                self.tixi.addTextElement(path + "/wingPaneling[" + str(i+1) +"]" , "spanwise", span)
                self.tixi.addTextElement(path + "/wingPaneling[" + str(i+1) +"]" , "chordwise", chord)
        else:
            # remove all but first element
            for j in range(self.tixi.getNamedChildrenCount(path, "wingPaneling"), 1, -1) :
                self.tixi.removeElement(path + "/wingPaneling[" + str(j) +"]")  
            
            if self.tixi.checkElement(path + "/wingPaneling/wingUID") :
                self.tixi.removeElement(path + "/wingPaneling/wingUID")
          
            self.__tixiUpdateTextElement(path + "/wingPaneling/spanwise", self.textSpanwise.text())
            self.__tixiUpdateTextElement(path + "/wingPaneling/chordwise", self.textChordwise.text())
            

    def __tixiUpdateTextElement(self, path, text):
        if text != self.tixi.getTextElement(path):
            self.tixi.updateTextElement(path, text)
    

    def __tixiUpdateListElement(self, path, child, qlist, start_idx=None):
        oldLoadCaseUIDs = set()
        for i in range(1, self.tixi.getNamedChildrenCount(path, child) + 1) :
            oldLoadCaseUIDs.add(self.tixi.getTextElement(path + "/" + child + "["+str(i)+"]"))

        newLoadCaseUIDs = set()
        for j in range(0, qlist.count()) :
            newLoadCaseUIDs.add(qlist.item(j).text())
            
        rmLoadCaseUIDs  = oldLoadCaseUIDs.difference(newLoadCaseUIDs)
        newLoadCaseUIDs = newLoadCaseUIDs.difference(oldLoadCaseUIDs)
        
        for k in range(self.tixi.getNamedChildrenCount(path, child), 0, -1) :        
            text = self.tixi.getTextElement(path + "/" + child + "["+str(k)+"]")
            
            if text in rmLoadCaseUIDs :
                self.tixi.removeElement(path + "/" + child + "["+str(k)+"]")
        
        idx = 1
        for newUID in newLoadCaseUIDs:
            if start_idx is not None:
                self.tixi.createElementAtIndex(path, child, start_idx)
                self.tixi.updateTextElement(path + "/" + child + "[" + str(idx) +"]", newUID) 
                idx += 1       
            else :
                self.tixi.createElementAtIndex(path, child, 1)
                self.tixi.updateTextElement(path + "/" + child + "[1]", newUID)         

    ## ========================================================================================================================================================
    ## ========================================================================================================================================================
    ## list functions
    ## ========================================================================================================================================================
    ## ========================================================================================================================================================  

    def fire_modelUIDSwitchLeft(self):
        self.switchBetweenLists(self.listAMUID2, self.listAMUID1, False)
        self.tixiGetLoadCaseUID()
        self.tixiGetControlSurfaceUID()
        self.__tixiGetToolParametersWingSpaneling()        
      
    def fire_modelUIDSwitchRight(self):
        self.switchBetweenLists(self.listAMUID1, self.listAMUID2, True)      
        self.tixiGetLoadCaseUID()
        self.tixiGetControlSurfaceUID()
        self.__tixiGetToolParametersWingSpaneling()  
        
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

    def fire_ctrlSurUIDSwitchLeft(self):
        self.switchBetweenLists2(self.listCtrlSurUID2, self.listCtrlSurUID1)

    def fire_ctrlSurUIDSwitchRight(self):
        self.switchBetweenLists2(self.listCtrlSurUID1, self.listCtrlSurUID2) 

    def fire_loadCaseUIDSwitchLeft(self):
        self.switchBetweenLists2(self.listLoadCaseUID2, self.listLoadCaseUID1)
      
    def fire_loadCaseUIDSwitchRight(self):
        self.switchBetweenLists2(self.listLoadCaseUID1, self.listLoadCaseUID2)  

    def switchBetweenLists2(self, list1, list2):
        item = list1.currentItem()
        list1.setCurrentItem(None)
        if item is not None :
            list1.takeItem(list1.row(item))
            list2.addItem(item)

#---------------------------------------------------- if __name__ == "__main__":
    #---------------------------------------------- app = QtGui.QApplication([])
    #------------------------------------------------------------- tixi = Tixi()
    #------------------------------- tixi.openDocument(Config.path_cpacs_D150_3)
    #------------------------------------------------ test = ToolX("name", tixi)
    #--------------------------------------------------------------- test.show()
#------------------------------------------------------------------------------ 
    #--------------------------------------------------------------- app.exec_()