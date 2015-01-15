'''
Created on Jan 14, 2015

@author: fran_re
'''

from PySide import QtGui

class NewFileDialog(QtGui.QWidget):
    '''
    This class represents a new file dialog widget. It will be used to create an empty cpacs file
    '''

    def __init__(self):
        '''
        constructs five input text fields and two buttons to for submitting the input or cancel the event
        '''
        super(NewFileDialog, self).__init__()          
        
        self.textDataSet = QtGui.QLineEdit()
        self.textCreator = QtGui.QLineEdit()
        self.textVersion = QtGui.QLineEdit()
        self.textDescrip = QtGui.QTextEdit()
        self.textCpacsVe = QtGui.QLineEdit()
        
        self.buttonBox = QtGui.QDialogButtonBox()
        self.buttonBox.addButton("ok", QtGui.QDialogButtonBox.AcceptRole)
        self.buttonBox.addButton("cancel", QtGui.QDialogButtonBox.RejectRole)
        
        self.closeAct = QtGui.QAction("C&lose", self, shortcut="Ctrl+Q",
        statusTip="Exit the application", triggered=None)
        
        layout = QtGui.QFormLayout()
        layout.addRow("&name of the data set", self.textDataSet)
        layout.addRow("&creator of the file", self.textCreator)
        layout.addRow("&version of the file", self.textVersion)
        layout.addRow("&description to the file", self.textDescrip)
        layout.addRow("&CPACS version number", self.textCpacsVe)
        
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addLayout(layout)
        mainLayout.addWidget(self.buttonBox)
        
        self.setLayout(mainLayout)
        self.setWindowTitle(self.tr("Create new CPACS file"))  
        self.setFixedSize(400,300)
        
    def submitInput(self):
        '''
        returns the input values from the new file dialog form
        '''        
        return dict(name        = self.textDataSet.text(), creator     = self.textCreator.text(), 
                   version      = self.textVersion.text(), description = self.textDescrip.toPlainText(),
                   cpacsVersion = self.textCpacsVe.text())


    def closeEvent(self,event):
        self.closeAct.trigger()
        event.accept()
        


if __name__ == "__main__":
    app = QtGui.QApplication([])
    test = NewFileDialog()
    test.show()
    app.exec_()       