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
    DEFAULT, BEZIER_NEW_4, BEZIER_OPENGL = range(3) 
    def __init__(self, uid='NACA0009', parent = None):
        super(Profile, self).__init__(parent)
           
        self._name                   = uid
        self.flag_draw_points        = False  
        self.flag_close_TrailingEdge = False
        self.flag_cosine_spacing     = False

        self.scale = 0.5
        self.trans_x = 0
        self.trans_y = 0
        self.rotate  = 0
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

    def init(self):
        GL.glEnable(GL.GL_COLOR_MATERIAL)
        GL.glEnable(GL.GL_MAP1_VERTEX_3)
        GL.glClearColor(1.0, 1.0 , 1.0, 1.0)
        GL.glShadeModel(GL.GL_FLAT)

    def resize(self, w, h):
        self.width , self.height = w , h
        GL.glViewport(0,0,w,h)

        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GLU.gluPerspective (self.fovy * self.scale, w*1.0/h, 0.0, 10.0)

    def display(self):

        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GLU.gluPerspective (self.fovy * self.scale, self.width*1.0/self.height, 0.0, 10.0)

        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()

        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        GL.glTranslatef(self.trans_x,self.trans_y,-1.5)

        self.drawGrid()
        
       # GL.glTranslatef(0.5, 0, 0)
       # GL.glRotatef(self.rotate, 0.0, 0.0, 1.0)
       # GL.glTranslatef(-0.5, 0, 0)
       # GL.glRotatef(self.rotate ,0, 0, 1) 
        self.drawProfile()

        GL.glFlush()

    def initializeGL(self):
        self.init()
    
    def resizeGL(self, w, h):
        self.resize(w, h)
 
    def paintGL(self):
        self.display()

    def set_pointList_top(self, plist):
        self.dataSet.setPointListTop(plist)
    
    def set_pointList_bot(self, plist):
        self.dataSet.setPointListBot(plist)

    def set_name(self, value):
        self._name = value
    
    def set_chord(self, value):
        self._chord = value

    def set_work_angle (self, value):
        self._work_angle  = value

    def set_profile_arch(self, value):
        self._profile_arch = value

    def set_profile_thickness(self, value):
        self._profile_thickness = value

    def setCloseTrailingEdge(self, value):
        self.flag_close_TrailingEdge = value

    def set_transX(self, value):
        self.trans_x = value

    def set_transY(self, value):
        self.trans_y = value

    def set_scale(self, value):
        self.scale = value
        
    def set_rotate(self, value):
        self.rotate = value
        self.dataSet.updateRotationLists(value)
        self.updateGL()

       

    def setDrawPointsOption(self, value):
        self.flag_draw_points = value 
        self.updateGL()        

    def setCosineSpacing(self, value):
        self.flag_cosine_spacing = value
        self.updateGL()

    def getPointList_top(self):
        return self.dataSet.getPointList_top()

    def getPointList_bot(self):
        return self.dataSet.getPointList_bot()

    def get_len_chord(self):
        # len Profiltiefe/Sehne
        return self.dataSet.getLenChord()

    def get_work_angle (self):
        # sin(x) = a/c
        start, end = self.dataSet.getEndPoints()
        x = start[1] / self.get_len_chord()
        return math.sin(x)

    # (Profilwoelbung) max Abweichung der Skelettlinie von der Profilsehne
    def get_profile_arch(self):
        #print self.dataSet.pointList_chord, self.dataSet.pointList_camber
        return 100.0 * self.dataSet.get_max_distance_btw_pointLists(self.dataSet.pointList_chord, self.dataSet.pointList_camber)
                                                     
    # (Profildicke) max Kreisdurchmesser auf der Skelettlinie
    def get_profile_thickness(self):
        #print self.dataSet.pointList_top, self.dataSet.pointList_bot
        return 100 * self.dataSet.get_max_distance_btw_pointLists(self.dataSet.pointList_top, self.dataSet.pointList_bot)        


    def get_name(self):
        return self._name
    
    def getFlagDrawPoints(self):
        return self.flag_draw_points    

    '''abstract method'''
    def drawProfile(self):
        return NotImplemented

    def fitToPage(self, boolean):
        if boolean :
            self.set_transX(0)
            self.set_transY(0)
            self.set_scale(0.5)
        self.setDisabled(boolean)
        self.updateGL()

    def drawChord(self):
        start, end = self.dataSet.getEndPoints()
        
        GL.glBegin(GL.GL_LINES)
        GL.glVertex3f(start[0], start[1], start[2]) # leftend (nose)
        GL.glVertex3f(end[0], end[1], end[2]) # right end
        GL.glEnd()

    def drawProfile_points(self):
        plist_top = self.dataSet.pointList_top
        plist_bot = self.dataSet.pointList_bot
        
        GL.glPointSize(5.0)        
        GL.glColor3f(1.0, 0.0, 0.0)
        GL.glBegin(GL.GL_POINTS)
        for i in range (0, len(plist_top), 1):
            GL.glVertex3f(plist_top[i][0], plist_top[i][1], plist_top[i][2])
        for j in range (0, len(plist_bot), 1):
            GL.glVertex3f(plist_bot[j][0], plist_bot[j][1], plist_bot[j][2])
        GL.glEnd() 

    def drawSkeleton(self):
        plist = self.dataSet.pointList_camber
        print "skeleton" , plist
        GL.glBegin(GL.GL_LINES)
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

        
    def norm_vec_list(self, vlist):
        '''set points of shape to center (0,0)'''
        minX_list, maxX_list = self.dataSet.get_min_max_of_List(vlist)
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
        

    # ============================================================================================================
    # mouse and key events
    # ============================================================================================================

    def keyPressEvent(self, event):
        redraw = False
        offsetScl = 0.008
        offsetTrans = 0.02
        if event.modifiers() == QtCore.Qt.ControlModifier:
            if event.key() == QtCore.Qt.Key_N :
                if self.flag_view_algo > 1 :
                    self.flag_view_algo = 0
                else : self.flag_view_algo += 1
            elif event.key() == QtCore.Qt.Key_S :
                self.nextTestValue()
            elif event.key() == QtCore.Qt.Key_A :
                self.prevTestValue()
            redraw = True
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
        self.dx = (event.pos().x() - self.lastPos_x ) 
        self.dy =  (event.pos().y() - self.lastPos_y ) 
        
        self.lastPos_x += self.dx
        self.lastPos_y += self.dy
        
        #Betrachtsfeld = -1 bis 1
        
        #print self.width 
        #print self.height 
        
        self.trans_x += (2*self.dx / (self.width*1.0) * self.scale) 
        self.trans_y -= (2*self.dy / (self.height*1.0) * self.scale)

        self.updateGL()

        
if __name__ == '__main__':
    app = QtGui.QApplication(["PyQt OpenGL"])
    widget = Profile()
    widget.show()
    app.exec_()          