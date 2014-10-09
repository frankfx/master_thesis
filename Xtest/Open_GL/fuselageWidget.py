'''
Created on Oct 8, 2014

@author: fran_re
'''
import sys
import math
import utility
from fuselage import Fuselage
from PySide import QtGui, QtCore
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
    
    @utility.overrides(Fuselage)
    def drawProfile(self):
        trX, _ = self.norm_vec_list(self.profile.getPointList())
        
        plist  = self.getSplineCurve() if self.getFlagSplineCurve() else self.profile.getPointList() 

        GL.glColor3f(0, 0, 1)  
        GL.glRotatef(self.xRot, 1.0, 0.0, 0.0)
        GL.glRotatef(self.yRot, 0.0, 1.0, 0.0)

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
        
    def drawPoints(self, plist):
        GL.glColor3f(1.0, 0.0, 0.0)
        GL.glPointSize(5)
        GL.glBegin(GL.GL_POINTS)    
        for p in plist :
            GL.glVertex3f(p[0], p[1], p[2])              
        GL.glEnd() 
        
 