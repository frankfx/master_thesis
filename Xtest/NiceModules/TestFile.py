'''
Created on Feb 9, 2015

@author: fran_re
'''
import sys
import re

from tiglwrapper   import Tigl, TiglException
from tixiwrapper   import Tixi, TixiException

from lxml import etree

import numpy as np

import matplotlib
matplotlib.use('Qt4Agg')
matplotlib.rcParams['backend.qt4']='PySide'
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from PySide import QtOpenGL, QtGui, QtCore

try:
    from OpenGL import GL, GLU
except ImportError:
    app = QtGui.QApplication(sys.argv)
    QtGui.QMessageBox.critical(None, "OpenGL hellogl",
                              "PyOpenGL must be installed to run this example.",
                            QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default,
                            QtGui.QMessageBox.NoButton)
    sys.exit(1)

class Renderer():
    def __init__(self, width, height):
        self._angleY = -70
        self._angleX = -70
        self.test()
        
    def test(self):
        # lxml test    
        try:
            root = etree.Element("root")
            print (root.tag)
            print ("lxml ok")
        except ImportError :
            print ("import error lxml")
        
        # matplot test
        try:
            figure = Figure(figsize=(5,4), dpi=100)
            plot   = figure.add_subplot(111)
            canvas = FigureCanvas(figure)
            print ("matplotlib ok")
        except ImportError :
            print ("import error matplotlib")
        
        # tixi, tigl
        try:
            tixi = Tixi()
            tixi.openDocument("toolOutput.xml")
            print ("tixi ok")
        except TixiException :
            print ("import error Tixi")     
        
        try:
            tigl = Tigl()
            tigl.open(tixi,"") 
            print ("tigl ok")            
        except TixiException :
            print ("import error Tigl")    
         
        try:
            np.arange(10000000)
            print ("numpy ok")
        except TixiException :
            print ("import error numpy") 
        
        
    def init(self):
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_COLOR_MATERIAL)
        GL.glEnable(GL.GL_LIGHTING)
        GL.glEnable(GL.GL_LIGHT0)
        GL.glEnable(GL.GL_LIGHT1)
        GL.glEnable(GL.GL_NORMALIZE)
        GL.glShadeModel(GL.GL_SMOOTH)
        print ("opengl ok")
    
    def resize(self, w, h):
        GL.glViewport(0, 0, w, h)
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GLU.gluPerspective(45.0, 1.0*w / h, 1.0, 200.0)        

    def display(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT) 
        
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()                

        GL.glTranslatef(0.0, 0.0, -8.0)
        
        self.plist = [  [-1.5, -1.0, 1.5], [1.5, -1.0, 1.5], [1.5, 1.0, 1.5], [-1.5, 1.0, 1.5],
                        [1.5, -1.0, -1.5], [1.5, 1.0, -1.5], [1.5, 1.0, 1.5], [1.5, -1.0, 1.5],
                        [-1.5, -1.0, -1.5], [-1.5, 1.0, -1.5], [1.5, 1.0, -1.5], [1.5, -1.0, -1.5] ]


        GL.glBegin(GL.GL_QUADS)
        for point in self.plist :
            GL.glVertex3fv(point)      
        GL.glEnd()
        

        


class Widget(QtOpenGL.QGLWidget):
    def __init__(self, parent = None):
        super(Widget, self).__init__(parent)
        self.width = 800
        self.height = 800
        self.resize(self.width ,self.height)
      
        grid = QtGui.QGridLayout()
        self.setLayout(grid)
        
        self.setSizePolicy ( QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.renderer = Renderer(self.width ,self.height)
    
        print ("pyside ok")
    
    def initializeGL(self):
        self.renderer.init()
    
    def resizeGL(self, w, h):
        self.renderer.resize(w, h)
 
    def paintGL(self):
        self.renderer.display()
    
if __name__ == '__main__':
    app = QtGui.QApplication(["PyQt OpenGL"])
    widget = Widget()
    widget.show()
    app.exec_()    