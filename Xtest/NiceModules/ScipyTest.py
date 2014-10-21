from numpy import linspace,exp,absolute
from numpy.random import randn
from scipy.interpolate import InterpolatedUnivariateSpline
from scipy.interpolate import UnivariateSpline
import matplotlib.pyplot as plt

import sys
from PySide import QtOpenGL, QtGui, QtCore
from Xtest.Open_GL.spline import Chaikin

try:
    from OpenGL import GL, GLU
except ImportError:
    app = QtGui.QApplication(sys.argv)
    QtGui.QMessageBox.critical(None, "OpenGL hellogl",
                              "PyOpenGL must be installed to run this example.",
                            QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default,
                            QtGui.QMessageBox.NoButton)
    sys.exit(1)
    

class OGL_Widget(QtOpenGL.QGLWidget):

    coords = [[1.0, 0.00095, 0.0], [0.95, 0.00605, 0.0], [0.9, 0.01086, 0.0], [0.8, 0.01967, 0.0], \
                           [0.7, 0.02748, 0.0], [0.6, 0.03423, 0.0], [0.5, 0.03971, 0.0], [0.4, 0.04352, 0.0], \
                           [0.3, 0.04501, 0.0], [0.25, 0.04456, 0.0], [0.2, 0.04303, 0.0], [0.15, 0.04009, 0.0], \
                           [0.1, 0.03512, 0.0], [0.075, 0.0315, 0.0], [0.05, 0.02666, 0.0], [0.025, 0.01961, 0.0], \
                           [0.0125, 0.0142, 0.0], [0.005, 0.0089, 0.0], [0.0, 0.0, 0.0], [0.005, -0.0089, 0.0], \
                           [0.0125, -0.0142, 0.0], [0.025, -0.01961, 0.0], [0.05, -0.02666, 0.0], [0.075, -0.0315, 0.0], \
                           [0.1, -0.03512, 0.0], [0.15, -0.04009, 0.0], [0.2, -0.04303, 0.0], [0.25, -0.04456, 0.0], \
                           [0.3, -0.04501, 0.0], [0.4, -0.04352, 0.0], [0.5, -0.03971, 0.0], [0.6, -0.03423, 0.0], \
                           [0.7, -0.02748, 0.0], [0.8, -0.01967, 0.0], [0.9, -0.01086, 0.0], [0.95, -0.00605, 0.0], \
                           [1.0, -0.00095, 0.0]]   
    
    def __init__(self, parent = None):
        super(OGL_Widget, self).__init__(parent)
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0
        self.xTrans = 0
        self.yTrans = 0
        self.lastPos_x = 0.0
        self.lastPos_y = 0.0
        self.width = 0
        self.height = 0
        self.scale = 1.0
        self.clearColor = QtGui.QColor()
        self.setFocusPolicy(QtCore.Qt.ClickFocus)

    def minimumSizeHint(self):
        return QtCore.QSize(50, 50)

    def sizeHint(self):
        return QtCore.QSize(200, 200)

    def setClearColor(self, color):
        self.clearColor = color
        self.updateGL()

    def initializeGL(self):
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_COLOR_MATERIAL)
        GL.glClearColor(0.0, 0.0 , 0.0, 1.0)
    
    def resizeGL(self, w, h):
        self.width = w
        self.height = h
        side = min(w, h)
        GL.glViewport((w - side) / 2, (h - side) / 2, side, side)
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GL.glOrtho(-0.5, +0.5, +0.5, -0.5, 0.0, 15.0)
        GL.glMatrixMode(GL.GL_MODELVIEW)        
        
    def paintGL(self):
        self.qglClearColor(self.clearColor)
        # Clear screen and Z-buffer
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT) 
        
        # Reset transformations
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()
       
        GL.glRotated(self.xRot, 1.0, 0.0, 0.0)
        GL.glRotated(self.yRot, 0.0, 1.0, 0.0)
        GL.glRotated(self.zRot, 0.0, 0.0, 1.0)        

        GL.glTranslatef(self.xTrans, self.yTrans, -1.0)  

        GL.glScale(self.scale,self.scale,1)              
        self.draw()
        
        GL.glFlush()          

    def drawPoints(self, xList, yList, color):
        GL.glColor3f( color[0], color[1], color[2] )
        GL.glPointSize(5)
        GL.glBegin(GL.GL_POINTS)    
        for i in range(0, len(xList)) :
            GL.glVertex3f(xList[i], yList[i], 0.5)              
        GL.glEnd()             
            
    def drawPolygon(self, xList, yList, color):
        GL.glBegin(GL.GL_LINE_STRIP)
        GL.glColor3f( color[0], color[1], color[2] )
        for i in range(0,len(xList)) :
            GL.glVertex3f(xList[i],yList[i],0.5)
        GL.glEnd()
        
        
            
    def draw(self):
        xList = []
        yList = []
        for p in OGL_Widget.coords :
            xList.append(p[0])
            yList.append(p[1])
            if p[0] == 0 : break
        
        s = InterpolatedUnivariateSpline(xList, yList)
        
        s.derivative(2)
        
        xnew = self.xSpline(xList, 1)
        
        ynew = s(xnew)
        
        print xnew
        print ynew
      #  sys.exit()
 
        self.drawPolygon(xList, yList, [1.0, 1.0, 0.0])
        self.drawPoints(xList, yList, [1.0, 1.0, 1.0])

        self.drawPolygon(xnew, ynew, [0.0,  1.0, 0.0])
        self.drawPoints(xnew, ynew, [1.0,  0.0, 0.0])
       
    def xSpline(self, plist, cnt):
        cnt += 1
        
        res = []
        for i in range(1, len(plist)) :
            res.append(plist[i-1])
            dist = absolute(plist[i-1]-plist[i]) / cnt
            j=1
            for j in range(1, cnt) :
                res.append(plist[i-1]-j*dist) 
        res.append(plist[len(plist)-1])
        return res

    def mousePressEvent(self, event):  
        self.lastPos_x = event.pos().x()
        self.lastPos_y = event.pos().y()
                
    def mouseMoveEvent(self, event):
        dx = (event.x() - self.lastPos_x ) 
        dy = (event.y() - self.lastPos_y ) 
        
        self.lastPos_x += dx
        self.lastPos_y += dy

        #Betrachtsfeld = -1 bis 1
        
        #print self.width 
        #print self.height 
        
        self.xTrans += (2*dx / (self.width*1.0)) 
        self.yTrans += (2*dy / (self.height*1.0))

        self.updateGL()


    def keyPressEvent(self, event):
        redraw = False
        offset_rot   = 5
        offset_scale = 0.02
        if event.key() == QtCore.Qt.Key_Right :
            self.yRot += offset_rot
            redraw = True
        elif event.key() == QtCore.Qt.Key_Left :
            self.yRot -= offset_rot
            redraw = True
        elif event.key() == QtCore.Qt.Key_Up :
            self.xRot += offset_rot
            redraw = True
        elif event.key() == QtCore.Qt.Key_Down :
            self.xRot -= offset_rot 
            redraw = True
        elif event.key() == QtCore.Qt.Key_Plus :
            self.scale += offset_scale
            redraw = True
        elif event.key() == QtCore.Qt.Key_Minus :
            self.scale -= offset_scale 
            redraw = True
  
        # Request display update
        if redraw :
            self.updateGL()


class Window(QtGui.QWidget):
    NumRows = 2
    NumColumns = 3

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        grid = QtGui.QGridLayout()
        self.glWidgets = []

        for i in range(Window.NumRows):
            self.glWidgets.append([])
            for j in range(Window.NumColumns):
                self.glWidgets[i].append(None)

        for i in range(Window.NumRows):
            for j in range(Window.NumColumns):
                clearColor = QtGui.QColor()
                clearColor.setHsv(((i * Window.NumColumns) + j) * 255
                                  / (Window.NumRows * Window.NumColumns - 1),
                                  255, 63)

                self.glWidgets[i][j] = OGL_Widget()
                self.glWidgets[i][j].setClearColor(clearColor)
                
                grid.addWidget(self.glWidgets[i][j], i, j)


        self.setLayout(grid)

        self.currentGlWidget = self.glWidgets[0][0]






class Spline(QtGui.QWidget):
    def __init__(self, parent = None):
        super(Spline, self).__init__(parent)

        grid = QtGui.QGridLayout()        
        grid.addLayout(self.createTopOfWidget(),0,1)
        grid.addWidget(self.ogl_widget, 1,1)

        self.setLayout(grid)
        self.setWindowTitle('Airfoil-Widget')   
        self.resize(560,520)              
        #self.setFixedSize(QtCore.QSize(400,400))
        self.show()


    def cubic_spline(self):
        ''' Cubic-spline '''   
        x = np.arange(0, 2*np.pi + np.pi / 4, 2*np.pi / 8)
        y = np.sin(x)
        tck = interpolate.splrep(x,y,s=0)
        xnew = np.arange(0,2*np.pi,np.pi/50)
        ynew = interpolate.splev(xnew,tck,der=0)







if __name__ == '__main__':
    app = QtGui.QApplication(["PyQt OpenGL"])
    widget = Window()
    widget.show()
    app.exec_()  