'''
Created on Jan 28, 2015

@author: rene
'''
from PySide import QtGui
from plotWidget import PlotWidget
from plotter import Plotter

class Plotter_BasePerMap(Plotter):
    def __init__(self, path="/cpacs/vehicles/aircraft/model[1]/analyses/aeroPerformanceMap", parent=None):
        super(Plotter_BasePerMap, self).__init__(path, parent) 
        
        # add observer
        self.plotWidgets = [PlotWidget("cfx"), PlotWidget("cfy"), PlotWidget("cfz"), 
                            PlotWidget("cmx"), PlotWidget("cmy"), PlotWidget("cmz")]

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
        

if __name__ == "__main__":
    app = QtGui.QApplication([])
    test = Plotter_BasePerMap()
    test.show()
    
    app.exec_() 
