'''
Created on Jan 28, 2015

@author: rene
'''
from PySide import QtGui, QtCore
from plotWidget import PlotWidget
from plotter import Plotter

class Plotter_BasePerMap(Plotter):
    def __init__(self, path="/cpacs/vehicles/aircraft/model[1]/analyses/aeroPerformanceMap", parent=None):
        super(Plotter_BasePerMap, self).__init__(path, parent) 
        
        # add observer
        self.plotWidgets = [PlotWidget("cfx"), PlotWidget("cfy"), PlotWidget("cfz"), 
                            PlotWidget("cmx"), PlotWidget("cmy"), PlotWidget("cmz")]
        
        i = 0 ; l = len(self.plotWidgets) / 4
        for widget in self.plotWidgets :
            if i < l :
                self.addSimpleWidget(widget, QtCore.Qt.LeftDockWidgetArea, True) 
            elif i < 2 * l :
                self.addSimpleWidget(widget, QtCore.Qt.RightDockWidgetArea, True)
            else :
                self.addSimpleWidget(widget, QtCore.Qt.BottomDockWidgetArea, False)
            i+=1

if __name__ == "__main__":
    app = QtGui.QApplication([])
    test = Plotter_BasePerMap()
    test.show()
    
    app.exec_() 
