'''
Created on Jan 15, 2015

@author: fran_re
'''
from PySide import QtGui

class PopUpFileSettings(QtGui.QWidget):
    
    def __init__(self, name):
        '''
        Constructor
        '''
        super(PopUpFileSettings, self).__init__()       
        
        self.closeAct = QtGui.QAction("C&lose", self, shortcut="Ctrl+Q",
        statusTip="Exit the application", triggered=None)        

        self.setWindowTitle(self.tr(name))  
        #self.setFixedSize(width, height)

        self.path_inputMapping = ""
        self.path_outputMapping = ""
        self.path_cpacs4Lili = ""
        self.path_xslt_proc  = ""
        
        self.text_inputMap  = QtGui.QLineEdit()
        self.text_outputMap = QtGui.QLineEdit()
        self.text_toolpath  = QtGui.QLineEdit()
        self.text_xslt_proc = QtGui.QLineEdit()

        self.buttonBox = QtGui.QDialogButtonBox()
        self.buttonBox.addButton(QtGui.QDialogButtonBox.Ok)
        self.buttonBox.addButton(QtGui.QDialogButtonBox.Cancel) 

        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).clicked.connect(self.fire_submitInput)
        self.buttonBox.button(QtGui.QDialogButtonBox.Cancel).clicked.connect(self.close)

        layout = QtGui.QFormLayout()
        layout.addRow("inputMapping", self.text_inputMap)
        layout.addRow("outputMapping", self.text_outputMap)
        layout.addRow("cpacs4Lili", self.text_toolpath)
        layout.addRow("xslt processor", self.text_xslt_proc)
        layout.addRow(self.buttonBox)
        
        self.setFixedSize(600, 150)
        self.setLayout(layout)
        # self.layout().setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.show()
        
    def fire_submitInput(self):
        self.path_inputMapping = self.text_inputMap.text()
        self.path_outputMapping = self.text_outputMap.text()
        self.path_cpacs4Lili = self.text_toolpath.text()
        self.path_xslt_proc  = self.text_xslt_proc.text()
    
    def getPathValues(self):
        return self.path_inputMapping, self.path_outputMapping, self.path_cpacs4Lili, self.path_xslt_proc
    
    def closeEvent(self,event):
        self.closeAct.trigger()