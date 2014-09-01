'''
Created on Aug 22, 2014

@author: rene
'''

'''
Created on Jul 30, 2014

@author: fran_re
'''
import numpy as np
import cv2
import sys
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
        self.scale = 1.0
        self.trans_x = 0
        self.trans_y = 0
        self.width = -1
        self.height = -1
        self.fovy = 64.0

    def init(self):
        ()
    
    def resize(self, w, h):
        self.width , self.height = w , h
        GL.glViewport(0,0,w,h) 
                                   
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        v=3.5#+self.scale
        print v
        #GLU.gluPerspective (64.0, w*1.0/h, 0.0, 10.0)
        if (w <= h) :
            GL.glFrustum(-v, v, -v * h / w, v * h / w, 1.1, 100)
        else :
            GL.glFrustum(-v * w / h, v * w / h, -v, v, 1.1, 100)
    
    def display(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT) 
        
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()
       
        
        GL.glTranslatef(self.trans_x,self.trans_y,-1.5)
        #self.drawTriangle2()
        self.drawProfile()
        GL.glFlush()    

    def drawTriangle(self):
        GL.glColor3f(1.0, 1.0, 1.0)
        GL.glBegin(GL.GL_POINTS)
        GL.glVertex3f(1.03, 3.59, -0.5)
        GL.glVertex3f(1.04, 3.58, -0.5)
        GL.glVertex3f(1.55, 3.5, -0.5)
        GL.glEnd()   
    
    def drawProfile(self):
        coord = self.detectProfile()
        GL.glColor3f(1.0, 1.0, 1.0)
        GL.glBegin(GL.GL_LINE_LOOP)        
        for i in range (0, len(coord)) :
            for j in range (0, len(coord[i])) :
                GL.glVertex3f(coord[i][j][0]/100.0, coord[i][j][1]/100.0, -0.5)
        GL.glEnd()
    
    def detectProfile(self):        
        img = cv2.imread('wing2.jpg')
        gray = cv2.imread('wing2.jpg',0)

        ret,thresh = cv2.threshold(gray,127,255,1)
        contours,h = cv2.findContours(thresh,1,2)
        n = 0

        for cnt in contours:
            approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
            if len(approx)==5:
                n+=1
            if n == 2 :
                return cnt

class MyWidget(QtOpenGL.QGLWidget):
    def __init__(self, parent = None):
        super(MyWidget, self).__init__(parent)
        self.resize(320,320)
        self.setWindowTitle("Rene Test")
        #self.setFixedSize(QtCore.QSize(400,400))
        self.dx = 0.0
        self.dy = 0.0
        self.lastPos_x = 0.0
        self.lastPos_y = 0.0
        
        self.renderer = Renderer()
    
    def initializeGL(self):
        self.renderer.init()
    
    def resizeGL(self, w, h):
        self.renderer.resize(w, h)
 
    def paintGL(self):
        self.renderer.display()

    def keyPressEvent(self, event):
        redraw = False
        offsetScl = 0.5
        offsetTrans = 0.02
        if event.modifiers() == QtCore.Qt.ControlModifier:
            if event.key() == QtCore.Qt.Key_N :
                if self.renderer.flag_view_algo > 1 :
                    self.renderer.flag_view_algo = 0
                else : self.renderer.flag_view_algo += 1
            elif event.key() == QtCore.Qt.Key_S :
                self.renderer.nextTestValue()
            elif event.key() == QtCore.Qt.Key_A :
                self.renderer.prevTestValue()
            redraw = True
        if event.key() == QtCore.Qt.Key_Plus:
            self.renderer.scale -= offsetScl
            redraw = True
        elif event.key() == QtCore.Qt.Key_Minus:
            self.renderer.scale += offsetScl
            redraw = True
        elif event.key() == QtCore.Qt.Key_Left:
            self.renderer.trans_x += offsetTrans
            redraw = True                         
        elif event.key() == QtCore.Qt.Key_Right:
            self.renderer.trans_x -= offsetTrans
            redraw = True
        elif event.key() == QtCore.Qt.Key_Up:
            self.renderer.trans_y -= offsetTrans
            redraw = True
        elif event.key() == QtCore.Qt.Key_Down:
            self.renderer.trans_y += offsetTrans
            redraw = True                                
        
        if redraw :
            self.updateGL()
            
    def mousePressEvent(self, event):      
        self.lastPos_x = event.pos().x()
        self.lastPos_y = event.pos().y()
                
    def mouseMoveEvent(self, event):
        self.dx = (event.pos().x() - self.lastPos_x ) 
        self.dy =  (event.pos().y() - self.lastPos_y ) 
        
        self.lastPos_x += self.dx
        self.lastPos_y += self.dy
        
        self.renderer.trans_x += (self.dx * 2.0 / self.width() * self.renderer.scale) 
        self.renderer.trans_y -= (self.dy * 2.0 / self.height() * self.renderer.scale)
        self.updateGL()

    
if __name__ == '__main__':
    app = QtGui.QApplication(["PyQt OpenGL"])
    widget = MyWidget()
    widget.show()
    app.exec_()    