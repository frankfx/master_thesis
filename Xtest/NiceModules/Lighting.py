'''
Created on Dec 16, 2014

@author: rene
'''

import sys
from PySide import QtOpenGL, QtGui, QtCore
import math

try:
    from OpenGL import GL, GLU, GLUT
except ImportError:
    app = QtGui.QApplication(sys.argv)
    QtGui.QMessageBox.critical(None, "OpenGL hellogl",
                              "PyOpenGL must be installed to run this example.",
                            QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default,
                            QtGui.QMessageBox.NoButton)
    sys.exit(1)

class Renderer():
    def __init__(self, width, height):
        self._angle = -70
        self.xRot = 0.0
        self.yRot = 0.0
        self.zRot = 0.0
        
    def init(self):
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_COLOR_MATERIAL)
        GL.glEnable(GL.GL_LIGHTING)
        GL.glEnable(GL.GL_LIGHT0)
        GL.glEnable(GL.GL_LIGHT1)
        GL.glEnable(GL.GL_NORMALIZE)
        # GL.glShadeModel(GL.GL_SMOOTH)
    
    def resize(self, w, h):
        GL.glViewport(0, 0, w, h)
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GLU.gluPerspective(45.0, 1.0*w / h, 1.0, 200.0)        

    def display(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT) 
        
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()                

        GL.glTranslatef(0.0, 0.0, -8.0)
 
        ambientColor = [0.2, 0.2, 0.2, 1.0]
        GL.glLightModelfv(GL.GL_LIGHT_MODEL_AMBIENT, ambientColor)
        
        lightColor0 = [0.5, 0.5, 0.5, 1.0]
        lightPos0   = [4.0, 0.0, 8.0, 1.0]
        GL.glLightfv(GL.GL_LIGHT0, GL.GL_DIFFUSE, lightColor0)
        GL.glLightfv(GL.GL_LIGHT0, GL.GL_POSITION, lightPos0)
 
        lightColor1 = [0.5, 0.2, 0.2, 1.0]
        lightPos1   = [-1.0, 0.5, 0.5, 0.0]
        GL.glLightfv(GL.GL_LIGHT1, GL.GL_DIFFUSE, lightColor1)
        GL.glLightfv(GL.GL_LIGHT1, GL.GL_POSITION, lightPos1)

        GL.glRotatef(self._angle, 0.0, 1.0, 0.0)
        GL.glColor3f(1.0, 1.0, 1.0)
        
        GL.glBegin(GL.GL_QUADS)
        ## Front
        GL.glNormal3f(0.0, 0.0, 1.0)
        # GL.glNormal3f(-1.0, 0.0, 1.0)
        GL.glVertex3f(-1.5, -1.0, 1.5)
        # GL.glNormal3f(1.0, 0.0, 1.0)
        GL.glVertex3f(1.5, -1.0, 1.5)
        # GL.glNormal3f(1.0, 0.0, 1.0)
        GL.glVertex3f(1.5, 1.0, 1.5)
        # GL.glNormal3f(-1.0, 0.0, 1.0)
        GL.glVertex3f(-1.5, 1.0, 1.5)
 
        ## Right
        GL.glNormal3f(1.0, 0.0, 0.0)
        # GL.glNormal3f(1.0, 0.0, -1.0)
        GL.glVertex3f(1.5, -1.0, -1.5)
        # GL.glNormal3f(1.0, 0.0, -1.0)
        GL.glVertex3f(1.5, 1.0, -1.5)
        # GL.glNormal3f(1.0, 0.0, 1.0)
        GL.glVertex3f(1.5, 1.0, 1.5)
        # GL.glNormal3f(1.0, 0.0, 1.0)
        GL.glVertex3f(1.5, -1.0, 1.5)
 
        ## Back
        GL.glNormal3f(0.0, 0.0, -1.0)
        # GL.glNormal3f(-1.0, 0.0, -1.0)
        GL.glVertex3f(-1.5, -1.0, -1.5)
        # GL.glNormal3f(-1.0, 0.0, -1.0)
        GL.glVertex3f(-1.5, 1.0, -1.5)
        # GL.glNormal3f(1.0, 0.0, -1.0)
        GL.glVertex3f(1.5, 1.0, -1.5)
        # GL.glNormal3f(1.0, 0.0, -1.0)
        GL.glVertex3f(1.5, -1.0, -1.5)

        ## Left
        GL.glNormal3f(-1.0, 0.0, 0.0)
        # GL.glNormal3f(-1.0, 0.0, -1.0)
        GL.glVertex3f(-1.5, -1.0, -1.5)
        # GL.glNormal3f(-1.0, 0.0, 1.0)
        GL.glVertex3f(-1.5, -1.0, 1.5)
        # GL.glNormal3f(-1.0, 0.0, 1.0)
        GL.glVertex3f(-1.5, 1.0, 1.5)
        # GL.glNormal3f(-1.0, 0.0, -1.0)
        GL.glVertex3f(-1.5, 1.0, -1.5)

        GL.glEnd()


class Widget(QtOpenGL.QGLWidget):
    def __init__(self, parent = None):
        super(Widget, self).__init__(parent)
        self.width = 800
        self.height = 800
        self.resize(self.width ,self.height)
      
        grid = QtGui.QGridLayout()
        self.setLayout(grid)
        
        self.setSizePolicy ( QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.renderer = Renderer(self.width ,self.height)
        

    def keyPressEvent(self, event):
        redraw = False
        offset_rot   = 1.5
        offset_scale = 0.2
        # Right arrow - increase rotation by 5 degree
        if event.key() == QtCore.Qt.Key_Right :
            self.renderer._angle += offset_rot
            redraw = True
        # Left arrow - decrease rotation by 5 degree
        elif event.key() == QtCore.Qt.Key_Left :
            self.renderer._angle -= offset_rot
            redraw = True
        elif event.key() == QtCore.Qt.Key_Up :
            self.renderer.xRot += offset_rot
            redraw = True
        elif event.key() == QtCore.Qt.Key_Down :
            self.renderer.xRot -= offset_rot
            redraw = True
        elif event.key() == QtCore.Qt.Key_Plus :
            self.renderer.scale += offset_scale
            redraw = True
        elif event.key() == QtCore.Qt.Key_Minus :
            self.renderer.scale -= offset_scale
            redraw = True

        if self.renderer._angle > 360 :
            self.renderer._angle -= 360

        # Request display update
        if redraw :
            self.updateGL()
    
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