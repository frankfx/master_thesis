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
from Xtest.Open_GL.profile import Profile
try:
    from OpenGL import GL, GLU
except ImportError:
    app = QtGui.QApplication(sys.argv)
    QtGui.QMessageBox.critical(None, "OpenGL hellogl",
                              "PyOpenGL must be installed to run this example.",
                            QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default,
                            QtGui.QMessageBox.NoButton)
    sys.exit(1)


class ProfileDetectorWidget(Profile):
    def __init__(self,parent = None):
        Profile.__init__(self)
        self.filename = ""
        self.width = 320
        self.height = 320
        self.img_width = -1
        self.img_height = -1
        self.resize(self.width,self.height)
        self.flagDetectProfile = False
        self.setWindowTitle("Rene Test")
        self.pointList = []

    def drawImage(self, filename):
        self.filename = filename
        self.initializeGL()
        self.updateGL()

    def initializeGL(self):
        self.textures = []
        #GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_TEXTURE_2D)
        pixmap = QtGui.QPixmap(self.filename)
        self.textures.append(self.bindTexture(pixmap))
        self.img_width, self.img_height = pixmap.width() , pixmap.height()  
    
    def resizeGL(self, w, h):
        self.width = w
        self.height = h
        GL.glViewport(0,0,w,h) 
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GLU.gluPerspective (144.0, w*1.0/h, 0.001, 10.0)
      
    def getPointList(self):
        return self.pointList
      
    def paintGL(self):
        GL.glClearColor(1,1,1,1)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT) 
        
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()
       
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.textures[0])
        
        if self.flagDetectProfile :
            self.drawDefaultProfile()    
        else :
            self.drawBackgroundImg()
            self.drawDefaultProfile()
            
            

        GL.glFlush()    
        
        
    # ================================================================================================================
    # draw the background
    # ================================================================================================================ 
    def isImageAvailable(self):
        return not self.img_height == 0.0 and not self.img_width == 0.0

    def drawBackgroundImg(self, xsize=1.0):
        if (self.isImageAvailable()) :
            px = xsize
            py = 1.0*self.img_height/self.img_width * px
            GL.glColor3f(1.0, 1.0, 1.0)
            GL.glTranslatef(self.trans_x, self.trans_y,0)
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
        else :
            print "no image"        
            
    # ================================================================================================================
    # default Naca profile
    # ================================================================================================================   
    def drawDefaultProfile(self):
        GL.glTranslatef(-self.trans_x, -self.trans_y,0)
        self.pointList = self.createSym_Naca(1.0, 12.0/100.0)
        GL.glLineWidth(2)
        GL.glColor3f(0.0, 0.0, 0.0)
        GL.glTranslatef(-0.5,0,-0.25)
        GL.glBegin(GL.GL_LINE_STRIP) 
        for p in self.pointList :
            GL.glVertex3f(p[0], p[1], p[2])              
        GL.glEnd()    
        GL.glColor3f(1.0, 0.0, 0.0)
        GL.glPointSize(6)
        GL.glBegin(GL.GL_POINTS) 
        for p in self.pointList :
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
    
    
    # ================================================================================================================
    # profile resizing
    # ================================================================================================================         
    '''
    get the world coordinates from the screen coordinates
    '''
    def fkt_winPosTo3DPos(self, x, y):
        point = [-1,-1,-1]                                      # result point
        modelview  = GL.glGetDoublev(GL.GL_MODELVIEW_MATRIX)    # get the modelview info
        projection = GL.glGetDoublev(GL.GL_PROJECTION_MATRIX)   # get the projection matrix info
        viewport   = GL.glGetIntegerv(GL.GL_VIEWPORT)           # get the viewport info
 
        # in OpenGL y soars (steigt) from bottom (0) to top
        y_new = viewport[3] - y     
 
        # read depth buffer at position (X/Y_new)
        z = GL.glReadPixels(x, y_new, 1, 1, GL.GL_DEPTH_COMPONENT, GL.GL_FLOAT)
        # winz should not be 0!!!
        # error when projection matrix not identity (gluPerspective) 
        point[0], point[1], point[2] = GLU.gluUnProject(x, y_new, z, modelview, projection, viewport)                         
        
        print "(",x,",",y,") = " , "(",point[0],",",point[1],",",point[2],")"
        return point

    '''
    get the the screen coordinates from the world coordinates 
    '''
    def fkt_3DPosToWinPos(self, x, y, z):
        point = [-1,-1,-1]                                      # result point
        modelview  = GL.glGetDoublev(GL.GL_MODELVIEW_MATRIX)    # get the modelview info
        projection = GL.glGetDoublev(GL.GL_PROJECTION_MATRIX)   # get the projection matrix info
        viewport   = GL.glGetIntegerv(GL.GL_VIEWPORT)           # get the viewport info

        # in OpenGL y soars (steigt) from bottom (0) to top
        y_new = y 
 
        point[0], point[1], point[2]  = GLU.gluProject(x, y_new, z, modelview, projection, viewport)                         
        point[1] = self.height -point[1]
        
        print "(",x,",",y,",",z,") = " , "(",point[0],",",point[1],")"
        return point        

    def __idxOfSelectedPoint(self, point, plist):
        for i in range(0, len(plist)) :
            if plist[i] == point :
                return i
        return -1
                
    # ================================================================================================================
    # mouse event
    # ================================================================================================================       
    def mousePressEvent(self, event):
        p = self.fkt_winPosTo3DPos(event.pos().x(), event.pos().y())
        idx = self.__idxOfSelectedPoint(p, self.pointList) 
        if idx >= 0 :
            print "point erwischt"
        else:
            print "p = " , p
            print "x, y = " , event.pos().x(), event.pos().y() 
            Profile.mousePressEvent(self, event)
        
if __name__ == '__main__':
    app = QtGui.QApplication(["PyQt OpenGL"])
    widget = ProfileDetectorWidget()
    widget.show()
    app.exec_()    