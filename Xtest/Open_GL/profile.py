'''
Created on Sep 3, 2014

@author: rene
'''

import sys
import math
from PySide import QtOpenGL, QtGui, QtCore
from dataSet import DataSet


try:
    from OpenGL import GL, GLU, GLUT
except ImportError:
    app = QtGui.QApplication(sys.argv)
    QtGui.QMessageBox.critical(None, "OpenGL hellogl",
                              "PyOpenGL must be installed to run this example.",
                            QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default,
                            QtGui.QMessageBox.NoButton)
    sys.exit(1)

class Profile(QtOpenGL.QGLWidget):
    def __init__(self, uid='NACA0009', parent = None):
        super(Profile, self).__init__(parent)
           
        self._name                   = uid
        self.flag_draw_points        = False  
        self.flag_close_TrailingEdge = False
        self.flag_spline_curve       = False
        self.flag_draw_camber        = False
        self.flag_draw_chord         = False

        self.rotate = 0.0
        self.scale = 0.5
        self.trans_x = 0
        self.trans_y = 0
        self.width = -1.0
        self.height = -1.0
        self.fovy = 64.0
        # helper ===================================================
        self.lastPos_x = 0.0
        self.lastPos_y = 0.0

        self.dataSet = DataSet(uid)

        self.resize(320,320)
        #self.setFixedSize(QtCore.QSize(400,400))
        self.setWindowTitle("Rene Test")

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
        GL.glTranslatef(self.trans_x,self.trans_y,-1.5)

        self.drawGrid()
        self.drawProfile()

        GL.glFlush()

    # ================================================================================================================
    # drawing functions
    # ================================================================================================================

    '''abstract method'''
    def drawProfile(self):
        return NotImplemented

    def drawChord(self):
        start, end = self.getEndPoints()
        
        GL.glBegin(GL.GL_LINES)
        GL.glVertex3f(start[0], start[1], start[2]) # leftend (nose)
        GL.glVertex3f(end[0], end[1], end[2]) # right end
        GL.glEnd()

    def drawCamber(self):
        plist = self.getPointListCamber()
        GL.glBegin(GL.GL_LINE_STRIP)
        for i in range(0, len(plist)) :
            GL.glVertex3f(plist[i][0], plist[i][1], plist[i][2])# left end == nose
        GL.glEnd()

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
        minX_list, maxX_list = self.dataSet.get_min_max_of_List(vlist,0)
        minY_list, maxY_list = self.dataSet.get_min_max_of_List(vlist,1)
        
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

    def setPointList(self, plist):
        self.dataSet.setPointList(plist)
    
    def setPointListTop(self, plist):
        self.dataSet.setPointListTop(plist)
    
    def setPointListBot(self, plist):
        self.dataSet.setPointListBot(plist)

    def setPointListChord(self, plist):
        self.dataSet.setPointListChord(plist)

    def setPointListCamber(self, plist):
        self.dataSet.setPointListCamber(plist)
        
    def setPointListTop_rot(self, plist):
        self.dataSet.setPointListTop_rot(plist)

    def setPointListBot_rot(self, plist):
        self.dataSet.setPointListBot_rot(plist)

    def setName(self, value):
        self._name = value

    def setTransX(self, value):
        self.trans_x = value

    def setTransY(self, value):
        self.trans_y = value

    def setScale(self, value):
        print "scale value" ,  value
        self.scale = (101 - value) / 100.0  # transform scale range (1 to 99) to perspective  
        self.updateGL()
        
    def setRotate(self, value):
        self.rotate = value
        #self.dataSet.updateRotationLists(value)
        self.updateGL()
        
    def setDrawPointsOption(self, value):
        self.flag_draw_points = value 
        self.updateGL()        

    def setFlagChaikinCurve(self, value):
        self.flag_spline_curve = value
        self.updateGL()        

    def setFlagDrawCamber(self, value):
        self.flag_draw_camber = value
        self.updateGL()      
        
    def setFlagDrawChord(self, value):
        self.flag_draw_chord = value
        self.updateGL()  

    def setFlagCloseTrailingEdge(self, value):
        self.flag_close_TrailingEdge = value
        self.updateGL()

    def getPointListTop(self):
        return self.dataSet.getPointListTop()

    def getPointListBot(self):
        return self.dataSet.getPointListBot()

    def getPointListChord(self):
        return self.dataSet.getPointListChord()

    def getPointListCamber(self):
        return self.dataSet.getPointListCamber()

    def getPointListTop_rot(self):
        return self.dataSet.setPointListTop_rot()

    def getPointListBot_rot(self):
        return self.dataSet.setPointListBot_rot()

    def getEndPoints(self):
        return self.dataSet.getEndPoints()
    
    def getName(self):
        return self._name

    def getLenChord(self):
        return self.dataSet.getLenChord()

    def getWorkAngle (self):
        ## sin(x) = a/c
        start, _ = self.dataSet.getEndPoints()
        x = start[1] / self.getLenChord()
        #return math.sin(x)
        return -self.getRotAngle()

    # (Profilwoelbung) max Abweichung der Skelettlinie von der Profilsehne
    def getProfileArch(self):
        return self.dataSet.getProfileArch()
                                                     
    # (Profildicke) max Kreisdurchmesser auf der Skelettlinie
    def getProfileThickness(self):
        return self.dataSet.getProfileThickness()
    
    def getFlagDrawPoints(self):
        return self.flag_draw_points    

    def getFlagCloseTrailingEdge(self):
        return self.flag_close_TrailingEdge
        
    def getFlagSplineCurve(self):
        return self.flag_spline_curve
    
    def getFlagDrawCamber(self):
        return self.flag_draw_camber
    
    def getFlagDrawChord(self):
        return self.flag_draw_chord

    def getRotAngle(self):
        return self.rotate

    # ============================================================================================================
    # mouse and key events
    # ============================================================================================================

    def keyPressEvent(self, event):
        redraw = False
        offsetScl = 0.008
        offsetTrans = 0.02
        if event.key() == QtCore.Qt.Key_Plus:
            self.scale -= offsetScl
            redraw = True
        elif event.key() == QtCore.Qt.Key_Minus:
            self.scale += offsetScl
            redraw = True
        elif event.key() == QtCore.Qt.Key_Left:
            self.trans_x += offsetTrans
            redraw = True                         
        elif event.key() == QtCore.Qt.Key_Right:
            self.trans_x -= offsetTrans
            redraw = True
        elif event.key() == QtCore.Qt.Key_Up:
            self.trans_y -= offsetTrans
            redraw = True
        elif event.key() == QtCore.Qt.Key_Down:
            self.trans_y += offsetTrans
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
        
        self.trans_x += (2*dx / (self.width*1.0) * self.scale) 
        self.trans_y -= (2*dy / (self.height*1.0) * self.scale)

        self.updateGL()

        
if __name__ == '__main__':
    app = QtGui.QApplication(["PyQt OpenGL"])
    widget = Profile()
    widget.show()
    app.exec_()          