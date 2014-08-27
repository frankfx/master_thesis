'''
Created on Jul 30, 2014

@author: fran_re
'''
import sys
import math
from PySide import QtOpenGL, QtGui, QtCore
from cpacsHandler import CPACS_Handler
from config import Config
from Xtest.Splines.BezierTest import Bezier

try:
    from OpenGL import GL, GLU
except ImportError:
    app = QtGui.QApplication(sys.argv)
    QtGui.QMessageBox.critical(None, "OpenGL hellogl",
                              "PyOpenGL must be installed to run this example.",
                            QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default,
                            QtGui.QMessageBox.NoButton)
    sys.exit(1)

class Renderer():
    OPEN, CLOSED = range(2)
    DEFAULT, BEZIER_NEW, BEZIER_NEW_4, BEZIER_OPENGL = range(4)
    
    def __init__(self, tixi):
        self.tixi = tixi
        self.scale = 1.0
        self.trans_x = 0
        self.trans_y = 0
        self.width = -1
        self.height = -1
        self.fovy = 64.0
        self.besier = Bezier()
        self.flag_view_algo = Renderer.DEFAULT
        self.flag_view = Renderer.OPEN

    def set_flag_view(self, view_algo, val=OPEN):
        self.flag_view_algo = view_algo
        self.flag_view = val

    def init(self):
        # GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_COLOR_MATERIAL)
        GL.glEnable(GL.GL_MAP1_VERTEX_3)
        GL.glClearColor(1.0, 1.0 , 1.0, 1.0)        
        GL.glShadeModel(GL.GL_FLAT)
    
    def resize(self, w, h):
        self.width , self.height = w , h
        GL.glViewport(0,0,w,h) #if w <= h else GL.glViewport(0,0,h,h) 
                                   
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

        GL.glFlush()                # clean puffer, execute all puffered commands


    def drawProfile(self):
        vecX = self.tixi.getVectorX('NACA0009')
        vecY = self.tixi.getVectorY('NACA0009')
        vecZ = self.tixi.getVectorZ('NACA0009')

        GL.glTranslatef(-self.norm_vec_list(vecX),0, 0)
        GL.glColor3f(0, 0, 1)
        
        if self.flag_view_algo == Renderer.DEFAULT : 
            print "DEFAULT"
            GL.glBegin(GL.GL_LINE_LOOP)
            for i in range (0, len(vecX)) :
                GL.glVertex3f(vecX[i], vecZ[i], vecY[i])
            GL.glEnd()
        elif self.flag_view_algo == Renderer.BEZIER_NEW :
            print "BEZIER_NEW"
            t = 31
            GL.glBegin(GL.GL_LINE_LOOP)
            for i in range(0, t, 1):
                pos = i*1.0 / t
                x = self.bezierCurve_full(pos, vecX)
                y = self.bezierCurve_full(pos, vecY)
                z = self.bezierCurve_full(pos, vecZ)

                GL.glVertex3f(x, z, y)            
            GL.glEnd()
            
        elif self.flag_view_algo == Renderer.BEZIER_NEW_4 :
            print "BEZIER_NEW_4"        
            t = 31
            GL.glBegin(GL.GL_LINE_LOOP)
            for a in range(0, len(vecX), 1) :  
                tmp = []
                hlp = 4 if a < len(vecX) - 3 else len(vecX) - a
                
                if hlp < 4 : break
                
                for b in range (a, a + hlp, 1) :
                    tmp.append([ vecX[b], vecY[b], vecZ[b] ])
                  
                for i in range(0, t, 1):
                    print "sdfsdfsdf"
                    pos = i*1.0 / t
                    x = self.bezierCurve(pos, tmp[0][0], tmp[1][0], tmp[2][0], tmp[3][0])
                    y = self.bezierCurve(pos, tmp[0][1], tmp[1][1], tmp[2][1], tmp[3][1])
                    z = self.bezierCurve(pos, tmp[0][2], tmp[1][2], tmp[2][2], tmp[3][2])
                            
                    GL.glVertex3f(x, z, y)                
            GL.glEnd()
            
            
        elif self.flag_view_algo == Renderer.BEZIER_OPENGL :
            print "BEZIER_OPENGL"
            plist = self.to_opengl_bezier_list(vecX, vecZ, vecY)
            GL.glColor3f(0.0, 0.0, 1.0)
            for a in range (0, len(plist), 7):
                tmp = []
                hlp = 8  if a < len(plist) -7 else len(plist) - a
                
                for b in range (a, a + hlp, 1) :
                    tmp.append(plist[b])
                
                if hlp < 8 and self.flag_view == Renderer.CLOSED :
                    tmp.append(plist[0])
    
                GL.glMap1f(GL.GL_MAP1_VERTEX_3, 0.0, 1.0, tmp)
    
                GL.glBegin(GL.GL_LINE_STRIP)
                for i in range (0, 31, 1):
                    GL.glEvalCoord1f(i/30.0)
                GL.glEnd()
                if (hlp < 8) :
                    break
        else :
            print "NOTHING"

        #The following code displays the control points as dots.
        i = 0
        GL.glPointSize(5.0)        
        GL.glColor3f(1.0, 0.0, 0.0)
        GL.glBegin(GL.GL_POINTS)
        for i in range (0, len(vecX), 1):
            GL.glVertex3f(vecX[i], vecZ[i], vecY[i])
        GL.glEnd()  
    
    def to_opengl_bezier_list(self, l1, l2, l3):
        res = []
        for i in range(0, len(l1)) :
            res.append([ l1[i], l2[i], l3[i] ])
        return res

    def creatBezierList(self, t, l1, l2, l3):
        res = []
        
        for z in range(0, len(l1)) :
            res.append([ l1[z], l2[z], l3[z] ])
        
        for a in range(0, len(l1), 1) :  
            tmp = []
            hlp = 4 if a < len(l1) - 3 else len(l2) - a
                
            if hlp < 4 : break
                
            for b in range (a, a + hlp, 1) :
                tmp.append([ l1[b], l2[b], l3[b] ])
                  
            for i in range(0, t, 1):
                pos = i*1.0 / t
                x = self.bezierCurve(pos, tmp[0][0], tmp[1][0], tmp[2][0], tmp[3][0])
                y = self.bezierCurve(pos, tmp[0][1], tmp[1][1], tmp[2][1], tmp[3][1])
                z = self.bezierCurve(pos, tmp[0][2], tmp[1][2], tmp[2][2], tmp[3][2])
                
                res.append([x,y,z])            
            
            res.sort(cmp=self.compare(), key=None, reverse=False)
            
            for u in range(0, len(res))

    def compare(self, x1, x2):
        return x1[0] > x2[0]
        
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

    def norm_vec_list(self, vlist):
        '''set points to center (0,0)'''
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
        if event.modifiers() == QtCore.Qt.ControlModifier and event.key() == QtCore.Qt.Key_N :
            if self.renderer.flag_view_algo > 2 :
                self.renderer.flag_view_algo = 0
            else : self.renderer.flag_view_algo += 1
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