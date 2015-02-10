from PySide import QtCore, QtGui
from Xtest.XML_Editor.editor_xml import EditorWindow
from Xtest.Vehicle.MainViewWidget import MainWidget
from Xtest.config import Config
from tiglwrapper   import Tigl, TiglException
from tixiwrapper   import Tixi

class MainWindow(QtGui.QMainWindow):
    """initialize editor"""
    def __init__(self):
        super(MainWindow, self).__init__()       

        self.setWindowTitle('Main Window')

        tixi = Tixi()
      #  tixi.open(conf.path_cpacs_simple)
        #tixi.open(Config.path_cpacs_D150_3)
        tixi.openDocument(Config.path_cpacs_simple) 
        #tixi.openDocument(conf.path_cpacs_A320_Wing) 
        #self.tixi.schemaValidateFromFile(cpacs_scheme)
        
        tigl = Tigl()
        try:
            tigl.open(tixi,"")
        except TiglException as err:    
            print ('Error opening tigl document: ', err.__str__())
        
       # self.setCentralWidget(self.button)
        
        xml_editor = EditorWindow(tixi, Config.path_cpacs_simple)
        ogl_editor = MainWidget(tixi, tigl)
        
       # dockWidgets = [('xml editor', xml_editor)]
        dockWidgets = [('xml editor', xml_editor), ('ogl editor', ogl_editor)]
        
        xml_editor.updateAction.triggered.connect(ogl_editor.updateView)
        
        for (name, widget) in dockWidgets :
            self.addSimpleWidget(name, widget)

    def addSimpleWidget(self, name, widget):
        dock = QtGui.QDockWidget(name)
        dock.setWidget(widget)
        dock.setAllowedAreas(QtCore.Qt.AllDockWidgetAreas)
        dock.setFeatures(QtGui.QDockWidget.DockWidgetMovable |
                         QtGui.QDockWidget.DockWidgetFloatable)
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea, dock)

if __name__ == '__main__':


    import sys
    app = QtGui.QApplication(sys.argv)
    pDesktop = QtGui.QApplication.desktop()
    geometry = pDesktop.availableGeometry(2)
     #move(geometry.topLeft());
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())