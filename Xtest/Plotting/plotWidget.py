'''
Created on Jan 28, 2015

@author: rene
'''
import matplotlib
matplotlib.use('Qt4Agg')
matplotlib.rcParams['backend.qt4']='PySide'
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar

from PySide import QtGui
from matplotlib.figure import Figure

class PlotWidget(QtGui.QWidget):
    def __init__(self, title, parent=None):
        super(PlotWidget, self).__init__(parent) 

        self.title = title
        self.createPlotCanvases(title)
        
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def getTitle(self):
        return self.title

    def setXLabel(self, xlabel):
        self.plot.set_xlabel(xlabel,fontsize=8)
    
    def createPlotCanvases(self, title):
        # create figure instances to plot on
        figure = Figure(figsize=(5,4), dpi=100)
        
        self.plot = figure.add_subplot(111)
        self.plot.grid(True)
        self.plot.tick_params(axis='x', labelsize=6)
        self.plot.tick_params(axis='y', labelsize=6)

        figure.subplots_adjust(left=0.15, bottom=0.2, right=0.9, top=0.9, wspace=0.2, hspace=0.5)
        
        figure.suptitle(title, fontsize=8)
        # this is the Canvas Widget that displays the `figure`
        self.canvas = FigureCanvas(figure)
        self.canvas.setContentsMargins(110, 50, 50, 50)
        # this is the Navigation widget
        self.toolbar = NavigationToolbar(self.canvas, self)  

    def updateReset(self):
        self.plot.clear()
        self.plot.grid(True)
        self.canvas.draw()

    def updatePlot(self, tixi, path, x_axis_idx, x_axis, array, dimPos, dimSize, displayOpt):
        """update the plot window. 
        
        Args:
            tixi       (Tixi)   : to get the Array value
            path       (String) : path to aeroPerformanceMap
            
            x_axis_idx (int)    : index of the chosen x-axis (e.g. in for all list)
            x_axis     ([float]): x-axis float array

            array      ([float]): coefficent array
            dimPos     ([int])  : e.g. dimPos = [mach_idx, reyn_idx, yaw_idx, att_idx, relDef_idx]
            dimSize    ([int])  : e.g. dimSize = [cnt_mach, cnt_reyn, cnt_angleYaw, cnt_angleAtt, cnt_relDef]
            displayOpt (String) : option if plots line or point style 
        
        """        
        y_axis = []

        dims = len(dimSize)

        for i in range(dimSize[x_axis_idx]) :
            dimPos[x_axis_idx] = i
            y_axis.append(tixi.getArrayValue(array, dimSize, dimPos, dims))
       
        print x_axis
        print y_axis
       
        self.plot.plot(x_axis, y_axis, displayOpt)
        self.canvas.draw()
        
if __name__ == "__main__":
    app = QtGui.QApplication([])
    test = PlotWidget("test")
    test.show()
    
    app.exec_()