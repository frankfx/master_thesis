'''
Created on Jul 30, 2014

@author: fran_re
'''
import sys
import math
from Xtest.Open_GL.profile_widget import Profile_Widget
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


class MyWidget(Profile_Widget):
    def __init__(self):
        Profile_Widget.__init__(self)
        
        self.resize(320,320)
        #self.setFixedSize(QtCore.QSize(400,400))
        self.setWindowTitle("Rene Test")
        #self.setFixedSize(QtCore.QSize(400,400))
        self.dx = 0.0
        self.dy = 0.0
        self.lastPos_x = 0.0
        self.lastPos_y = 0.0
        self.last_zoom = -1
        
        self.set_flag_view(Profile_Widget.CLOSED)    
    
    def initializeGL(self):
        self.init()
    
    def resizeGL(self, w, h):
        self.resize(w, h)
 
    def paintGL(self):
        self.display()

    def zoom(self, value):
        self.scale = (101 - value) / 100.0
        self.updateGL()

    def getFlagDrawPoints(self):
        return self.flag_draw_points

    def setFlagDrawPoints(self, value):
        self.flag_draw_points = value
        self.updateGL()


    def drawProfile(self):

        if self.get_flag_view() == Profile_Widget.OPEN : shape = GL.GL_LINE_STRIP
        else : shape = GL.GL_LINE_LOOP
        
        GL.glColor3f(0, 0, 1)
        GL.glTranslatef(-self.norm_vec_list(self.pointList_top),0, 0)
        
        self.drawProfile_default(self.pointList_top, self.pointList_bot, shape)
        # self.drawProfile_bezier(self.pointList_top, self.pointList_bot, shape, self.testValue)
        # self.drawProfile_openGL(self.pointList_top, self.pointList_bot, shape, 5)
       
        #The following code displays the control points as dots.
        if self.flag_draw_points :
            self.drawProfile_points()

    def drawProfile_default(self, top_prof, bot_prof, shape):
        p_list = top_prof# + bot_prof
        GL.glBegin(shape)
        for i in range (0, len(p_list)) :
            GL.glVertex3f(p_list[i][0], p_list[i][1], p_list[i][2])
        GL.glEnd()  
        #self.drawChord()      
        self.drawSkeleton()


  

if __name__ == '__main__':
    app = QtGui.QApplication(["PyQt OpenGL"])
    widget = MyWidget()
    widget.show()
    app.exec_()    