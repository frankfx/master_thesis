'''
Created on Aug 19, 2014

@author: fran_re
'''
'''
Created on Jul 30, 2014

@author: fran_re
'''
'''
Created on Jul 30, 2014

@author: fran_re
'''
import math
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
        GL.glEnable(GL.GL_DEPTH_TEST)   # Wenn aktiviert werden Tiefenvergleiche getaetigt und der Tiefenpuffer aktualisiert.
        
    def resize(self, w, h):
        GL.glViewport(0,0,w,h) 
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
       # GLU.gluOrtho2D(0.0, w, 0.0, h)  # == 0, 320, 0, 320
       
       # GL.glOrtho(-1, 1, -1, 1, -1, 1)
        #GLU.gluOrtho2D(-0.5, 7 , -0.5, 7)
      #  GLU.gluPerspective (65.0, w/h, 0.1, 10.0)
        
    def display(self):
        
        GL.glClearColor(0.0, 0.0, 0.0, 0.0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()
        
#        x_list          = [0,20,30,40,50,60]
#        y_list          = [10,10,10,10,10,10]
        
        
       # GL.glTranslate(100,200,0)
        #----------------------------------------------- GL.glScale(0.4,0.4,0.0)
        #------------------------------------------- GL.glBegin(GL.GL_TRIANGLES)
        #------------------------------------------------ GL.glVertex2f(-2.5, 0)
        #------------------------------------------------- GL.glVertex2f(2.5, 0)
        #--------------------------------------------------- GL.glVertex2f(0, 4)
        #------------------------------------------ GL.glVertex3f(-2.5, 0, -0.5)
        #------------------------------------------- GL.glVertex3f(2.5, 0, -0.5)
        #--------------------------------------------- GL.glVertex3f(0, 4, -0.5)
    #    GL.glEnd()        

        #----------------- GL.glBegin(GL.GL_LINE_LOOP)     # circle in x-y plane
        #--------------------------------------------- for a in range(0,360,1) :
            #----------------------------------------- angle = math.pi / 180 * a
            #---------------- GL.glVertex3f(math.cos(angle), math.sin(angle), 0)
        #------------------------------------------------------------ GL.glEnd()
        
        GL.glRotatef(90, 0, 1, 0)
        self.drawXCoord()
       # self.drawYCoord()
        
        GL.glFlush()  
                 
        
                     
        
    def drawXCoord(self):
        GL.glPushMatrix()
       # GL.glRotatef(-90, 0, 1, 0)
        GL.glBegin(GL.GL_LINES)
        GL.glVertex2f(0.0, 0.0)    # x-axis
        GL.glVertex2f(0.0, -0.5)
        GL.glEnd()
    
        GL.glBegin(GL.GL_TRIANGLES)     
        GL.glVertex2f(-0.05,-0.5)
        GL.glVertex2f(0.05, -0.5)
        GL.glVertex2f(0.0, -0.55)
        GL.glEnd()
        GL.glPopMatrix()
 
    def drawYCoord(self):
        GL.glPushMatrix()
        GL.glRotatef(90, 1, 0, 0)
        self.drawXCoord()
        GL.glPopMatrix()                  



class MyWidget(QtOpenGL.QGLWidget):
    def __init__(self, parent = None):
        super(MyWidget, self).__init__(parent)
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
    widget = MyWidget()
    widget.show()
    app.exec_()    