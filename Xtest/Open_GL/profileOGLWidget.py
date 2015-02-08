'''
Created on Oct 9, 2014

@author: rene
'''

import sys
from Xtest import utility
from PySide import QtOpenGL, QtGui, QtCore

try:
    from OpenGL import GL
except ImportError:
    app = QtGui.QApplication(sys.argv)
    QtGui.QMessageBox.critical(None, "OpenGL hellogl",
                              "PyOpenGL must be installed to run this example.",
                            QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default,
                            QtGui.QMessageBox.NoButton)
    sys.exit(1)

class ProfileOGLWidget(QtOpenGL.QGLWidget):
    def __init__(self, profile, parent = None):
        super(ProfileOGLWidget, self).__init__(parent)

        self.flag_draw_points  = False  
        self.flag_chaikin_spline = False
        self.flag_b_spline = False
        
        self.profile = profile
        
        # viewing rotation
        self.xRot = 0.0
        self.yRot = 0.0
        self.zRot = 0.0 
        
        # profile rotation
        self.rotate = 0.0
        
        self.aspect = self.profile.getLength()
        
        self.viewwidth = 0.0
        self.viewheight = 0.0

        self.scale  = self.aspect
        self.xTrans = 0.0
        self.yTrans = 0.0
        
        # helper
        self.lastPos_x = 0.0
        self.lastPos_y = 0.0

        self.resize(320,320)
        self.setMinimumHeight(200)
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.setSizePolicy ( QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)        
        self.setWindowTitle("Profile Widget")

    def initializeGL(self):
        GL.glClearColor(1.0, 1.0 , 1.0, 1.0)

    def resizeGL(self, w, h):
        self.viewwidth  = w
        self.viewheight = h
        
        GL.glViewport(0, 0, self.viewwidth, self.viewheight)
        self.setProjection() 

    def paintGL(self):
        self.setProjection()
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        GL.glTranslatef(self.xTrans,self.yTrans,-1.5)
        self.drawGrid()
        self.drawProfile()
        GL.glFlush()
    
    def setProjection(self):
        h = 1 if self.viewheight == 0 else self.viewheight
        ratio = 1.0 * self.viewwidth / h
        
        self.aspect_width = self.aspect*ratio
        
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GL.glOrtho(-self.aspect_width, self.aspect_width,
                   self.aspect, -self.aspect, -100.0, 100.0)

    # ================================================================================================================
    # drawing functions
    # ================================================================================================================
    '''abstract method'''
    def drawProfile(self):
        return NotImplemented
    
    def drawGrid(self, x_fr = -1.0, x_to = 1.0, y_fr = -1.0, y_to = 1.0, no_lines = 5):
        GL.glColor3f(1, 0.85, 0.55)
        GL.glBegin(GL.GL_LINES)
        # line at y-axis through the center
        GL.glVertex3f(x_fr, 0, 0)
        GL.glVertex3f(x_to, 0, 0)
        # line at x-axis through the center
        GL.glVertex3f(0, y_fr, 0)
        GL.glVertex3f(0, y_to, 0)
        for i in range(1, no_lines, 1) :
            # positive lines at y-axis
            GL.glVertex3f(x_fr,  i*1.0/no_lines, 0)
            GL.glVertex3f(x_to,  i*1.0/no_lines, 0)
            # negative lines at y-axis
            GL.glVertex3f(x_fr, -i*1.0/no_lines, 0)
            GL.glVertex3f(x_to, -i*1.0/no_lines, 0)
            # positive lines at x-axis
            GL.glVertex3f( i*1.0/no_lines, y_fr, 0)
            GL.glVertex3f( i*1.0/no_lines, y_to, 0)
            # negative lines at x-axis
            GL.glVertex3f(-i*1.0/no_lines, y_fr, 0)
            GL.glVertex3f(-i*1.0/no_lines, y_to, 0)
        GL.glEnd()

    # ================================================================================================================
    # helper and drawing options
    # ================================================================================================================
    def fitToPage(self, boolean):
        if boolean :
            self.setScale(51.0)
            self.setTrans(0.0, 0.0)
            self.setXYTRot(0.0, 0.0, 0.0)
        self.setDisabled(boolean)
        
    def norm_vec_list(self, vlist):
        '''set points of shape to center (0,0)'''
        minX_list, maxX_list = utility.get_min_max_of_List(vlist,0)
        minY_list, maxY_list = utility.get_min_max_of_List(vlist,1)
        
        mnX = minX_list[0] 
        mxX = maxX_list[0] 
        mnY = minY_list[1]
        mxY = maxY_list[1]

        distX = mxX - mnX
        distY = mxY - mnY
        
        midX = distX / 2.0
        midY = distY / 2.0

        shiftX = mxX - midX
        shiftY = mxY - midY

        return shiftX , -shiftY           

    # ================================================================================================================
    # getter and setter
    # ================================================================================================================
    def setRotAngle(self, value):
        self.rotate = value

    def setScale(self, value):
        self.aspect = self.scale * ( (50.0-value) * 9.0/500.0 +1.0 )

    def setTrans(self, xTrans, yTrans):
        self.xTrans = xTrans
        self.yTrans = yTrans
        
    def setXYTRot(self, xRot, yRot, zRot):
        self.setXRotation(xRot)
        self.setYRotation(yRot)
        self.setZRotation(zRot)
        
    def setXRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.xRot:
            self.xRot = angle
            self.emit(QtCore.SIGNAL("xRotationChanged(int)"), angle)
            self.updateGL()

    def setYRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.yRot:
            self.yRot = angle
            self.emit(QtCore.SIGNAL("yRotationChanged(int)"), angle)
            self.updateGL()

    def setZRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.zRot:
            self.zRot = angle
            self.emit(QtCore.SIGNAL("zRotationChanged(int)"), angle)
            self.updateGL()
    
    def normalizeAngle(self, angle):
        while angle < 0:
            angle += 360 * 2
        while angle > 360 * 2:
            angle -= 360 * 2
        return angle    
        
    def setFlagDrawPoints(self, value):
        self.flag_draw_points = value 

    def setFlagChaikinSpline(self, value):
        self.flag_chaikin_spline = value

    def setFlagBSpline(self, value):
        self.flag_b_spline = value

    def setProfile(self, profile):
        self.profile = profile

    def getProfile(self):
        return self.profile    
    
    def getFlagDrawPoints(self):
        return self.flag_draw_points    
        
    def getFlagChaikinSpline(self):
        return self.flag_chaikin_spline

    def getFlagBSpline(self):
        return self.flag_b_spline

    def getRotAngle(self):
        return self.rotate
    
    def getXRotation(self):
        return self.xRot

    def getYRotation(self):
        return self.yRot

    def getZRotation(self):
        return self.zRot
    
    '''
    @return: chaikin spline of point list
    '''  
    def getChaikinSplineCurve(self):
        return self.profile.computeChaikinSplineCurve()
    
    def getBSplineCurve(self):
        return self.profile.computeBSplineCurve()


    # ============================================================================================================
    # mouse and key events
    # ============================================================================================================

    def keyPressEvent(self, event):
        redraw = False
        offset_rot   = 2.0
        offset_scale = 0.1       
        if event.key() == QtCore.Qt.Key_Plus:
            self.scale -= offset_scale
            redraw = True
        elif event.key() == QtCore.Qt.Key_Minus:
            self.scale += offset_scale
            redraw = True
        elif event.key() == QtCore.Qt.Key_Left:
            self.setYRotation(self.yRot + offset_rot)
            redraw = True                         
        elif event.key() == QtCore.Qt.Key_Right:
            self.setYRotation(self.yRot - offset_rot)
            redraw = True
        elif event.key() == QtCore.Qt.Key_Up:
            self.setXRotation(self.xRot + offset_rot)
            redraw = True
        elif event.key() == QtCore.Qt.Key_Down:
            self.setXRotation(self.xRot - offset_rot)
            redraw = True                                
        
        if redraw :
            self.updateGL()
                       
            
    def mousePressEvent(self, event):  
        self.lastPos_x = event.pos().x()
        self.lastPos_y = event.pos().y()
                
    def mouseMoveEvent(self, event):
        dx = (event.x() - self.lastPos_x ) 
        dy = (event.y() - self.lastPos_y ) 
        
        self.lastPos_x += dx
        self.lastPos_y += dy

        #Betrachtsfeld = -aspect bis aspect
        
        oglXunit = 2.0 * self.aspect_width
        oglYunit = 2.0 * self.aspect
        
        # pixel real world to Pixel ogl world 
        oglXTrans = oglXunit * 1.0 / self.viewwidth
        oglYTrans = oglYunit * 1.0 / self.viewheight
        
        self.xTrans += (dx * oglXTrans) 
        self.yTrans += (dy * oglYTrans)

        self.updateGL()