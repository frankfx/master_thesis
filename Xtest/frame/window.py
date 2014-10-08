'''
Created on Jul 30, 2014

@author: fran_re
'''
'''
Created on Jul 30, 2014

@author: fran_re
'''
import sys
from Xtest.frame.graphics import plane
from Xtest.frame.graphics import coordinate_system
from Xtest.frame.graphics import symbol
from Xtest.frame.graphics import pyramid
from PySide import QtOpenGL, QtGui, QtCore
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
    def __init__(self):
        self.rot1 = 0.0
        self.rot2 = 0.0
        self.rot3 = 0.0
        self.scale = 1.0

        self.objCoord   = coordinate_system.CoordinateSystem()        
        self.objPlane   = plane.Plane()
        self.objSymbol  = symbol.Symbol()
        self.objPyramid = pyramid.Pyramid()
        
        self.objCount = 3 # plane, symbol, Pyramid - coords will drawn all the time
        self.flag_obj_switcher = 0  # flag to switch between the objects
        
        GL.glEnable(GL.GL_DEPTH_TEST)   # Wenn aktiviert werden Tiefenvergleiche getaetigt und der Tiefenpuffer aktualisiert.
        
    def resize(self, w, h):
        GL.glViewport(0,0,w,h) 
        GL.glMatrixMode(GL.GL_PROJECTION);
        GL.glLoadIdentity();
        GLU.gluPerspective (65.0, w/h, 0.1, 10.0);    
        
    def display(self):
        
        GL.glClearColor(0.0, 0.0, 0.0, 0.0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()

        # view scene from the side
        GL.glTranslatef(0.0,0.0,-3.0);
        GL.glRotatef( -45.0, 0.0, 0.0, 1.0)
        GL.glRotatef( -45.0, 0.0, 1.0, 0.0)
        GL.glRotatef( 135.0, 1.0, 0.0, 0.0)

        # rotate around z
        GL.glRotatef(self.rot1, 0, 0, 1)
        GL.glColor3f(0, 0, 1)
        self.objCoord.drawCoordinateAxisZ()

        # rotate around y
        GL.glRotatef(self.rot2, 0, 1, 0)
        GL.glColor3f(0, 1, 0)
        self.objCoord.drawCoordinateAxisY()

        # rotate around local x
        GL.glRotatef(self.rot3, 1, 0, 0)
        GL.glColor3f(1, 0, 0)
        self.objCoord.drawCoordinateAxisX()

        GL.glScale(self.scale, self.scale, self.scale)
       
        if self.flag_obj_switcher == 0 :
            self.objPlane.draw()
            self.objSymbol.draw()
        elif self.flag_obj_switcher == 1 :
            self.objPyramid.draw()
        else :
            GL.glCallList(self.objSymbol.draw())
        
        GL.glFlush()               
        

class AirfoilDetectorWidget(QtOpenGL.QGLWidget):
    def __init__(self, parent = None):
        super(AirfoilDetectorWidget, self).__init__(parent)
        self.resize(320,320)
        self.setWindowTitle("Rene Test")
        self.renderer = Renderer()
    
    def initializeGL(self):
        self.renderer.__init__()
    
    def resizeGL(self, w, h):
        self.renderer.resize(w, h)
 
    def paintGL(self):
        self.renderer.display()
  
    def keyPressEvent(self, event):
        redraw = False
        offsetRot = 2.5
        offsetScl = 0.25
        if event.modifiers() == QtCore.Qt.ControlModifier :
            offsetRot = -1 *offsetRot
            offsetScl = -1 *offsetScl

        if event.key() == QtCore.Qt.Key_4 :
            if self.renderer.flag_obj_switcher >= self.renderer.objCount - 1 :
                self.renderer.flag_obj_switcher = 0
            else :
                self.renderer.flag_obj_switcher += 1
            redraw = True
        elif event.key() == QtCore.Qt.Key_1:
            self.renderer.rot1 += offsetRot
            redraw = True
        elif event.key() == QtCore.Qt.Key_2:
            self.renderer.rot2 += offsetRot
            redraw = True
        elif event.key() == QtCore.Qt.Key_3:
            self.renderer.rot3 += offsetRot
            redraw = True
        elif event.key() == QtCore.Qt.Key_5:
            self.renderer.scale += offsetScl
            redraw = True
        elif event.key() == QtCore.Qt.Key_0:
            self.renderer.rot1 = 0.0
            self.renderer.rot2 = 0.0
            self.renderer.rot3 = 0.0
            self.renderer.scale = 1.0
            redraw = True
        if redraw :
            self.updateGL()
        print self.renderer.scale

    def mousePressEvent(self, event):
        self.lastPos = QtCore.QPoint(event.pos())

    def mouseMoveEvent(self, event):
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()

        if event.buttons() & QtCore.Qt.LeftButton:
            self.renderer.rot3 = self.renderer.rot3 + 0.51 * dx
            self.renderer.rot2 = self.renderer.rot2 + 0.51 * dy
        elif event.buttons() & QtCore.Qt.RightButton :
            self.renderer.rot3 = self.renderer.rot3 + 0.51 * dy
            self.renderer.rot1 = self.renderer.rot1 + 0.51 * dx

        self.lastPos = QtCore.QPoint(event.pos())
        self.updateGL()
  
  
if __name__ == '__main__':
    app = QtGui.QApplication(["PyQt OpenGL"])
    widget = AirfoilDetectorWidget()
    widget.show()
    app.exec_()    