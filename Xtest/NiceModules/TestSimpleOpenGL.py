 
'''
Created on Aug 22, 2014

@author: rene
'''
from Xtest.Open_GL import airfoilDetectWidget, utility
import math
import Xtest

'''
Created on Jul 30, 2014

@author: fran_re
'''
import sys
import math
import Xtest.Open_GL.utility 
from PySide import QtOpenGL, QtGui, QtCore
from Xtest.Open_GL.cpacsHandler import CPACS_Handler
from Xtest.Open_GL.configuration.config import Config
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
        self.plist = [[1.0, 0.00095, 0.0], [0.95, 0.00605, 0.0], [0.9, 0.01086, 0.0], [0.8, 0.01967, 0.0], \
                           [0.7, 0.02748, 0.0], [0.6, 0.03423, 0.0], [0.5, 0.03971, 0.0], [0.4, 0.04352, 0.0], \
                           [0.3, 0.04501, 0.0], [0.25, 0.04456, 0.0], [0.2, 0.04303, 0.0], [0.15, 0.04009, 0.0], \
                           [0.1, 0.03512, 0.0], [0.075, 0.0315, 0.0], [0.05, 0.02666, 0.0], [0.025, 0.01961, 0.0], \
                           [0.0125, 0.0142, 0.0], [0.005, 0.0089, 0.0], [0.0, 0.0, 0.0], [0.005, -0.0089, 0.0], \
                           [0.0125, -0.0142, 0.0], [0.025, -0.01961, 0.0], [0.05, -0.02666, 0.0], [0.075, -0.0315, 0.0], \
                           [0.1, -0.03512, 0.0], [0.15, -0.04009, 0.0], [0.2, -0.04303, 0.0], [0.25, -0.04456, 0.0], \
                           [0.3, -0.04501, 0.0], [0.4, -0.04352, 0.0], [0.5, -0.03971, 0.0], [0.6, -0.03423, 0.0], \
                           [0.7, -0.02748, 0.0], [0.8, -0.01967, 0.0], [0.9, -0.01086, 0.0], [0.95, -0.00605, 0.0], \
                           [1.0, -0.00095, 0.0]]        
        self.object = 0
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0   
        self.scale = 1    
        
        
    def init(self):
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_COLOR_MATERIAL)
        GL.glClearColor(0.0, 0.0 , 0.0, 1.0)
    
    def resize(self, w, h):
        side = min(w, h)
        GL.glViewport(0,0,w,h)
        #GL.glViewport((w - side) / 2, (h - side) / 2, side, side)

        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
       
#        '''gluunproject vs gluperspective'''
        GLU.gluPerspective (100.0, w*1.0/h, 0.00001, 20.0)
        
    def display(self):
        # Clear screen and Z-buffer
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT) 
        
        # Reset transformations
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()
       
        GL.glTranslated(0.0, 0.0, -5.0)              
       # GL.glRotated(self.xRot, 1.0, 0.0, 0.0)
       # GL.glRotated(self.yRot, 0.0, 1.0, 0.0)
       # GL.glRotated(self.zRot, 0.0, 0.0, 1.0) 
       # GL.glScalef(self.scale,self.scale,self.scale)
        
        self.drawSuperEllipse_Top(4.0, 4.0, 3.0, 10.0)
        self.drawSuperEllipse_Bot(7.0, 4.0, 1.0, 10.0)

        GL.glFlush()    


    def drawSuperEllipse_Top(self, a, b, n, cnt):
        plist = self.__createSuperEllipse(a, b, n, cnt)
        
        GL.glLineWidth(2)
        GL.glColor3f(0.0, 0.0, 1.0)
        GL.glBegin(GL.GL_LINE_STRIP) 
        
        for p in plist :
            GL.glVertex3f(p[0], p[1], p[2])              
        GL.glEnd() 
    
    def drawSuperEllipse_Bot(self, a, b, n, cnt):
        plist = self.__createSuperEllipse(a, b, n, cnt)
        
        GL.glLineWidth(2)
        GL.glColor3f(0.0, 0.0, 1.0)
        GL.glBegin(GL.GL_LINE_STRIP) 
        
        for p in plist :
            GL.glVertex3f(p[0], -p[1], p[2])              
        GL.glEnd() 
        

    def __createSuperEllipse(self, a=4.0, b=5.0, n=1.0, cnt=10, z=0.5):
        plist = []
        x = -a
        dist = (2.0*a) / cnt
        
        while x < a or utility.equalFloats2(x, a) :
            y = b * math.pow( utility.absolut(1 - math.pow( utility.absolut(x / a), 2/n) ), n/2 )
            plist.append([x, y, z])
            x += dist 
        return plist

    def drawTriangle(self):
        GL.glLineWidth(2)
        GL.glColor3f(0.0, 0.0, 1.0)
        GL.glBegin(GL.GL_LINE_STRIP) 
        for p in self.plist :
            GL.glVertex3f(p[0], p[1], p[2])              
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

class Widget(QtOpenGL.QGLWidget):
    def __init__(self, parent = None):
        super(Widget, self).__init__(parent)
        self.width = 320
        self.height = 302
        self.resize(self.width ,self.height)
        self.setWindowTitle("Rene Test")
      
      
        grid = QtGui.QGridLayout()
      
        self.widthSpinBox = QtGui.QDoubleSpinBox()
        self.widthSpinBox.setRange(20, 200)
        self.widthSpinBox.setSingleStep(5)
        self.widthSpinBox.setSuffix('pts')
        self.widthSpinBox.setValue(10)
        
        self.heightSpinBox = QtGui.QDoubleSpinBox()
        self.heightSpinBox.setRange(20, 200)
        self.heightSpinBox.setSingleStep(5)
        self.heightSpinBox.setSuffix('pts')
        self.heightSpinBox.setValue(10)        
        
        self.curveSpinBox = QtGui.QDoubleSpinBox()
        self.curveSpinBox.setRange(20, 200)
        self.curveSpinBox.setSingleStep(5)
        self.curveSpinBox.setSuffix('pts')
        self.curveSpinBox.setValue(10)       
        
        self.pcntSpinBox = QtGui.QDoubleSpinBox()
        self.pcntSpinBox.setRange(20, 200)
        self.pcntSpinBox.setSingleStep(5)
        self.pcntSpinBox.setSuffix('pts')
        self.pcntSpinBox.setValue(10)       
        
        
        grid.addWidget(self.widthSpinBox, 0,0)
        grid.addWidget(self.heightSpinBox, 0,1)
        grid.addWidget(self.curveSpinBox, 0,2)
        grid.addWidget(self.pcntSpinBox, 0,3)        
        
        self.setLayout(grid)
        
        
        
        
        
        
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
            ()
            #self.renderer.set_coordinates(event.x(), event.y(), 1)
        elif event.buttons() & QtCore.Qt.RightButton :
            ()

        self.lastPos = QtCore.QPoint(event.pos())
        self.updateGL()

    def keyPressEvent(self, event):
        redraw = False
        offset_rot   = 5
        offset_scale = 1
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
  
        # Request display update
        if redraw :
            self.updateGL()
    
if __name__ == '__main__':
    app = QtGui.QApplication(["PyQt OpenGL"])
    widget = Widget()
    widget.show()
    app.exec_()    