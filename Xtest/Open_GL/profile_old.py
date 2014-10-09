'''
Created on Oct 8, 2014

@author: fran_re
'''

import sys
import utility
from PySide import QtOpenGL, QtGui, QtCore
from cpacsHandler import CPACS_Handler
from Xtest.Open_GL.spline import Chaikin
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




class Profile(QtOpenGL.QGLWidget):
    def __init__(self, name, plist, parent = None):
        super(Profile, self).__init__(parent)

        self._name                   = name
        self.pointList               = plist
           
        self.flag_draw_points        = False  
        self.flag_spline_curve       = False
        
        # viewing rotation
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0 
        # profile rotation
        self.rotate = 0
        
        self.scale = 0.5
        self.xTrans = 0
        self.yTrans = 0
        self.width = -1.0
        self.height = -1.0
        self.fovy = 64.0
        # helper ===================================================
        self.lastPos_x = 0.0
        self.lastPos_y = 0.0

        self.resize(320,320)
        self.setWindowTitle("profile")

    def initializeGL(self):
        GL.glEnable(GL.GL_COLOR_MATERIAL)
        GL.glEnable(GL.GL_MAP1_VERTEX_3)
        GL.glClearColor(1.0, 1.0 , 1.0, 1.0)
        GL.glShadeModel(GL.GL_FLAT)

    def resizeGL(self, w, h):
        self.width , self.height = w , h
        GL.glViewport(0,0,w,h)

        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GLU.gluPerspective (self.fovy * self.scale, w*1.0/h, 0.0, 10.0)

    def paintGL(self):
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GLU.gluPerspective (self.fovy * self.scale, self.width*1.0/self.height, 0.0, 10.0)

        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()

        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        GL.glTranslatef(self.xTrans,self.yTrans,-1.5)

        self.drawGrid()
        self.drawProfile()

        GL.glFlush()

    # ================================================================================================================
    # drawing functions
    # ================================================================================================================
    '''abstract method'''
    def drawProfile(self):
        return NotImplemented
    
    '''abstract method'''
    def getWorkAngle(self):
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
            self.setTransX(0)
            self.setTransY(0)
            self.setScale(0.5)
        self.setDisabled(boolean)
        self.updateGL()
        
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
    def setName(self, value):
        self._name = value

    def setTransX(self, value):
        self.xTrans = value

    def setTransY(self, value):
        self.yTrans = value

    def setScale(self, value):
        self.scale = (101 - value) / 100.0  # transform scale range (1 to 99) to perspective  
        self.updateGL()
    
    def setRotate(self, value):
        self.rotate = value
        self.updateGL()    
        
    def setDrawPointsOption(self, value):
        self.flag_draw_points = value 
        self.updateGL()        

    def setFlagSplineCurve(self, value):
        self.flag_spline_curve = value
        self.updateGL()        

    def setPointListTop_rot(self, plist):
        self.dataSet.setPointListTop_rot(plist)

    def setPointListBot_rot(self, plist):
        self.dataSet.setPointListBot_rot(plist)    

    def setPointList(self, plist):
        self.pointList = plist

    def setPointToPointListAtIdx(self, idx, val):
        self.pointList[idx] = val

    def insertToPointList(self, idx, val):
        self.pointList.insert(idx, val)
    
    def removeFromPointList(self, idx):
        del self.pointList[idx] 
    
    def getName(self):
        return self._name
    
    def getPointList(self):
        return self.pointList    
    
    def getFlagDrawPoints(self):
        return self.flag_draw_points    
        
    def getFlagSplineCurve(self):
        return self.flag_spline_curve

    def getRotAngle(self):
        return self.rotate
    
    def getPointListTop_rot(self):
        return self.pointList_top_rot

    def getPointListBot_rot(self):
        return self.pointList_bot_rot
    
    '''
    @return: chaikin spline of point list
    '''  
    def getSplineCurve(self):
        spline = Chaikin(self.getPointList())
        spline.IncreaseLod()
        spline.IncreaseLod()
        return spline.getPointList()    

    # ============================================================================================================
    # mouse and key events
    # ============================================================================================================

    def keyPressEvent(self, event):
        redraw = False
        print "hier"
        offset_rot   = 0.02
        offset_scale = 0.008       
        if event.key() == QtCore.Qt.Key_Plus:
            self.scale -= offset_scale
            redraw = True
        elif event.key() == QtCore.Qt.Key_Minus:
            self.scale += offset_scale
            redraw = True
        elif event.key() == QtCore.Qt.Key_Left:
            self.Xrot += offset_rot
            redraw = True                         
        elif event.key() == QtCore.Qt.Key_Right:
            self.Xrot -= offset_rot
            redraw = True
        elif event.key() == QtCore.Qt.Key_Up:
            self.yTrans -= offset_rot
            redraw = True
        elif event.key() == QtCore.Qt.Key_Down:
            self.yTrans += offset_rot
            print "down"
            redraw = True                                
        
        if redraw :
            self.updateGL()
            
    def mousePressEvent(self, event):  
        self.lastPos_x = event.pos().x()
        self.lastPos_y = event.pos().y()
                
    def mouseMoveEvent(self, event):
        dx = (event.pos().x() - self.lastPos_x ) 
        dy =  (event.pos().y() - self.lastPos_y ) 
        
        self.lastPos_x += dx
        self.lastPos_y += dy
        
        #Betrachtsfeld = -1 bis 1
        
        #print self.width 
        #print self.height 
        
        self.xTrans += (2*dx / (self.width*1.0) * self.scale) 
        self.yTrans -= (2*dy / (self.height*1.0) * self.scale)

        self.updateGL()

        
if __name__ == '__main__':
    app = QtGui.QApplication(["PyQt OpenGL"])
    widget = Profile()
    widget.show()
