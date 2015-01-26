'''
Created on Jan 15, 2015

@author: fran_re
'''

from PySide import QtGui


class PopUpTool(QtGui.QWidget):
    '''
    this is an abstract class to represent popUp widget to use extern tools
    '''
    def __init__(self, name, width, height):
        '''
        Constructor
        '''
        super(PopUpTool, self).__init__()       
        
        self.closeAct = QtGui.QAction("C&lose", self, shortcut="Ctrl+Q",
        statusTip="Exit the application", triggered=None)        

        self.setWindowTitle(self.tr(name))  
        #self.setFixedSize(width, height)
        
       
    def setupWidget(self):
        '''abstract method'''
        return NotImplemented

    def setConnection(self):
        '''abstract method'''
        return NotImplemented  
    
    def fire_submitInput(self):
        '''abstract method'''
        print "Rene ist gut"
        return NotImplemented

    def fire_submitInputAndStartTool(self):
        '''abstract method'''
        return NotImplemented
    
    def closeEvent(self,event):
        self.closeAct.trigger()
        
        
