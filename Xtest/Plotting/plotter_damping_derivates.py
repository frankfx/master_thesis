'''
Created on Jan 28, 2015

@author: rene
'''
'''
Created on Jan 28, 2015

@author: rene
'''
from PySide import QtGui, QtCore
from plotWidget import PlotWidget
from plotter import Plotter

class Plotter_DamingDerivates(Plotter):
    def __init__(self, path="/cpacs/vehicles/aircraft/model[1]/analyses/aeroPerformanceMap/dampingDerivatives/positiveRates", parent=None):
        super(Plotter_DamingDerivates, self).__init__(path, parent) 
    
        self.plotWidgets = [PlotWidget("dcfxdpstar"), PlotWidget("dcfxdqstar"), PlotWidget("dcfxdrstar"), 
                            PlotWidget("dcfydpstar"), PlotWidget("dcfydqstar"), PlotWidget("dcfydrstar"),
                            PlotWidget("dcfzdpstar"), PlotWidget("dcfzdqstar"), PlotWidget("dcfzdrstar"),
                            PlotWidget("dcmxdpstar"), PlotWidget("dcmxdqstar"), PlotWidget("dcmxdrstar"),
                            PlotWidget("dcmydpstar"), PlotWidget("dcmydqstar"), PlotWidget("dcmydrstar"),
                            PlotWidget("dcmzdpstar"), PlotWidget("dcmzdqstar"), PlotWidget("dcmzdrstar")]
        
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
    test = Plotter_DamingDerivates()
    test.show()
    
    app.exec_() 
