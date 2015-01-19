'''
Created on Jan 14, 2015

@author: fran_re
'''

from PySide import QtGui, QtCore
from PySide.QtGui import QApplication

class XPathDialog(QtGui.QMainWindow):
    '''
    ...
    '''
    def __init__(self, xpath_idx, xpath_uid):
        '''
        Constructor
        '''
        super(XPathDialog, self).__init__()          
        
        self.xpath_idx  = xpath_idx
        self.xpath_uid  = xpath_uid
        
        widget = QtGui.QWidget()
        self.setCentralWidget(widget)

        topFiller = QtGui.QWidget()
        topFiller.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        
        self.infoLabel = QtGui.QLabel("  " + xpath_uid + "  ")
        self.infoLabel.setStyleSheet("font: 14px")
        

        self.scrollArea = QtGui.QScrollArea()
        self.scrollArea.setFixedHeight(60)
        self.scrollArea.setWidget(self.infoLabel)
        
       
        bottomFiller = QtGui.QWidget()
        bottomFiller.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)        

        vbox = QtGui.QVBoxLayout()
        vbox.setContentsMargins(5, 5, 5, 5)
        vbox.addWidget(topFiller)
        vbox.addWidget(self.scrollArea)
        vbox.addWidget(bottomFiller)
        widget.setLayout(vbox)

        self.createActions()
        self.createMenus()

        message = "A context menu is available by right-clicking"
        self.statusBar().showMessage(message)

        self.setWindowTitle("Menus")
        self.setMinimumSize(160,160)
        self.resize(480,320)

    def contextMenuEvent(self, event):
        menu = QtGui.QMenu(self)
        menu.addAction(self.copyAct)
        menu.addAction(self.xpathIdxAct)
        menu.addAction(self.xpathUidAct)
        menu.exec_(event.globalPos())        
        
    def createMenus(self):
        self.editMenu = self.menuBar().addMenu("&Menu")
        self.editMenu.addAction(self.copyAct)
        self.editMenu.addAction(self.xpathIdxAct)
        self.editMenu.addAction(self.xpathUidAct)
        self.editMenu.addAction(self.closeAct)
        
    def createActions(self):
        self.copyAct = QtGui.QAction("&Copy", self,
                shortcut=QtGui.QKeySequence.Copy,
                statusTip="Copy the current selection's contents to the clipboard",
                triggered=self.copy)        

        self.xpathIdxAct = QtGui.QAction("&XPath Index", self,
                statusTip="Show XPath with indices",
                triggered=self.setIdxXPath)

        self.xpathUidAct = QtGui.QAction("&XPath uID", self,
                statusTip="Show XPath with uids",
                triggered=self.setUidXPath)
    
        self.closeAct = QtGui.QAction("C&lose", self, shortcut="Ctrl+Q",
                statusTip="Exit the application", triggered=self.close)
    
    def setUidXPath(self):
        self.infoLabel.setText("  "+self.xpath_uid+"  ")
        self.infoLabel.setFixedWidth(self.infoLabel.fontMetrics().boundingRect(self.infoLabel.text()).width())
    
    def setIdxXPath(self):
        self.infoLabel.setText("  "+self.xpath_idx+"  ")
        self.infoLabel.setFixedWidth(self.infoLabel.fontMetrics().boundingRect(self.infoLabel.text()).width())
    
    def copy(self):
        self.clipboard = QtGui.QApplication.clipboard()
        self.clipboard.setText(self.infoLabel.text().replace(" ", ""), QtGui.QClipboard.Clipboard)

    def closeEvent(self,event):
        print "hi"
        # bad solution but it works - for editor_Window getCursorXPath 
        self.closeAct.trigger()
        event.accept()

if __name__ == "__main__":
    app = QtGui.QApplication([])
    test = XPathDialog("hallo Rene", "jens pfeifer")
    test.show()
    app.exec_()       