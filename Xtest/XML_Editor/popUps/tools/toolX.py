'''
Created on Jan 14, 2015

@author: fran_re
'''

from PySide import QtGui
from popUp_tool import PopUpTool
from Xtest.XML_Editor.externTools import difficultTestTool
from Xtest.Open_GL import utility
from pylab import *

class ToolX(PopUpTool):
    '''
    This class represents a new file dialog widget. It will be used to create an empty cpacs file
    '''
    def __init__(self, name, width=200, height=300):
        '''
        constructs five input text fields and two buttons to for submitting the input or cancel the event
        '''
        super(ToolX, self).__init__(name, width, height)          
        
        self.setupWidget()
        
        layout = QtGui.QFormLayout()
        layout.addRow("&x", self.text1)
        layout.addRow("&y", self.text2)
        
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addLayout(layout)
        mainLayout.addWidget(self.buttonBox)
        
        self.setLayout(mainLayout)

    @utility.overrides(PopUpTool)    
    def setupWidget(self):
        self.text1 = QtGui.QLineEdit()
        self.text2 = QtGui.QLineEdit()
        
        self.buttonBox = QtGui.QDialogButtonBox()
        self.buttonBox.addButton("ok", QtGui.QDialogButtonBox.AcceptRole)
        self.buttonBox.addButton("cancel", QtGui.QDialogButtonBox.RejectRole)
        
        self.buttonBox.accepted.connect(self.submitInput)        

    @utility.overrides(PopUpTool)    
    def setConnection(self):
        # call difficult tool with command line
        self.tool = difficultTestTool.init()

    @utility.overrides(PopUpTool)    
    def submitInput(self):
        '''
        returns the input values from the new file dialog form
        '''        
        try :
            a = int(self.text1.text())
            b = int(self.text2.text())
            self.tool = difficultTestTool.doSomething(a, b)
        except :
            print "error"
            self.tool = np.arange(2.0, 0.1)
        s = sin(2*pi*self.tool)
        plot(self.tool, s)

        xlabel('time (s)')
        ylabel('voltage (mV)')
        title('About as simple as it gets, folks')
        grid(True)
        savefig("test.png")
        show()


if __name__ == "__main__":
    app = QtGui.QApplication([])
    test = ToolX("name")
    test.show()
    app.exec_()       