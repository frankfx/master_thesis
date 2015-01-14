'''
Created on Jan 14, 2015

@author: fran_re
'''

from PySide import QtGui
from Xtest.XML_Editor import difficultTestTool
import numpy as np

class ToolX(QtGui.QWidget):
    '''
    This class represents a new file dialog widget. It will be used to create an empty cpacs file
    '''

    def __init__(self):
        '''
        constructs five input text fields and two buttons to for submitting the input or cancel the event
        '''
        super(ToolX, self).__init__()          
        
        self.text1 = QtGui.QLineEdit()
        self.text2 = QtGui.QLineEdit()
       
        
        self.buttonBox = QtGui.QDialogButtonBox()
        self.buttonBox.addButton("ok", QtGui.QDialogButtonBox.AcceptRole)
        self.buttonBox.addButton("cancel", QtGui.QDialogButtonBox.RejectRole)
        
        self.buttonBox.accepted.connect(self.submitInput)
        
        self.closeAct = QtGui.QAction("C&lose", self, shortcut="Ctrl+Q",
        statusTip="Exit the application", triggered=None)
        
        layout = QtGui.QFormLayout()
        layout.addRow("&x", self.text1)
        layout.addRow("&y", self.text2)
        
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addLayout(layout)
        mainLayout.addWidget(self.buttonBox)
        
        self.setLayout(mainLayout)
        self.setWindowTitle(self.tr("Tool X"))  
        self.setFixedSize(400,300)
        
    def submitInput(self):
        '''
        returns the input values from the new file dialog form
        '''        
        # call difficult tool with command line
        t = difficultTestTool.doSomething(int(self.text1.text()), int(self.text2.text()))

        t = np.arange(0.0, 2.0, 0.01)
        
        print t
        from pylab import *

       
        s = sin(2*pi*t)
        plot(t, s)

        xlabel('time (s)')
        ylabel('voltage (mV)')
        title('About as simple as it gets, folks')
        grid(True)
        savefig("test.png")
        show()


    def closeEvent(self,event):
        self.closeAct.trigger()
        event.accept()
        

if __name__ == "__main__":
    app = QtGui.QApplication([])
    test = ToolX()
    test.show()
    app.exec_()       