'''
Created on Jul 30, 2014

@author: fran_re
'''
import sys
from PySide import QtOpenGL, QtGui, QtCore
from cpacsHandler import CPACS_Handler
from config import Config
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
    def __init__(self, tixi):
        self.tixi = tixi
        self.scale = 1.0

    def init(self):
        # GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_COLOR_MATERIAL)
        GL.glClearColor(1.0, 1.0 , 1.0, 1.0)        
    
    def resize(self, w, h):
        GL.glViewport(0,0,w,h) #if w <= h else GL.glViewport(0,0,h,h) 
                                   
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        
      #  GLU.gluPerspective (64.0, w*1.0/h, 0.0, 10.0)
        
    def display(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT) 
        
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()
       
        #GL.glTranslatef(-0.51,0,-1)
        
        self.drawProfile()

        GL.glFlush()                # clean puffer, execute all puffered commands


    def drawProfile(self):
        vecX = self.tixi.getVectorX('NACA0009')
        vecY = self.tixi.getVectorY('NACA0009')
        vecZ = self.tixi.getVectorZ('NACA0009')
        
        GL.glColor3f(0, 0, 1)
        GL.glScale(self.scale, self.scale, 1)
        GL.glTranslatef(-self.norm_vec_list(vecX),0,-1)
        
        GL.glBegin(GL.GL_LINE_LOOP)
        for i in range (0, len(vecX)) :
            GL.glVertex3f(vecX[i], vecZ[i], vecY[i])
        GL.glEnd()      
        
    def norm_vec_list(self, vlist):
        '''set points to center (0,0)'''
        vlist = list(vlist)
        mx = max(vlist)
        mn = min(vlist)
        dist = mx - mn
        mid = dist / 2.0
        shift = mx - mid

        return shift       

class ProfileDetectorWidget(QtOpenGL.QGLWidget):
    def __init__(self, parent = None):
        super(ProfileDetectorWidget, self).__init__(parent)
        self.resize(320,320)
        self.setWindowTitle("Rene Test")
        #self.setFixedSize(QtCore.QSize(400,400))
        tixi = CPACS_Handler()
        tixi.loadFile(Config.path_cpacs_A320_Fuse, Config.path_cpacs_21_schema)
        self.renderer = Renderer(tixi)    
    
    def initializeGL(self):
        self.renderer.init()
    
    def resizeGL(self, w, h):
        self.renderer.resize(w, h)
 
    def paintGL(self):
        self.renderer.display()

    def keyPressEvent(self, event):
        redraw = False
        offsetScl = 0.1
        if event.modifiers() == QtCore.Qt.ControlModifier :
            offsetScl = -1 *offsetScl

        if event.key() == QtCore.Qt.Key_1:
            self.renderer.scale += offsetScl
            redraw = True
        elif event.key() == QtCore.Qt.Key_0:
            self.renderer.xRot = 0.0
            self.renderer.yRot = 0.0
            self.renderer.zRot = 0.0
            self.renderer.scale = 1.0
            redraw = True
        if redraw :
            self.updateGL()
    
if __name__ == '__main__':
    app = QtGui.QApplication(["PyQt OpenGL"])
    widget = ProfileDetectorWidget()
    widget.show()
    app.exec_()    