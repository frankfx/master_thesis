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
import utility
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
        self.img_width = -1
        self.img_height = -1
        self.scaleImg = 1
        self.scale = 2
        self.flag_detected = False
        self.resize(self.width,self.height)
        self.setWindowTitle("Rene Test")

    def initializeGL(self):
        self.textures = []
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

    def paintGL(self):
        GL.glClearColor(1,1,1,1)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT) 
        
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()
       
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.textures[0])
        
        if self.filename != "" : 
            GL.glTranslatef(self.trans_x, self.trans_y, 0)
            GL.glScalef(self.scaleImg, self.scaleImg,1)
            self.drawBackgroundImg()
            GL.glTranslatef(-self.trans_x, -self.trans_y, 0)
        if self.flag_detected:
            GL.glScalef(self.scale, self.scale,1)
            self.drawProfile()

        GL.glFlush()    

    # ================================================================================================================
    # profile drawing
    # ================================================================================================================ 
    def drawProfile(self):
        if self.getPointList() == [] :
            self.createDefaultProfile()

        trX, trY = self.norm_vec_list(self.getPointList())
        GL.glTranslatef(-trX, trY, 0) 

        # draw profile by pointList        
        GL.glLineWidth(2)
        GL.glColor3f(0.0, 0.0, 0.0)
        GL.glBegin(GL.GL_LINE_STRIP) 
        for p in self.getPointList() :
            GL.glVertex3f(p[0], p[1], p[2])              
        GL.glEnd()    
        
        # draw profile points
        GL.glColor3f(1.0, 0.0, 0.0)
        GL.glPointSize(10)
        GL.glBegin(GL.GL_POINTS) 
        for p in self.getPointList() :
            GL.glVertex3f(p[0], p[1], p[2])              
        GL.glEnd()         
        
    # ================================================================================================================
    # draw the background
    # ================================================================================================================ 
    def setFileName(self, filename):
        self.filename = filename
        self.initializeGL()    
    
    def isImageAvailable(self):
        return not self.img_height == 0.0 and not self.img_width == 0.0

    def drawBackgroundImg(self, xsize=1.0):
        if (self.isImageAvailable()) :
            px = xsize
            py = 1.0*self.img_height/self.img_width * px
            GL.glColor3f(1.0, 1.0, 1.0)
            # GL.glTranslatef(self.trans_x, self.trans_y,0)
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

    # ================================================================================================================
    # default Naca 0009 profile
    # ================================================================================================================   
    def createDefaultProfile(self):
        self.setPointList([[1.0, 0.00095, 0.0], [0.95, 0.00605, 0.0], [0.9, 0.01086, 0.0], [0.8, 0.01967, 0.0], \
                           [0.7, 0.02748, 0.0], [0.6, 0.03423, 0.0], [0.5, 0.03971, 0.0], [0.4, 0.04352, 0.0], \
                           [0.3, 0.04501, 0.0], [0.25, 0.04456, 0.0], [0.2, 0.04303, 0.0], [0.15, 0.04009, 0.0], \
                           [0.1, 0.03512, 0.0], [0.075, 0.0315, 0.0], [0.05, 0.02666, 0.0], [0.025, 0.01961, 0.0], \
                           [0.0125, 0.0142, 0.0], [0.005, 0.0089, 0.0], [0.0, 0.0, 0.0], [0.005, -0.0089, 0.0], \
                           [0.0125, -0.0142, 0.0], [0.025, -0.01961, 0.0], [0.05, -0.02666, 0.0], [0.075, -0.0315, 0.0], \
                           [0.1, -0.03512, 0.0], [0.15, -0.04009, 0.0], [0.2, -0.04303, 0.0], [0.25, -0.04456, 0.0], \
                           [0.3, -0.04501, 0.0], [0.4, -0.04352, 0.0], [0.5, -0.03971, 0.0], [0.6, -0.03423, 0.0], \
                           [0.7, -0.02748, 0.0], [0.8, -0.01967, 0.0], [0.9, -0.01086, 0.0], [0.95, -0.00605, 0.0], \
                           [1.0, -0.00095, 0.0]])
    
    # ================================================================================================================
    # opengl vs window transformation
    # ================================================================================================================         
    '''
    get the world coordinates from the screen coordinates
    '''
    def __winPosTo3DPos(self, x, y):
        point = [None, None, None]                                      # result point
        modelview  = GL.glGetDoublev(GL.GL_MODELVIEW_MATRIX)    # get the modelview info
        projection = GL.glGetDoublev(GL.GL_PROJECTION_MATRIX)   # get the projection matrix info
        viewport   = GL.glGetIntegerv(GL.GL_VIEWPORT)           # get the viewport info
 
        # in OpenGL y soars (steigt) from bottom (0) to top
        y_new = viewport[3] - y     
 
        # read depth buffer at position (X/Y_new)
        z = GL.glReadPixels(x, y_new, 1, 1, GL.GL_DEPTH_COMPONENT, GL.GL_FLOAT)
        # z should not be 0!!!
        # error when projection matrix not identity (gluPerspective) 
        point[0], point[1], point[2] = GLU.gluUnProject(x, y_new, z, modelview, projection, viewport)                         
        point[2] = 0
        return point

    '''
    get the the screen coordinates from the world coordinates 
    '''
    def fkt_3DPosToWinPos(self, x, y, z):
        point = [None, None, None]                                      # result point
        modelview  = GL.glGetDoublev(GL.GL_MODELVIEW_MATRIX)    # get the modelview info
        projection = GL.glGetDoublev(GL.GL_PROJECTION_MATRIX)   # get the projection matrix info
        viewport   = GL.glGetIntegerv(GL.GL_VIEWPORT)           # get the viewport info

        # in OpenGL y soars (steigt) from bottom (0) to top
        y_new = y 
 
        point[0], point[1], point[2]  = GLU.gluProject(x, y_new, z, modelview, projection, viewport)                         
        point[1] = self.height -point[1]
        return point        
   
    # ================================================================================================================
    # profile detecting
    # ================================================================================================================  
    def detectProfile(self):
        self.flag_detected = True
        if False :
            ()
        else :
            QtGui.QMessageBox.about(self, "error", "create default profile" )
        
        print "do something for detection" 

    # ================================================================================================================
    # helper point selection
    # ================================================================================================================ 
    def __roundPnt(self, p):
        return [round(p[0],2), round(p[1],2), round(p[2],2)]

    def __isInRange(self, x, xfrom, xto):
        return x >= xfrom and x <= xto

    def __getIdxOfSelectedPoint(self, point, plist, radius=0.01):
        point = self.__roundPnt(point)
        for i in range(0, len(plist)) :
            p = self.__roundPnt(plist[i])
            if self.__isInRange(point[0], p[0]-radius, p[0]+radius) and \
               self.__isInRange(point[1], p[1]-radius, p[1]+radius) :
                return i
        return -1
    
    # ================================================================================================================
    # mouse events and others
    # ================================================================================================================       
    def cancelWidget(self):
        self.setPointList([])
        self.flag_detected = False
        self.setFileName("")    
    
    def mousePressEvent(self, event):
        self.updateGL() # important for __winPosTo3DPos
        self.__selectedPoint    = self.__winPosTo3DPos(event.pos().x(), event.pos().y())
        self.__idxSelectedPoint = self.__getIdxOfSelectedPoint(self.__selectedPoint, self.getPointList()) 
        if self.__idxSelectedPoint < 0 :
            if(event.button() == QtCore.Qt.RightButton) :
                ()
            else : 
                Profile.mousePressEvent(self, event)
        
    def mouseMoveEvent(self, event):
        if self.__idxSelectedPoint >= 0 :
            p = self.__winPosTo3DPos(event.pos().x(), event.pos().y())
            self.setPointListAtIdx(self.__idxSelectedPoint, p)
            self.updateGL()
        else:
            Profile.mouseMoveEvent(self, event)
        
    def addPoint(self):
        idx = utility.computeIdxOfPointWithMinDistance(self.__selectedPoint, self.getPointList(), 1)[0]
        if idx == None :
            self.insertToPointList(0, self.__selectedPoint)
        else :
            idx_l = len(self.getPointList()) - 1 if idx == 0 else idx - 1
            idx_r = 0 if idx == len(self.getPointList()) - 1 else idx + 1
            
            dist_l = utility.getDistanceBtwPoints(self.__selectedPoint, self.getPointList()[idx_l])
            dist_r = utility.getDistanceBtwPoints(self.__selectedPoint, self.getPointList()[idx_r])
            
            if dist_l < dist_r :
                self.insertToPointList(idx, self.__selectedPoint)
            else : self.insertToPointList(idx_r, self.__selectedPoint)
        
        #self.insertToPointList(idx, self.__selectedPoint) if dist_l < dist_r else self.insertToPointList(idx_r, self.__selectedPoint)
        self.updateGL()

    def removePoint(self):
        if self.__idxSelectedPoint >= 0 :
            self.removeFromPointList(self.__idxSelectedPoint)
            self.updateGL()

    def contextMenuEvent(self, event):
        self.addAct = QtGui.QAction("add", self)
        self.delAct = QtGui.QAction("delete", self)
        self.addAct.triggered.connect(self.addPoint) 
        self.delAct.triggered.connect(self.removePoint)
        
        self.menu = QtGui.QMenu(self)
        self.menuwth = QtGui.QMenu(self)

        self.menu.addAction(self.delAct)
        self.menu.addAction(self.addAct)        
        self.menuwth.addAction(self.addAct)

        # if point is selected show menu with delete else show menu without delete
        if self.__idxSelectedPoint >= 0 :
            self.menu.exec_(event.globalPos())
        else :
            self.menuwth.exec_(event.globalPos())
        
        
if __name__ == '__main__':
    app = QtGui.QApplication(["PyQt OpenGL"])
    widget = ProfileDetectorWidget()
    widget.show()
    app.exec_()    