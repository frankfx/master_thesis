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
    def __init__(self, xpath):
        '''
        Constructor
        '''
        super(XPathDialog, self).__init__()          
        
        widget = QtGui.QWidget()
        self.setCentralWidget(widget)

        topFiller = QtGui.QWidget()
        topFiller.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        
        self.infoLabel = QtGui.QLabel(xpath , alignment=QtCore.Qt.AlignCenter)
        self.infoLabel.setFrameStyle(QtGui.QFrame.StyledPanel | QtGui.QFrame.Sunken)        
        
        bottomFiller = QtGui.QWidget()
        bottomFiller.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)        

        vbox = QtGui.QVBoxLayout()
        vbox.setContentsMargins(5, 5, 5, 5)
        vbox.addWidget(topFiller)
        vbox.addWidget(self.infoLabel)
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
        menu.exec_(event.globalPos())        
        
    def createMenus(self):
        self.editMenu = self.menuBar().addMenu("&Edit")
        self.editMenu.addAction(self.copyAct)
        self.editMenu.addAction(self.closeAct)
        
        
    def createActions(self):
        self.copyAct = QtGui.QAction("&Copy", self,
                shortcut=QtGui.QKeySequence.Copy,
                statusTip="Copy the current selection's contents to the clipboard",
                triggered=self.copy)        
    
        self.closeAct = QtGui.QAction("C&lose", self, shortcut="Ctrl+Q",
                statusTip="Exit the application", triggered=None)
    
    def copy(self):
        self.clipboard = QtGui.QApplication.clipboard()
        self.clipboard.setText(self.infoLabel.text().replace("</*i>", ""), QtGui.QClipboard.Clipboard)

    def closeEvent(self,event):
        event.accept()

if __name__ == "__main__":
    app = QtGui.QApplication([])
    test = XPathDialog("hallo Rene du bist toll")
    test.show()
    app.exec_()       