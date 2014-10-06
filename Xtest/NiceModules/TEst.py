'''
Created on Oct 1, 2014

@author: fran_re
'''

import sys
import math
from PySide import QtOpenGL, QtGui, QtCore

try:
    from OpenGL import GL, GLU, GLUT
except ImportError:
    app = QtGui.QApplication(sys.argv)
    QtGui.QMessageBox.critical(None, "OpenGL hellogl",
                              "PyOpenGL must be installed to run this example.",
                            QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default,
                            QtGui.QMessageBox.NoButton)
    sys.exit(1)


class TestWidget(QtGui.QWidget): 
    def __init__(self, parent = None):
        super(TestWidget, self).__init__(parent)

        editor = QtGui.QTextEdit()
        grid   = QtGui.QGridLayout()
        grid.addWidget(editor, 1,1)
        
        self.setLayout(grid) 

class Profile(QtOpenGL.QGLWidget):
    def __init__(self, parent = None):
        super(Profile, self).__init__(parent)
           
    def initializeGL(self):
        GL.glClearColor(1.0, 1.0 , 1.0, 1.0)

    def paintGL(self):
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
   

class ProfileDetectWidget(QtGui.QWidget): 
    def __init__(self, parent = None):
        super(ProfileDetectWidget, self).__init__(parent)
      
        self.ogl_widget = Profile() 
        # self.ogl_widget = TestWidget() 
 
        grid = QtGui.QGridLayout()
        grid.addWidget(self.ogl_widget, 2,1)
       
        self.createActions()
        self.createMenus()
        
        self.setLayout(grid) 
        self.resize(420,320)
        
    def createActions(self):
        self.openAct = QtGui.QAction('Open...', self)
        
    def createMenus(self):
        fileMenu = QtGui.QMenu("File", self)
        fileMenu.addAction(self.openAct)

        menubar = QtGui.QMenuBar(self)
        menubar.addMenu(fileMenu)

if __name__ == '__main__':
    app = QtGui.QApplication(["PyQt OpenGL"])
    widget = ProfileDetectWidget()
    widget.show()
    app.exec_()    