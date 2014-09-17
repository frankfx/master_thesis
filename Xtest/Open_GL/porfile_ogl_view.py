'''
Created on Jul 30, 2014

@author: fran_re
'''
import sys
import math
from Xtest.Open_GL.profile_ogl import Profile
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


class MyProfileWidget(Profile):
    def __init__(self):
        Profile.__init__(self)
        
        self.resize(320,320)
        self.setMinimumHeight(200)
        self.setSizePolicy ( QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        #self.setFixedSize(QtCore.QSize(400,400))
        self.setWindowTitle("Rene Test")
        #self.setFixedSize(QtCore.QSize(400,400))
        self.dx = 0.0
        self.dy = 0.0
        self.lastPos_x = 0.0
        self.lastPos_y = 0.0
        self.last_zoom = -1

    def slider_zoom(self, value):
        self.scale = (101 - value) / 100.0
        self.updateGL()

    def createSym_Naca(self, length, thickness, pcnt=10):
        res_top = []
        res_bot = []
    
        c = length
        t = thickness
        plist = self.__createXcoords(c, pcnt)
    
        for x in plist:
            y = self.__computeY_t(x, c, t) 
            res_top.append([x,  y, 0])
            res_bot.append([x, -y, 0])
        self.dataSet.setPointListTop(res_top)
        self.dataSet.setPointListBot(res_bot)
        self.updateGL()

    def createCambered_Naca(self, length, thickness, maxCamber, posMaxCamber, pcnt=10):
        res_top = []
        res_bot = []     
        res_camber = []   
        
        plist = self.__createXcoords(length, pcnt)
        for x in plist :
            y_t = self.__computeY_t(x, length, thickness)
            y_c = self.__computeY_c(x, length, maxCamber, posMaxCamber)
            theta = self.__computeCamber(x, length, maxCamber, posMaxCamber)
            
            x_u = x - y_t * math.sin(theta)
            x_l = x + y_t * math.sin(theta)
            y_u = y_c + y_t * math.cos(theta)
            y_l = y_c - y_t * math.cos(theta)
            
            res_top.append([x_u, y_u, 0])
            print "res_top" , [x_u, y_u, 0]
            print "res_bot" , [x_l, y_u, 0]
            res_bot.append([x_l, y_l, 0])
            res_camber.append([x, y_c, 0])
        self.dataSet.setPointListTop(res_top)
        self.dataSet.setPointListBot(res_bot)
        self.dataSet.setPointListCamber(res_camber)
        self.dataSet.updatePointlistCamber()
        self.updateGL()
        
           
    def __computeCamber(self, x, length, maxCamber, posMaxCamber):
        p = posMaxCamber
        m = maxCamber
        c = length
        
        if x >= 0 and x <= p*c :
            res = (2*m)/(p*p) * (p - x/c)
        elif x >= p*c and x <= c :
            res = 2*m / ((1-p)*(1-p)) * (p - x/c)
        else :
            return None
        return math.atan(res)
    
    def __computeY_c(self, x, length, maxChamber, posMaxChamber):
        m = maxChamber
        p = posMaxChamber
        c = length
        
        if x >= 0 and x < p*c :
            y = m * (x / (p*p)) * (2 * p - x / c) 
        elif x >= p*c and x <= c :
            y = m * ((c-x) / ((1-p)*(1-p))) * (1 + x/c - 2*p)
        return y
    
    def __computeY_t(self, x, c, t):
        tmp = -0.1036 if (x/c) == 1 else -0.1015
        y = t/0.2 * c * math.fabs( ( 0.2969  * math.sqrt(x/c)   +
                        (-0.1260) * (x/c)            +
                        (-0.3516) * math.pow(x/c, 2) +
                        ( 0.2843) * math.pow(x/c, 3) +
                        (tmp)     * math.pow(x/c, 4)) )        
        return y


    def __createXcoords(self, dist=1.0, point_cnt=35):
        
        
        interval = dist/ point_cnt
        
        res = [0]
        for i in range(0, point_cnt):
            p = round(res[i] + interval, 3)
            if p < dist : 
                res.append(p)
            elif p == dist : 
                res.append(p)
                return res
            else :
                break
        
        res.append(dist)
        return res


    def drawProfile_bezier(self, plist):
        GL.glBegin(GL.GL_LINE_STRIP) 
        for i in range (0, len(plist), 1) :
            GL.glVertex3f(plist[i][0], plist[i][1], plist[i][2])              
        GL.glEnd()       


    #---------------------------------------------------- def drawProfile(self):
#------------------------------------------------------------------------------ 
        #------------------------------- profi = self.dataSet.createBezierList()
        #----------------------------------------------- print "hier444" , profi
        #---------------------------------- trX, trY = self.norm_vec_list(profi)
#------------------------------------------------------------------------------ 
#------------------------------------------------------------------------------ 
        #------------------------------------------------- GL.glColor3f(0, 0, 1)
        #----------------------------------------- GL.glTranslatef(-trX, trY, 0)
#------------------------------------------------------------------------------ 
        #---------------------------------------- self.drawProfile_bezier(profi)
#------------------------------------------------------------------------------ 
        #--------------------------------------------------- #The Trainling edge
        #--------------------------------- if self.getCloseTrailingEdgeValue() :
            #--------- p1 = self.dataSet.getEndPoint(self.dataSet.pointList_top)
            #--------- p2 = self.dataSet.getEndPoint(self.dataSet.pointList_bot)
            #------------------------------------- self.drawTrailingEdge(p1, p2)
#------------------------------------------------------------------------------ 
        #-------------- #The following code displays the control points as dots.
        #-------------------------------------------- if self.flag_draw_points :
            #----------------------------------------- self.drawProfile_points()



    def drawProfile(self):

        trX, trY = self.norm_vec_list(self.dataSet.pointList_top + self.dataSet.pointList_bot)

        GL.glColor3f(0, 0, 1)
        GL.glTranslatef(-trX, trY, 0)

        if self.rotate == 0 :
            self.drawProfile_default(self.dataSet.pointList_top, self.dataSet.pointList_bot)
        else:
            self.drawProfile_default(self.dataSet.pointList_top, self.dataSet.pointList_bot)
          # self.drawProfile_bezier(self.pointList_top, self.pointList_bot, shape, self.testValue)
          # self.drawProfile_openGL(self.pointList_top, self.pointList_bot, shape, 5)

        #The Trainling edge
        if self.getCloseTrailingEdgeValue() :
            p1 = self.dataSet.getEndPoint(self.dataSet.pointList_top)
            p2 = self.dataSet.getEndPoint(self.dataSet.pointList_bot)
            self.drawTrailingEdge(p1, p2)

        #The following code displays the control points as dots.
        if self.flag_draw_points :
            self.drawProfile_points()

    def drawProfile_default(self, top_prof, bot_prof):
        self.drawProfile_default_hlp(top_prof)
        self.drawProfile_default_hlp(bot_prof)
        #self.drawChord()      
        self.drawCamber()        

    def drawProfile_default_hlp(self, plist):
        GL.glBegin(GL.GL_LINE_STRIP)
        for i in range (0, len(plist)) :
            GL.glVertex3f(plist[i][0], plist[i][1], plist[i][2])
        GL.glEnd()
        
    def drawTrailingEdge(self, p1, p2):
        GL.glBegin(GL.GL_LINES)
        GL.glVertex3f(p1[0], p1[1], p1[2])
        GL.glVertex3f(p2[0], p2[1], p2[2])
        GL.glEnd()        

if __name__ == '__main__':
    app = QtGui.QApplication(["PyQt OpenGL"])
    widget = MyProfileWidget()
    widget.show()
    app.exec_()    