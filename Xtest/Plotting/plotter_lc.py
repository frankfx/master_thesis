'''
Created on Jan 28, 2015

@author: rene
'''
from tixiwrapper import Tixi
from PySide import QtGui, QtCore
from plotWidget import PlotWidget
from Xtest.config import Config
from __builtin__ import str

class Plotter_LC(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(Plotter_LC, self).__init__(parent) 
        
        self.tixi = Tixi()
        self.tixi.open(Config.path_cpacs_lc_ref)

        self.buttonBox = QtGui.QDialogButtonBox()
        self.buttonBox.addButton(QtGui.QDialogButtonBox.Ok)
        self.buttonBox.addButton(QtGui.QDialogButtonBox.Reset)
        self.buttonBox.addButton(QtGui.QDialogButtonBox.Cancel)

        self.plot_widget = PlotWidget("LC")

        self.comboBoxLoadCases = QtGui.QComboBox()
        self.fillComboBoxLoadCases()
        self.fire_LoadCaseChanged(0)

        self.grid = QtGui.QGridLayout()
        
        self.grid.addWidget(self.comboBoxLoadCases, 0,0)
        self.grid.addWidget(self.plot_widget, 1, 0)

        # set the layout
        layout = QtGui.QGridLayout()
        layout.addLayout(self.grid, 0,0,1,3)
        
        layout.addWidget(self.buttonBox, 5, 0, 1,3)
    
        widget = QtGui.QWidget()
        widget.setLayout(layout)
        
        self.setCentralWidget(widget)
    
        # ===============================================================================================
        # actions
        # ===============================================================================================
        self.comboBoxLoadCases.currentIndexChanged.connect(self.fire_LoadCaseChanged)
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).clicked.connect(self.close)
        self.buttonBox.button(QtGui.QDialogButtonBox.Reset).clicked.connect(self.close)
        self.buttonBox.button(QtGui.QDialogButtonBox.Cancel).clicked.connect(self.close)

    def fire_LoadCaseChanged(self, idx):
        uid = self.comboBoxLoadCases.currentText()
        path = '/cpacs/vehicles/aircraft/model[1]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID="' + uid + '"]'        
        x_axis, y_axis = self.getPlotPointValues(path)
        self.plot_widget.plot.clear()
        self.plot_widget.plot.grid(True)
        self.plot_widget.simplePlot(x_axis, y_axis)

    def fillComboBoxLoadCases(self):
        path_lc = "/cpacs/vehicles/aircraft/model[1]/analyses/loadAnalysis/loadCases"
        
        for idx_lc in range(1, self.tixi.getNumberOfChilds(path_lc) + 1) :
            tmp_path = path_lc + "/flightLoadCase[" + str(idx_lc) + "]"
            self.comboBoxLoadCases.addItem( self.tixi.getTextAttribute(tmp_path,"uID") )
            
    def getPlotPointValues(self, path):
        """... 
        
        Args:
            path  (String): path to specific flightLoadCase
        
        Returns:
            ...
        """ 
        xaxis = []
        yaxis = []
        path_wings = path + "/aeroLoads/wings"
        for idx_wing in range(1, self.tixi.getNumberOfChilds(path_wings) + 1) :
            path_segs = path_wings + "/wing[" + str(idx_wing) + "]/segments"
            for idx_seg in range(1, self.tixi.getNumberOfChilds(path_segs) + 1) :
                for idx_strip in range(1, self.tixi.getNamedChildrenCount(path_segs + "/segment[" + str(idx_seg) + "]", "strip") + 1) :
                    x =  self.tixi.getDoubleElement(path_segs + "/segment[" + str(idx_seg) + "]/strip[" + str(idx_strip) + "]/reference/point/x")
                    y = self.tixi.getDoubleElement(path_segs + "/segment[" + str(idx_seg) + "]/strip[" + str(idx_strip) + "]/reference/point/y")
                    xaxis.append(x)
                    yaxis.append(y)
        return xaxis, yaxis

if __name__ == "__main__":
    app = QtGui.QApplication([])
    test = Plotter_LC()
    test.show()
    
    app.exec_() 
