'''
Created on Jul 30, 2014

@author: fran_re
'''
import sys
from PySide import QtOpenGL, QtGui
from OpenGL import *
try:
    from OpenGL import GL
except ImportError:
    app = QtGui.QApplication(sys.argv)
    QtGui.QMessageBox.critical(None, "OpenGL hellogl",
                              "PyOpenGL must be installed to run this example.",
                            QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default,
                            QtGui.QMessageBox.NoButton)
    sys.exit(1)


class Renderer():
    def init(self):
        ()
    
    def resize(self, w, h):
        GL.glViewport(0,0,w,h)      # describes current viewer window - first two params are for the pos of left bottom edge
                                    # glViewport gibt Transformation von Geraetekoordinaten auf Fensterkoordinaten an
                                    # Geraetekoordinaten bilden Bereich eines Ausgabemediums (viewport) auf Koordinatenspanne -1..1 auf jeder Achse ab.
                                    # Wenn (xnd, ynd) normalisierte Geraetekoordinaten sind, dann werden die Fensterkoordinaten (xw, yw) wie folgt ermittelt
                                    # xw = (xnd + 1)(width / 2) + x
                                    # yw = (ynd + 1)(height / 2) + y
        GL.glMatrixMode(GL.GL_PROJECTION);
        GL.glLoadIdentity();
    def display(self):
        GL.glClearColor(0.0, 0.0, 0.0, 0.0) # Legt die Farbe fest, welche ein Farbpuffer nach seiner Leerung mit glClear enthaelt. 
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)  # Leert die im Parameter festgelegten Buffer, indem sie mit einen Leerwert gefuellt werden. 
        GL.glOrtho(-1, 1, -1, 1, -1, 1)     # aktiviert einen orthogonalen 2D-Rendermodus - glOrtho(left, right, bottom, top, znear, zfar)
                                            # schaltet OpenGL in einen 2D-Modus, wo die Z-Koordiante keine Rolle mehr im Bezug auf die Groesse eines Objektes hat 
                                            # (weit entfernte Objekte (mit hoher Z-Koordinate) werden genau so gross gezeichnet, wie nahe.)
                                            # Damit dient die Z-Koordiante nur noch zur "Anordnung" von Vorder- und Hintergruenden auf der 2D-Zeichenflaeche. 
        GL.glLoadIdentity()                   # Ersetzt die aktuelle Matrix durch die Einheitsmatrix
        GL.glColor3f(1, 1, 1)               # sets current color
        self.drawTriangle()
        
        GL.glColor3f(0, 0, 1)
        GL.glScalef(0.5, 0.5, 0.0)
        self.drawTriangle()

        GL.glColor3f(1.0, 0.0, 0.0);
        GL.glRotatef(45.0, 0.0, 0.0, 1.0); #rotate 45 degrees
        self.drawTriangle();

        GL.glColor3f(0.0, 1.0, 0.0);
        GL.glTranslatef(0.5, 0.5, 0.0);    # translate
        self.drawTriangle();

        GL.glFlush()                # clean puffer, execute all puffered commands

    def drawTriangle(self):
        GL.glBegin(GL.GL_TRIANGLES)
        GL.glVertex2f(-0.5, -0.5)   # vertex on the left
        GL.glVertex2f( 0.5, -0.5)   # vertex on the right
        GL.glVertex2f( 0.0,  0.5)   # vertex at the top of the triangle
        GL.glEnd()
        

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