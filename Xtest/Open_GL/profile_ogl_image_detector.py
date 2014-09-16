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


class MyProfileWidget(QtOpenGL.QGLWidget):
    def __init__(self,parent = None):
        super(MyProfileWidget, self).__init__(parent)
        self.filename = ""
        self.img_width = -1
        self.img_height = -1
        self.resize(320,320)
        self.setWindowTitle("Rene Test")

    def drawImage(self, filename):
        self.filename = filename
        self.initializeGL()
        self.updateGL()

    def initializeGL(self):
       # GL.glEnable(GL.GL_DEPTH_TEST)
        #GL.glEnable(GL.GL_CULL_FACE)
        GL.glEnable(GL.GL_TEXTURE_2D)
        self.textures = []
        pixmap = QtGui.QPixmap(self.filename)
        self.textures.append(self.bindTexture(pixmap))
        self.img_width, self.img_height = pixmap.width() , pixmap.height()  
    
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
                   
        self.drawRectangle()

        GL.glFlush()    

    def isImageAvailable(self):
        return not self.img_height == 0.0 and not self.img_width == 0.0

    def drawRectangle(self, xsize=1.0):
        if (self.isImageAvailable()) :
            px = xsize
            py = 1.0*self.img_height/self.img_width * px
            GL.glColor3f(1.0, 1.0, 1.0)
            GL.glBegin(GL.GL_QUADS)
            GL.glTexCoord2f(0,0)
            GL.glVertex3f(-px, -py, -0.5)
            GL.glTexCoord2f(1, 0)
            GL.glVertex3f( px, -py, -0.5)
            GL.glTexCoord2f(1, 1)
            GL.glVertex3f( px,  py, -0.5)
            GL.glTexCoord2f(0,  1)
            GL.glVertex3f(-px,  py, -0.5)
            GL.glEnd()         
              
    
if __name__ == '__main__':
    app = QtGui.QApplication(["PyQt OpenGL"])
    widget = MyProfileWidget()
    widget.show()
    app.exec_()    