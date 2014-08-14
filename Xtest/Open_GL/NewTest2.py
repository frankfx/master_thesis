'''
Created on Jul 30, 2014

@author: fran_re
'''
'''
Created on Jul 30, 2014

@author: fran_re
'''
import sys
import math
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
    def init(self):
        self.rot1 = 0.0
        self.rot2 = 0.0
        self.rot3 = 0.0
        self.flat_obj_switcher = True
        
        
        # read vertex data from file
        f = open('ToyPlaneData.txt', 'r')
        self.vertSize = f.readline()
        
        if self.vertSize > 0 :
            self.toyPlaneData = [0] * int(self.vertSize)
            i = 0
            
            for vertData in f :
                if i < self.vertSize :
                    # store it in the vector
                    self.toyPlaneData[i] = float(vertData)
                i+=1
        f.close()
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
        self.drawCoordinateAxisZ()

        # rotate around y
        GL.glRotatef(self.rot2, 0, 1, 0)
        GL.glColor3f(0, 1, 0)
        self.drawCoordinateAxisY()

        # rotate around local x
        GL.glRotatef(self.rot3, 1, 0, 0)
        GL.glColor3f(1, 0, 0)
        self.drawCoordinateAxisX()

        # draw the plane in the local coordinate system
        if self.flat_obj_switcher :
            self.drawToyPlane();
        else :
            GL.glCallList(self.makeObject())
        
        GL.glFlush()               
        
    def drawCoordinateAxisZ(self):
        GL.glBegin(GL.GL_LINE_LOOP)     # circle in x-y plane
        for a in range(0,360,1) :
            angle = math.pi / 180 * a
            GL.glVertex3f(math.cos(angle), math.sin(angle), 0)
        GL.glEnd()
        
        GL.glBegin(GL.GL_LINES);
        GL.glVertex3f(0.9, 0.0, 0.0)    # x-axis
        GL.glVertex3f(1.0, 0.0, 0.0)
        GL.glVertex3f(0.0, 0.9, 0.0)    # y-axis
        GL.glVertex3f(0.0, 1.0, 0.0)
        GL.glVertex3f(0.0, 0.0,-1.0)    # z-axis
        GL.glVertex3f(0.0, 0.0, 1.0)
        GL.glEnd();
    
        GL.glBegin(GL.GL_TRIANGLES)     # z-axis tip
        GL.glVertex3f(0.0,-0.1, 0.9)
        GL.glVertex3f(0.0, 0.0, 1.0)
        GL.glVertex3f(0.0, 0.1, 0.9)
        GL.glEnd();        
            
    def drawCoordinateAxisX(self):
        GL.glPushMatrix()
        GL.glRotatef(90, 1, 0, 0)
        self.drawCoordinateAxisZ()
        GL.glPopMatrix()            
        
    def drawCoordinateAxisY(self):
        GL.glPushMatrix()
        GL.glRotatef(-90, 0, 1, 0)
        self.drawCoordinateAxisZ()
        GL.glPopMatrix()
        
    def drawToyPlane(self):
        GL.glColor3f(0,5, 0.5, 0,5)
        GL.glBegin(GL.GL_TRIANGLES)
        for i in range(0, len(self.toyPlaneData), 3)  :
            GL.glVertex3d(self.toyPlaneData[i], self.toyPlaneData[i+1], self.toyPlaneData[i+2])       
        GL.glEnd()
        
    def makeObject(self):
        genList = GL.glGenLists(1)
        GL.glNewList(genList, GL.GL_COMPILE)

        GL.glBegin(GL.GL_QUADS)

        x1 = +0.06
        y1 = -0.14
        x2 = +0.14
        y2 = -0.06
        x3 = +0.08
        y3 = +0.00
        x4 = +0.30
        y4 = +0.22

        GL.glVertex3d(x1, y1, +0.05)
        GL.glVertex3d(x2, y2, +0.05)
        GL.glVertex3d(x2, y2, -0.05)
        GL.glVertex3d(x1, y1, -0.05)

        self.quad(x1, y1, x2, y2, y2, x2, y1, x1)
        self.quad(x3, y3, x4, y4, y4, x4, y3, x3)


        self.extrude(x1, y1, x2, y2)
        self.extrude(x2, y2, y2, x2)
        self.extrude(y2, x2, y1, x1)
        self.extrude(y1, x1, x1, y1)
        self.extrude(x3, y3, x4, y4)
        self.extrude(x4, y4, y4, x4)
        self.extrude(y4, x4, y3, x3)

        Pi = 3.14159265358979323846
        NumSectors = 200

        for i in range(NumSectors):
            angle1 = (i * 2 * Pi) / NumSectors

            x5 = 0.30 * math.sin(angle1)
            y5 = 0.30 * math.cos(angle1)
            x6 = 0.20 * math.sin(angle1)
            y6 = 0.20 * math.cos(angle1)

            angle2 = ((i + 1) * 2 * Pi) / NumSectors
            x7 = 0.20 * math.sin(angle2)
            y7 = 0.20 * math.cos(angle2)
            x8 = 0.30 * math.sin(angle2)
            y8 = 0.30 * math.cos(angle2)

            self.quad(x5, y5, x6, y6, x7, y7, x8, y8)

            self.extrude(x6, y6, x7, y7)
            self.extrude(x8, y8, x5, y5)

        GL.glEnd()
        GL.glEndList()

        return genList

    def quad(self, x1, y1, x2, y2, x3, y3, x4, y4):
        GL.glColor3f(1, 0, 0)

        GL.glVertex3d(x1, y1, -0.05)
        GL.glVertex3d(x2, y2, -0.05)
        GL.glVertex3d(x3, y3, -0.05)
        GL.glVertex3d(x4, y4, -0.05)

        GL.glVertex3d(x4, y4, +0.05)
        GL.glVertex3d(x3, y3, +0.05)
        GL.glVertex3d(x2, y2, +0.05)
        GL.glVertex3d(x1, y1, +0.05)

    def extrude(self, x1, y1, x2, y2):
        GL.glColor3f(0.81, 0, 0)

        GL.glVertex3d(x1, y1, +0.05)
        GL.glVertex3d(x2, y2, +0.05)
        GL.glVertex3d(x2, y2, -0.05)
        GL.glVertex3d(x1, y1, -0.05)        
        
        

class MyWidget(QtOpenGL.QGLWidget):
    def __init__(self, parent = None):
        super(MyWidget, self).__init__(parent)
       # self.resize(320,320)
        self.setWindowTitle("Rene Test")
        self.renderer = Renderer()
    
    def initializeGL(self):
        self.renderer.init()
    
    def resizeGL(self, w, h):
        self.renderer.resize(w, h)
 
    def paintGL(self):
        self.renderer.display()
  
    def keyPressEvent(self, event):
        redraw = False
        offset = 2.5
        if event.modifiers() == QtCore.Qt.ControlModifier :
            offset = -1 *offset
        
        if event.key() == QtCore.Qt.Key_4 :
            self.renderer.flat_obj_switcher = not self.renderer.flat_obj_switcher
            redraw = True
        elif event.key() == QtCore.Qt.Key_1:
            self.renderer.rot1 += offset
            redraw = True
        elif event.key() == QtCore.Qt.Key_2:
            self.renderer.rot2 += offset
            redraw = True
        elif event.key() == QtCore.Qt.Key_3:
            self.renderer.rot3 += offset
            redraw = True
        elif event.key() == QtCore.Qt.Key_0:
            self.renderer.rot1 = 0
            self.renderer.rot2 = 0
            self.renderer.rot3 = 0
            redraw = True
        if redraw :
            self.updateGL()
  
    def mousePressEvent(self, event):
        self.lastPos = QtCore.QPoint(event.pos())

    def mouseMoveEvent(self, event):
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()

        if event.buttons() & QtCore.Qt.LeftButton:
            self.renderer.rot3 = self.renderer.rot3 + 0.51 * dy
            self.renderer.rot2 = self.renderer.rot2 + 0.51 * dx
        elif event.buttons() & QtCore.Qt.RightButton :
            self.renderer.rot3 = self.renderer.rot3 + 0.51 * dy 
            self.renderer.rot1 = self.renderer.rot1 + 0.51 * dx 
 
        self.lastPos = QtCore.QPoint(event.pos())  
        self.updateGL()
  
  
if __name__ == '__main__':
    app = QtGui.QApplication(["PyQt OpenGL"])
    widget = MyWidget()
    widget.show()
    app.exec_()    