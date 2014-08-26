'''
Created on Aug 25, 2014

@author: rene
'''
from PySide import QtGui, QtCore
import sys

class Example(QtGui.QWidget):
    
    def __init__(self, parent=None):
        super(Example, self).__init__(parent)
        
        self.initUI()
        
    def initUI(self):      
        self.mm = MyWidget()
        self.nn = MyWidget2()
        layout = QtGui.QGridLayout()
        layout.addWidget(self.mm, 0, 1)
        layout.addWidget(self.nn, 0, 2)
        layout.addWidget(QtGui.QLabel('gjgjgj'), 0, 3)
        #self.setFocus()
        self.nn.activateWindow()
        self.setFixedSize(300,300)
        self.setLayout(layout)
        self.show()
        
    def changeTitle(self, state):
      
        if state == QtCore.Qt.Checked:
            self.setWindowTitle('QtGui.QCheckBox')
        else:
            self.setWindowTitle('')


class MyWidget(QtGui.QWidget):
    
    def __init__(self):
        super(MyWidget, self).__init__()
        self.initUI()
        
    def initUI(self):      

        bt = QtGui.QPushButton("test")
        layout = QtGui.QGridLayout()
        layout.addWidget(bt)
        self.setFixedSize(100,100)
        self.setLayout(layout)        
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('QtGui.QCheckBox')
        self.show()
        
    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_1:
            print "widget 1"
        
    def changeTitle(self, state):
      
        if state == QtCore.Qt.Checked:
            self.setWindowTitle('QtGui.QCheckBox')
        else:
            self.setWindowTitle('')


class MyWidget2(QtGui.QWidget):
    
    def __init__(self):
        super(MyWidget2, self).__init__()
        self.initUI()
        self.setFocus()
        
    def initUI(self):      

        bt = QtGui.QPushButton("test2")
        layout = QtGui.QGridLayout()
        layout.addWidget(bt)
        self.setFixedSize(100,100)
        self.setLayout(layout)        
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('QtGui.QCheckBox2')
        self.show()
        
    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_1:
            print "widget 2"
        
    def changeTitle(self, state):
      
        if state == QtCore.Qt.Checked:
            self.setWindowTitle('QtGui.QCheckBox2')
        else:
            self.setWindowTitle('')

        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()