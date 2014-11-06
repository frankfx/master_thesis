'''
Created on Nov 6, 2014

@author: fran_re
'''

import sys

from tiglwrapper import Tigl, TiglException
from tixiwrapper import Tixi
from PySide import QtOpenGL, QtGui, QtCore
from Xtest.Open_GL import utility

try:
    from OpenGL import GL, GLU, GLUT
except ImportError:
    app = QtGui.QApplication(sys.argv)
    QtGui.QMessageBox.critical(None, "OpenGL hellogl",
                              "PyOpenGL must be installed to run this example.",
                            QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default,
                            QtGui.QMessageBox.NoButton)
    sys.exit(1)

class Renderer() :
    def init(self) : 
        mat_specular   = [1.0, 1.0, 1.0, 1.0]
        mat_shininess  = [50.0]
        light_position = [0.75, 0.0, 1.0, 0.0]
   
        GL.glClearColor (1.0, 1.0, 1.0, 0.0)
        GL.glShadeModel (GL.GL_SMOOTH)

        GL.glMaterialfv(GL.GL_FRONT, GL.GL_SPECULAR, mat_specular)
        GL.glMaterialfv(GL.GL_FRONT, GL.GL_SHININESS, mat_shininess)
        GL.glLightfv(GL.GL_LIGHT0, GL.GL_POSITION, light_position)

        #GL.glEnable(GL.GL_COLOR_MATERIAL)
        GL.glEnable(GL.GL_LIGHTING)
        GL.glEnable(GL.GL_LIGHT0)
        GL.glEnable(GL.GL_DEPTH_TEST)

    def display(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        GLUT.glutInit()
        GLUT.glutSolidSphere (1.0, 20, 16)
        GL.glFlush()

    def resize(self, w, h):
        GL.glViewport (0, 0, w, h)
        GL.glMatrixMode (GL.GL_PROJECTION)
        GL.glLoadIdentity()
        if w <= h :
            GL.glOrtho (-1.5, 1.5, -1.5*h/w,1.5*h/w, -10.0, 10.0)
        else :
            GL.glOrtho (-1.5*w/h,1.5*w/h, -1.5, 1.5, -10.0, 10.0)
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()

class Widget(QtOpenGL.QGLWidget):
    def __init__(self, parent = None):
        super(Widget, self).__init__(parent)
        self.resize(800 , 800)
        self.renderer = Renderer()

    def initializeGL(self):
        self.renderer.init()
        
    def resizeGL(self, w, h):
        self.renderer.resize(w, h)
 
    def paintGL(self):
        self.renderer.display()      

if __name__ == '__main__':
    app = QtGui.QApplication(["PyQt OpenGL"])
    widget = Widget()
    widget.show()
    app.exec_()      
    
    

