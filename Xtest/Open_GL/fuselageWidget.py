'''
Created on Oct 8, 2014

@author: fran_re
'''
import sys
import math
import utility
from fuselage import Fuselage
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

class FuselageWidget(Fuselage):
    def __init__(self, plist):
        Fuselage.__init__(self, plist)
        
        self.resize(320,320)
        self.setMinimumHeight(200)
        self.setSizePolicy ( QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
    
    @utility.overrides(Fuselage)
    def drawProfile(self):
        trX, _ = self.norm_vec_list(self.getPointList())
        
        GL.glTranslatef(-trX, 0, 0) 
        GL.glColor3f(0, 0, 1)
        
        plist = self.getSplineCurve() if self.getFlagSplineCurve() else self.getPointList()  
        
        GL.glBegin(GL.GL_LINE_STRIP) 
        for p in plist :
            GL.glVertex3f(p[0], p[1], p[2])              
        GL.glEnd()            

        #The following code displays the control points as dots.
        if self.getFlagDrawPoints() :
            self.drawPoints(plist)
            