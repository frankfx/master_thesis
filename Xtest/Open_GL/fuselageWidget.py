'''
Created on Oct 8, 2014

@author: fran_re
'''
import sys
import math
import utility
from fuselage import Fuselage
from PySide import QtGui
from profileWidget import ProfileWidget

try:
    from OpenGL import GL
except ImportError:
    app = QtGui.QApplication(sys.argv)
    QtGui.QMessageBox.critical(None, "OpenGL hellogl",
                              "PyOpenGL must be installed to run this example.",
                            QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default,
                            QtGui.QMessageBox.NoButton)
    sys.exit(1)

class FuselageWidget(ProfileWidget):
    def __init__(self, profile):
        ProfileWidget.__init__(self, profile)
    
    @utility.overrides(ProfileWidget)
    def drawProfile(self):
        trX, _ = self.norm_vec_list(self.profile.getPointList())
        
        plist  = self.getChaikinSplineCurve() if self.getFlagChaikinSpline() else self.profile.getPointList() 

        GL.glColor3f(0, 0, 1)  
        GL.glRotatef(self.xRot, 1.0, 0.0, 0.0)
        GL.glRotatef(self.yRot, 0.0, 1.0, 0.0)
        GL.glRotatef(self.zRot, 0.0, 0.0, 1.0)

        print self.xRot , self.yRot , self.zRot

        # rotate around y to see the profile
        GL.glRotatef(90,0,1,0)      
        
        #GL.glTranslatef(-trX, 0, 0) 
        GL.glBegin(GL.GL_LINE_STRIP) 
        for p in plist :
            GL.glVertex3f(p[0], p[1], p[2])              
        GL.glEnd()            

        # draw profile points
        if self.getFlagDrawPoints() :
            self.drawPoints(plist)

        GL.glFlush()    

    def createSuperEllipse(self, topSide, botSide):
        plist_t = self.__createSuperEllipse(topSide[0], topSide[1], topSide[2], topSide[3], 0.5, True)
        plist_b = self.__createSuperEllipse(botSide[0], botSide[1], botSide[2], botSide[3], 0.5, False)        
        
        self.profile.setPointList(plist_t + plist_b)
        self.updateGL() 

    def __createSuperEllipse(self, a=4.0, b=5.0, n=1.0, cnt=10, z=0.5, isTopSide=True):
        plist = []
        x = -a
        dist = (2.0*a) / cnt
        
        while x < a or utility.equalFloats2(x, a) :
            y = b * math.pow( utility.absolut(1 - math.pow( utility.absolut(x / a), 2/n) ), n/2 )
            if isTopSide : plist.append([x, y, z])
            else : plist.append([x, -y, z])
            x += dist 
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