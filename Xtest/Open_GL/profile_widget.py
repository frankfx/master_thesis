'''
Created on Sep 3, 2014

@author: rene
'''

import sys
import math
from PySide import QtOpenGL, QtGui, QtCore
from cpacsHandler import CPACS_Handler
from config import Config

try:
    from OpenGL import GL, GLU, GLUT
except ImportError:
    app = QtGui.QApplication(sys.argv)
    QtGui.QMessageBox.critical(None, "OpenGL hellogl",
                              "PyOpenGL must be installed to run this example.",
                            QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default,
                            QtGui.QMessageBox.NoButton)
    sys.exit(1)

class Profile_Widget(QtOpenGL.QGLWidget):
    OPEN, CLOSED = range(2)
    DEFAULT, BEZIER_NEW_4, BEZIER_OPENGL = range(3) 
    def __init__(self, uid='NACA0009', parent = None):
        super(Profile_Widget, self).__init__(parent)
           
        self._name               = uid
        self._chord              = -1     # Profiltiefe/Sehne
        self._work_angle         = -1     # Anstellwinkel
        self._profile_arch       = -1     # Profilwoelbung
        self._profile_thickness  = -1     # Profildicke
        self.flag_draw_points    = False  
        self._flag_view          = Profile_Widget.OPEN
        # ==========================================================
        self.tixi = CPACS_Handler()
        self.tixi.loadFile(Config.path_cpacs_A320_Fuse, Config.path_cpacs_21_schema)
        # ==========================================================
        self.scale = 0.5
        self.trans_x = 0
        self.trans_y = 0
        self.width = -1
        self.height = -1
        self.fovy = 64.0
        # helper ===================================================
        self.lastPos_x = 0.0
        self.lastPos_y = 0.0

        self.pointList_top, self.pointList_bot = self.__createPointList(uid)

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
        self.drawProfile()

        GL.glFlush()

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

    def set_flag_view(self, vflag=OPEN):
        self._flag_view = vflag

    def set_transX(self, value):
        self.trans_x = value

    def set_transY(self, value):
        self.trans_y = value

    def set_scale(self, value):
        self.scale = value

    def get_chord(self):
        return self._chord

    def get_work_angle (self):
        return self._work_angle

    def get_profile_arch(self):
        return self._profile_arch

    def get_profile_thickness(self):
        return self._profile_thickness

    def get_flag_view(self):
        return self._flag_view

    def get_name(self):
        return self._name

    def drawProfile(self):
        return NotImplemented

    def fitToPage(self, bool):
        if bool :
            self.set_transX(0)
            self.set_transY(0)
            self.set_scale(0.5)
        self.setDisabled(bool)
        self.updateGL()

    def drawChord(self):

        min_t, max_t = self.__get_min_max_of_List(self.pointList_top)
        min_b, max_b = self.__get_min_max_of_List(self.pointList_bot)

        mini = min_t if min_t[0] < min_b[0] else min_b
        maxi = max_t if max_t[0] > max_b[0] else max_b
        maxi = [maxi[0], max_b[1] + (max_t[1] - max_b[1])/2, maxi[2]]


        GL.glBegin(GL.GL_LINES)
        GL.glVertex3f(mini[0], mini[1], mini[2]) # left end (nose)
        GL.glVertex3f(maxi[0], maxi[1], maxi[2]) # right end
        GL.glEnd()

    def drawProfile_points(self):
        GL.glPointSize(5.0)        
        GL.glColor3f(1.0, 0.0, 0.0)
        GL.glBegin(GL.GL_POINTS)
        for i in range (0, len(self.pointList_top), 1):
            GL.glVertex3f(self.pointList_top[i][0], self.pointList_top[i][1], self.pointList_top[i][2])
        i = 0
        for i in range (0, len(self.pointList_bot), 1):
            GL.glVertex3f(self.pointList_bot[i][0], self.pointList_bot[i][1], self.pointList_bot[i][2])
        GL.glEnd() 

    def drawSkeleton(self):
        GL.glBegin(GL.GL_LINES)
        for i in range(0, len(self.pointList_top)) :
            p = self.__computePoint(self.pointList_top[i], self.pointList_bot)
            GL.glVertex3f(p[0], p[1], p[2]) # left end (nose)
        GL.glEnd()

    def drawGrid(self, x_fr = -1.0, x_to = 1.0, y_fr = -1.0, y_to = 1.0, no_lines = 6):
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
        min_list, max_list = self.__get_min_max_of_List(vlist)
        mn = min_list[0] 
        mx = max_list[0] 
        dist = mx - mn
        mid = dist / 2.0
        shift = mx - mid

        return shift 

    '''
    @param: uid from cpacs
    @param: sort_desc boolean flag for splitting option
     @return: lists for top and bottom profile in format [ [x0,y0,z0] , [x1,y1,z1] , ...  ]
    '''
    def __createPointList(self, uid, sort_desc = True):
        vecX = self.tixi.getVectorX(uid)
        vecY = self.tixi.getVectorZ(uid)
        vecZ = self.tixi.getVectorY(uid)
        l_fst = []
        l_snd = []
        for i in range(0, len(vecX)-1, 1) :
            if sort_desc:
                if(vecX[i] > vecX[i+1]) :
                    l_fst.append([ vecX[i], vecY[i], vecZ[i] ])
                else : break
            else :
                if vecX[i] < vecX[i+1] :
                    l_fst.append([ vecX[i], vecY[i], vecZ[i] ])
                else: break

        for j in range(i, len(vecX), 1) :
            l_snd.append([ vecX[j], vecY[j], vecZ[j] ])

        return l_fst , l_snd


    def __computePoint(self, p1, plist):
        index_r = -1
        index_l = -1
        mini, maxi = self.__get_min_max_of_List(plist)

        right_of_x = maxi[0]
        left_of_x = mini[0]

        for i in range(0 , len(plist)) :
            if plist[i][0] < p1[0] and plist[i][0] > left_of_x :
                left_of_x = plist[i][0]
                index_l = i
            if plist[i][0] > p1[0] and plist[i][0] < right_of_x :
                right_of_x = plist[i][0]
                index_r = i

        # b = y2 - m-x2 ; m = (y2-y1) / (x2-x1)
        m = ( plist[index_r][1] - plist[index_l][1] ) / ( plist[index_r][0] - plist[index_l][0] )
        b = plist[index_r][1] - m * plist[index_r][0]

        y = m * p1[0] + b

        return [p1[0], p1[1] - (p1[1] - y) / 2.0, p1[2]]

    def initializeGL(self):
        self.init()
    
    def resizeGL(self, w, h):
        self.resize(w, h)
 
    def paintGL(self):
        self.display()

    def __get_min_max_of_List(self, plist):
        m_max = -1000 # random value
        m_min = 1000  # random value
        id_max = -1
        id_min = -1
        for i in range (0, len(plist),1) :
            if m_max < plist[i][0] :
                m_max = plist[i][0]
                id_max = i
            if m_min > plist[i][0] :
                m_min = plist[i][0]
                id_min = i

        return plist[id_min], plist[id_max]


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
        
        self.trans_x += (self.dx * 2.0 / self.width * self.scale) 
        self.trans_y -= (self.dy * 2.0 / self.height * self.scale)
        self.updateGL()

        
if __name__ == '__main__':
    app = QtGui.QApplication(["PyQt OpenGL"])
    widget = Profile_Widget()
    widget.show()
    app.exec_()          