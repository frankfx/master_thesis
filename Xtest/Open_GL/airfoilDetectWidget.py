'''
Created on Aug 22, 2014

@author: rene
'''
from Xtest.Open_GL.profileWidget import ProfileWidget
from Xtest.Open_GL.airfoilWidget import AirfoilWidget
from profile import Profile

'''
Created on Jul 30, 2014

@author: fran_re
'''
import sys
import utility
from PySide import QtOpenGL, QtGui, QtCore
from Xtest.Open_GL.airfoil import Airfoil
try:
    from OpenGL import GL, GLU
except ImportError:
    app = QtGui.QApplication(sys.argv)
    QtGui.QMessageBox.critical(None, "OpenGL hellogl",
                              "PyOpenGL must be installed to run this example.",
                            QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default,
                            QtGui.QMessageBox.NoButton)
    sys.exit(1)


class AirfoilDetectWidget(QtGui.QWidget): 
    def __init__(self, ogl_widget, parent = None):
        super(AirfoilDetectWidget, self).__init__(parent)
        
        label1 = QtGui.QLabel("Name")
        self.text1Name = QtGui.QLineEdit()
        self.butCreate = QtGui.QPushButton("create")
        self.butDetect = QtGui.QPushButton("detect")
        self.butCancel = QtGui.QPushButton("cancel")
        self.butDelPnt = QtGui.QPushButton("reduce")
        self.checkCenter = QtGui.QCheckBox("center")

        label2 = QtGui.QLabel("Image size")
        self.spin_Img_zoom = QtGui.QSpinBox()
        self.spin_Img_zoom.setRange(1, 100)
        self.spin_Img_zoom.setSingleStep(5)
        self.spin_Img_zoom.setSuffix('%')
        self.spin_Img_zoom.setValue(50)

        label3 = QtGui.QLabel("Airfoil size")
        self.spin_zoom = QtGui.QSpinBox()
        self.spin_zoom.setRange(1, 100)
        self.spin_zoom.setSingleStep(5)
        self.spin_zoom.setSuffix('%')
        self.spin_zoom.setValue(50)

        self.ogl_widget          = ogl_widget
        self.ogl_detector_widget = AirfoilDetectOglWidget()
        #self.ogl_widget.setFixedSize(200,200)
        
        # space between menu and widgets
        space = QtGui.QSpacerItem(0,10)
        grid = QtGui.QGridLayout()
        grid.addItem(space)
        grid.addWidget(label2,                          1,1)
        grid.addWidget(self.spin_Img_zoom,              1,2)
        grid.addWidget(label3,                          1,3)
        grid.addWidget(self.spin_zoom,                  1,4)
        grid.addWidget(self.butDelPnt,                  1,5)
        grid.addWidget(self.checkCenter,                1,6)
        grid.addWidget(self.ogl_detector_widget,    2,1,1,6)
        grid.addWidget(label1,                       3,1)
        grid.addWidget(self.text1Name,               3,2)
        grid.addWidget(self.butCreate,               3,3)
        grid.addWidget(self.butDetect,               3,4)
        grid.addWidget(self.butCancel,               3,5)
        
        self.butCreate.clicked.connect(self.fireButtonCreate)
        self.butDetect.clicked.connect(self.fireButtonDetect)
        self.butDelPnt.clicked.connect(self.fireButtonReduce)
        self.butCancel.clicked.connect(self.fireButtonClose)
        
        self.spin_Img_zoom.valueChanged.connect(self.fireSetScaleImg)
        self.spin_zoom.valueChanged.connect(self.fireSetScale)
        self.checkCenter.toggled.connect(self.fireSetToCenter)
        
        self.createActions()
        self.createMenus()
        
        self.setLayout(grid) 
        self.resize(420,320)
        
    def fireSetToCenter(self, value):
        self.ogl_detector_widget.flag_setCenter = value  
        self.ogl_detector_widget.updateGL() 
        
    def fireButtonReduce(self):
        plist = self.ogl_detector_widget.profile.getPointList()
        if plist == None :
            return

        for i in range(1, len(plist)/2) : 
            self.ogl_detector_widget.profile.removeFromPointList(i)
        self.ogl_detector_widget.updateGL()
    
    def fireSetScaleImg(self):
        self.ogl_detector_widget.scaleImg = float(self.spin_Img_zoom.value()) /50
        self.ogl_detector_widget.updateGL()

    def fireSetScale(self):
        self.ogl_detector_widget.scale = float(self.spin_zoom.value()) /25
        self.ogl_detector_widget.updateGL()
    
    def fireButtonCreate(self):
        name = self.text1Name.text() if self.text1Name.text() != "" else "untitled"
        self.ogl_widget.profile.setName(name)
        plist = []
        for p in self.ogl_detector_widget.profile.getPointList():
            plist.append([p[0], p[2], p[1]])
        self.ogl_widget.profile.setPointList(plist)
        self.ogl_widget.profile.updateAll()
        self.ogl_widget.updateGL()

    def fireButtonDetect(self):
        self.ogl_detector_widget.detectProfile()
        self.ogl_detector_widget.updateGL()

    def fireButtonClose(self):
        self.ogl_detector_widget.cancelWidget()
        self.close()

    def open(self) :
        (fileName, _) = QtGui.QFileDialog.getOpenFileName(self,
                                     "Open File", QtCore.QDir.currentPath())
        if (fileName) :
            self.ogl_detector_widget.setFileName(fileName)
            self.ogl_detector_widget.updateGL()

    def createActions(self):
        self.openAct = QtGui.QAction('Open...', self)
        self.openAct.triggered.connect(self.open)    
        
        self.exitAct = QtGui.QAction("Exit", self);
        self.exitAct.triggered.connect(self.close)
        
    def createMenus(self):
        fileMenu = QtGui.QMenu("File", self)
        fileMenu.addAction(self.openAct)
        fileMenu.addSeparator()
        fileMenu.addAction(self.exitAct)

        menubar = QtGui.QMenuBar(self)
        menubar.addMenu(fileMenu)



class AirfoilDetectOglWidget(ProfileWidget):
    def __init__(self, profile = Profile("untitled", None, []), parent = None):
        super(AirfoilDetectOglWidget, self).__init__(profile)
        
        
        self.filename = ""
        self.img_width = -1
        self.img_height = -1
        self.scaleImg = 1
        self.scale = 2
        self.flag_detected = False
        self.flag_setCenter = False
        #self.resize(self.width,self.height)
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
            GL.glPushMatrix()
            GL.glTranslatef(self.xTrans, self.yTrans, 0)
            GL.glScalef(self.scaleImg, self.scaleImg,1)
            self.drawBackgroundImg()
            #GL.glTranslatef(-self.xTrans, -self.yTrans, 0)
            GL.glPopMatrix()
        if self.flag_detected:
            GL.glScalef(self.scale, self.scale,1)
            self.drawProfile()

        GL.glFlush()    

    # ================================================================================================================
    # profile drawing
    # ================================================================================================================ 
    def drawProfile(self):
        if self.profile.getPointList() == [] :
            self.createDefaultProfile()
        
        if self.flag_setCenter :
            trX, trY = self.norm_vec_list(self.profile.getPointList())
            GL.glTranslatef(-trX, trY, 0) 

        # draw profile by pointList        
        GL.glLineWidth(2)
        GL.glColor3f(0.0, 0.0, 0.0)
        GL.glBegin(GL.GL_LINE_STRIP) 
        for p in self.profile.getPointList() :
            GL.glVertex3f(p[0], p[1], p[2])              
        GL.glEnd()    
        
        # draw profile points
        GL.glColor3f(1.0, 0.0, 0.0)
        GL.glPointSize(10)
        GL.glBegin(GL.GL_POINTS) 
        for p in self.profile.getPointList() :
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

    #----------------------------------- def drawBackgroundImg(self, xsize=1.0):
        #---------------------------------------- if (self.isImageAvailable()) :
            #-------------------------------------------------------- px = xsize
            #---------------------- py = 1.0*self.img_height/self.img_width * px
#------------------------------------------------------------------------------ 
            #--------------------------------------- GL.glColor3f(1.0, 1.0, 1.0)
            #------------------- # GL.glTranslatef(self.xTrans, self.yTrans,0)
            #------------------------------------------- GL.glBegin(GL.GL_QUADS)
            #---------------------------------------------- GL.glTexCoord2f(0,0)
            #------------------------------------- GL.glVertex3f(-px, -py, -0.5)
            #--------------------------------------------- GL.glTexCoord2f(1, 0)
            #------------------------------------- GL.glVertex3f( px, -py, -0.5)
            #--------------------------------------------- GL.glTexCoord2f(1, 1)
            #------------------------------------- GL.glVertex3f( px,  py, -0.5)
            #-------------------------------------------- GL.glTexCoord2f(0,  1)
            #------------------------------------- GL.glVertex3f(-px,  py, -0.5)
            #-------------------------------------------------------- GL.glEnd()
            
    def drawBackgroundImg(self, xsize=1.0):
        if (self.isImageAvailable()) :
            if self.height > self.width :
                if self.img_height > self.img_width :
                    px = (1.0 * self.img_width / self.img_height) * (self.width / self.height)
                    py = 1.0 
                else :
                    px = 1.0 * (self.width / self.height)
                    py = 1.0 * (self.img_height / self.img_width)
            else : 
                if self.img_height > self.img_width :
                    px = (1.0 * self.img_width / self.img_height)
                    py = 1.0 * (self.width / self.height)
                else :
                    px = 1.0 
                    py = 1.0 * (self.img_height / self.img_width) * (self.width / self.height)          
           
            GL.glColor3f(1.0, 1.0, 1.0)
            # GL.glTranslatef(self.xTrans, self.yTrans,0)
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
        self.profile.setPointList([[1.0, 0.00095, 0.0], [0.95, 0.00605, 0.0], [0.9, 0.01086, 0.0], [0.8, 0.01967, 0.0], \
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
            self.profile.setPointList([])
        
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
        self.profile.setPointList([])
        self.flag_detected = False
        self.setFileName("")    
    
    def mousePressEvent(self, event):
        self.updateGL() # important for __winPosTo3DPos
        self.__selectedPoint    = self.__winPosTo3DPos(event.pos().x(), event.pos().y())
        self.__idxSelectedPoint = self.__getIdxOfSelectedPoint(self.__selectedPoint, self.profile.getPointList()) 
        if self.__idxSelectedPoint < 0 :
            if(event.button() == QtCore.Qt.RightButton) :
                ()
            else : 
                super(AirfoilDetectOglWidget, self).mousePressEvent(event)
        
    def mouseMoveEvent(self, event):
        if self.__idxSelectedPoint >= 0 :
            p = self.__winPosTo3DPos(event.pos().x(), event.pos().y())
            self.profile.setPointToPointListAtIdx(self.__idxSelectedPoint, p)
            self.updateGL()
        else:
            super(AirfoilDetectOglWidget, self).mouseMoveEvent(event)
        
    def addPoint(self):
        idx = utility.computeIdxOfPointWithMinDistance(self.__selectedPoint, self.profile.getPointList(), 1)[0]
        if idx == None :
            self.profile.insertToPointList(0, self.__selectedPoint)
        else :
            idx_l = len(self.profile.getPointList()) - 1 if idx == 0 else idx - 1
            idx_r = 0 if idx == len(self.profile.getPointList()) - 1 else idx + 1
            
            dist_l = utility.getDistanceBtwPoints(self.__selectedPoint, self.profile.getPointList()[idx_l])
            dist_r = utility.getDistanceBtwPoints(self.__selectedPoint, self.profile.getPointList()[idx_r])
            
            if dist_l < dist_r :
                self.profile.insertToPointList(idx, self.__selectedPoint)
            else : self.profile.insertToPointList(idx_r, self.__selectedPoint)
        
        #self.insertToPointList(idx, self.__selectedPoint) if dist_l < dist_r else self.insertToPointList(idx_r, self.__selectedPoint)
        self.updateGL()

    def removePoint(self):
        if self.__idxSelectedPoint >= 0 :
            self.profile.removeFromPointList(self.__idxSelectedPoint)
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
    widget = AirfoilDetectWidget()
    widget.show()
    app.exec_()    