'''
Created on Jul 30, 2014

@author: fran_re
'''
import sys
from PySide import QtOpenGL, QtGui, QtCore
from cpacsHandler import CPACS_Handler
from config import Config
from PySide.QtGui import QPushButton
from Xtest.BezierTest import Bezier

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
    def __init__(self, tixi):
        self.tixi = tixi
        self.scale = 1.0
        self.trans_x = 0
        self.trans_y = 0
        self.width = -1
        self.height = -1
        self.fovy = 64.0
        self.besier = Bezier()
        self.flag = 0
        self.ctrlpoints = [
                          [-0.4, -0.4, 0.0],
                          [-0.2,  0.4, 0.0],
                          [ 0.2, -0.4, 0.0],
                          [ 0.4,  0.4, 0.0]
                         ]        

    def init(self):
        # GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_COLOR_MATERIAL)
        GL.glClearColor(1.0, 1.0 , 1.0, 1.0)        

        GL.glShadeModel(GL.GL_FLAT)
    
    def resize(self, w, h):
        self.width , self.height = w , h
        GL.glViewport(0,0,w,h) #if w <= h else GL.glViewport(0,0,h,h) 
                                   
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        #GLU.gluPerspective (self.fovy * self.scale, w*1.0/h, 0.0, 10.0)
        
    def display(self):
        
        #------------------------------------------------------------------ i= 0
#------------------------------------------------------------------------------ 
        #------------------------------------ GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        #------------------------------------------- GL.glColor3f(0.0, 0.0, 0.0)
        #------------------------------------------ GL.glBegin(GL.GL_LINE_STRIP)
        #----------------------------------------------- for i in range(0, 31) :
            #------------------------------------------ GL.glEvalCoord1f(i/30.0)
        #------------------------------------------------------------ GL.glEnd()
        #-------- ''' The following code displays the control points as dots.'''
        #--------------------------------------------------- GL.glPointSize(5.0)
        #------------------------------------------- GL.glColor3f(1.0, 1.0, 0.0)
        #---------------------------------------------- GL.glBegin(GL.GL_POINTS)
        #------------------------------------------------- for j in range(0, 4):
            # GL.glVertex3f(self.ctrlpoints[j][0], self.ctrlpoints[j][1], self.ctrlpoints[j][2])
        #------------------------------------------------------------ GL.glEnd()
        
        
        
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GLU.gluPerspective (self.fovy * self.scale, self.width*1.0/self.height, 0.0, 10.0)

        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()

        GL.glTranslatef(self.trans_x,self.trans_y,-1.5)

        self.drawGrid()
        self.drawProfile()

        GL.glFlush()                # clean puffer, execute all puffered commands


    def drawProfile(self):
        vecX = self.tixi.getVectorX('NACA0009')
        vecY = self.tixi.getVectorY('NACA0009')
        vecZ = self.tixi.getVectorZ('NACA0009')
        
        chord_min_idx = self.get_index_of_min(vecX)
        chord_max_idx = self.get_index_of_max(vecX)

        if(self.flag == 0):
            print "bezier"
            vecX2 = self.createBezierList(vecX)
            vecY2 = self.createBezierList(vecY)
            vecZ2 = self.createBezierList(vecZ)  
            # draw profile        
            GL.glColor3f(0, 0, 1)
            #GL.glTranslatef(-self.norm_vec_list(vecX),0, 0)
            #GL.glTranslatef(self.tx, self.ty, 0)
            GL.glBegin(GL.GL_LINE_LOOP)
            for i in range (0, len(vecX2)) :
                for j in range (0, 4) :
                    GL.glVertex3f(vecX2[i], vecZ2[i], vecY2[i])
            GL.glEnd()             
        elif(self.flag == 1) :
            print "normal"
            # draw profile        
            GL.glColor3f(0, 0, 1)
            #GL.glTranslatef(-self.norm_vec_list(vecX),0, 0)
            #GL.glTranslatef(self.tx, self.ty, 0)
            GL.glBegin(GL.GL_LINE_LOOP)
            for i in range (0, len(vecX)) :
                GL.glVertex3f(vecX[i], vecZ[i], vecY[i])
            GL.glEnd()
        else:
            i= 0
            vec = self.createList(vecX, vecZ, vecY)
            
            GL.glMap1f(GL.GL_MAP1_VERTEX_3, 0.0, 1.0, vec)
            GL.glEnable(GL.GL_MAP1_VERTEX_3)
            
            GL.glBegin(GL.GL_LINE_STRIP)
            for i in range(0, 31) :
                GL.glEvalCoord1f(i/30.0)
            GL.glEnd()

 
 
 
 
 
 
 
 
#        def drawSomething(self):

          
          
        # draw profile        
        #GL.glTranslatef(-self.norm_vec_list(vecX),0, 0)
        #GL.glTranslatef(self.tx, self.ty, 0)

        
        # draw chord
        #------------------------------------------- GL.glLineStipple(2, 0xAAAA)
        #--------------------------------------- GL.glEnable(GL.GL_LINE_STIPPLE)
        #----------------------------------------------- GL.glBegin(GL.GL_LINES)
        # GL.glVertex3f(vecX[chord_min_idx], vecZ[chord_min_idx], vecY[chord_min_idx])
        # GL.glVertex3f(vecX[chord_max_idx], vecZ[chord_max_idx], vecY[chord_max_idx])
        #------------------------------------------------------------ GL.glEnd()
        #-------------------------------------- GL.glDisable(GL.GL_LINE_STIPPLE)
    
    def createBezierList(self, vlist):
        res = []
        
        for i in range(0, len(vlist)-3, 4) :
            t = 0
            while True :
                if (t>1.0) :
                    break
                res.append( self.besier.bezier(vlist[i], vlist[i+1], vlist[i+2], vlist[i+3],t) )
                t += 0.001  

        return res


    def createList(self, list1, list2, list3):
        res = []
        res2 = []
        
        for i in range(0, len(list1), 1) :
            res.append([list1[i],list2[i],list3[i]])
            
        lengthres = len(res)
        for j in range(0, lengthres-3, 4) :
            res2.append([ res[j], res[j+1], res[j+2], res[j+3] ])
        
        print res2
        
        return res2


    def get_index_of_min(self, vlist):
        res = vlist[0]
        index = 0

        for i in range (1, len(vlist), 1) :
            if vlist[i] < res :
                res = vlist[i]
                index = i
        
        return index

    def get_index_of_max(self, vlist):
        res = vlist[0]
        index = 0

        for i in range (1, len(vlist), 1) :
            if vlist[i] > res :
                res = vlist[i]
                index = i
        
        return index

    
    def getIndex_of_list_minimum(self, vlist):
        resMin = vlist[0]
        resMax = vlist[0]
        indexMin = 0
        indexMax = 0
        for i in range (1, len(vlist), 1) :
            if vlist[i] < resMin :
                resMin = vlist[i]
                indexMin = i
            elif vlist [i] > resMax :
                resMax = vlist[i]
                indexMax = i
                
        return [(indexMin, resMin),(indexMax, resMax)]
                
        
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
            if self.renderer.flag > 2 :
                self.renderer.flag = 0
            else : self.renderer.flag += 1
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