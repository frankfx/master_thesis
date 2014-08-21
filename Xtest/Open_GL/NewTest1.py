'''
Created on Aug 20, 2014

@author: fran_re
'''

import sys
from PySide import QtOpenGL, QtGui, QtCore
from cpacsHandler import CPACS_Handler
from config import Config

try:
    from OpenGL import GL,GLU, GLUT
except ImportError:
    app = QtGui.QApplication(sys.argv)
    QtGui.QMessageBox.critical(None, "OpenGL hellogl",
                            "PyOpenGL must be installed to run this example.",
                            QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default,
                            QtGui.QMessageBox.NoButton)
    sys.exit(1)


class Renderer():
    
    def __init__(self, tixi):
        self.tixi = tixi
    '''Initializes 3D rendering'''
    def init(self):
        '''Makes 3D drawing work when something is in front of something else'''
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_COLOR_MATERIAL)
        GL.glClearColor(1.0, 1.0 , 1.0, 1.0)
        #GL.glOrtho(-13123.0, 1213.0, 0.0, 512.0, 0.0, 1.0)        
    '''Called when the window is resized'''            
    def resize(self, w, h):
        '''Tell OpenGL how to convert from coordinates to pixel values'''
       # GL.glViewport(0,0,w,h)      # describes current viewer window - first two params are for the pos of left bottom edge
                                    # glViewport gibt Transformation von Geraetekoordinaten auf Fensterkoordinaten an
                                    # Geraetekoordinaten bilden Bereich eines Ausgabemediums (viewport) auf Koordinatenspanne -1..1 auf jeder Achse ab.
        '''Set the camera perspective'''
       # GL.glLoadIdentity()
        # wird nur gebraucht wenn eine perspektivische Projektion benutzt werden soll.
 #       GLU.gluPerspective(45,              # The camera/eye angle
 #                           w*1.0/h*1.0,     # The width-to-height ratio (ratio = Verhaeltnis)
 #                          2.0,             # The near z clipping coordinate
 #                          200.0)           # The far z clipping coordinate

        #GL.glOrtho(-13123.0, 1213.0, 0.0, 512.0, 0.0, 1.0)
      #  GLU.gluPerspective (65.0, w/h, 0.1, 10.0);
        GL.glOrtho (0, w, h, 0, 0, 1)

    '''Draws the 3D scene'''
    def display(self):
        '''Clear information from last draw'''
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT) 
        '''Switch to the drawing perspective'''
        GL.glMatrixMode(GL.GL_MODELVIEW)
        '''Reset the drawing perspective'''
        GL.glLoadIdentity()
        
        self.drawProfile()

        GL.glFlush()                # clean puffer, execute all puffered commands



    def drawProfile(self):
        
        vecX = self.tixi.getVectorX('NACA0009')
        vecY = self.tixi.getVectorY('NACA0009')
        vecZ = self.tixi.getVectorZ('NACA0009')       
        #----------------------------------------------- GL.glBegin(GL.GL_LINES)
        #-------------------------------------------------- GL.glVertex3f(0,0,0)
        #------------------------------------------------ GL.glVertex3f(0.5,0,0)
        #------------------------------------------------------------ GL.glEnd()
        GL.glColor3f(0.0, 0.0, 1.0)
       # GL.glTranslatef(-1.0 ,0.0, 0.0)
      #  GL.glScalef(2.5, 2.5, 1)
        GL.glBegin(GL.GL_LINE_STRIP)
        for i in range (0, len(vecX)) :
#            GL.glVertex3f(vecX[i], vecZ[i], vecY[i])
            GL.glVertex3f(vecX[i], 0.0075, 0)
        GL.glEnd()

        GL.glColor3f(0.0, 0.0, 0.0)
        GL.glBegin(GL.GL_LINE_STRIP)
        for i in range (0, len(vecX)) :
#            GL.glVertex3f(vecX[i], vecZ[i], vecY[i])
            GL.glVertex3f(0.5, vecY[i], 0)
        GL.glEnd()

  #  def normVector(self, list-vec):
        

class MyWidget(QtOpenGL.QGLWidget):
    def __init__(self, parent = None):
        super(MyWidget, self).__init__(parent)
        self.resize(400,400)
        self.setWindowTitle("Rene Test")
        self.tixi = CPACS_Handler()
        self.tixi.loadFile(Config.path_cpacs_A320_Fuse, Config.path_cpacs_21_schema)
        self.renderer = Renderer(self.tixi)
        self.setFixedSize(QtCore.QSize(400,400))
    
    def initializeGL(self):
        self.renderer.init()
    
    def resizeGL(self, w, h):
        self.renderer.resize(w, h)
 
    def paintGL(self):
        self.renderer.display()
        
    
if __name__ == '__main__':
    app = QtGui.QApplication(["PyQt OpenGL"])
    widget = MyWidget()
    widget.show()
    app.exec_()    