'''
Created on Jul 31, 2014

@author: fran_re
'''

import sys
from shape import Shape
from PySide import QtGui
try:
    from OpenGL import GL
except ImportError:
    app = QtGui.QApplication(sys.argv)
    QtGui.QMessageBox.critical(None, "OpenGL hellogl",
                            "PyOpenGL must be installed to run this example.",
                            QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default,
                            QtGui.QMessageBox.NoButton)
    sys.exit(1)

class Pyramid(Shape):

    def __init__(self):
        super(Pyramid, self).__init__()

    def draw(self):
        GL.glTranslate(self.transX, self.transY, self.transZ) 
       
#---------------------------------------------- glRotate() // rotate the pyramid
#------------------------------------------------ glscale() // scale the pyramid
        GL.glBegin(GL.GL_TRIANGLES)
        GL.glColor3f(1.0, 0.0, 0.0) 
        GL.glVertex3f(0.0, 1.0, 0.0)
        GL.glColor3f(0.0, 1.0, 0.0) 
        GL.glVertex3f(-1.0, -1.0, 1.0)
        GL.glColor3f(0.0, 0.0, 1.0) 
        GL.glVertex3f(1.0, -1.0, 1.0)
        GL.glColor3f(1.0, 0.0, 0.0) 
        GL.glVertex3f(0.0, 1.0, 0.0)
        GL.glColor3f(0.0, 1.0, 0.0) 
        GL.glVertex3f(-1.0, -1.0, 1.0)
        GL.glColor3f(0.0, 0.0, 1.0) 
        GL.glVertex3f(0.0, -1.0, -1.0)
        GL.glColor3f(1.0, 0.0, 0.0) 
        GL.glVertex3f(0.0, 1.0, 0.0)
        GL.glColor3f(0.0, 1.0, 0.0) 
        GL.glVertex3f(0.0, -1.0, -1.0)
        GL.glColor3f(0.0, 0.0, 1.0) 
        GL.glVertex3f(1.0, -1.0, 1.0)
        GL.glColor3f(1.0, 0.0, 0.0) 
        GL.glVertex3f(-1.0, -1.0, 1.0)
        GL.glColor3f(0.0, 1.0, 0.0) 
        GL.glVertex3f(0.0, -1.0, -1.0)
        GL.glColor3f(0.0, 0.0, 1.0) 
        GL.glVertex3f(1.0, -1.0, 1.0)
        GL.glEnd()
