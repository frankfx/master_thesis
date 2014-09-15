'''
Created on Jul 31, 2014

@author: fran_re
'''

import sys
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


class Plane():
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

    def draw(self):
        # GL.glScale(self.scale,self.scale,self.scale)
        GL.glColor3f(0,5, 0.5, 0,5)
        GL.glBegin(GL.GL_TRIANGLES)
        for i in range(0, len(self.toyPlaneData), 3)  :
            GL.glVertex3d(self.toyPlaneData[i], self.toyPlaneData[i+1], self.toyPlaneData[i+2])       
        GL.glEnd()    