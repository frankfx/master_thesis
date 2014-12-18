'''
Created on Dec 16, 2014

@author: rene
'''

import sys
from PySide import QtOpenGL, QtGui, QtCore
import math

try:
    from OpenGL import GL, GLU, GLUT
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
        
    def init(self):
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_COLOR_MATERIAL)
        GL.glEnable(GL.GL_LIGHTING)
        GL.glEnable(GL.GL_LIGHT0)
        GL.glEnable(GL.GL_LIGHT1)
        GL.glEnable(GL.GL_NORMALIZE)
        GL.glShadeModel(GL.GL_SMOOTH)
    
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
 
        
        ambientColor = [0.2, 0.2, 0.2, 1.0]
        GL.glLightModelfv(GL.GL_LIGHT_MODEL_AMBIENT, ambientColor)
        
        lightColor0 = [0.75164, 0.60648, 0.22648, 1.0]
        lightPos0   = [4.0, 0.0, 8.0, 1.0]
        GL.glLightfv(GL.GL_LIGHT0, GL.GL_DIFFUSE, lightColor0)
        GL.glLightfv(GL.GL_LIGHT0, GL.GL_POSITION, lightPos0)
        
 
        lightColor1 = [0.75164, 0.60648, 0.22648, 1.0]
        lightPos1   = [-1.0, 0.5, 0.5, 0.0]
        GL.glLightfv(GL.GL_LIGHT1, GL.GL_DIFFUSE, lightColor1)
        GL.glLightfv(GL.GL_LIGHT1, GL.GL_POSITION, lightPos1)
        GL.glLightModeli(GL.GL_LIGHT_MODEL_TWO_SIDE, GL.GL_TRUE)
        

        GL.glRotatef(self._angleY, 0.0, 1.0, 0.0)
        GL.glRotatef(self._angleX, 1.0, 0.0, 0.0)
        
        GL.glColor3f(1.0, 1.0, 1.0)
        
        self.plist = [  [-1.5, -1.0, 1.5], [1.5, -1.0, 1.5], [1.5, 1.0, 1.5], [-1.5, 1.0, 1.5],
                        [1.5, -1.0, -1.5], [1.5, 1.0, -1.5], [1.5, 1.0, 1.5], [1.5, -1.0, 1.5],
                        [-1.5, -1.0, -1.5], [-1.5, 1.0, -1.5], [1.5, 1.0, -1.5], [1.5, -1.0, -1.5],
                        [-1.5, -1.0, -1.5], [-1.5, -1.0, 1.5], [-1.5, 1.0, 1.5], [-1.5, 1.0, -1.5]
                    ]
        
        self.plist_wing = [
                           [
                            [[0.0, 0.0, 0.0], [0.24999999999999994, 0.0, 0.059412421875], [0.24999999999999994, 1.0, 0.059412421875], [0.0, 1.0, 0.0], [0.24999999999999994, 0.0, 0.059412421875], [0.7499999999999999, 0.0, 0.0316030623052], [0.7499999999999999, 1.0, 0.0316030623052], [0.24999999999999994, 1.0, 0.059412421875], [0.7499999999999999, 0.0, 0.0316030623052], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0], [0.7499999999999999, 1.0, 0.0316030623052]], [[0.0, 1.0, 0.0], [0.24999999999999994, 1.0, 0.059412421875], [0.625, 2.0, 0.029706210937499998], [0.5, 2.0, 0.0], [0.24999999999999994, 1.0, 0.059412421875], [0.7499999999999999, 1.0, 0.0316030623052], [0.875, 2.0, 0.0158015311526], [0.625, 2.0, 0.029706210937499998], [0.7499999999999999, 1.0, 0.0316030623052], [1.0, 1.0, 0.0], [1.0, 2.0, 0.0], [0.875, 2.0, 0.0158015311526]]]
                          ]

        
        self.plist_wing2 = [[[[0.0, 0.0, 0.0], [0.24999999999999994, 0.0, -0.059412421875], [0.24999999999999994, 1.0, -0.059412421875], [0.0, 1.0, 0.0], [0.24999999999999994, 0.0, -0.059412421875], [0.7499999999999999, 0.0, -0.031603062305200005], [0.7499999999999999, 1.0, -0.031603062305200005], [0.24999999999999994, 1.0, -0.059412421875], [0.7499999999999999, 0.0, -0.031603062305200005], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0], [0.7499999999999999, 1.0, -0.031603062305200005]], [[0.0, 1.0, 0.0], [0.24999999999999994, 1.0, -0.059412421875], [0.625, 2.0, -0.029706210937499998], [0.5, 2.0, 0.0], [0.24999999999999994, 1.0, -0.059412421875], [0.7499999999999999, 1.0, -0.031603062305200005], [0.875, 2.0, -0.015801531152600003], [0.625, 2.0, -0.029706210937499998], [0.7499999999999999, 1.0, -0.031603062305200005], [1.0, 1.0, 0.0], [1.0, 2.0, 0.0], [0.875, 2.0, -0.015801531152600003]]]]

        
        self.surfaceNormals = self.calculateSurfaceNormals(self.plist_wing)
        self.surfaceNormals2 = self.calculateSurfaceNormals(self.plist_wing2)
        
        
        GL.glBegin(GL.GL_QUADS)
        j = 0
        for shape in self.plist_wing2 :
            for seg in shape :
                for i in range(0, len(seg)) :
                    if i % 4 == 0 :
                        GL.glNormal3fv(self.surfaceNormals2[j])
                        j += 1
                    GL.glVertex3fv(seg[i])       
        GL.glEnd()
        
        GL.glBegin(GL.GL_QUADS)
        j = 0
        for shape in self.plist_wing :
            for seg in shape :
                for i in range(0, len(seg)) :
                    if i % 4 == 0 :
                        GL.glNormal3fv(self.surfaceNormals[j])
                        j += 1
                    GL.glVertex3fv(seg[i])

        #=======================================================================
        # i = 0
        # j = 0
        # for p in self.plist:
        #     if i % 4 == 0:
        #         GL.glNormal3fv(self.surfaceNormals[j])
        #         print self.surfaceNormals[j]
        #         j +=1
        #     GL.glVertex3fv(p)
        #     i += 1
        #     print p
        #=======================================================================
        ## Front
        #GL.glNormal3f(0.0, 0.0, 1.0)        
        #----------------------------------------- GL.glNormal3f(-1.0, 0.0, 1.0)
        #---------------------------------------- GL.glVertex3f(-1.5, -1.0, 1.5)
        #------------------------------------------ GL.glNormal3f(1.0, 0.0, 1.0)
        #----------------------------------------- GL.glVertex3f(1.5, -1.0, 1.5)
        #------------------------------------------ GL.glNormal3f(1.0, 0.0, 1.0)
        #------------------------------------------ GL.glVertex3f(1.5, 1.0, 1.5)
        #----------------------------------------- GL.glNormal3f(-1.0, 0.0, 1.0)
        #----------------------------------------- GL.glVertex3f(-1.5, 1.0, 1.5)
#------------------------------------------------------------------------------ 
        #-------------------------------------------------------------- ## Right
        #----------------------------------------- #GL.glNormal3f(1.0, 0.0, 0.0)
        #----------------------------------------- GL.glNormal3f(1.0, 0.0, -1.0)
        #---------------------------------------- GL.glVertex3f(1.5, -1.0, -1.5)
        #----------------------------------------- GL.glNormal3f(1.0, 0.0, -1.0)
        #----------------------------------------- GL.glVertex3f(1.5, 1.0, -1.5)
        #------------------------------------------ GL.glNormal3f(1.0, 0.0, 1.0)
        #------------------------------------------ GL.glVertex3f(1.5, 1.0, 1.5)
        #------------------------------------------ GL.glNormal3f(1.0, 0.0, 1.0)
        #----------------------------------------- GL.glVertex3f(1.5, -1.0, 1.5)
#------------------------------------------------------------------------------ 
        #--------------------------------------------------------------- ## Back
        #---------------------------------------- #GL.glNormal3f(0.0, 0.0, -1.0)
        #---------------------------------------- GL.glNormal3f(-1.0, 0.0, -1.0)
        #--------------------------------------- GL.glVertex3f(-1.5, -1.0, -1.5)
        #---------------------------------------- GL.glNormal3f(-1.0, 0.0, -1.0)
        #---------------------------------------- GL.glVertex3f(-1.5, 1.0, -1.5)
        #----------------------------------------- GL.glNormal3f(1.0, 0.0, -1.0)
        #----------------------------------------- GL.glVertex3f(1.5, 1.0, -1.5)
        #----------------------------------------- GL.glNormal3f(1.0, 0.0, -1.0)
        #---------------------------------------- GL.glVertex3f(1.5, -1.0, -1.5)
#------------------------------------------------------------------------------ 
        #--------------------------------------------------------------- ## Left
        #---------------------------------------- #GL.glNormal3f(-1.0, 0.0, 0.0)
        #---------------------------------------- GL.glNormal3f(-1.0, 0.0, -1.0)
        #--------------------------------------- GL.glVertex3f(-1.5, -1.0, -1.5)
        #----------------------------------------- GL.glNormal3f(-1.0, 0.0, 1.0)
        #---------------------------------------- GL.glVertex3f(-1.5, -1.0, 1.5)
        #----------------------------------------- GL.glNormal3f(-1.0, 0.0, 1.0)
        #----------------------------------------- GL.glVertex3f(-1.5, 1.0, 1.5)
        #---------------------------------------- GL.glNormal3f(-1.0, 0.0, -1.0)
        #---------------------------------------- GL.glVertex3f(-1.5, 1.0, -1.5)

        GL.glEnd()
        
        
        GL.glColor3f(0.0,1.0, 1.0)
        GL.glBegin(GL.GL_LINES)
        GL.glVertex3f(-1.0, 0.0, 1.0)
        GL.glVertex3f(-1.5, -1.0, 1.5)
        GL.glVertex3f(1.0, 0.0, 1.0)
        GL.glVertex3f(1.5, -1.0, 1.5)
        GL.glVertex3f(1.0, 0.0, 1.0)
        GL.glVertex3f(1.5, 1.0, 1.5)
        GL.glVertex3f(-1.0, 0.0, 1.0)
        GL.glVertex3f(-1.5, 1.0, 1.5) 
        
        GL.glVertex3f(1.0, 0.0, -1.0)
        GL.glVertex3f(1.5, -1.0, -1.5)
        GL.glVertex3f(1.0, 0.0, -1.0)
        GL.glVertex3f(1.5, 1.0, -1.5)
        GL.glVertex3f(1.0, 0.0, 1.0)
        GL.glVertex3f(1.5, 1.0, 1.5)
        GL.glVertex3f(1.0, 0.0, 1.0)
        GL.glVertex3f(1.5, -1.0, 1.5) 
        
        GL.glVertex3fv([1.0, 0.0, 0.0])
        GL.glVertex3fv([1.5, -1.0, -1.5])
                      
        GL.glEnd()


    def calculateVertexNormals(self, nlist):
        pass
    
    def __calculateVertexNormal(self, normals):
        res = [0.0, 0.0, 0.0]
        for n in normals :
            res[0] += n[0] ; res[1] += n[1] ; res[2] += n[2]
        res[0] = res[0] / len(normals) ; res[1] = res[1] / len(normals) ; res[2] = res[2] / len(normals)
        
        return res / len(normals)

    def calculateSurfaceNormals(self, plist):
        tmp = []
        for shape in plist:
            for seg in shape:
                for i in range (0, len(seg), 4) :
                    tmp.append(self.__calculateSurfaceNormal([seg[i], seg[i+1], seg[i+2], seg[i+3]]))
        return tmp
    
    def __calculateSurfaceNormal(self, polynom):
        normal = [0.0, 0.0, 0.0]
        for i in range (len(polynom)) :
            cur = polynom[i]
            nxt = polynom[(i+1) % len(polynom)]
            
            normal[0] = normal[0] + ( (cur[1] - nxt[1]) * (cur[2] + nxt[2])) 
            normal[1] = normal[1] + ( (cur[2] - nxt[2]) * (cur[0] + nxt[0])) 
            normal[2] = normal[2] + ( (cur[0] - nxt[0]) * (cur[1] + nxt[1])) 
            
        return self.__normalised(normal)        


    def __lenVector(self, v):
        return math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2])

    def __normalised(self, v):
        l = self.__lenVector(v)
        if l == 0.0 :
            return [0.0, 0.0, 0.0]
        else :
            return [v[0] / l, v[1] / l, v[2] / l]  



        

    def calculateVertexNformal(self, p1, p2, p3, face_value):
        vec1 = [p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2]]
        vec2 = [p3[0] - p1[0], p3[1] - p1[1], p3[2] - p1[2]]
        #vec1 = [p1[0] - p2[0], p1[1] - p2[1], p1[2] - p2[2]]
        #vec2 = [p1[0] - p3[0], p1[1] - p3[1], p1[2] - p3[2]]
               
               
        return self.normalised(self.__crossproduct(vec1, vec2, face_value))  #self.normalised(self.__crossproduct(vec1, vec2))

    
    def __crossproduct(self, vec1, vec2, face_value):
        x = face_value * (vec1[1] * vec2[2] - vec1[2] * vec2[1]) 
        y = face_value * (vec1[2] * vec2[0] - vec1[0] * vec2[2]) 
        z = face_value * (vec1[0] * vec2[1] - vec1[1] * vec2[0])
        
        return [x, y, z]         


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
        

    def keyPressEvent(self, event):
        redraw = False
        offset_rot   = 1.5
        offset_scale = 0.2
        # Right arrow - increase rotation by 5 degree
        if event.key() == QtCore.Qt.Key_Right :
            self.renderer._angleY += offset_rot
            redraw = True
        # Left arrow - decrease rotation by 5 degree
        elif event.key() == QtCore.Qt.Key_Left :
            self.renderer._angleY -= offset_rot
            redraw = True
        elif event.key() == QtCore.Qt.Key_Up :
            self.renderer._angleX += offset_rot
            redraw = True
        elif event.key() == QtCore.Qt.Key_Down :
            self.renderer._angleX -= offset_rot
            redraw = True
        elif event.key() == QtCore.Qt.Key_Plus :
            self.renderer.scale += offset_scale
            redraw = True
        elif event.key() == QtCore.Qt.Key_Minus :
            self.renderer.scale -= offset_scale
            redraw = True

        if self.renderer._angleX > 360 :
            self.renderer._angleX -= 360

        if self.renderer._angleY > 360 :
            self.renderer._angleY -= 360

        # Request display update
        if redraw :
            self.updateGL()
    
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
    
    
    
    
    
    
    
    
    
    
    

        



        # make program the default program to be ran. 
        # We can do it now because we'll use a single in this example:
            
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    