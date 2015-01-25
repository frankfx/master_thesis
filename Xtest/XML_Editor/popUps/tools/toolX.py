'''
Created on Jan 14, 2015

@author: fran_re
'''

from PySide import QtGui, QtCore
from popUp_tool import PopUpTool
from Xtest.Open_GL import utility
from Xtest.XML_Editor.configuration.config import Config
from tixiwrapper   import Tixi, TixiException
import os, sys



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
        os.system("xsltproc -o " + Config.path_cpacs_test + " " + Config.path_cpacs_inputMapping + " " + Config.path_cpacs_D150_3)

    @utility.overrides(PopUpTool)    
    def fire_submitInput(self):
        self.tixiSetToolName()
        self.tixiSetToolVersion()
        self.tixiSetAircraftModelUID()
        self.tixi.saveDocument("text.xml")
        self.close()  

    @utility.overrides(PopUpTool)            
    def fire_submitInputAndStartTool(self):
        pass

    

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

        self.gridQuasiSteadyRotation.addWidget(self.labelPositiveQuasiSteadyRotation,0 ,0, 1, 3)
        self.gridQuasiSteadyRotation.addWidget(self.labelPositiveSteadi_pstar, 1, 0)
        self.gridQuasiSteadyRotation.addWidget(self.labelPositiveSteadi_qstar, 2, 0)
        self.gridQuasiSteadyRotation.addWidget(self.labelPositiveSteadi_rstar, 3, 0)
        self.gridQuasiSteadyRotation.addWidget(self.textPositiveSteadi_pstar,  1, 1)
        self.gridQuasiSteadyRotation.addWidget(self.textPositiveSteadi_qstar,  2, 1)
        self.gridQuasiSteadyRotation.addWidget(self.textPositiveSteadi_rstar,  3, 1)
        self.gridQuasiSteadyRotation.addWidget(self.labelNegativeQuasiSteadyRotation, 0, 3, 1, 3)        
        self.gridQuasiSteadyRotation.addWidget(self.labelNegativeSteadi_pstar,  1, 3)
        self.gridQuasiSteadyRotation.addWidget(self.labelNegativeSteadi_qstar,  2, 3)
        self.gridQuasiSteadyRotation.addWidget(self.labelNegativeSteadi_rstar,  3, 3)
        self.gridQuasiSteadyRotation.addWidget(self.textNegativeSteadi_pstar,  1, 4)
        self.gridQuasiSteadyRotation.addWidget(self.textNegativeSteadi_qstar,  2, 4)
        self.gridQuasiSteadyRotation.addWidget(self.textNegativeSteadi_rstar,  3, 4)

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
        self.textParallelComputation.setValidator(QtGui.QIntValidator(0, 10000, self) )       
        
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
            QtGui.QMessageBox.about(self, "error", "no toolspecific found in the given file")
            self.close()
        
    def tixiGetToolName(self):
        self.textName.setText(self.tixi.getTextElement("/cpacs/toolspecific/liftingLine/tool/name"))

    def tixiGetToolVersion(self):
        self.textVers.setText(self.tixi.getTextElement("/cpacs/toolspecific/liftingLine/tool/version"))
        
    def tixiGetAircraftModelUID(self):
        uids_avail = []
        for j in range(1, self.tixi.getNamedChildrenCount("/cpacs/toolspecific/liftingLine", "aircraftModelUID") + 1) :
            item = self.tixi.getTextElement("/cpacs/toolspecific/liftingLine/aircraftModelUID["+str(j)+"]")
            self.listAMUID2.addItem(item)
            uids_avail.append(item)
       
        for i in range(1, self.tixi.getNamedChildrenCount("/cpacs/vehicles/aircraft", "model") + 1) :
            item = self.tixi.getTextAttribute("/cpacs/vehicles/aircraft/model[" + str(i) +"]" , 'uID')
            if not item in uids_avail:
                self.listAMUID1.addItem(item)


    def tixiGetDatasetName(self):
        if self.tixi.checkElement("/cpacs/toolspecific/liftingLine/datasetName"):
            self.textDataset.setText(self.tixi.getTextElement("/cpacs/toolspecific/liftingLine/datasetName"))        

    def tixiGetControlSurfaceUID(self):
        # AircraftModelUID has changed, we must clear current available ControlSurfaces (list 1)
        if self.listCtrlSurUID1.count() > 0 :
            self.listCtrlSurUID1.clear()
        
        # save current ControlSurface selection and remove them from list2
        uids = set()
        for _ in range(0, self.listCtrlSurUID2.count()):
            uids.add(self.listCtrlSurUID2.takeItem(0).text())
            
        # check if AircraftModelUID was selected (AMUID list 2)
        if self.listAMUID2.count() > 0:
            # get selected model
            model_uid  = self.listAMUID2.item(0).text()
            # read available ControlSurfaces for this model and save in list 1
            uids_avail = set()
            for j in range(1, self.tixi.getNamedChildrenCount('/cpacs/vehicles/aircraft/model[@uID="' + model_uid + '"]/analyses/aeroPerformanceMap/controlSurfaces', 'controlSurface') + 1) :
                item = self.tixi.getTextElement('/cpacs/vehicles/aircraft/model[@uID="' + model_uid + '"]/analyses/aeroPerformanceMap/controlSurfaces/controlSurface['+str(j)+']/controlSurfaceUID')
                uids_avail.add(item)

            # set items of old ControlSurface selection back to list 2 if they are available for this model
            uids = uids.intersection(uids_avail)
            
            # read given ControlSurfaces
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
            
            # read given loadCases
            for i in range(1, self.tixi.getNamedChildrenCount("/cpacs/toolspecific/liftingLine/loadCases", "loadCaseUID") + 1) :
                item = self.tixi.getTextElement("/cpacs/toolspecific/liftingLine/loadCases/loadCaseUID["+str(i)+"]")
                # check if given loadCase available for given AircraftModel
                if item in uids_avail :
                    # set them to LoadCase Set
                    uids_LoadCases.add(item)
                    print uids_LoadCases
            # set them to list
            for item in uids_LoadCases:
                self.listLoadCaseUID2.addItem(item)
            
            for item in uids_avail.difference(uids_LoadCases):
                self.listLoadCaseUID1.addItem(item)

    def tixiGetPositiveQuasiSteadyRotation(self):
        path = "/cpacs/toolspecific/liftingLine/performanceMap/positiveQuasiSteadyRotation"
        self.textPositiveSteadi_pstar.setText(self.tixi.getTextElement(path+"/pstar"))
        self.textPositiveSteadi_qstar.setText(self.tixi.getTextElement(path+"/qstar"))
        self.textPositiveSteadi_rstar.setText(self.tixi.getTextElement(path+"/rstar"))
        
    def tixiGetNegativeQuasiSteadyRotation(self):
        path = "/cpacs/toolspecific/liftingLine/performanceMap/negativeQuasiSteadyRotation"
        self.textNegativeSteadi_pstar.setText(self.tixi.getTextElement(path+"/pstar"))
        self.textNegativeSteadi_qstar.setText(self.tixi.getTextElement(path+"/qstar"))
        self.textNegativeSteadi_rstar.setText(self.tixi.getTextElement(path+"/rstar"))

    def tixiGetToolParameters(self):
        b = self.tixi.getBooleanElement("/cpacs/toolspecific/liftingLine/toolParameters/usePOLINT")
        self.comboUsePOLINT.setCurrentIndex(0 if b else 1)
        b = self.tixi.getIntegerElement("/cpacs/toolspecific/liftingLine/toolParameters/archiveMode")
        self.comboArchiveMode.setCurrentIndex(b)
        b = self.tixi.getIntegerElement("/cpacs/toolspecific/liftingLine/toolParameters/parallelComputation")
        self.textParallelComputation.setText(str(b))

        # if AircraftModelUID has changed, we must clear current available wingUIDs)
        if self.listWingUID.count() > 0 :
            self.listWingUID.clear()
            self.listWingUIDALL.clear()

        # check if AircraftModelUID was selected (AMUID list 2)
        if self.listAMUID2.count() > 0:
            # get selected model (list has only 0 or 1 items)
            model_uid  = self.listAMUID2.item(0).text()
            path = '/cpacs/vehicles/aircraft/model[@uID="' + model_uid + '"]/wings'
        
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
                else :
                    if cnt_wingPaneling > 1 :
                        print "ERROR!!!!!!!! more than one wingPaneling available but no uids"
                        break
                    else:
                        span  = self.tixi.getIntegerElement(path + "/wingPaneling[" + str(i) +"]/spanwise")
                        chord = self.tixi.getIntegerElement(path + "/wingPaneling[" + str(i) +"]/chordwise")
         

    ## ========================================================================================================================================================
    ## ========================================================================================================================================================
    ## checkbox fired functions
    ## ========================================================================================================================================================
    ## ========================================================================================================================================================

    def fire_enableTextDatasetName(self, n):
        self.textDataset.setEnabled(n)          

    def fire_enableTextWingUID(self, n):
        self.listWingUID.setVisible(n)
        self.labelWingUID.setVisible(n)
        
        if not n :
            # ATTENSION!!! clearSelection sends signal list item changed --> call fire_updateWingPanelingData
            self.listWingUID.clearSelection()
            self.__cur_wing_uid = ""
        self.textSpanwise.clear()
        self.textChordwise.clear()

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

    ## ========================================================================================================================================================
    ## ========================================================================================================================================================
    ## get values
    ## ========================================================================================================================================================
    ## ========================================================================================================================================================          
 
    
    def tixiSetToolName(self):
        self.__tixiUpdateTextElement("/cpacs/toolspecific/liftingLine/tool/name", self.textName.text())
    
    def tixiSetToolVersion(self):
        self.__tixiUpdateTextElement("/cpacs/toolspecific/liftingLine/tool/version", self.textVers.text())

    def tixiSetAircraftModelUID(self):
        self.__tixiUpdateTextElement("/cpacs/toolspecific/liftingLine/aircraftModelUID", self.listAMUID2.item(0))        

    def tixiSetDatasetName(self):
        isAvailNodeDatasetName = self.tixi.checkElement("/cpacs/toolspecific/liftingLine/datasetName")
        
        if self.checkDataset :
            if not isAvailNodeDatasetName :
                self.tixi.createElement("/cpacs/toolspecific/liftingLine", "datasetName") 
            self.__tixiUpdateTextElement("/cpacs/toolspecific/liftingLine/datasetName", self.textDataset.text()) 
        elif isAvailNodeDatasetName :
            self.tixi.removeElement("/cpacs/toolspecific/liftingLine/datasetName")

    
    def tixiSetLoadCaseOrPerformanceMap(self):
        # if loadCase
        if self.radioCaseVsPerMap1.isChecked() :
            self.__tixiSetLoadCaseOrPerformanceMap("/cpacs/toolspecific/liftingLine", "loadCases", "performanceMap")
            self.__tixiUpdateListElement("/cpacs/toolspecific/liftingLine/loadCases", "loadCaseUID", self.listLoadCaseUID2)
        else :
            self.__tixiSetLoadCaseOrPerformanceMap("/cpacs/toolspecific/liftingLine", "performanceMap", "loadCases")
            self.__tixiSetControlSurfaceUID()
            self.__tixiSetPositiveQuasiSteadyRotation()
            self.__tixiSetNegativeQuasiSteadyRotation()
            
    
    def __tixiSetLoadCaseOrPerformanceMap(self, path, used_child, unused_child):
        if not self.tixi.checkElement(path + "/" + used_child) :
            self.tixi.createElement(path, used_child)
            
        if self.tixi.checkElement(path + "/" + unused_child) :
            self.tixi.removeElement(path + "/" + unused_child)
        
    def __tixiSetControlSurfaceUID(self):
        self.__tixiUpdateListElement("/cpacs/toolspecific/liftingLine/performanceMap", "controlSurfaceUID", self.listCtrlSurUID2)        
        
    def __tixiSetPositiveQuasiSteadyRotation(self):
        path = "/cpacs/toolspecific/liftingLine/performanceMap/positiveQuasiSteadyRotation"
        self.__tixiUpdateTextElement(path + "/pstar", self.textPositiveSteadi_pstar)
        self.__tixiUpdateTextElement(path + "/qstar", self.textPositiveSteadi_qstar)
        self.__tixiUpdateTextElement(path + "/rstar", self.textPositiveSteadi_rstar)
    
    def __tixiSetNegativeQuasiSteadyRotation(self):
        path = "/cpacs/toolspecific/liftingLine/performanceMap/negativeQuasiSteadyRotation"
        self.__tixiUpdateTextElement(path + "/pstar", self.textNegativeSteadi_pstar)
        self.__tixiUpdateTextElement(path + "/qstar", self.textNegativeSteadi_qstar)
        self.__tixiUpdateTextElement(path + "/rstar", self.textNegativeSteadi_rstar)
    
    
    # if first wingPaneling has an uid then the following wingPanelings have to have one too
    def tixiSetSetToolParameters(self):
        self.__tixiUpdateTextElement("/cpacs/toolspecific/liftingLine/toolParameters/usePOLINT", self.comboUsePOLINT.currentText())
        self.__tixiUpdateTextElement("/cpacs/toolspecific/liftingLine/toolParameters/archiveMode", self.comboUsePOLINT.currentText())
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
                self.tixi.createElement(path, "wingPaneling[" + str(i+1) +"]")
                self.tixi.addTextElement(path + "/wingPaneling[" + str(i+1) +"]" , "wingUID", keys[i])
                self.tixi.addTextElement(path + "/wingPaneling[" + str(i+1) +"]" , "spanwise", span)
                self.tixi.addTextElement(path + "/wingPaneling[" + str(i+1) +"]" , "chordwise", chord)
        else:
            # remove all but first element
            for j in range(self.tixi.getNamedChildrenCount(path, "wingPaneling"), 0, -1) :
                self.tixi.removeElement(path + "/wingPaneling[" + str(j) +"]")  
            
            if self.tixi.checkElement(path + "wingPaneling/wingUID") :
                self.tixi.removeElement(path + "wingPaneling/wingUID")
          
            self.__tixiUpdateTextElement(path + "/wingPaneling/spanwise", self.textSpanwise.text())
            self.__tixiUpdateTextElement(path + "/wingPaneling/chordwise", self.textChordwise.text())
            

    def __tixiUpdateTextElement(self, path, text):
        if text != self.tixi.getTextElement(path):
            self.tixi.updateTextElement(path, text)
    

    def __tixiUpdateListElement(self, path, child, qlist):
        oldLoadCaseUIDs = set()
        for i in range(1, self.tixi.getNamedChildrenCount(path, child) + 1) :
            oldLoadCaseUIDs.update(self.tixi.getTextElement(path + "/" + child + "["+str(i)+"]"))

        newLoadCaseUIDs = set()
        for j in range(0, qlist.count()) :
            newLoadCaseUIDs.update(qlist.item(j))
            
        rmLoadCaseUIDs  = oldLoadCaseUIDs.difference(newLoadCaseUIDs)
        newLoadCaseUIDs = newLoadCaseUIDs.difference(oldLoadCaseUIDs)
        
        for k in range(self.tixi.getNamedChildrenCount(path, child), 0, -1) :        
            text = self.tixi.getTextElement(path + "/" + child + "["+str(k)+"]")
            
            if text in rmLoadCaseUIDs :
                self.tixi.removeElement(path + "/" + child + "["+str(k)+"]")
        
        for newUID in newLoadCaseUIDs:
            self.tixi.createElementAtIndex(path, child, 1)
            self.tixi.updateTextElement(path + "/" + child + "[1]", newUID)        
        
        
        
        
    
    def getValuesAircraftModelUID(self):
        print "not implemented yet"
        
    def getValuesDatasetName(self):
        return self.textDataset.text()
    
    def getValuesLoadCasesLoadCaseUID(self):
        return self.textLoadCaseUID.text()

    def getValuesPerformanceMap_1(self):
        return self.textPositiveSteadi.text() , self.textNegativeSteadi.text(), self.textCtrlSurUID.text()

    def getValuesPerformanceMap_2(self):
        return self.textMachNum.text(), self.textReynNum.text(), self.textAngleYaw.text(), self.textAngleAtt.text(), self.textPositiveSteadi.text(), self.textNegativeSteadi.text(), self.textCtrlSurfaces.text()


    ## ========================================================================================================================================================
    ## ========================================================================================================================================================
    ## list functions
    ## ========================================================================================================================================================
    ## ========================================================================================================================================================  

    def fire_modelUIDSwitchLeft(self):
        self.switchBetweenLists(self.listAMUID2, self.listAMUID1, False)
        self.tixiGetLoadCaseUID()
      
    def fire_modelUIDSwitchRight(self):
        self.switchBetweenLists(self.listAMUID1, self.listAMUID2, True)      
        self.tixiGetLoadCaseUID()
        
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

if __name__ == "__main__":
    app = QtGui.QApplication([])
    tixi = Tixi()
    tixi.openDocument(Config.path_cpacs_D150_2)
    test = ToolX("name", tixi)
    test.show()
    
    app.exec_()       