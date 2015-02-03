'''
Created on Jan 28, 2015

@author: rene
'''
from tixiwrapper import Tixi
from PySide import QtGui, QtCore
from plotWidget import PlotWidget
from Xtest.config import Config

class Plotter_ControlSurfaces(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(Plotter_ControlSurfaces, self).__init__(parent) 
        
        self.tixi = Tixi()
        self.tixi.open(Config.path_cpacs_pm_ref)

        self.buttonBox = QtGui.QDialogButtonBox()
        self.buttonBox.addButton(QtGui.QDialogButtonBox.Ok)
        self.buttonBox.addButton(QtGui.QDialogButtonBox.Reset)
        self.buttonBox.addButton(QtGui.QDialogButtonBox.Cancel)

        self.comboBoxXAxis = QtGui.QComboBox()
        self.comboBoxXAxis.addItem("machNumber")
        self.comboBoxXAxis.addItem("reynoldsNumber")
        self.comboBoxXAxis.addItem("angleOfYaw")
        self.comboBoxXAxis.addItem("angleOfAttack")
        self.comboBoxXAxis.addItem("relDeflection")

        self.comboBoxPlotPnt = QtGui.QComboBox()
        self.comboBoxPlotPnt.addItem("curve")
        self.comboBoxPlotPnt.addItem("points")

        self.comboBoxCtrlSurUID = QtGui.QComboBox()
        
        self.labelCtrlSurUID  = QtGui.QLabel("controlSurfaceUID")
        self.labelXAxis       = QtGui.QLabel("set x-axis")
        self.labelDisplay     = QtGui.QLabel("display")
        self.labelMachNum     = QtGui.QLabel("machNumber")
        self.labelReynoldsNum = QtGui.QLabel("reynoldsNumber")
        self.labelAngleOfYaw  = QtGui.QLabel("angleOfYaw")
        self.labelAngleOfAtt  = QtGui.QLabel("angleOfAttack")
        self.labelRelDefl     = QtGui.QLabel("relDeflection")

        self.listMachNum     = QtGui.QListWidget()
        self.listReynoldsNum = QtGui.QListWidget()
        self.listAngleOfYaw  = QtGui.QListWidget()
        self.listAngleOfAtt  = QtGui.QListWidget()
        self.listRelDefl     = QtGui.QListWidget()

        self.hidePlotLists(True, False, False, False, False)
        self.fillPlotLists("/cpacs/vehicles/aircraft/model[1]/analyses/aeroPerformanceMap")

        self.grid = QtGui.QGridLayout()
        
        self.grid.addWidget(self.labelCtrlSurUID,  0, 0, 1, 5)
        self.grid.addWidget(self.comboBoxCtrlSurUID,1,0, 1, 5)
        self.grid.addWidget(self.labelXAxis,       2,0,1,3)
        self.grid.addWidget(self.labelDisplay,     2,3,1,2)
        self.grid.addWidget(self.comboBoxXAxis,    3,0,1,3)
        self.grid.addWidget(self.comboBoxPlotPnt,  3,3,1,2)
        
        self.grid.addWidget(self.labelMachNum,     4,0)
        self.grid.addWidget(self.listMachNum,      5,0)
        self.grid.addWidget(self.labelReynoldsNum, 4,1)
        self.grid.addWidget(self.listReynoldsNum,  5,1)
        self.grid.addWidget(self.labelAngleOfYaw,  4,2)
        self.grid.addWidget(self.listAngleOfYaw,   5,2)
        self.grid.addWidget(self.labelAngleOfAtt,  4,3)
        self.grid.addWidget(self.listAngleOfAtt,   5,3)
        self.grid.addWidget(self.labelRelDefl,     4,4)
        self.grid.addWidget(self.listRelDefl,      5,4)

        # set the layout
        layout = QtGui.QGridLayout()
        layout.addLayout(self.grid, 0,0,1,3)
        
        layout.addWidget(self.buttonBox, 5, 0, 1,3)
    
        widget = QtGui.QWidget()
        widget.setLayout(layout)
        
        self.setCentralWidget(widget)
    
        # add observer
        self.plotWidgets = [PlotWidget("dcfx"), PlotWidget("dcfy"), PlotWidget("dcfz"), PlotWidget("dcmx"), PlotWidget("dcmy"), PlotWidget("dcmz")]
        
        self.dockList = []
        
        for widget in self.plotWidgets :
            dock = self.addSimpleWidget(widget.getTitle(), widget)
            insertIndex = len(self.dockList) - 1
            self.dockList.insert(insertIndex, dock)

        if len(self.dockList) > 1:
            for index in range(0, len(self.dockList) - 1):
                self.tabifyDockWidget(self.dockList[index],
                                      self.dockList[index + 1])
        self.dockList[0].raise_()
        self.nextindex = 1  

        # ===============================================================================================
        # actions
        # ===============================================================================================
        self.comboBoxXAxis.currentIndexChanged.connect(self.fire_XAxisChanged)
        self.comboBoxCtrlSurUID.currentIndexChanged.connect(self.fire_CtrlSurfacesChanged)
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).clicked.connect(self.plot)
        self.buttonBox.button(QtGui.QDialogButtonBox.Reset).clicked.connect(self.reset)
        self.buttonBox.button(QtGui.QDialogButtonBox.Cancel).clicked.connect(self.close)


    def addSimpleWidget(self, name, widget):
        ''' create dock widget and set it to main window'''
        dock = QtGui.QDockWidget(name)
        dock.setWidget(widget)
        dock.setMinimumWidth(100)
        dock.setMinimumHeight(300)
        
        dock.setAllowedAreas(QtCore.Qt.AllDockWidgetAreas)
        dock.setFeatures(QtGui.QDockWidget.DockWidgetClosable |
                         QtGui.QDockWidget.DockWidgetMovable |
                         QtGui.QDockWidget.DockWidgetFloatable)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, dock)
        return dock


    def fire_XAxisChanged(self, idx):
        '''sets all options if the x-axis was changed'''
        self.reset()
        self.hidePlotLists(idx == 0, idx == 1, idx == 2, idx == 3, idx == 4)

    def fire_CtrlSurfacesChanged(self, idx):
        '''sets all options if the controlSurface was changed'''
        self.reset()
        self.listRelDefl.clear()
        
        for item in self.getRelDeflectionVector("/cpacs/vehicles/aircraft/model[1]/analyses/aeroPerformanceMap", self.comboBoxCtrlSurUID.currentText()):
            self.listRelDefl.addItem(str(item))

    def plot(self):
        '''updates all observer plot widgets'''

        path = "/cpacs/vehicles/aircraft/model[1]/analyses/aeroPerformanceMap"

        x_axis_idx = self.comboBoxXAxis.currentIndex()

        # indices of the lists
        mach_idx   = self.listMachNum.currentRow()
        reyn_idx   = self.listReynoldsNum.currentRow()
        yaw_idx    = self.listAngleOfYaw.currentRow()
        att_idx    = self.listAngleOfAtt.currentRow()  
        relDef_idx = self.listRelDefl.currentRow() 

        # get uid of chosen controlSurfaces
        relDef_uid = self.comboBoxCtrlSurUID.currentText()

        # determine x-axis
        if x_axis_idx == 0 :
            x_axis = self.getMachNumberVector(path)
        elif x_axis_idx == 1 :
            x_axis = self.getReynoldsNumberVector(path)
        elif x_axis_idx == 2 :
            x_axis = self.getAngleOfYawVector(path)  
        elif x_axis_idx == 3 :
            x_axis = self.getAngleOfAttackVector(path)  
        elif x_axis_idx == 4 :
            x_axis = self.getRelDeflectionVector(path, relDef_uid)
        
        # dimSize == product over all sizes (for complete array size)
        # cnt_mach, cnt_reyn, cnt_angleYaw, cnt_angleAtt) == size of coefficients
        ((cnt_mach, cnt_reyn, cnt_angleYaw, cnt_angleAtt), size) = self.tixi.getArrayDimensionSizes(path, 4)
        
        # the same for controlSurface
        ((cnt_relDef,_), _) = self.tixi.getArrayDimensionSizes(path + "/controlSurfaces/controlSurface[" 
                                                               + str(self.tixiGetIdxOfUID(relDef_uid)) + "]", 2)
        # determine complete array size (including relDeflection)
        size = size * cnt_relDef
        
        # set drawing option
        displayOpt = 'go' if self.comboBoxPlotPnt.currentText() == "points" else "" 

        dimPos = [mach_idx, reyn_idx, yaw_idx, att_idx, relDef_idx]
        dimSize = [cnt_mach, cnt_reyn, cnt_angleYaw, cnt_angleAtt, cnt_relDef]
        dims = 5 # self.tixi.getArrayDimensions(path + "/controlSurfaces/controlSurface[" + str(self.tixiGetIdxOfUID(relDef_uid)) + "]") + oben dims 
         
        # update all observer
        for widget in self.plotWidgets:
            # determine coefficient array 
            array = self.getCoefficientArray(path + "/controlSurfaces/controlSurface[1]", widget.getTitle(), size)
            
            widget.setXLabel(self.comboBoxXAxis.currentText())
            widget.updatePlot(array, dimSize, dimPos, dims, x_axis, x_axis_idx, self.tixi, path, displayOpt)
            
    def reset(self):
        '''resets all observer'''
        for widget in self.plotWidgets:
            widget.updateReset()

    def tixiGetIdxOfUID(self, uID):
        """determines the index of a given controlSurface uID  
        
        Args:
            uID (String): controlSurface uID
        
        Returns:
            the index of the controlSurface with the given uID
        """   
        path = "/cpacs/vehicles/aircraft/model[1]/analyses/aeroPerformanceMap/controlSurfaces"
        for i in range(1, self.tixi.getNumberOfChilds(path) +1 ) :
            tmp_uid = self.tixi.getTextElement(path + "/controlSurface[" + str(i) + "]/controlSurfaceUID")
            if uID == tmp_uid :
                return i
        return None

    def fillPlotLists(self, path):
        """fills the five list boxes
        
        Args:
            path (String): path to aeroPerformanceMap
        """         
        
        for item in self.getMachNumberVector(path) :
            self.listMachNum.addItem(str(item))
        
        for item in self.getReynoldsNumberVector(path) :
            self.listReynoldsNum.addItem(str(item))

        for item in self.getAngleOfYawVector(path) :
            self.listAngleOfYaw.addItem(str(item))
        
        for item in self.getAngleOfAttackVector(path) :
            self.listAngleOfAtt.addItem(str(item))
            
        for i in range(1, self.tixi.getNumberOfChilds(path + "/controlSurfaces") +1) :
            uid = self.tixi.getTextElement(path + "/controlSurfaces/controlSurface[" + str(i) + "]/controlSurfaceUID")
            self.comboBoxCtrlSurUID.addItem(uid)
            if(i == 1): # pre-fill relDeflection list
                for item in self.getRelDeflectionVector(path, uid):
                    self.listRelDefl.addItem(str(item))
        
    def getAngleOfYawVector(self, path):
        return self.tixi.getFloatVector(path + "/angleOfYaw", self.tixi.getVectorSize(path + "/angleOfYaw"))

    def getAngleOfAttackVector(self, path):
        return self.tixi.getFloatVector(path + "/angleOfAttack", self.tixi.getVectorSize(path + "/angleOfAttack"))

    def getReynoldsNumberVector(self, path):
        return self.tixi.getFloatVector(path + "/reynoldsNumber", self.tixi.getVectorSize(path + "/reynoldsNumber"))

    def getMachNumberVector(self, path):
        return self.tixi.getFloatVector(path + "/machNumber", self.tixi.getVectorSize(path + "/machNumber"))

    def getRelDeflectionVector(self, path, uid):
        """returns relDeflection of a controlSurface given by a uid
        
        Args:
            path (String): path to aeroPerformanceMap
        """         
        for i in range(1, self.tixi.getNumberOfChilds(path) +1) : 
            _uid = self.tixi.getTextElement(path + "/controlSurfaces/controlSurface[" + str(i) + "]/controlSurfaceUID")
            if(_uid == uid): 
                p = path + "/controlSurfaces/controlSurface[" + str(i) + "]/relDeflection"
                return self.tixi.getFloatVector(p, self.tixi.getVectorSize(p))
        return None
        
    def getCoefficientArray(self, path, child, num):
        """returns the array of a given path, child node and element count  
        
        Args:
            path  (String): path to array
            child (String): child node to array 
            num   (int): count of elements
        
        Returns:
            the square root of n.
        """        
        return self.tixi.getArray(path, child, num)

    # This function hides labels and plot lists.
    def hidePlotLists(self, flag_mach, flag_reyn, flag_yaw, flag_att, flag_relDef):
        """hides labels and plot lists. 
        
        Args:
            flag_mach   (bool): hide label of machNumber and list of machNumber
            flag_reyn   (bool): hide label of reynoldNumber and list of reynoldNumber
            flag_yaw    (bool): hide label of angleOfYaw and list of angleOfYaw
            flag_att    (bool): hide label of angleOfAttack and list of angleOfAttack
            flag_relDef (bool): hide label of relDeflection and list of relDeflection
        """
        self.labelMachNum.setHidden(flag_mach)
        self.labelReynoldsNum.setHidden(flag_reyn)
        self.labelAngleOfYaw.setHidden(flag_yaw)
        self.labelAngleOfAtt.setHidden(flag_att)
        self.labelRelDefl.setHidden(flag_relDef)
        self.listMachNum.setHidden(flag_mach)
        self.listReynoldsNum.setHidden(flag_reyn)
        self.listAngleOfYaw.setHidden(flag_yaw)
        self.listAngleOfAtt.setHidden(flag_att)
        self.listRelDefl.setHidden(flag_relDef)

if __name__ == "__main__":
    app = QtGui.QApplication([])
    test = Plotter_ControlSurfaces()
    test.show()
    
    app.exec_() 
