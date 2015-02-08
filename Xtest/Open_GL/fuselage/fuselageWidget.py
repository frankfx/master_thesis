'''
Created on Oct 8, 2014

@author: fran_re
'''
import sys
import math
from Xtest import utility
from PySide import QtGui
from Xtest.Open_GL.profileOGLWidget import ProfileOGLWidget

try:
    from OpenGL import GL
except ImportError:
    app = QtGui.QApplication(sys.argv)
    QtGui.QMessageBox.critical(None, "OpenGL hellogl",
                              "PyOpenGL must be installed to run this example.",
                            QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default,
                            QtGui.QMessageBox.NoButton)
    sys.exit(1)

class FuselageWidget(ProfileOGLWidget):
    def __init__(self, profile):
        ProfileOGLWidget.__init__(self, profile)
    
    @utility.overrides(ProfileOGLWidget)
    def drawProfile(self):
        trX, _ = self.norm_vec_list(self.profile.getPointList())
        
        plist  = self.getChaikinSplineCurve() if self.getFlagChaikinSpline() else self.profile.getPointList() 

        GL.glColor3f(0, 0, 1)  
        GL.glRotatef(self.xRot, 1.0, 0.0, 0.0)
        GL.glRotatef(self.yRot, 0.0, 1.0, 0.0)
        GL.glRotatef(self.zRot, 0.0, 0.0, 1.0)

        print "Rotations: " , self.xRot , self.yRot , self.zRot

        # rotate around y to see the profile
        GL.glRotatef(90,0,1,0)      
        
        #GL.glTranslatef(-trX, 0, 0) 
        GL.glBegin(GL.GL_LINE_STRIP) 
        print "plist, before paint: "
        print plist
        for p in plist :
            GL.glVertex3f(p[0], p[1], p[2])              
        GL.glEnd()            

        # draw profile points
        if self.getFlagDrawPoints() :
            self.drawPoints(plist)

        GL.glFlush()    

    def createSuperEllipse(self, topSide, botSide):
        plist_t = self.__createSuperEllipse(topSide[0], topSide[1], topSide[2], topSide[3], topSide[4], True)
        plist_b = self.__createSuperEllipse(botSide[0], botSide[1], botSide[2], botSide[3], botSide[4], False)        
        
        self.profile.setPointList(plist_t + plist_b)
        self.updateGL() 

    def __createSuperEllipse(self, a=1.0, b=1.0, m=4.0, n=4.0, cnt=100, isTopSide=True):
        """creates a super-ellipse with Cartesian equation : 
                |x/a|^m + |y/b|^n = 1 

           converted to: 
                y = ( (1 -(x/a)^m) ^ (1/n) ) / b
            
        Args:
            a (float): half-axes 
            b (float): half-axes
            m (float): exponent of a, default: 4.0
            n (float): exponent of b, default: 4.0
            cnt (float): count of points
            isTopSide (Bool): ...
        Returns:
            pointList of half super-ellipse specified by boolean "isTopSide"
        """      

        # set first x and run on x-axis from -a to a in "dist" steps
        x = -a
        
        print a, cnt
        dist = (2.0 * a) / cnt

        print "dist" ,dist

        plist = []
        
        while x < a or utility.equalFloats2(x, a) :

            
            tmp = utility.absolut(x / a)
            tmp = utility.absolut(1.0 - math.pow(tmp, m ))            
            
            y = math.pow(tmp , 1/n ) / b
            
            plist.append([0, y, x]) if isTopSide else plist.append([0, -y, x])
            x += dist 

            print a, x, dist
        
        print "plist after calc"
        print plist
        return plist

            
    def drawPoints(self, plist):
        GL.glColor3f(1.0, 0.0, 0.0)
        GL.glPointSize(5)
        GL.glBegin(GL.GL_POINTS)    
        for p in plist :
            GL.glVertex3f(p[0], p[1], p[2])              
        GL.glEnd() 
        
        GL.glColor3f(0.0, 0.0, 1.0)
        GL.glBegin(GL.GL_POINTS)
        GL.glVertex3f(plist[0][0], plist[0][1], plist[0][2])  
        GL.glEnd() 