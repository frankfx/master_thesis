'''
Created on Aug 27, 2014

@author: fran_re
'''
import sys
import math
from PySide import QtOpenGL, QtGui, QtCore
from PySide.QtGui import QPushButton
from Xtest.Splines.BezierTest import Bezier

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
    OPEN,CLOSED = range(2)
    def __init__(self):
        self.ctrlpoints = [ [1.0, 0.00095, 0.0], [0.95, 0.00605, 0.0], [0.9, 0.01086, 0.0], [0.8, 0.01967, 0.0], [0.7, 0.02748, 0.0], [0.6, 0.03423, 0.0], [0.5, 0.03971, 0.0], [0.4, 0.04352, 0.0], [0.3, 0.04501, 0.0], [0.25, 0.04456, 0.0], [0.2, 0.04303, 0.0], [0.15, 0.04009, 0.0], [0.1, 0.03512, 0.0], [0.075, 0.0315, 0.0], [0.05, 0.02666, 0.0], [0.025, 0.01961, 0.0], [0.0125, 0.0142, 0.0], [0.005, 0.0089, 0.0], [0.0, 0.0, 0.0], [0.005, -0.0089, 0.0], [0.0125, -0.0142, 0.0], [0.025, -0.01961, 0.0], [0.05, -0.02666, 0.0], [0.075, -0.0315, 0.0], [0.1, -0.03512, 0.0], [0.15, -0.04009, 0.0], [0.2, -0.04303, 0.0], [0.25, -0.04456, 0.0], [0.3, -0.04501, 0.0], [0.4, -0.04352, 0.0], [0.5, -0.03971, 0.0] ]
        self.flag_view_algo = Renderer.OPEN
    
    def flag_view(self, value):
        self.flag_view_algo = value
        
    def init(self):
        GL.glEnable(GL.GL_COLOR_MATERIAL)
        GL.glEnable(GL.GL_MAP1_VERTEX_3)
        GL.glClearColor(0.0, 0.0, 0.0, 0.0)       
        GL.glShadeModel(GL.GL_FLAT)        
        
    def display(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        GL.glColor3f(1.0, 1.0, 1.0)              
           
        for a in range (0, len(self.ctrlpoints), 7):
            tmp = []
            hlp = 8  if a < len(self.ctrlpoints) -7 else len(self.ctrlpoints) - a
            
            for b in range (a, a + hlp, 1) :
                tmp.append(self.ctrlpoints[b])
            
            if hlp < 8 and self.flag_view_algo == Renderer.CLOSED :
                tmp.append(self.ctrlpoints[0])

            GL.glMap1f(GL.GL_MAP1_VERTEX_3, 0.0, 1.0, tmp)

            GL.glBegin(GL.GL_LINE_STRIP)
            for i in range (0, 31, 1):
                GL.glEvalCoord1f(i/30.0)
            GL.glEnd()
            if (hlp < 8) :
                break
        
        #The following code displays the control points as dots.
        i=0
        GL.glPointSize(5.0)        
        GL.glColor3f(1.0, 0.0, 0.0)
        GL.glBegin(GL.GL_POINTS)
        for i in range (0, len(self.ctrlpoints), 1):
            GL.glVertex3f(self.ctrlpoints[i][0], self.ctrlpoints[i][1], self.ctrlpoints[i][2])
        GL.glEnd()
        
        GL.glFlush()


        
    def split_profile(self, l_1, l_2, l_3):
        l_fst = []
        l_snd = []
        for i in range(0, len(l_1)-1, 1) :
            if l_1[i] > l_1[i+1] :
                l_fst.append([ l_1[i], l_2[i], l_3[i] ]) 
            else:
                break
        for j in range(j, len(l_1), 1) :
            l_snd.append([ l_1[i], l_2[i], l_3[i] ])

        return l_fst , l_snd

    def resize(self, w, h) :
        v = 0.5
        GL.glViewport(0, 0, w, h)
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        # glOrtho scales the matrix by multiplying the matrix
        if (w <= h) :
            GL.glOrtho(-v*0.1, v, -v * h / w, v * h / w, -v, v)
        else :
            GL.glOrtho(-v * w / h, v * w / h, -v, v, -v, v)
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()


class MyProfileWidget(QtOpenGL.QGLWidget):
    def __init__(self, parent = None):
        super(MyProfileWidget, self).__init__(parent)
        self.resize(620,620)
        self.setWindowTitle("Rene Test")



        self.renderer = Renderer()    
        self.renderer.flag_view(Renderer.CLOSED)
        
        self.rede
    
    def initializeGL(self):
        self.renderer.init()
    
    def resizeGL(self, w, h):
        self.renderer.resize(w, h)
 
    def paintGL(self):
        self.renderer.display()

if __name__ == '__main__':
    app = QtGui.QApplication(["PyQt OpenGL"])
    widget = MyProfileWidget()
    widget.show()
    app.exec_()    



