'''
Created on Aug 22, 2014

@author: rene
'''

'''
Created on Jul 30, 2014

@author: fran_re
'''
import numpy as np
import cv2
import sys
from PySide import QtOpenGL, QtGui, QtCore
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
    def __init__(self):
        self.scale = 1.0
        self.trans_x = 0
        self.trans_y = 0
        self.width = -1
        self.height = -1
        self.fovy = 166.0

    def init(self):
        ()
    
    def resize(self, w, h):
        self.width , self.height = w , h
        GL.glViewport(0,0,w,h) 
                                   
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        v=1.5+self.scale
        print "v  ==============\n" , v
        GLU.gluPerspective (166.0, w*1.0/h, 0.0, 100.0)
        #--------------------------------------------------------- if (w <= h) :
            #-------------- GL.glFrustum(-v, v, -v * h / w, v * h / w, 1.1, 100)
        #---------------------------------------------------------------- else :
            #-------------- GL.glFrustum(-v * w / h, v * w / h, -v, v, 1.1, 100)
    
    def display(self):
        
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GLU.gluPerspective (self.fovy * self.scale, self.width*1.0/self.height, 0.0, 10.0)

        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()

        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
       
        
        GL.glTranslatef(self.trans_x,self.trans_y,0)

        #self.drawTriangle()
        self.drawProfile()
        GL.glFlush()    

    def drawTriangle(self):
        GL.glColor3f(1.0, 1.0, 1.0)
        GL.glBegin(GL.GL_POINTS)
        GL.glVertex3f(1.03, 3.59, -0.5)
        GL.glVertex3f(1.04, 3.58, -0.5)
        GL.glVertex3f(1.55, 3.5, -0.5)
        GL.glEnd()   
        
    def drawTriangle2(self):
        GL.glColor3f(1.0, 1.0, 1.0)
        GL.glBegin(GL.GL_TRIANGLES)
        GL.glVertex3f(-0.5, -0.5, -0.5)
        GL.glVertex3f( 0.5, -0.5, -0.5)
        GL.glVertex3f( 0.0,  0.5, -0.5)
        GL.glEnd()        
    
    def drawProfile(self):
        top, bot = self.splineProfile(0.2)
        
        trX, trY = self.norm_vec_list(top) 
        
        GL.glTranslatef(-trX, -trY, 0)
        GL.glColor3f(1.0, 1.0, 1.0)
        GL.glBegin(GL.GL_LINE_LOOP)        
        for i in range (0, len(top)) :
            GL.glVertex3f(top[i][0], top[i][1], top[i][2])
        GL.glEnd()
    
    def __getEndPoints(self, toplist, botlist):
        min_t, max_t = self.__get_min_max_of_List(toplist)
        min_b, max_b = self.__get_min_max_of_List(botlist)

        mini = min_t if min_t[0] < min_b[0] else min_b
        maxi = max_t if max_t[0] > max_b[0] else max_b
        maxi = [maxi[0], max_b[1] + (max_t[1] - max_b[1])/2, maxi[2]]

        return mini , maxi
   
    def __createPointList(self, plist, sort_desc = True):
        l_fst = []
        l_snd = []
        for i in range(0, len(plist)-1, 1) :
            if sort_desc:
                if(plist[i][0] > plist[i+1][0]) :
                    l_fst.append([ plist[i][0], plist[i][1], plist[i][2] ])
                else : 
                    l_fst.append([ plist[i][0], plist[i][1], plist[i][2] ])
                    break
            else :
                if plist[i][0] < plist[i+1][0] :
                    l_fst.append([ plist[i][0], plist[i][1], plist[i][2] ])
                else:
                    l_fst.append([ plist[i][0], plist[i][1], plist[i][2] ])
                    break                    

        for j in range(i, len(plist), 1) :
            l_snd.append([ plist[j][0], plist[j][1], plist[j][2] ])

        return l_fst , l_snd
   

    def printList(self, vlist):
        res = []
        for t in vlist :
            res.append(t[0])
        print "dsfasfs" ,res
    
    def splineProfile(self, distance):
        coord = self.detectProfile()
        toplist, botlist = self.__createPointList(coord)
        
        start, end = self.__getEndPoints(toplist, botlist)    
        resTop = [toplist[0]]
        resBot = [toplist[0]]
        
        cur = 0
        for i in range(1, len(toplist)) :
            if resTop[cur][0] + distance >= toplist[i][0] :
                resTop.append(toplist[i])
                cur += 1
        cur = 0
        for j in range(0, len(botlist)) :
            if resBot[cur][0] + distance >= botlist[i][0] :
                resBot.append(botlist[i])
                cur += 1
        
        return resTop, resBot
    
    def transformCoord(self, vlist):
        res = []
        for i in range (0, len(vlist)) :
            for j in range (0, len(vlist[i])) :
                res.append([vlist[i][j][0]/100.0, vlist[i][j][1]/100.0, -0.5])
        print "res" , res
        return res
    
    def detectProfile(self):        
        img = cv2.imread('wing3.jpg')
        gray = cv2.imread('wing3.jpg',0)

        ret,thresh = cv2.threshold(gray,127,255,1)
        contours,h = cv2.findContours(thresh,1,2)
        n = 0

        for cnt in contours:
            approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
            if len(approx)==5:
                n+=1
            if n == 2 :
                return self.transformCoord(cnt)


    def norm_vec_list(self, vlist):
        '''set points of shape to center (0,0)'''
        minX_list, maxX_list = self.__get_min_max_of_List(vlist)
        minY_list, maxY_list = self.__get_min_max_of_List(vlist,1)
        
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

        return shiftX , shiftY

    '''
    @param plist: format [ [x0,y0,z0] , [x1,y1,z1] , ...  ]
    @param dim: dimension e.g. 0==x, 1==y, 2==z 
    @return: minimum and maximum sublist compared by x 
    '''
    def __get_min_max_of_List(self, plist, dim=0):
        id_max = 0 
        id_min = 0
        for i in range (1, len(plist),1) :
            if plist[id_max][dim] < plist[i][dim] :
                id_max = i
            if plist[id_min][dim] > plist[i][dim] :
                id_min = i
        return plist[id_min], plist[id_max]

class AirfoilDetectorWidget(QtOpenGL.QGLWidget):
    def __init__(self, parent = None):
        super(AirfoilDetectorWidget, self).__init__(parent)
        self.resize(320,320)
        self.setWindowTitle("Rene Test")
        #self.setFixedSize(QtCore.QSize(400,400))
        self.dx = 0.0
        self.dy = 0.0
        self.lastPos_x = 0.0
        self.lastPos_y = 0.0
        
        self.renderer = Renderer()
    
    def initializeGL(self):
        self.renderer.init()
    
    def resizeGL(self, w, h):
        self.renderer.resize(w, h)
 
    def paintGL(self):
        self.renderer.display()

    def keyPressEvent(self, event):
        redraw = False
        offsetScl = 0.01
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
    widget = AirfoilDetectorWidget()
    widget.show()
    app.exec_()    