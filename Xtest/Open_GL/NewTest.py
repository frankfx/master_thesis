'''
Created on Jul 30, 2014

@author: fran_re
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

class Renderer():
    OPEN, CLOSED = range(2)
    DEFAULT, BEZIER_NEW_4, BEZIER_OPENGL = range(3)
    
    def nextTestValue(self):
        if(self.testValue > 36) :
            self.testValue = 2
        else:
            self.testValue +=1  

    def prevTestValue(self):
        if(self.testValue < 3) :
            self.testValue = 36
        else:
            self.testValue -=1  
    
    def __init__(self, tixi):
        self.tixi = tixi
        self.scale = 1.0
        self.trans_x = 0
        self.trans_y = 0
        self.width = -1
        self.height = -1
        self.fovy = 64.0
        self.flag_view_algo = Renderer.DEFAULT
        self.flag_view = Renderer.OPEN
        self.testValue = 2

    def set_flag_view(self, view_algo, cflag=OPEN):
        self.flag_view_algo = view_algo
        self.flag_view = cflag

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


    def drawProfile(self):
        vecX = self.tixi.getVectorX('NACA0009')
        vecY = self.tixi.getVectorZ('NACA0009')
        vecZ = self.tixi.getVectorY('NACA0009')
        
        top_prof, bot_prof = self.split_profile(vecX, vecY, vecZ)
        if self.flag_view == Renderer.OPEN : shape = GL.GL_LINE_STRIP
        else : shape = GL.GL_LINE_LOOP
        
        GL.glColor3f(0, 0, 1)
        GL.glTranslatef(-self.__norm_vec_list(vecX),0, 0)
        
        if self.flag_view_algo == Renderer.DEFAULT : 
            print "DEFAULT"
            self.drawProfile_default(top_prof, bot_prof, shape)
        elif self.flag_view_algo == Renderer.BEZIER_NEW_4 :
            print "BEZIER_NEW_4"        
            self.drawProfile_bezier(top_prof, bot_prof, shape, self.testValue)
        elif self.flag_view_algo == Renderer.BEZIER_OPENGL :
            print "BEZIER_OPENGL"
            self.drawProfile_openGL(top_prof, bot_prof, shape, 5)
        else :
            print "NOTHING"

        #The following code displays the control points as dots.
        i = 0
        GL.glPointSize(5.0)        
        GL.glColor3f(1.0, 0.0, 0.0)
        GL.glBegin(GL.GL_POINTS)
        for i in range (0, len(vecX), 1):
            GL.glVertex3f(vecX[i], vecY[i], vecZ[i])
        GL.glEnd()  

    def drawProfile_default(self, top_prof, bot_prof, shape):
        p_list = top_prof + bot_prof
        GL.glBegin(shape)
        for i in range (0, len(p_list)) :
            GL.glVertex3f(p_list[i][0], p_list[i][1], p_list[i][2])
        GL.glEnd()        

    def drawProfile_bezier(self, top_prof, bot_prof, shape, step):
        p_list = self.createBezierList(top_prof + bot_prof, step)
        GL.glBegin(shape) 
        for i in range (0, len(p_list), 1) :
            GL.glVertex3f(p_list[i][0], p_list[i][1], p_list[i][2])              
        GL.glEnd()       

    def drawProfile_openGL(self, top_prof, bot_prof, shape, step):
        l_prof = top_prof + bot_prof #self.createBezierList_for_mapf(top_prof + bot_prof)
        for i in range (0, len(l_prof), step-1):
            tmp = []
            hlp = step  if i < len(l_prof) -(step-1) else len(l_prof) - i
                
            for b in range (i, i + hlp, 1) :
                tmp.append(l_prof[b])
                
            if hlp < step and self.flag_view == Renderer.CLOSED :
                tmp.append(l_prof[0])
    
            GL.glMap1f(GL.GL_MAP1_VERTEX_3, 0.0, 1.0, tmp)
    
            j = 0
            GL.glBegin(GL.GL_LINE_STRIP)
            for j in range (0, 31, 1):
                GL.glEvalCoord1f(j/30.0)
            GL.glEnd()
            if (hlp < step) :
                break


    def drawGrid(self, x_fr = -0.9, x_to = 0.9, y_fr = -0.9, y_to = 0.9, no_lines = 6):
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


    '''
    @param: l_x, l_y, l_z lists with coordinates for x, y and z
    @param: sort_desc boolean flag for splitting option
    @return: lists for top and bottom profile in format [ [x0,y0,z0] , [x1,y1,z1] , ...  ]
    '''
    def split_profile(self, l_x, l_y, l_z, sort_desc = True):
        l_fst = []
        l_snd = []
        
        for i in range(0, len(l_x)-1, 1) :
            if sort_desc:
                if l_x[i] > l_x[i+1] :
                    l_fst.append([ l_x[i], l_y[i], l_z[i] ]) 
                else: break
            else :
                if l_x[i] < l_x[i+1] :
                    l_fst.append([ l_x[i], l_y[i], l_z[i] ]) 
                else: break                
                
        for j in range(i, len(l_x), 1) :
            l_snd.append([ l_x[j], l_y[j], l_z[j] ])

        return l_fst , l_snd

    '''
    @param: p_list list in format [ [x0,y0,z0] , [x1,y1,z1] , ...  ]
    @param: sort_desc boolean flag for splitting option
    @return: lists for top and bottom profile in format [ [x0,y0,z0] , [x1,y1,z1] , ...  ]
    '''
    def split_profile_plist(self, p_list, sort_desc = True):
        l_fst = []
        l_snd = []

        for i in range(0, len(p_list)-1, 1) :
            if sort_desc:
                if p_list[i][0] > p_list[i+1][0] :
                    l_fst.append(p_list[i]) 
                else: break
            else :
                if p_list[i][0] < p_list[i+1][0] :
                    l_fst.append(p_list[i]) 
                else: break                
                        
            for j in range(i, len(p_list), 1) :
                l_snd.append(p_list[j])              

        return l_fst , l_snd       

    '''
    @param: list with points [ [x0,y0,z0] , [x1,y1,z1] , ...  ]
    @return: list with additional control points
    '''
    def createBezierList_for_mapf(self, p_list):
        
        res = []
        for i in range(0, len(p_list)-1) :
            tan1, tan2 = self.__compute_bezier_tangent(p_list[i], p_list[i+1])            
            res.append(p_list[i])
            res.append(tan1)
            res.append(tan2)
            res.append(p_list[i+1])
            
        return res
        
    def createBezierList(self, p_list, step, t=31):
        res = []
                
        for i in range(0, len(p_list), step-1) :  
           # start = p_list[i]
           # end   = p_list[i+1]
           # tan1, tan2 = self.__compute_bezier_tangent(start, end)
 
            hlp = step  if i < len(p_list) -(step-1) else len(p_list) - i
                    
            tmpX = []
            tmpY = []
            tmpZ = []
            k = 0
            for k in range (0, hlp):
                tmpX.append(p_list[i+k][0])
                tmpY.append(p_list[i+k][1])
                tmpZ.append(p_list[i+k][2])      
             
            j = 0     
            for j in range(0, t, 1):
                pos = j*1.0 / t
               # x = self.bezierCurve_full(pos, [ start[0], tan1[0], tan2[0], end[0] ])
               # y = self.bezierCurve_full(pos, [ start[1], tan1[1], tan2[1], end[1] ])
               # z = self.bezierCurve_full(pos, [ start[2], tan1[2], tan2[2], end[2] ])
                    
                x = self.bezierCurve_full(pos, tmpX)
                y = self.bezierCurve_full(pos, tmpY)
                z = self.bezierCurve_full(pos, tmpZ)
                
                res.append([x,y,z])    
        res.append(p_list[len(p_list)-1])
        print step , len(res)
        return res

    def bezierCurve_full(self, t, pList):
        # Curve with level n has n + 1 points : P0 ... Pn
        n = len(pList) - 1
        return self.bezierCurve_full_rec(0, n, t, pList)

    def bezierCurve_full_rec(self, i, n, t, pList):
        if i == n :
            return math.pow(t, i) * pList[i]
        else :
            return self.compute_Bernsteinpolynom(i, n, t) * pList[i] + self.bezierCurve_full_rec(i+1, n, t, pList)
            
    def compute_Bernsteinpolynom(self,i, n, t):
        return math.factorial(n) / ( math.factorial(i) * math.factorial(n-i) ) * math.pow(t,i) * math.pow(1-t, n-i) 

    def bezierCurve(self, t, P_0, P_1, P_2, P_3):
        # Cubic bezier Curve
        point = (math.pow((1-t), 3.0) * P_0) + \
                (3 * math.pow((1-t),2) * t * P_1) + \
                (3 * (1-t) * t * t * P_2) + \
                (math.pow(t, 3) * P_3)
        return point

    def __compute_bezier_tangent(self, p1, p2):
        dx = (p2[0] - p1[0]) / 3
        dy = (p2[1] - p1[1]) / 3

        x3 = p1[0] + dx
        y3 = p1[1] + dy

        x4 = x3 + dx
        y4 = y3 + dy
    
        return [x3, y3, 0] , [x4, y4, 0]

    def __norm_vec_list(self, vlist):
        '''set points of shape to center (0,0)'''
        vlist = list(vlist)
        mx = max(vlist)
        mn = min(vlist)
        dist = mx - mn
        mid = dist / 2.0
        shift = mx - mid

        return shift       

class MyWidget(QtOpenGL.QGLWidget):
    def __init__(self, parent = None):
        super(MyWidget, self).__init__(parent)
        self.resize(320,320)
        self.setWindowTitle("Rene Test")
        #self.setFixedSize(QtCore.QSize(400,400))
        self.dx = 0.0
        self.dy = 0.0
        self.lastPos_x = 0.0
        self.lastPos_y = 0.0
        
        tixi = CPACS_Handler()
        tixi.loadFile(Config.path_cpacs_A320_Fuse, Config.path_cpacs_21_schema)
        self.renderer = Renderer(tixi)
        self.renderer.set_flag_view(Renderer.DEFAULT, Renderer.CLOSED)    
    
    def initializeGL(self):
        self.renderer.init()
    
    def resizeGL(self, w, h):
        self.renderer.resize(w, h)
 
    def paintGL(self):
        self.renderer.display()

    def keyPressEvent(self, event):
        redraw = False
        offsetScl = 0.008
        offsetTrans = 0.02
        if event.modifiers() == QtCore.Qt.ControlModifier:
            if event.key() == QtCore.Qt.Key_N :
                if self.renderer.flag_view_algo > 1 :
                    self.renderer.flag_view_algo = 0
                else : self.renderer.flag_view_algo += 1
            elif event.key() == QtCore.Qt.Key_S :
                self.renderer.nextTestValue()
            elif event.key() == QtCore.Qt.Key_A :
                self.renderer.prevTestValue()
            redraw = True
        if event.key() == QtCore.Qt.Key_Plus:
            self.renderer.scale -= offsetScl
            redraw = True
        elif event.key() == QtCore.Qt.Key_Minus:
            self.renderer.scale += offsetScl
            redraw = True
        elif event.key() == QtCore.Qt.Key_Left:
            self.renderer.trans_x += offsetTrans
            redraw = True                         
        elif event.key() == QtCore.Qt.Key_Right:
            self.renderer.trans_x -= offsetTrans
            redraw = True
        elif event.key() == QtCore.Qt.Key_Up:
            self.renderer.trans_y -= offsetTrans
            redraw = True
        elif event.key() == QtCore.Qt.Key_Down:
            self.renderer.trans_y += offsetTrans
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
        
        self.renderer.trans_x += (self.dx * 2.0 / self.width() * self.renderer.scale) 
        self.renderer.trans_y -= (self.dy * 2.0 / self.height() * self.renderer.scale)
        self.updateGL()
        
if __name__ == '__main__':
    app = QtGui.QApplication(["PyQt OpenGL"])
    widget = MyWidget()
    widget.show()
    app.exec_()    