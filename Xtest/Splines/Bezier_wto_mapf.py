'''
Created on Aug 27, 2014

@author: fran_re
'''
import sys
import math
from PySide import QtOpenGL, QtGui

try:
    from OpenGL import GL
except ImportError:
    app = QtGui.QApplication(sys.argv)
    QtGui.QMessageBox.critical(None, "OpenGL hellogl",
                              "PyOpenGL must be installed to run this example.",
                            QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default,
                            QtGui.QMessageBox.NoButton)
    sys.exit(1)


class Point :
    def __init__(self, idx, x, y, z):
        self._id = idx
        self._x = x
        self._y = y
        self._z = z

    def PrintPoint(self) :
        print("Point %d = <%f, %f, %f>\n" % (self._id, self._x, self._y, self._z))

class Renderer:
    OPEN,CLOSED = range(2)
    def __init__(self):
        self.flag_view_algo = Renderer.OPEN
        self.ctrlpointsX = [1.0, 0.95, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.25, 0.2, 0.15, 0.1, 0.075, 0.05, 0.025, 0.0125, 0.005, 0.0, 0.005, 0.0125, 0.025, 0.05, 0.075, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5]
        self.ctrlpointsZ = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.ctrlpointsY = [0.00095, 0.00605, 0.01086, 0.01967, 0.02748, 0.03423, 0.03971, 0.04352, 0.04501, 0.04456, 0.04303, 0.04009, 0.03512, 0.0315, 0.02666, 0.01961, 0.0142, 0.0089, 0.0, -0.0089, -0.0142, -0.01961, -0.02666, -0.0315, -0.03512, -0.04009, -0.04303, -0.04456, -0.04501, -0.04352, -0.03971]        

    def set_flag_view(self, value):
        self.flag_view_algo = value

    def init(self):
        GL.glEnable(GL.GL_COLOR_MATERIAL)
        GL.glClearColor(0.0, 0.0 , 0.0, 0.0)        
        GL.glShadeModel(GL.GL_FLAT)        

    def bezierCurve(self, t, P_0, P_1, P_2, P_3):
        # Cubic bezier Curve
        point = (math.pow((1-t), 3.0) * P_0) + \
                (3 * math.pow((1-t),2) * t * P_1) + \
                (3 * (1-t) * t * t * P_2) + \
                (math.pow(t, 3) * P_3)
        return point

    def bezierCurve_full(self, t, pList):
        # Curve with level n has n + 1 points : P0 ... Pn
        n = len(pList) - 1
        return self.bezierCurve_full_rec(0, n, t, pList)

    def bezierCurve_full_rec(self, i, n, t, pList):
        if i == n :
            return math.pow(t, i) * pList[i]
        else :
            return self.compute_Bernsteinpolynom(i, n, t) * pList[i] + self.bezierCurve_full_rec(i+1, n, t, pList)
            
    def compute_Bernsteinpolynom(self,i, n, t):
        return math.factorial(n) / ( math.factorial(i) * math.factorial(n-i) ) * math.pow(t,i) * math.pow(1-t, n-i) 

    
    def display(self):
        
        # our control points
        #start = Point(0, -0.6, -0.4, 0)
        #tan1  = Point(0.1, -0.2,  0.6, 0)
        #tan2 = Point(0.2,  0.2, -0.4, 0)
        #end   = Point(0.3,  0.6,  0.4, 0)

        #start = Point(0,   -0.6, -0.4, 0)
        #tan1  = Point(0.1, -0.2,  0.6, 0)
        #tan2  = Point(0.2,  0.2, -0.4, 0)
        #end   = Point(0.3,  0.6,  0.4, 0)

        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        GL.glColor3f(1.0, 1.0, 1.0)
        
        GL.glBegin(GL.GL_LINE_LOOP)
        t = 31
        for i in range(0, t, 1):
            pos = i*1.0 / t
            #x = self.bezierCurve(pos, start._x, tan1._x, tan2._x, end._x)
            #y = self.bezierCurve(pos, start._y, tan1._y, tan2._y, end._y)
            x = self.bezierCurve_full(pos, self.ctrlpointsX)
            y = self.bezierCurve_full(pos, self.ctrlpointsY)
            z = self.bezierCurve_full(pos, self.ctrlpointsZ)
                
            #In our case, the z should always be empty
            #z = self.bezierCurve(pos, start._z, tan1._z, tan2._z, end._z)
            
            result = Point(4, x, y, z)
            result.PrintPoint()
            GL.glVertex3f(x, y, z)
        GL.glEnd()

        #The following code displays the control points as dots.
        i = 0
        GL.glPointSize(5.0)        
        GL.glColor3f(1.0, 0.0, 0.0)
        GL.glBegin(GL.GL_POINTS)
        for i in range (0, len(self.ctrlpointsX), 1):
            GL.glVertex3f(self.ctrlpointsX[i], self.ctrlpointsY[i], self.ctrlpointsZ[i])
        GL.glEnd()        
        
        GL.glFlush()

    def resize(self, w, h) :
        v = 0.5
        GL.glViewport(0, 0, w, h)
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        # glOrtho scales the matrix by multiplying the matrix
        if (w <= h) :
            GL.glOrtho(-v, v+1, -v * h / w, v * h / w, -v, v)
        else :
            GL.glOrtho(-v * w / h, v * w / h, -v, v, -v, v)
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()



class MyWidget(QtOpenGL.QGLWidget):
    def __init__(self, parent = None):
        super(MyWidget, self).__init__(parent)
        self.resize(620,620)
        self.setWindowTitle("Rene Test")

        self.renderer = Renderer()  
        self.renderer.set_flag_view(Renderer.CLOSED) 
    
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



