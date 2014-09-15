'''
Created on Jul 31, 2014

@author: fran_re
'''

import sys
import math
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


class CoordinateSystem():

    def __init__(self):

        # read vertex data from file
        f = open('graphics/ToyPlaneData.txt', 'r')
        self.vertSize = f.readline()
        
        if self.vertSize > 0 :
            self.toyPlaneData = [0] * int(self.vertSize)
            i = 0
            
            for vertData in f :
                if i < self.vertSize :
                    # store it in the vector
                    self.toyPlaneData[i] = float(vertData)
                i+=1
        f.close()

    def drawCoordinateAxisZ(self):
        #----------------- GL.glBegin(GL.GL_LINE_LOOP)     # circle in x-y plane
        #--------------------------------------------- for a in range(0,360,1) :
            #----------------------------------------- angle = math.pi / 180 * a
            #---------------- GL.glVertex3f(math.cos(angle), math.sin(angle), 0)
        #------------------------------------------------------------ GL.glEnd()
        
        GL.glBegin(GL.GL_LINES);
        GL.glVertex3f(0.9, 0.0, 0.0)    # x-axis
        GL.glVertex3f(1.0, 0.0, 0.0)
        GL.glVertex3f(0.0, 0.9, 0.0)    # y-axis
        GL.glVertex3f(0.0, 1.0, 0.0)
        GL.glVertex3f(0.0, 0.0,-1.0)    # z-axis
        GL.glVertex3f(0.0, 0.0, 1.0)
        GL.glEnd();
    
        GL.glBegin(GL.GL_TRIANGLES)     # z-axis tip
        GL.glVertex3f(0.0,-0.1, 0.9)
        GL.glVertex3f(0.0, 0.0, 1.0)
        GL.glVertex3f(0.0, 0.1, 0.9)
        GL.glEnd();        
            
    def drawCoordinateAxisX(self):
        GL.glPushMatrix()
        GL.glRotatef(90, 1, 0, 0)
        self.drawCoordinateAxisZ()
        GL.glPopMatrix()            
        
    def drawCoordinateAxisY(self):
        GL.glPushMatrix()
        GL.glRotatef(-90, 0, 1, 0)
        self.drawCoordinateAxisZ()
        GL.glPopMatrix()