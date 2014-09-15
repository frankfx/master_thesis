'''
Created on Aug 22, 2014

@author: rene
'''

'''
Created on Jul 30, 2014

@author: fran_re
'''
import sys
from PySide import QtOpenGL, QtGui, QtCore
#from cpacsHandler import CPACS_Handler
from config import Config
try:
    from OpenGL import GL, GLU
except ImportError:
    app = QtGui.QApplication(sys.argv)
    QtGui.QMessageBox.critical(None, "OpenGL hellogl",
                              "PyOpenGL must be installed to run this example.",
                            QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default,
                            QtGui.QMessageBox.NoButton)
    sys.exit(1)


class Renderer(QtOpenGL.QGLWidget):
    def __init__(self, parent = None):
        super(Renderer, self).__init__(parent)
        self.resize(320,320)
        self.setWindowTitle("Rene Test")
        #self.setFixedSize(QtCore.QSize(400,400))

    def initializeGL(self):
        print "sdfsdf"
       # GL.glEnable(GL.GL_DEPTH_TEST)
       # GL.glEnable(GL.GL_CULL_FACE)
        GL.glEnable(GL.GL_TEXTURE_2D)
        
        self.textures = []
        self.textures.append(self.bindTexture(QtGui.QPixmap("duck.bmp")))
        print len(self.textures)
    
    def resizeGL(self, w, h):
        GL.glViewport(0,0,w,h) 
                                   
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        
        GLU.gluPerspective (144.0, w*1.0/h, 0.0, 10.0)
        
    def paintGL(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT) 
        
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()
       
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.textures[0])
                   
        self.drawTriangle()

        GL.glFlush()    

    def drawTriangle(self):
        p = 1.9
        GL.glColor3f(1.0, 1.0, 1.0)
        GL.glBegin(GL.GL_QUADS)
        GL.glTexCoord2f(0,0)
        GL.glVertex3f(-p, -p, -0.5)
        GL.glTexCoord2f(1, 0)
        GL.glVertex3f( p, -p, -0.5)
        GL.glTexCoord2f(1, 1)
        GL.glVertex3f( p,  p, -0.5)
        GL.glTexCoord2f(0,  1)
        GL.glVertex3f(-p,  p, -0.5)
        GL.glEnd()            
              

class MyProfileWidget():
    def __init__(self, parent = None):
        super(MyProfileWidget, self).__init__(parent)
        self.resize(320,320)
        self.setWindowTitle("Rene Test")
        #self.setFixedSize(QtCore.QSize(400,400))
        self.renderer = Renderer()    
    
    def initializeGL(self):
        self.renderer.init()



    
    def resizeGL(self, w, h):
        self.renderer.resize(w, h)
 
    def paintGL(self):
        self.renderer.display()

    
if __name__ == '__main__':
    app = QtGui.QApplication(["PyQt OpenGL"])
    widget = Renderer()
    widget.show()
    app.exec_()    