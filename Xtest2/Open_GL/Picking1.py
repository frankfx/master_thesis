'''
Created on Jul 30, 2014

@author: fran_re
'''

import sys
from PySide import QtOpenGL, QtGui
try:
    from OpenGL import GL,GLU, GLUT
except ImportError:
    app = QtGui.QApplication(sys.argv)
    QtGui.QMessageBox.critical(None, "OpenGL hellogl",
                            "PyOpenGL must be installed to run this example.",
                            QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default,
                            QtGui.QMessageBox.NoButton)
    sys.exit(1)

class Renderer():

    def init(self):
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glShadeModel(GL.GL_FLAT)    

    def resize(self, w, h):
        GL.glViewport(0,0,w,h) 
        GL.glMatrixMode(GL.GL_PROJECTION);
        GL.glLoadIdentity();
        GLU.gluPerspective (65.0, w/h, 0.1, 10.0); 
        
    def display(self):
        GL.glClearColor (0.0, 0.0, 0.0, 0.0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        self.drawScene ()
        self.selectObjects ()
        GL.glFlush()

    def drawScene (self):
        GL.glMatrixMode (GL.GL_PROJECTION)
        GL.glLoadIdentity ()
        GLU.gluPerspective (40.0, 4.0/3.0, 1.0, 100.0)   
        
        GL.glMatrixMode (GL.GL_MODELVIEW)
        GL.glLoadIdentity ();
        GLU.gluLookAt (7.5, 7.5, 12.5, 2.5, 2.5, -5.0, 0.0, 1.0, 0.0)
        GL.glColor3f (0.0, 1.0, 0.0)   #  green triangle      
        self.drawTriangle (2.0, 2.0, 3.0, 2.0, 2.5, 3.0, -5.0)
        GL.glColor3f (1.0, 0.0, 0.0);   #  red triangle        
        self.drawTriangle (2.0, 7.0, 3.0, 7.0, 2.5, 8.0, -5.0)
        GL.glColor3f (1.0, 1.0, 0.0)   #  yellow triangles    
        self.drawTriangle (2.0, 2.0, 3.0, 2.0, 2.5, 3.0, 0.0)
        self.drawTriangle (2.0, 2.0, 3.0, 2.0, 2.5, 3.0, -10.0)
        self.drawViewVolume (0.0, 5.0, 0.0, 5.0, 0.0, 10.0)

    def drawTriangle(self, x1, y1, x2, y2, x3, y3, z):
        GL.glBegin(GL.GL_TRIANGLES)
        GL.glVertex3f (x1, y1, z)
        GL.glVertex3f (x2, y2, z)
        GL.glVertex3f (x3, y3, z)
        GL.glEnd()

    def drawViewVolume(self, x1, x2, y1, y2, z1, z2):
        GL.glColor3f(1.0, 1.0, 1.0)
        GL.glBegin(GL.GL_LINE_LOOP)
        GL.glVertex3f (x1, y1, -z1)
        GL.glVertex3f (x2, y1, -z1)
        GL.glVertex3f (x2, y2, -z1)
        GL.glVertex3f (x1, y2, -z1)
        GL.glEnd()
    
        GL.glBegin (GL.GL_LINE_LOOP)
        GL.glVertex3f (x1, y1, -z2)
        GL.glVertex3f (x2, y1, -z2)
        GL.glVertex3f (x2, y2, -z2)
        GL.glVertex3f (x1, y2, -z2)
        GL.glEnd ()
        
        GL.glBegin (GL.GL_LINES)
        GL.glVertex3f (x1, y1, -z1)
        GL.glVertex3f (x1, y1, -z2)
        GL.glVertex3f (x1, y2, -z1)
        GL.glVertex3f (x1, y2, -z2)
        GL.glVertex3f (x2, y1, -z1)
        GL.glVertex3f (x2, y1, -z2)
        GL.glVertex3f (x2, y2, -z1)
        GL.glVertex3f (x2, y2, -z2)
        GL.glEnd ()
    

    
    
    def processHits(self, hits, buffer):
       
        print "hits =" + str(hits)

        ptr = buffer;
        for i in range(0, hits, 1) : # for each hit
            names = ptr
            print (" number of names for hit = " + names)
            ptr+=1
            print("  z1 is " + str(ptr/0x7fffffff)) 
            ptr+=1
            print(" z2 is " + str(ptr/0x7fffffff)) 
            ptr+=1
            print ("   the name is ");
            for j in range(0, names, 1) :    #  for each name 
                print (ptr) 
                ptr+=1
    
    
    def selectObjects(self):
        
        selectBuf = GL.glSelectBuffer(512)
        
        GL.glInitNames()
        GL.glPushName(0)
        
        GL.glPushMatrix()
        GL.glMatrixMode (GL.GL_PROJECTION)
        GL.glLoadIdentity ()
        GL.glOrtho (0.0, 5.0, 0.0, 5.0, 0.0, 10.0)
        GL.glMatrixMode (GL.GL_MODELVIEW)
        GL.glLoadIdentity ()
        GL.glLoadName(1)
        self.drawTriangle (2.0, 2.0, 3.0, 2.0, 2.5, 3.0, -5.0)
        GL.glLoadName(2)
        self.drawTriangle (2.0, 7.0, 3.0, 7.0, 2.5, 8.0, -5.0)
        GL.glLoadName(3)
        self.drawTriangle (2.0, 2.0, 3.0, 2.0, 2.5, 3.0, 0.0)
        self.drawTriangle (2.0, 2.0, 3.0, 2.0, 2.5, 3.0, -10.0)
        GL.glPopMatrix ()
        GL.glFlush ()
    
        hits = GL.glRenderMode(GL.GL_RENDER)
        self.processHits(hits,selectBuf)
        

class MyWidget(QtOpenGL.QGLWidget):
    def __init__(self, parent = None):
        super(MyWidget, self).__init__(parent)
   
        self.resize(320,320)
        self.setWindowTitle("Rene Test")
        self.renderer = Renderer()

    
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