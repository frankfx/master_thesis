'''
Created on Aug 22, 2014

@author: rene
'''

'''
Created on Jul 30, 2014

@author: fran_re
'''
import sys
import math
from PySide import QtOpenGL, QtGui, QtCore
#from cpacsHandler import CPACS_Handler
from Xtest.Open_GL.configuration.config import Config
try:
    from OpenGL import GL, GLU
except ImportError:
    app = QtGui.QApplication(sys.argv)
    QtGui.QMessageBox.critical(None, "OpenGL hellogl",
                              "PyOpenGL must be installed to run this example.",
                            QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default,
                            QtGui.QMessageBox.NoButton)
    sys.exit(1)


class ProfileDetectorWidget(QtOpenGL.QGLWidget):
    def __init__(self,parent = None):
        super(ProfileDetectorWidget, self).__init__(parent)
        self.filename = ""
        self.img_width = -1
        self.img_height = -1
        self.resize(320,320)
        self.flagDrawDefaultProfile = False
        self.setWindowTitle("Rene Test")
        self.pointList = []

    def drawImage(self, filename):
        self.filename = filename
        self.initializeGL()
        self.updateGL()

    def initializeGL(self):
       # GL.glEnable(GL.GL_DEPTH_TEST)
        #GL.glEnable(GL.GL_CULL_FACE)
        GL.glEnable(GL.GL_TEXTURE_2D)
        self.textures = []
        pixmap = QtGui.QPixmap(self.filename)
        self.textures.append(self.bindTexture(pixmap))
        self.img_width, self.img_height = pixmap.width() , pixmap.height()  
    
    def resizeGL(self, w, h):
        GL.glViewport(0,0,w,h) 
                                   
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        
        GLU.gluPerspective (144.0, w*1.0/h, 0.0, 10.0)
      
    def getPointList(self):
        return self.pointList
      
    def paintGL(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT) 
        
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()
       
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.textures[0])
        
        if self.flagDrawDefaultProfile :
            self.drawProfile()    
        else :
            self.drawRectangle()

        GL.glFlush()    

    def isImageAvailable(self):
        return not self.img_height == 0.0 and not self.img_width == 0.0

    def drawRectangle(self, xsize=1.0):
        if (self.isImageAvailable()) :
            px = xsize
            py = 1.0*self.img_height/self.img_width * px
            GL.glColor3f(1.0, 1.0, 1.0)
            GL.glBegin(GL.GL_QUADS)
            GL.glTexCoord2f(0,0)
            GL.glVertex3f(-px, -py, -0.5)
            GL.glTexCoord2f(1, 0)
            GL.glVertex3f( px, -py, -0.5)
            GL.glTexCoord2f(1, 1)
            GL.glVertex3f( px,  py, -0.5)
            GL.glTexCoord2f(0,  1)
            GL.glVertex3f(-px,  py, -0.5)
            GL.glEnd()         

    
    def drawProfile(self):
        self.pointList = self.createSym_Naca(1.0, 12.0/100.0)
        plist = self.getPointList()
        GL.glTranslatef(-0.5,0,-0.25)
        GL.glBegin(GL.GL_LINE_STRIP) 
        for p in plist :
            GL.glVertex3f(p[0], p[1], p[2])              
        GL.glEnd()        
    

    def createSym_Naca(self, length, thickness, pcnt=10):
        res_top = []
        res_bot = []
    
        c = length
        t = thickness
        plist = self.__createXcoords(c, pcnt)
    
        for x in plist:
            y = self.__computeY_t(x, c, t) 
            res_top.append([x,  y, 0])
            res_bot.append([x, -y, 0])
        
        res_bot.reverse()    
        return res_bot + res_top[1:]
  
    def __createXcoords(self, dist=1.0, point_cnt=35):
        interval = dist/ point_cnt
        
        res = [0]
        for i in range(0, point_cnt):
            p = round(res[i] + interval, 3)
            if p < dist : 
                res.append(p)
            elif p == dist : 
                res.append(p)
                return res
            else :
                break
        res.append(dist)
        return res               
    
    def __computeY_t(self, x, c, t):
        tmp = -0.1036 if (x/c) == 1 else -0.1015
        y = t/0.2 * c * math.fabs( ( 0.2969  * math.sqrt(x/c)   +
                        (-0.1260) * (x/c)            +
                        (-0.3516) * math.pow(x/c, 2) +
                        ( 0.2843) * math.pow(x/c, 3) +
                        (tmp)     * math.pow(x/c, 4)) )        
        return y  
    
if __name__ == '__main__':
    app = QtGui.QApplication(["PyQt OpenGL"])
    widget = ProfileDetectorWidget()
    widget.show()
    app.exec_()    