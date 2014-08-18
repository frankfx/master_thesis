'''
Created on Aug 4, 2014

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

class Triangle(Shape):

    def __init__(self):
        super(Triangle, self).__init__()

    def draw(self):
        GL.glTranslate(self.transX, self.transY, self.transZ) 
#---------------------------------------------- glRotate() // rotate the pyramid
#------------------------------------------------ glscale() // scale the pyramid        
        GL.glBegin(GL.GL_TRIANGLES)
        GL.glVertex3f(-2.5, 0, -0.5)
        GL.glVertex3f(2.5, 0, -0.5)
        GL.glVertex3f(0, 4, -0.5)
        GL.glEnd()