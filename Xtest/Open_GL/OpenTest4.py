'''
Created on Jul 29, 2014

@author: fran_re
'''
import sys
from PySide import QtCore, QtGui, QtOpenGL
#from pylab import *

try:
    from OpenGL import GL,GLU, GLUT
except ImportError:
    app = QtGui.QApplication(sys.argv)
    QtGui.QMessageBox.critical(None, "OpenGL hellogl",
                            "PyOpenGL must be installed to run this example.",
                            QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default,
                            QtGui.QMessageBox.NoButton)
    sys.exit(1)

class ShapeNames:
    dict = {0:"dreieck", 1:"viereck", 2:"stern"}
       
    def getValue(self, key):
        return self.dict.get(key)
    
    def getKey(self, value):
        try:
            return self.dict.keys()[self.dict.values().index(value)]
        except ValueError:
            return None         

        
class Renderer():
    def init(self):
        ()
        
    def resize(self, w, h):
        GL.glViewport(0,0,w,h) 
        GL.glMatrixMode(GL.GL_PROJECTION);
        GL.glLoadIdentity();
        GLU.gluPerspective (65.0, w/h, 0.1, 10.0);    
        
    def display(self):
       
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        GL.glLoadIdentity()
        GL.glTranslatef(0,0,-6)
        
        GL.glInitNames()
        GL.glPushName(0)

        GL.glColor3f(1.0, 0.0, 0.0)
        GL.glLoadName(ShapeNames().getKey("dreieck"))
        GL.glBegin(GL.GL_TRIANGLES)
        GL.glVertex3f(-0.5, 1, 0)
        GL.glVertex3f(0.5, 1, 0)
        GL.glVertex3f(0, 2, 0)
        GL.glEnd()

        GL.glColor3f(0,1,0);
        GL.glLoadName(ShapeNames().getKey("viereck"))
        GL.glBegin(GL.GL_QUADS)
        GL.glVertex3f(-1,0,0)
        GL.glVertex3f(-2,0,0)
        GL.glVertex3f(-2,-1,0)
        GL.glVertex3f(-1,-1,0)
        GL.glEnd()

        GL.glColor3f(1,1,0)
        GL.glLoadName(ShapeNames().getKey("stern"))
        GL.glBegin(GL.GL_TRIANGLES)
        GL.glVertex3f(1,0,0)
        GL.glVertex3f(2,0,0)
        GL.glVertex3f(1.5,-1,0)
        GL.glVertex3f(1,-0.65,0)
        GL.glVertex3f(2,-0.65,0)
        GL.glVertex3f(1.5,0.35,0)
        GL.glEnd()  
        
        GL.glFlush()      


    def drawTriangle(self):         
        GL.glBegin(GL.GL_TRIANGLES);
        GL.glVertex3f(1,0,0);
        GL.glVertex3f(0,1,0);
        GL.glVertex3f(0,0,1);
        GL.glEnd;


class WfWidget(QtOpenGL.QGLWidget):
    def __init__(self, parent = None):
        super(WfWidget, self).__init__(parent)
        self.renderer = Renderer() 

    def initializeGL(self):
        GLUT.glutInit()

    def resizeGL(self, w, h):
        self.renderer.resize(w,h)

    def paintGL(self):
        self.renderer.display()

    def selection(self):
        
        self.viewport   = GL.glGetIntegerv(GL.GL_VIEWPORT)
        self.puffer     = GL.glSelectBuffer(256)
        
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glRenderMode(GL.GL_SELECT)
        GL.glPushMatrix()
        GL.glLoadIdentity()
              
        GLU.gluPickMatrix(self.mousePressPos.x(), self.viewport[3]-self.mousePressPos.y(), 1.0, 1.0, self.viewport)
        GLU.gluPerspective(60.0, self.viewport[2]/self.viewport[3], 1, 256)
        GL.glMatrixMode(GL.GL_MODELVIEW) 
        
        self.paintGL()
        
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glPopMatrix()
        
        treffer = GL.glRenderMode(GL.GL_RENDER)
        
        getroffen = sys.maxint*3                  #Hoechsten moeglichen Wert annehmen
        z_wert   = sys.maxint*3

        for i in range(0, len(treffer)):
            if self.puffer[i*4+1] < z_wert :
                getroffen   = self.puffer[i*4+3]
                z_wert      = self.puffer[i*4+1]
            
        if getroffen == sys.maxint:
            result = -1
        else:
            result = getroffen
                 
        return result

    def mousePressEvent(self, event):
        self.mousePressPos = QtCore.QPointF(event.pos())

        res = ShapeNames().getValue(self.selection())
        if res != None:       
            print "Sie haben auf " + res + " geklickt!"
        else:
            print "Nix geklickt"



if __name__ == '__main__':
    app = QtGui.QApplication(["Winfred's PyQt OpenGL"])
    widget = WfWidget()
    widget.show()
    app.exec_()