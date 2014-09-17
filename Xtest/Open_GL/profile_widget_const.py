'''
Created on Sep 8, 2014

@author: rene
'''

import sys
import math
from Xtest.Open_GL.profile_ogl import Profile
from PySide import QtOpenGL, QtGui, QtCore
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


class MyProfileWidget_Const(Profile):
    def __init__(self):
        Profile.__init__(self)
        
        self.resize(320,320)
        #self.setFixedSize(QtCore.QSize(400,400))
        self.setWindowTitle("Rene Test")
        #self.setFixedSize(QtCore.QSize(400,400))
        self.dx = 0.0
        self.dy = 0.0
        self.lastPos_x = 0.0
        self.lastPos_y = 0.0
        self.last_zoom = -1
        
        self.set_flag_view(Profile.CLOSED)
        self.setPointListTop([])
        self.setPointListBot([])    

    def slider_zoom(self, value):
        self.scale = (101 - value) / 100.0
        self.updateGL()

    def createSym_Naca(self, length, thickness, pcnt=10):
        res_top = []
        res_bot = []
    
        c = length
        t = thickness
        plist = self.__createXcoords(c, pcnt)
        print plist
    
        for x in plist:
            y = self.__computeY_t(x, c, t) 
            res_top.append([x,  y, 0])
            res_bot.append([x, -y, 0])
        self.setPointListTop(res_top)
        self.setPointListBot(res_bot)
        self.updateGL()

    def createCambered_Naca(self, length, thickness, maxCamber, posMaxCamber, pcnt=10):
        res_top = []
        res_bot = []        
        
        plist = self.__createXcoords(length, pcnt)
        
        for x in plist :
            x_u = x - self.__computeY_t(x, length, thickness) * math.sin(self.__computeCamber(x, length, maxCamber, posMaxCamber))
            x_l = x + self.__computeY_t(x, length, thickness) * math.sin(self.__computeCamber(x, length, maxCamber, posMaxCamber))
            y_u = self.__computeY_c(x, length, maxCamber, posMaxCamber) + self.__computeCamber(x, length, maxCamber, posMaxCamber) * math.cos(self.__computeCamber(x, length, maxCamber, posMaxCamber))
            y_l = self.__computeY_c(x, length, maxCamber, posMaxCamber) + self.__computeCamber(x, length, maxCamber, posMaxCamber) * math.cos(self.__computeCamber(x, length, maxCamber, posMaxCamber))
            res_top.append([x_u, y_u, 0])
            res_bot.append([x_l, y_l, 0])
        self.setPointListTop(res_top)
        self.setPointListBot(res_bot)
        self.updateGL()
           
    def __computeCamber(self, x, length, maxCamber, posMaxCamber):
        p = posMaxCamber
        m = maxCamber
        c = length
        
        if x >= 0 and x <= p*c :
            res = (2*m)/p * (p - x/c)
        elif x >= p*c and x <= c :
            res = 2*m / (math.pow(1-p,2)) * (p - x/c)
        else :
            return None
        return math.atan(res)
    
    def __computeY_c(self, x, length, maxChamber, posMaxChamber):
        m = maxChamber / 100.00
        p = posMaxChamber / 10.0
        c = length
        
        if x >= 0 and x <= p*c :
            y = m * (x / math.pow(p, 2)) * (2 * p - x / c) 
        elif x >= p*c and x <= c :
            y = m * ((c-x) / math.pow((1-p),2)) * (1 + x/c - 2*p)
    
    def __computeY_t(self, x, c, t):
        tmp = -0.1036 if (x/c) == 1 else -0.1015
        y = t/0.2 * c * ( 0.2969  * math.sqrt(x/c)   +
                        (-0.1260) * (x/c)            +
                        (-0.3516) * math.pow(x/c, 2) +
                        ( 0.2843) * math.pow(x/c, 3) +
                        (tmp)     * math.pow(x/c, 4))        
        return y

    def __createXcoords(self, dist=1.0, point_cnt=35):
        
        interval = round(dist/ point_cnt,5)
        print interval  
        
        res = [0]
        for i in range(0, point_cnt):
            p = round(res[i] + interval, 3)
            res.append(p)
            
        print res
        return res


    def drawProfile(self):
        if self.pointList_top == [] : return
        if self.get_flag_view() == Profile.OPEN : shape = GL.GL_LINE_STRIP
        else : shape = GL.GL_LINE_LOOP
        
        print self.pointList_top
        GL.glColor3f(0, 0, 1)
        GL.glTranslatef(-self.norm_vec_list(self.pointList_top),0, 0)
        
        self.drawProfile_default(self.pointList_top, self.pointList_bot, shape)
        #self.drawProfile_bezier(self.pointList_top, self.pointList_bot, shape, self.testValue)
        #self.drawProfile_openGL(self.pointList_top, self.pointList_bot, shape, 5)
       
        #The following code displays the control points as dots.
        if self.flag_draw_points :
            self.drawProfile_points()

    def drawProfile_default(self, top_prof, bot_prof, shape):
        if top_prof == [] :
            return
        p_list = top_prof# + bot_prof
        GL.glBegin(shape)
        for i in range (0, len(p_list)) :
            GL.glVertex3f(p_list[i][0], p_list[i][1], p_list[i][2])
        GL.glEnd()  
        #self.drawChord()      
        self.drawCamber()


  

if __name__ == '__main__':
    app = QtGui.QApplication(["PyQt OpenGL"])
    widget = MyProfileWidget_Const()
    widget.show()
    app.exec_()    