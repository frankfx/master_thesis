#! /usr/bin/env python

import sys

import numpy as np
import PySide
from PySide import QtOpenGL, QtGui, QtCore
try:
    from OpenGL.GL import *
    from OpenGL.arrays import vbo
   # from OpenGLContext.arrays import *
    from OpenGL.GL import shaders
    from OpenGL import GLU, GLUT, GLE
except ImportError:
    app = QtGui.QApplication(sys.argv)
    QtGui.QMessageBox.critical(None, "OpenGL hellogl",
                              "PyOpenGL must be installed to run this example.",
                            QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default,
                            QtGui.QMessageBox.NoButton)
    sys.exit(1)


class Renderer():
    """Creates a simple vertex shader..."""    
    def __init__(self):
        print glGetString(GL_VERSION)
        t =  glGetString(GL_SHADING_LANGUAGE_VERSION)
        print t
        
        VERTEX_SHADER = shaders.compileShader("""#version 330 
        void main() { 
            gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex; 
        }""", GL_VERTEX_SHADER)
        FRAGMENT_SHADER = shaders.compileShader("""#version 330 
        void main() { 
            gl_FragColor = vec4( 0, 1, 0, 1 ); 
        }""", GL_FRAGMENT_SHADER)         
        
        self.shader = shaders.compileProgram(VERTEX_SHADER,FRAGMENT_SHADER)
        
        self.vbo = vbo.VBO( np.array( [ [ 0, 1, 0 ], [ -1,-1, 0 ], [ 1,-1, 0 ], [ 2,-1, 0 ], [ 4,-1, 0 ], [ 4, 1, 0 ], [ 2,-1, 0 ], [ 4, 1, 0 ], [ 2, 1, 0 ], ],'f') )
        
    def Render( self, mode): 
        """Render the geometry for the scene."""
        shaders.glUseProgram(self.shader)
        
        try: 
            self.vbo.bind() 
            try:
                glEnableClientState(GL_VERTEX_ARRAY); glVertexPointerf( self.vbo )
                glDrawArrays(GL_TRIANGLES, 0, 9)   
            finally: 
                self.vbo.unbind() 
                glDisableClientState(GL_VERTEX_ARRAY); 
        finally: shaders.glUseProgram( 0 ) 
   
class Widget(QtOpenGL.QGLWidget):
    def __init__(self, parent = None):
        super(Widget, self).__init__(parent)
        self.width = 320
        self.height = 302
        self.resize(self.width ,self.height)
        self.setWindowTitle("Rene Test")
        self.renderer = Renderer()   

    def initializeGL(self): 
        print glGetString(GL_VERSION)  

    
if __name__ == '__main__':
    app = QtGui.QApplication(["PyQt OpenGL"])
    widget = Widget()
    widget.show()

    app.exec_()          