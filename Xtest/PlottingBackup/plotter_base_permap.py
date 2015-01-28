'''
Created on Jan 28, 2015

@author: rene
'''
from tixiwrapper import Tixi
from PySide import QtGui, QtCore
from plotWidget import PlotWidget

class Plotter_BasePerMap(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(Plotter_BasePerMap, self).__init__(parent) 
        
        self.tixi = Tixi()
        self.tixi.open("../cpacs_files/outputfile_PM_Ref.xml")

        self.buttonBox = QtGui.QDialogButtonBox()
        self.buttonBox.addButton(QtGui.QDialogButtonBox.Ok)
        self.buttonBox.addButton(QtGui.QDialogButtonBox.Reset)
        self.buttonBox.addButton(QtGui.QDialogButtonBox.Cancel)

        self.comboBoxXAxis = QtGui.QComboBox()
        self.comboBoxXAxis.addItem("machNumber")
        self.comboBoxXAxis.addItem("reynoldsNumber")
        self.comboBoxXAxis.addItem("angleOfYaw")
        self.comboBoxXAxis.addItem("angleOfAttack")

        self.comboBoxPlotPnt = QtGui.QComboBox()
        self.comboBoxPlotPnt.addItem("curve")
        self.comboBoxPlotPnt.addItem("points")
        
        self.labelXAxis       = QtGui.QLabel("set x-axis")
        self.labelDisplay     = QtGui.QLabel("display")
        self.labelMachNum     = QtGui.QLabel("machNumber")
        self.labelReynoldsNum = QtGui.QLabel("reynoldsNumber")
        self.labelAngleOfYaw  = QtGui.QLabel("angleOfYaw")
        self.labelAngleOfAtt  = QtGui.QLabel("angleOfAttack")

        self.listMachNum     = QtGui.QListWidget()
        self.listReynoldsNum = QtGui.QListWidget()
        self.listAngleOfYaw  = QtGui.QListWidget()
        self.listAngleOfAtt  = QtGui.QListWidget()

        #self.comboBoxXAxis.setCurrentIndex(0)
        self.__hidePlotLists(True, False, False, False)
        self.__fillPlotLists("/cpacs/vehicles/aircraft/model[1]/analyses/aeroPerformanceMap")

        self.grid = QtGui.QGridLayout()

        self.grid.addWidget(self.labelXAxis,       0,0,1,3)
        self.grid.addWidget(self.labelDisplay,     0,3)
        self.grid.addWidget(self.comboBoxXAxis,    1,0,1,3)
        self.grid.addWidget(self.comboBoxPlotPnt,  1,3)
        
        self.grid.addWidget(self.labelMachNum,     2,0)
        self.grid.addWidget(self.listMachNum,      3,0)
        self.grid.addWidget(self.labelReynoldsNum, 2,1)
        self.grid.addWidget(self.listReynoldsNum,  3,1)
        self.grid.addWidget(self.labelAngleOfYaw,  2,2)
        self.grid.addWidget(self.listAngleOfYaw,   3,2)
        self.grid.addWidget(self.labelAngleOfAtt,  2,3)
        self.grid.addWidget(self.listAngleOfAtt,   3,3)

        # set the layout
        layout = QtGui.QGridLayout()
        layout.addLayout(self.grid, 0,0,1,3)
        
        layout.addWidget(self.buttonBox, 5, 0, 1,3)
    
        widget = QtGui.QWidget()
        widget.setLayout(layout)
        
        self.setCentralWidget(widget)
    
        self.plotWidgets = [PlotWidget("cfx"), PlotWidget("cfy"), PlotWidget("cfz"), PlotWidget("cmx"), PlotWidget("cmy"), PlotWidget("cmz")]
        
        i = 0 ; l = len(self.plotWidgets) / 4
        for widget in self.plotWidgets :
            if i < l :
                self.addSimpleWidget(widget, QtCore.Qt.LeftDockWidgetArea, True) 
            elif i < 2 * l :
                self.addSimpleWidget(widget, QtCore.Qt.RightDockWidgetArea, True)
            else :
                self.addSimpleWidget(widget, QtCore.Qt.BottomDockWidgetArea, False)
            i+=1

        # ===============================================================================================
        # actions
        # ===============================================================================================
        self.comboBoxXAxis.currentIndexChanged.connect(self.fire_XAxisChanged)
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).clicked.connect(self.plot)
        self.buttonBox.button(QtGui.QDialogButtonBox.Reset).clicked.connect(self.reset)
        self.buttonBox.button(QtGui.QDialogButtonBox.Cancel).clicked.connect(self.close)


    def addSimpleWidget(self,widget, dockWidgetArea, flag_side):
        dock = QtGui.QDockWidget()
        dock.setWidget(widget)
        if flag_side :
            dock.setMinimumWidth(300)
            dock.setMinimumHeight(300)
        else: 
            dock.setMinimumWidth(200)
            dock.setMinimumHeight(300)
        
        dock.setAllowedAreas(dockWidgetArea)
        dock.setFeatures(QtGui.QDockWidget.DockWidgetClosable |
                         QtGui.QDockWidget.DockWidgetMovable |
                         QtGui.QDockWidget.DockWidgetFloatable)
        self.addDockWidget(dockWidgetArea, dock)


    def fire_XAxisChanged(self, idx):
        self.reset()
        self.__setPlotListVisibility(idx == 0, idx == 1, idx == 2, idx == 3)

    def plot(self):
        x_axis_idx = self.comboBoxXAxis.currentIndex()
        mach_idx   = self.listMachNum.currentRow()
        reyn_idx   = self.listReynoldsNum.currentRow()
        yaw_idx    = self.listAngleOfYaw.currentRow()
        att_idx    = self.listAngleOfAtt.currentRow()   
        
        path = "/cpacs/vehicles/aircraft/model[1]/analyses/aeroPerformanceMap"
        
        if x_axis_idx == 0 :
            x_axis = self.getMachNumberVector(path)
        elif x_axis_idx == 1 :
            x_axis = self.getReynoldsNumberVector(path)
        elif x_axis_idx == 2 :
            x_axis = self.getAngleOfYawVector(path)  
        elif x_axis_idx == 3 :
            x_axis = self.getAngleOfAttackVector(path)  
        
        ((cnt_mach, cnt_reyn, cnt_angleYaw, cnt_angleAtt), size) = self.tixi.getArrayDimensionSizes(path, 4)
        
        displayOpt = 'go' if self.comboBoxPlotPnt.currentText() == "points" else "" 
        
        for widget in self.plotWidgets:
            array = self.getCoefficientArray(path, widget.getTitle(), size)
            
            dimPos = [mach_idx, reyn_idx, yaw_idx, att_idx]
            dimSize = [cnt_mach, cnt_reyn, cnt_angleYaw, cnt_angleAtt]
                        
            
            widget.setXLabel(self.comboBoxXAxis.currentText())
            widget.updatePlot(self.tixi, path, x_axis_idx, x_axis, array, dimPos, dimSize, displayOpt)
            
    def reset(self):
        for widget in self.plotWidgets:
            widget.updateReset()


    def __fillPlotLists(self, path):
        for item in self.getMachNumberVector(path) :
            self.listMachNum.addItem(str(item))
        
        for item in self.getReynoldsNumberVector(path) :
            self.listReynoldsNum.addItem(str(item))

        for item in self.getAngleOfYawVector(path) :
            self.listAngleOfYaw.addItem(str(item))
        
        for item in self.getAngleOfAttackVector(path) :
            self.listAngleOfAtt.addItem(str(item))

    def getAngleOfYawVector(self, path):
        return self.tixi.getFloatVector(path + "/angleOfYaw", self.tixi.getVectorSize(path + "/angleOfYaw"))

    def getAngleOfAttackVector(self, path):
        return self.tixi.getFloatVector(path + "/angleOfAttack", self.tixi.getVectorSize(path + "/angleOfAttack"))

    def getReynoldsNumberVector(self, path):
        return self.tixi.getFloatVector(path + "/reynoldsNumber", self.tixi.getVectorSize(path + "/reynoldsNumber"))

    def getMachNumberVector(self, path):
        return self.tixi.getFloatVector(path + "/machNumber", self.tixi.getVectorSize(path + "/machNumber"))

    def getCoefficientArray(self, path, child, num):
        return self.tixi.getArray(path , child, num)

    def __hidePlotLists(self, flag_mach, flag_reyn, flag_yaw, flag_att):
        self.__setPlotListVisibility(flag_mach, flag_reyn, flag_yaw, flag_att)

    def __setPlotListVisibility(self, flag_mach, flag_reyn, flag_yaw, flag_att):
        self.labelMachNum.setHidden(flag_mach)
        self.labelReynoldsNum.setHidden(flag_reyn)
        self.labelAngleOfYaw.setHidden(flag_yaw)
        self.labelAngleOfAtt.setHidden(flag_att)
        self.listMachNum.setHidden(flag_mach)
        self.listReynoldsNum.setHidden(flag_reyn)
        self.listAngleOfYaw.setHidden(flag_yaw)
        self.listAngleOfAtt.setHidden(flag_att)

if __name__ == "__main__":
    app = QtGui.QApplication([])
    test = Plotter_BasePerMap()
    test.show()
    
    app.exec_() 
