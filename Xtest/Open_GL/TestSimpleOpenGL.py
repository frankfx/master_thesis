'''
Created on Aug 22, 2014

@author: rene
'''
from Xtest.Open_GL import profile_ogl_image_detector

'''
Created on Jul 30, 2014

@author: fran_re
'''
import sys
from PySide import QtOpenGL, QtGui, QtCore
from cpacsHandler import CPACS_Handler
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


class Renderer():
    def __init__(self, width, height):
        self.x = 0
        self.y = 0
        self.z = 1
        self.rotX = 0
        self.rotY = 0
        self.width = width
        self.height = height
        
        
    def init(self):
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_COLOR_MATERIAL)
        GL.glClearColor(0.0, 0.0 , 0.0, 1.0)
    
    def resize(self, w, h):
        self.width = w
        self.height = h
        GL.glViewport(0,0,w,h) 
                                   
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
       
        '''gluunproject vs gluperspective'''
      #  GLU.gluPerspective (200.0, w*1.0/h, 0.0, 10.0)
        
    def display(self):
        # Clear screen and Z-buffer
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT) 
        
        # Reset transformations
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()
       
        # Other Transformations
        #GL.glTranslatef( 0.1, 0.0, 0.0 )      # Not included
        #GL.glRotatef( 180, 0.0, 1.0, 0.0 )    # Not included       
       
        # Rotate when user changes rotate_x and rotate_y
        GL.glRotatef( self.rotX, 1.0, 0.0, 0.0 )
        GL.glRotatef( self.rotY, 0.0, 1.0, 0.0 )       
       
        # Other Transformations
        #GL.glScalef( 2.0, 2.0, 0.0 )          # Not included
 
                    #GL.glTranslatef(-0.51,0,-1)
                    #self.drawTriangle()
        #Multi-colored side - FRONT
        self.drawCube()
        GL.glFlush()    

    def set_coordinates(self, x, y, z):

        modelview  = GL.glGetDoublev(GL.GL_MODELVIEW_MATRIX)    # get the modelview info
        projection = GL.glGetDoublev(GL.GL_PROJECTION_MATRIX)   # get the projection matrix info
        viewport   = GL.glGetIntegerv(GL.GL_VIEWPORT)           # get the viewport info
 
        winX = x
        winY = viewport[3] - y
        winZ = 1
 
        # get the world coordinates from the screen coordinates
        ''' winz should not be 0!!!!!!!!!!'''
        ''' error when projection matrix not identity (gluPerspective) '''
        self.x, self.y, self.z = GLU.gluUnProject(winX, winY, winZ, modelview, projection, viewport)

    def drawTriangle(self):
        GL.glColor3f(1.0, 1.0, 1.0)
        GL.glBegin(GL.GL_TRIANGLES)
        GL.glVertex3f(-0.5 + self.x, -0.5 + self.y, -0.5)
        GL.glVertex3f( 0.5 + self.x, -0.5 + self.y, -0.5)
        GL.glVertex3f( 0.0 + self.x,  0.5 + self.y, -0.5)
        GL.glEnd()            
              
    def drawCube(self):
        # Multi-colored side - FRONT
        GL.glBegin(GL.GL_POLYGON)
 
        GL.glColor3f( 1.0, 0.0, 0.0 )  ,   GL.glVertex3f(  0.5, -0.5, -0.5 )      # P1 is red
        GL.glColor3f( 0.0, 1.0, 0.0 )  ,   GL.glVertex3f(  0.5,  0.5, -0.5 )       # P2 is green
        GL.glColor3f( 0.0, 0.0, 1.0 )  ,   GL.glVertex3f( -0.5,  0.5, -0.5 )       # P3 is blue
        GL.glColor3f( 1.0, 0.0, 1.0 )  ,   GL.glVertex3f( -0.5, -0.5, -0.5 )       # P4 is purple
 
        GL.glEnd()
 
        # White side - BACK
        GL.glBegin(GL.GL_POLYGON)
        GL.glColor3f(   1.0,  1.0, 1.0 )
        GL.glVertex3f(  0.5, -0.5, 0.5 )
        GL.glVertex3f(  0.5,  0.5, 0.5 )
        GL.glVertex3f( -0.5,  0.5, 0.5 )
        GL.glVertex3f( -0.5, -0.5, 0.5 )
        GL.glEnd()
 
        # Purple side - RIGHT
        GL.glBegin(GL.GL_POLYGON)
        GL.glColor3f(  1.0,  0.0,  1.0 )
        GL.glVertex3f( 0.5, -0.5, -0.5 )
        GL.glVertex3f( 0.5,  0.5, -0.5 )
        GL.glVertex3f( 0.5,  0.5,  0.5 )
        GL.glVertex3f( 0.5, -0.5,  0.5 )
        GL.glEnd()
 
        # Green side - LEFT
        GL.glBegin(GL.GL_POLYGON)
        GL.glColor3f(   0.0,  1.0,  0.0 )
        GL.glVertex3f( -0.5, -0.5,  0.5 )
        GL.glVertex3f( -0.5,  0.5,  0.5 )
        GL.glVertex3f( -0.5,  0.5, -0.5 )
        GL.glVertex3f( -0.5, -0.5, -0.5 )
        GL.glEnd()
 
        # Blue side - TOP
        GL.glBegin(GL.GL_POLYGON)
        GL.glColor3f(   0.0,  0.0,  1.0 )
        GL.glVertex3f(  0.5,  0.5,  0.5 )
        GL.glVertex3f(  0.5,  0.5, -0.5 )
        GL.glVertex3f( -0.5,  0.5, -0.5 )
        GL.glVertex3f( -0.5,  0.5,  0.5 )
        GL.glEnd()
 
        # Red side - BOTTOM
        GL.glBegin(GL.GL_POLYGON)
        GL.glColor3f(   1.0,  0.0,  0.0 )
        GL.glVertex3f(  0.5, -0.5, -0.5 )
        GL.glVertex3f(  0.5, -0.5,  0.5 )
        GL.glVertex3f( -0.5, -0.5,  0.5 )
        GL.glVertex3f( -0.5, -0.5, -0.5 )
        GL.glEnd()
               

class MyProfileWidget(QtOpenGL.QGLWidget):
    def __init__(self, parent = None):
        super(MyProfileWidget, self).__init__(parent)
        self.width = 320
        self.height = 302
        self.resize(self.width ,self.height)
        self.setWindowTitle("Rene Test")
        #self.setFixedSize(QtCore.QSize(400,400))
        self.setSizePolicy ( QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.renderer = Renderer(self.width ,self.height)    
        
        
    
    def initializeGL(self):
        self.renderer.init()
    
    def resizeGL(self, w, h):
        self.renderer.resize(w, h)
 
    def paintGL(self):
        self.renderer.display()

    def mousePressEvent(self, event):
        self.lastPos = QtCore.QPoint(event.pos())

    def mouseMoveEvent(self, event):
        
        if event.buttons() & QtCore.Qt.LeftButton:
            self.renderer.set_coordinates(event.x(), event.y(), 1)
        elif event.buttons() & QtCore.Qt.RightButton :
            ()

        self.lastPos = QtCore.QPoint(event.pos())
        self.updateGL()

    def keyPressEvent(self, event):
        redraw = False
        # Right arrow - increase rotation by 5 degree
        if event.key() == QtCore.Qt.Key_Right :
            self.renderer.rotY += 5
            redraw = True
        # Left arrow - decrease rotation by 5 degree
        elif event.key() == QtCore.Qt.Key_Left :
            self.renderer.rotY -= 5
            redraw = True
        elif event.key() == QtCore.Qt.Key_Up :
            self.renderer.rotX += 5
            redraw = True
        elif event.key() == QtCore.Qt.Key_Down :
            self.renderer.rotX -= 5  
            redraw = True
  
        # Request display update
        if redraw :
            self.updateGL()

    
if __name__ == '__main__':
    app = QtGui.QApplication(["PyQt OpenGL"])
    widget = MyProfileWidget()
    widget.show()
    app.exec_()    