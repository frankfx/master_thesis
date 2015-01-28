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
    test = Plotter_DamingDerivates()
    test.show()
    
    app.exec_() 
