'''
Created on Oct 8, 2014

@author: fran_re
'''
import sys
import math
import utility
from profileWidget import ProfileWidget
from airfoil import Airfoil
from PySide import QtGui

try:
    from OpenGL import GL
except ImportError:
    app = QtGui.QApplication(sys.argv)
    QtGui.QMessageBox.critical(None, "OpenGL hellogl",
                              "PyOpenGL must be installed to run this example.",
                            QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default,
                            QtGui.QMessageBox.NoButton)
    sys.exit(1)

class AirfoilWidget(ProfileWidget):
    def __init__(self, profile):
        ProfileWidget.__init__(self, profile)

        self.flag_close_TrailingEdge = False
        self.flag_draw_camber        = False
        self.flag_draw_chord         = False        
        
        
    @utility.overrides(Airfoil)
    def drawProfile(self):
        trX, _ = self.norm_vec_list(self.profile.getPointList())
        plist  = self.getSplineCurve() if self.getFlagSplineCurve() else self.profile.getPointList()         
        
        GL.glColor3f(0, 0, 1)  
        # rotate profile in space
        GL.glRotatef(self.xRot, 1.0, 0.0, 0.0)
        GL.glRotatef(self.yRot, 0.0, 1.0, 0.0)       
        
        # translate to center point
        GL.glTranslatef(-trX, 0, 0) 

        # rotate around user given angle                  
        GL.glTranslatef(1,0,0)
        GL.glRotate(self.getRotAngle(), 0,0,1)
        GL.glTranslatef(-1,0,0)  
       
        # rotate around x to see the profile
        GL.glRotatef(90,1,0,0)       
     
        GL.glBegin(GL.GL_LINE_STRIP) 
        for p in plist :
            GL.glVertex3f(p[0], p[1], p[2])              
        GL.glEnd()            

        if self.getFlagDrawCamber() :      
            self.drawCamber() 

        if self.getFlagDrawChord() :
            self.drawChord()

        # The Trailing edge
        if self.getFlagCloseTrailingEdge() :
            self.drawTrailingEdge(self.profile.getTrailingEdge())

        # draw profile points
        if self.getFlagDrawPoints() :
            self.drawPoints(plist)
            
    def drawPoints(self, plist):
        GL.glColor3f(1.0, 0.0, 0.0)
        GL.glPointSize(5)
        GL.glBegin(GL.GL_POINTS)    
        for p in plist :
            GL.glVertex3f(p[0], p[1], p[2])              
        GL.glEnd()             
            
    def drawTrailingEdge(self, p):
        plist = self.profile.getPointList()
        p1 = plist[0]
        p2 = plist[len(plist)-1]
        GL.glBegin(GL.GL_LINE_STRIP)
        GL.glVertex3f(p1[0], p1[1], p1[2])
        GL.glVertex3f(p[0], p[1], p[2])
        GL.glVertex3f(p2[0], p2[1], p2[2])
        GL.glEnd()               
            
    def drawChord(self):
        start, end = self.profile.getEndPoints()
        
        GL.glBegin(GL.GL_LINES)
        GL.glVertex3f(start[0], start[1], start[2]) # leftend (nose)
        GL.glVertex3f(end[0], end[1], end[2]) # right end
        GL.glEnd()

    def drawCamber(self):
        GL.glBegin(GL.GL_LINE_STRIP)
        for p in self.profile.getPointListCamber() :
            GL.glVertex3f(p[0], p[1], p[2])# left end == nose
        GL.glEnd()            
            
    def setFlagDrawCamber(self, value):
        self.flag_draw_camber = value
        
    def setFlagDrawChord(self, value):
        self.flag_draw_chord = value

    def setFlagCloseTrailingEdge(self, value):
        self.flag_close_TrailingEdge = value
            
    def getFlagCloseTrailingEdge(self):
        return self.flag_close_TrailingEdge
    
    def getFlagDrawCamber(self):
        return self.flag_draw_camber
    
    def getFlagDrawChord(self):
        return self.flag_draw_chord  

    # ================================================================================================================
    # profile generator
    # ================================================================================================================
    '''
    @summary: generating naca airfoils, based on http://en.wikipedia.org/wiki/NACA_airfoil
    NACA4  
    '''
    def createSym_Naca(self, length, thickness, pcnt=10):
        res_top = []
        res_bot = []
    
        c = length
        t = thickness
        plist = utility.createXcoordsCosineSpacing(c, pcnt)
    
        for x in plist:
            y = self.__computeY_t(x, c, t) 
            res_top.append([x,  y, 0])
            res_bot.append([x, -y, 0])
        
        res_bot.reverse()    
        self.profile.setPointList(res_bot + res_top[1:])
        self.profile.updateAll()
        self.updateGL()

    def createCambered_Naca(self, length, maxCamber, posMaxCamber, thickness, pcnt=10):
        res_top = []
        res_bot = []     
        res_camber = []   
        
        plist = utility.createXcoordsCosineSpacing(length, pcnt)
        for x in plist :
            y_t = self.__computeY_t(x, length, thickness)
            y_c = self.__computeY_c(x, length, maxCamber, posMaxCamber)
            theta = math.atan(self.__computeCamber(x, length, maxCamber, posMaxCamber))
            
            x_u = x - y_t * math.sin(theta)
            x_l = x + y_t * math.sin(theta)
            y_u = y_c + y_t * math.cos(theta)
            y_l = y_c - y_t * math.cos(theta)
            
            res_top.append([x_u, y_u, 0])
            res_bot.append([x_l, y_l, 0])
            res_camber.append([x, y_c, 0])
        res_bot.reverse()

        self.profile.setPointList(res_bot + res_top[1:])      
        self.profile.setPointListCamber(res_camber)
        self.profile.updatePointListsForNaca()
        self.profile.updateThickness()
        self.updateGL()

    def __computeY_c(self, x, length, maxCamber, posMaxCamber):
        m = maxCamber
        p = posMaxCamber
        c = length
        
        if x >= 0 and x < p*c :
            y = m * (x / (p*p)) * (2 * p - x / c) 
        elif x >= p*c and x <= c :
            y = m * ((c-x) / ((1-p)*(1-p))) * (1 + x/c - 2*p)
        return y
    
    def __computeY_t(self, x, c, t):
        tmp = -0.1036 if utility.equalFloats((x/c), 1) else -0.1015
        y = t/0.2 * c * math.fabs( ( 0.2969  * math.sqrt(x/c)   +
                        (-0.1260) * (x/c)            +
                        (-0.3516) * math.pow(x/c, 2) +
                        ( 0.2843) * math.pow(x/c, 3) +
                        (tmp)     * math.pow(x/c, 4)) )        
        return y

    '''
    @summary: generating naca airfoils, based on http://en.wikipedia.org/wiki/NACA_airfoil
    NACA5  
    '''
    def createCambered_Naca5(self, liftCoeff, posMaxCamber, reflex, thickness, pcnt=10):
        c  = 1.0
        p  = posMaxCamber*5/100.0
        t  = thickness/100.0
        cl = liftCoeff*(3.0/2.0) / 10.0        
        m , k1 , k2_k1 = self.__setConstantsOfP(p, reflex) # constant values 

        res_top , res_bot , res_camber = [] , [] , []
        plist = self.__createXcoordsCosineSpacing(c, pcnt)
        
        for x in plist :
            y_t = self.__computeY_t(x, c, t)
            
            if reflex: 
                if x >= 0 and x < m :
                    y_c = k1 / 6 * ((x-m)*(x-m)*(x-m) - k2_k1*(1-m)*(1-m)*(1-m)*x - m*m*m*x + m*m*m) 
                elif x >= m and x <= c :
                    y_c = k1 / 6 * (k2_k1*(x-m)*(x-m)*(x-m) - k2_k1*(1-m)*(1-m)*(1-m)*x - m*m*m*x + m*m*m)
            else :         
                if x >= 0 and x < m :
                    y_c = k1 / 6 * ( x*x*x - 3*m*x*x + m*m*(3-m) * x)
                elif x >= m and x <= c :
                    y_c = (k1 * m * m * m) / 6 * (1-x)  
            
            # constant values of the maximum camber at a coefficient for lift value at 0.3. 
            # The camber and gradient can be scaled linearly to the required Cl value.            
            y_c = y_c * cl / 0.3
            
            if reflex :
                if x >= 0 and x < m :
                    gradient = k1/6 * (3*(x-m)*(x-m) - k2_k1*(1-m)*(1-m)*(1-m) - m*m*m)
                elif x >= m and x <= c :
                    gradient = k1/6 * (3*k2_k1*(x-m)*(x-m) - k2_k1*(1-m)*(1-m)*(1-m) - m*m*m)
            else:
                if x >= 0 and x < m :
                    gradient = k1/6 * (3*x*x - 6*m*x + m*m*(3-m) )
                elif x >= m and x <= c :
                    gradient = - k1*m*m*m/6
            
            theta = math.atan(gradient*cl/0.3)
            
            x_u = x - y_t * math.sin(theta)
            x_l = x + y_t * math.sin(theta)
            y_u = y_c + y_t * math.cos(theta)
            y_l = y_c - y_t * math.cos(theta)

            res_top.append([x_u, y_u, 0])
            res_bot.append([x_l, y_l, 0])
            res_camber.append([x, y_c, 0])
        res_bot.reverse()

        self.profile.setPointList(res_bot + res_top[1:])      
        self.profile.setPointListCamber(res_camber)
        self.profile.updatePointListsForNaca()
        self.profile.updateThickness()        
        self.updateGL()

    def __setConstantsOfP(self, p, reflex):       
        if reflex :
            P = [0.1,0.15,0.2,0.25]
            M = [0.1300,0.2170,0.3180,0.4410]
            K = [51.990, 15.793,6.520,3.191]           
            K1_K2 = [0.000764, 0.00677, 0.0303, 0.1355]          
        else :
            P = [0.05,0.1,0.15,0.2,0.25]
            M = [0.0580,0.1260,0.2025,0.2900,0.3910]
            K = [361.4,51.64,15.957,6.643,3.230]
            K1_K2 = [None, None, None, None, None] 
        for i in range(0, len(P)) :
            if utility.equalFloats(p, P[i]):
                return M[i] , K[i], K1_K2[i]                  
        print "nix gefunden"
           
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
        return res