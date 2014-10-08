'''
Created on Sep 23, 2014

@author: fran_re
'''
import sys
from PySide import QtOpenGL, QtGui, QtCore
from Xtest.Splines.chaikin_spline import Chaikin

try:
    from OpenGL import GL, GLU
except ImportError:
    app = QtGui.QApplication(sys.argv)
    QtGui.QMessageBox.critical(None, "OpenGL hellogl",
                              "PyOpenGL must be installed to run this example.",
                            QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default,
                            QtGui.QMessageBox.NoButton)
    sys.exit(1)



class Renderer:
    def __init__(self):
        pntX = [1.0, 0.95, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.25, 0.2, 0.15, 0.1, 0.075, 0.05, 0.025, 0.0125, 0.005, 0.0, 0.005, 0.0125, 0.025, 0.05, 0.075, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5]
        pntZ = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        pntY = [0.00095, 0.00605, 0.01086, 0.01967, 0.02748, 0.03423, 0.03971, 0.04352, 0.04501, 0.04456, 0.04303, 0.04009, 0.03512, 0.0315, 0.02666, 0.01961, 0.0142, 0.0089, 0.0, -0.0089, -0.0142, -0.01961, -0.02666, -0.0315, -0.03512, -0.04009, -0.04303, -0.04456, -0.04501, -0.04352, -0.03971]        
        self.curve = Chaikin.initPLists(pntX, pntY, pntZ)
        self.width = -1.0
        self.height = -1.0     
        self.scale = 0.5
        self.fovy = 164   

    def init(self):
        GL.glEnable(GL.GL_COLOR_MATERIAL)
        GL.glClearColor(0.0, 0.0 , 0.0, 0.0)        
        GL.glShadeModel(GL.GL_FLAT)        

    def display(self):
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GLU.gluPerspective (self.fovy * self.scale, self.width*1.0/self.height, 0.0, 10.0)

        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()

        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        
        pList = self.curve.getPointList()
        
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        GL.glColor3f(1.0, 1.0, 1.0)
        
        GL.glBegin(GL.GL_LINE_LOOP)
        for p in pList :
            GL.glVertex3f(p.x, p.y, p.z)
        GL.glEnd()

        #The following code displays the control points as dots.
        GL.glPointSize(5.0)        
        GL.glColor3f(1.0, 0.0, 0.0)
        GL.glBegin(GL.GL_POINTS)
        for p in pList :
            GL.glVertex3f(p.x, p.y, p.z)
        GL.glEnd()        
        
        GL.glFlush()

    def resize(self, w, h) :
        self.width , self.height = w , h
        GL.glViewport(0,0,w,h)

        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GLU.gluPerspective (self.fovy * self.scale, w*1.0/h, 0.0, 10.0)

class AirfoilDetectorWidget(QtOpenGL.QGLWidget):
    def __init__(self, parent = None):
        super(AirfoilDetectorWidget, self).__init__(parent)
        self.resize(620,620)
        self.setWindowTitle("Rene Test")

        self.renderer = Renderer()  
    
    def initializeGL(self):
        self.renderer.init()
    
    def resizeGL(self, w, h):
        self.renderer.resize(w, h)
 
    def paintGL(self):
        self.renderer.display()

    def keyPressEvent(self,event):
            
        # increase the LOD   
        if event.key() == QtCore.Qt.Key_Plus :
            self.renderer.curve.IncreaseLod()
        # // decrease the LOD
        elif event.key() == QtCore.Qt.Key_Minus :            
            self.renderer.curve.DecreaseLod()
        elif event.key() == QtCore.Qt.Key_1 :            
            self.renderer.scale -= 0.02           
        elif event.key() == QtCore.Qt.Key_2 :            
            self.renderer.scale += 0.02 
            
        self.updateGL()
            
            
            
if __name__ == '__main__':
    app = QtGui.QApplication(["PyQt OpenGL"])
    widget = AirfoilDetectorWidget()
    widget.show()
    app.exec_()             
