'''
Created on Jul 25, 2014

@author: fran_re
'''
from PySide.QtGui import * 
from PySide.QtCore import *

class Window(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.button1    = QPushButton("update"  , self)
        self.button2    = QPushButton("clear"   , self)
        self.button3    = QPushButton("reload"  , self)
        self.editor     = QTextEdit  ('Editor'  , self)
        
        self.button1.clicked.connect(self.handleButton1)
        self.button2.clicked.connect(self.handleButton2)
        self.button3.clicked.connect(self.handleButton3)
        
        layout = QGridLayout(self)
        layout.addWidget(self.button1, 0, 0)
        layout.addWidget(self.button2, 0, 1)
        layout.addWidget(self.button3, 0, 2)
        layout.addWidget(self.editor,  1, 0, 1, 3)

    def handleButton1(self):
        print ('Hello World')

    def handleButton2(self):
        print ('Hello Rene')
        
    def handleButton3(self):
        print ('Hello Test')        

if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())