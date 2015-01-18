from PySide import QtCore, QtGui
from Xtest.XML_Editor.editor_xml import EditorWindow
from Xtest.Vehicle.sideViewOGL import Widget
from Xtest.XML_Editor.configuration.config import Config
from tiglwrapper   import Tigl, TiglException
from tixiwrapper   import Tixi, TixiException

class MainWindow(QtGui.QMainWindow):
    """initialize editor"""
    def __init__(self):
        super(MainWindow, self).__init__()       

        self.setWindowTitle('Main Window')

        conf = Config()
        tixi = Tixi()
        tixi.open(conf.path_cpacs_simple)
        #tixi.open(conf.path_cpacs_D150)
        
        tigl = Tigl()
        try:
            tigl.open(tixi,"")
        except TiglException as err:    
            print 'Error opening tigl document: ', err.__str__()
        
        
        self.button = QtGui.QPushButton('Raise Next Tab', self)
        self.button.clicked.connect(self.handleButton)
        self.setCentralWidget(self.button)
       
        dockWidgets = [('xml editor', EditorWindow(tixi)), ('ogl editor', Widget(tixi, tigl)), 
                       ('Red', QtGui.QListWidget()), ('Green', QtGui.QListWidget())]
        
        #dockWidgets[0].updateAction.triggered.connect(self.fireUpdate)
        
        self.dockList = []

        for (name, widget) in dockWidgets :
            dock = self.addSimpleWidget(name, widget)
            insertIndex = len(self.dockList) - 1
            self.dockList.insert(insertIndex, dock)

        if len(self.dockList) > 1:
            for index in range(0, len(self.dockList) - 1):
                self.tabifyDockWidget(self.dockList[index],
                                      self.dockList[index + 1])
        self.dockList[0].raise_()
        self.nextindex = 1

    def addSimpleWidget(self, name, widget):
        dock = QtGui.QDockWidget(name)
        dock.setWidget(widget)
        dock.setAllowedAreas(QtCore.Qt.TopDockWidgetArea)
        dock.setFeatures(QtGui.QDockWidget.DockWidgetMovable |
                         QtGui.QDockWidget.DockWidgetFloatable)
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea, dock)
        return dock       

    def handleButton(self):
        self.dockList[self.nextindex].raise_()
        self.nextindex += 1
        if self.nextindex > len(self.dockList) - 1:
            self.nextindex = 0

if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())