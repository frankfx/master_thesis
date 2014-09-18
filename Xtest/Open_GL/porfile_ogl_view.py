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

    # ================================================================================================================
    # implement abstract method
    # ================================================================================================================
    def drawProfile(self):
        trX, trY = self.norm_vec_list(self.dataSet.pointList_top + self.dataSet.pointList_bot)

        GL.glColor3f(0, 0, 1)
        GL.glTranslatef(-trX, trY, 0)
        
        if self.getFlagBezierCurve():
            self.drawProfile_bezier(self.getPointListTop(), self.getPointListBot())
        else :
            self.drawProfile_default(self.getPointListTop(), self.getPointListBot())
        #self.drawChord()      
        #self.drawCamber() 

        #The Trailing edge
        if self.getFlagCloseTrailingEdge() :
            p1 = self.dataSet.getEndPoint(self.getPointListTop())
            p2 = self.dataSet.getEndPoint(self.getPointListBot())
            self.drawTrailingEdge(p1, p2)

        #The following code displays the control points as dots.
        if self.getFlagDrawPoints() :
            self.drawProfilePoints()
            
    # ================================================================================================================
    # specific drawing functions
    # ================================================================================================================
    def drawProfile_default(self, plist_top, plist_bot):
        GL.glBegin(GL.GL_LINE_STRIP)
        for i in range (0, len(plist_top)) :
            GL.glVertex3f(plist_top[i][0], plist_top[i][1], plist_top[i][2])
        for j in range (0, len(plist_bot)) :
            GL.glVertex3f(plist_bot[j][0], plist_bot[j][1], plist_bot[j][2])            
        GL.glEnd()
    
    # bezier functions  
    # ================================================================================================================ 
    def drawProfile_bezier(self, plist_top, plist_bot, step):
        p_list = self.createBezierList(plist_top + plist_bot, step)
        GL.glBegin(GL.GL_LINE_STRIP) 
        for i in range (0, len(p_list), 1) :
            GL.glVertex3f(p_list[i][0], p_list[i][1], p_list[i][2])              
        GL.glEnd()          
       
    def __bezierCurve_full(self, t, pList):
        # Curve with level n has n + 1 points : P0 ... Pn
        n = len(pList) - 1
        return self.__bezierCurve_full_rec(0, n, t, pList)

    def __bezierCurve_full_rec(self, i, n, t, pList):
        if i == n :
            return math.pow(t, i) * pList[i]
        else :
            return self.__compute_Bernsteinpolynom(i, n, t) * pList[i] + self.__bezierCurve_full_rec(i+1, n, t, pList)
            
    def __compute_Bernsteinpolynom(self,i, n, t):
        return math.factorial(n) / ( math.factorial(i) * math.factorial(n-i) ) * math.pow(t,i) * math.pow(1-t, n-i) 
       
    def createBezierList(self, plist, t=31):
        res = []
        start       = None
        tan1, tan2  = None
        end         = None
            
        for j in range(0, t, 1):
            pos = j*1.0 / t
            x = self.bezierCurve_full(pos, [ start[0], tan1[0], tan2[0], end[0] ])
            y = self.bezierCurve_full(pos, [ start[1], tan1[1], tan2[1], end[1] ])
            z = self.bezierCurve_full(pos, [ start[2], tan1[2], tan2[2], end[2] ])

            res.append([x,y,z])    
        res.append(plist[len(plist)-1])
        return res
    # ================================================================================================================


    # ================================================================================================================
    # profile generator
    # ================================================================================================================
    '''
    @summary: generating naca airfoils, based on http://en.wikipedia.org/wiki/NACA_airfoil    
    '''
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
        self.setPointListTop(res_top)
        self.setPointListBot(res_bot)
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
            res_bot.append([x_l, y_l, 0])
            res_camber.append([x, y_c, 0])
        self.setPointListTop(res_top)
        self.setPointListBot(res_bot)
        self.setPointListCamber(res_camber)
        self.dataSet.updatePointLists()
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
    
    def __computeY_c(self, x, length, maxCamber, posMaxCamber):
        m = maxCamber
        p = posMaxCamber
        c = length
        
        if x >= 0 and x < p*c :
            y = m * (x / (p*p)) * (2 * p - x / c) 
        elif x >= p*c and x <= c :
            
            print "((1-p)*(1-p)) * (1 + x/c - 2*p)"
            print "p (==posMaxCamber) = " , p , "x = " , x , "c (==length) = " , c ,
            
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


if __name__ == '__main__':
    app = QtGui.QApplication(["PyQt OpenGL"])
    widget = MyProfileWidget()
    widget.show()
    app.exec_()    