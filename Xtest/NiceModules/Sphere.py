'''
Created on Jul 30, 2014

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

class Renderer():

    def __init__(self, width, height):
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0
        self.xTrans = 0
        self.yTrans = 0  
        self.scale = 6.0 
        self.aspect= 0.5  
        self.viewwidth = 0.0
        self.viewheight = 0.0
        self.highShininess    = False # Whether the shininess parameter is high
        self.lowSpecularity   = False # Whether the specularity parameter is high
        self.emission         = False # Whether the emission parameter is turned on
        self.radius           = 1.0
        
    def init(self):
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_LIGHTING)
        GL.glEnable(GL.GL_LIGHT0)
        GL.glEnable(GL.GL_NORMALIZE)
        GL.glShadeModel(GL.GL_SMOOTH)
        #Disable color materials, so that glMaterial calls work
        GL.glDisable(GL.GL_COLOR_MATERIAL)      
        
    def resize(self, w, h):
        side = min(w, h)
        self.viewwidth = side
        self.viewheight = side
        
        GL.glViewport((w - side) / 2, (h - side) / 2, self.viewwidth, self.viewheight)

        self.__setRendermodus()        

    def __setRendermodus(self):
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
       
        GL.glOrtho(-1.0 * self.aspect * self.scale, +1.0 * self.aspect * self.scale,
                    +1.0* self.aspect * self.scale, -1.0* self.aspect * self.scale, -10.0, 12.0)
      
      
  
    def initLight(self):
        
        ambientLight = [0.2, 0.2, 0.2, 1.0]
        GL.glLightModelfv(GL.GL_LIGHT_MODEL_AMBIENT, ambientLight)
    
        lightColor  = [0.6, 0.6, 0.6, 1.0]
        lightPos    = [1.5 * self.radius, 2 * self.radius, 1.5 * self.radius, 1.0]
        # Diffuse (non-shiny) light component
        GL.glLightfv(GL.GL_LIGHT0, GL.GL_DIFFUSE, lightColor)
        # Specular (shiny) light component
        GL.glLightfv(GL.GL_LIGHT0, GL.GL_SPECULAR, lightColor)
        GL.glLightfv(GL.GL_LIGHT0, GL.GL_POSITION, lightPos)
        
        specularity = 0.0
        emissivity  = 0.0
        shininess   = 0.0
        
        if self.lowSpecularity :
            specularity = 0.3
        else :
            specularity = 1.0
        
        if self.emission :
            emissivity = 0.05
        else :
            emissivity = 0
        
        if self.highShininess :
            shininess = 25
        else :
            shininess = 12
        
        # The color of the sphere
        materialColor = [0.2, 0.2, 1.0, 1.0]
        # The specular (shiny) component of the material
        materialSpecular = [specularity, specularity, specularity, 1.0]
        # The color emitted by the material
        materialEmission = [emissivity, emissivity, emissivity, 1.0]
    
        GL.glMaterialfv(GL.GL_FRONT, GL.GL_AMBIENT_AND_DIFFUSE, materialColor)
        GL.glMaterialfv(GL.GL_FRONT, GL.GL_SPECULAR, materialSpecular)
        GL.glMaterialfv(GL.GL_FRONT, GL.GL_EMISSION, materialEmission)
        GL.glMaterialf(GL.GL_FRONT, GL.GL_SHININESS, shininess) #The shininess parameter        
      
      
      
      
      
      
      
   glBegin(GL_QUADS);
    
    //Front
    glNormal3f(0.0f, 0.0f, 1.0f);
    glVertex3f(-1.5f, -1.0f, 1.5f);
    glVertex3f(1.5f, -1.0f, 1.5f);
    glVertex3f(1.5f, 1.0f, 1.5f);
    glVertex3f(-1.5f, 1.0f, 1.5f);
    
    //Right
    glNormal3f(1.0f, 0.0f, 0.0f);
    glVertex3f(1.5f, -1.0f, -1.5f);
    glVertex3f(1.5f, 1.0f, -1.5f);
    glVertex3f(1.5f, 1.0f, 1.5f);
    glVertex3f(1.5f, -1.0f, 1.5f);
    
    //Back
    glNormal3f(0.0f, 0.0f, -1.0f);
    glVertex3f(-1.5f, -1.0f, -1.5f);
    glVertex3f(-1.5f, 1.0f, -1.5f);
    glVertex3f(1.5f, 1.0f, -1.5f);
    glVertex3f(1.5f, -1.0f, -1.5f);
    
    //Left
    glNormal3f(-1.0f, 0.0f, 0.0f);
    glVertex3f(-1.5f, -1.0f, -1.5f);
    glVertex3f(-1.5f, -1.0f, 1.5f);
    glVertex3f(-1.5f, 1.0f, 1.5f);
    glVertex3f(-1.5f, 1.0f, -1.5f);
    
    glEnd();      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
        

        
    def display(self):
       # self.__setRendermodus()
        
        # Clear screen and Z-buffer
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT) 
        
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()        
        
        GL.glPushMatrix()
        GL.glTranslatef(0.0, 0.0, -5.0)
        GL.glRotated(self.xRot, 1.0, 0.0, 0.0)
        GL.glRotated(self.yRot, 0.0, 1.0, 0.0)
        GL.glRotated(self.zRot, 0.0, 0.0, 1.0)  
       
        # Draw the sphere
        GLUT.glutInit()
       # GLUT.glutSolidCone(1.0,1.0,150,80)
       # GLUT.glutSolidTeapot(1.0)
        GLUT.glutWireTeapot(1.0)
        #GLUT.glutSolidSphere (1.0, 150, 80)
        GL.glPopMatrix()

        self.initLight()
        
        GL.glFlush() 


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
    
    def initializeGL(self):
        self.renderer.init()
    
    def resizeGL(self, w, h):
        self.renderer.resize(w, h)
 
    def paintGL(self):
        self.renderer.display()

    def mousePressEvent(self, event):  
        self.lastPos_x = event.pos().x()
        self.lastPos_y = event.pos().y()
                
    def mouseMoveEvent(self, event):
        dx = (event.x() - self.lastPos_x ) 
        dy = (event.y() - self.lastPos_y ) 
        
        self.lastPos_x += dx
        self.lastPos_y += dy

        #Betrachtsfeld = -aspect bis aspect
        
        oglXunit = 2.0 * self.renderer.aspect * self.renderer.scale
        oglYunit = oglXunit
        
        # pixel real world to Pixel ogl world 
        oglXTrans = oglXunit * 1.0 / self.renderer.viewwidth
        oglYTrans = oglYunit * 1.0 / self.renderer.viewheight
        
        self.renderer.xTrans += (dx * oglXTrans) 
        self.renderer.yTrans += (dy * oglYTrans)

        self.updateGL()

    def keyPressEvent(self, event):
        redraw = False
        offset_rot   = 2.0
        offset_scale = 0.1
        # Right arrow - increase rotation by 5 degree
        if event.key() == QtCore.Qt.Key_Right :
            self.renderer.yRot += offset_rot
            redraw = True
        # Left arrow - decrease rotation by 5 degree
        elif event.key() == QtCore.Qt.Key_Left :
            self.renderer.yRot -= offset_rot
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
        elif event.key() == QtCore.Qt.Key_Escape :
            sys.exit()
        elif event.key() == QtCore.Qt.Key_S :
            self.renderer.highShininess = not self.renderer.highShininess
            redraw = True
        elif event.key() == QtCore.Qt.Key_P :
            self.renderer.lowSpecularity = not self.renderer.lowSpecularity
            redraw = True
        elif event.key() == QtCore.Qt.Key_E :
            self.renderer.emission = not self.renderer.emission
            redraw = True            
  
        # Request display update
        if redraw :
            self.updateGL()
    
if __name__ == '__main__':
    app = QtGui.QApplication(["PyQt OpenGL"])
    widget = Widget()
    widget.show()
    app.exec_()    