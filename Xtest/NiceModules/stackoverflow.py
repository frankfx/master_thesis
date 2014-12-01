'''
Created on Nov 11, 2014

@author: rene
'''

import sys
from PySide import QtOpenGL, QtGui, QtCore

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
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0
        self.xTrans = 0
        self.yTrans = 0  
        self.scale   = 5.0 
        self.aspect  = 0.25  
        self.viewwidth  = 0.0
        self.viewheight = 0.0
        
    def init(self):
        GL.glEnable(GL.GL_DEPTH_TEST)

        GL.glEnable(GL.GL_NORMALIZE)
      #  GL.glEnable(GL.GL_BLEND)
      #  GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        GL.glShadeModel(GL.GL_SMOOTH)
        #GL.glClearColor (1.0, 1.0, 1.0, 0.0)
        #self.initLight()

    def initLight(self):
        mat_ambient    = [0.2, 0.2, 0.2, 1.0]
        mat_diffuse    = [1.0, 1.0, 1.0, 1.0]
        mat_specular   = [1.0, 1.0, 1.0, 1.0] 

        light_position = [1.0, 1.0, 0.0, 1.0]        

        GL.glLightModelfv(GL.GL_LIGHT_MODEL_AMBIENT, mat_ambient)
       # GL.glEnable(GL.GL_LIGHTING)
       # GL.glEnable(GL.GL_LIGHT0)
        GL.glEnable(GL.GL_COLOR_MATERIAL)
        
        mat_materialSpecular = [1.0, 1.0, 1.0, 1.0]
        mat_materialEmission = [0.0, 0.0, 0.0, 1.0]
        
        
        GL.glColorMaterial(GL.GL_FRONT, GL.GL_AMBIENT_AND_DIFFUSE)
        GL.glMaterialfv(GL.GL_FRONT_AND_BACK, GL.GL_AMBIENT, mat_materialSpecular)
        
        GL.glColor4f(1.0, 0.0, 0.0, 0.2)
    
    
    def resize(self, w, h):
        side = min(w, h)
        self.viewwidth = side
        self.viewheight = side
        
        GL.glViewport((w - side) / 2, (h - side) / 2, self.viewwidth, self.viewheight)

        self.__setProjection()        
        
    def __setProjection(self):
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
       
        GL.glOrtho(-1.0 * self.aspect * self.scale, +1.0 * self.aspect * self.scale,
                    +1.0* self.aspect * self.scale, -1.0* self.aspect * self.scale, -10.0, 12.0)

    def display(self):
        self.__setProjection()
 
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT) 
        
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()                

       # self.initLight()

        #GL.glPushMatrix() 
        GL.glTranslatef(self.xTrans,self.yTrans,-6.5)
        GL.glScalef(0.1, 0.1,1.0)
        GL.glRotated(self.xRot, 1.0, 0.0, 0.0)
        GL.glRotated(self.yRot, 0.0, 1.0, 0.0)
        GL.glRotated(self.zRot, 0.0, 0.0, 1.0)
        #self.drawTestObject()
        #self.drawTriangle2()
        #self.drawQuad()
        self.drawRec()
        #GL.glPolygonMode(GL.GL_FRONT_AND_BACK,GL.GL_LINE)
        GL.glPolygonMode(GL.GL_FRONT_AND_BACK,GL.GL_FILL)
       # GL.glEnable(GL.GL_LIGHTING)
        GL.glCallList(self.theTorus)
        
       # GL.glPopMatrix()

       # GL.glPushMatrix()
       # light_position = [0.0, 0.0, 0.0, 1.0]        
       # GL.glLightfv(GL.GL_LIGHT0, GL.GL_POSITION, light_position)         
        #GL.glPopMatrix()



        #GLUT.glutInit()#
        #GLUT.glutSolidSphere(0.5,40,40)
        GL.glFlush() 

    


    def calculateSurfaceNormal (self,p1, p2, p3) :
 
        u = [p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2]]
        v = [p3[0] - p1[0], p3[1] - p1[1], p3[2] - p1[2]]
        n = [0.0,0.0,0.0]
        n[0] = u[1] * v[2] - u[2] * v[1]
        n[1] = u[2] * v[0] - u[0] * v[2]
        n[2] = u[0] * v[1] - u[1] * v[0]

        return n


    def lenVector(self, v):
        import math
        return math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2])
    
    def normalised(self, v):
        l = self.lenVector(v)
        if l == 0.0 :
            return [0.0, 0.0, 0.0]
        else :
            return [v[0] / l, v[1] / l, v[2] / l]


    # normal in p1
    def calculateVertexNormal(self, p1, p2, p3):
        vec1 = [p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2]]
        vec2 = [p3[0] - p1[0], p3[1] - p1[1], p3[2] - p1[2]]
        v = [0.0, 0.0, 0.0]
        v[0] = vec1[1] * vec2[2] - vec1[2] * vec2[1] 
        v[1] = vec1[2] * vec2[0] - vec1[0] * vec2[2]
        v[2] = vec1[0] * vec2[1] - vec1[1] * vec2[0]
        
        return v

    def drawRec(self):
        self.theTorus = GL.glGenLists (5)
        print "df" , self.theTorus
        GL.glNewList(self.theTorus,GL.GL_COMPILE)
    
        # Ground plane 
        GL.glNormal3f(0.0,1.0,0.0)
        for i in range(-10, 10, 1) :
            GL.glColor3f(0.0,(i+10)/20.0,0.0)
            GL.glBegin(GL.GL_QUAD_STRIP)
            for j in range (-10, 10, 1) :
                GL.glVertex3f(i,0.0,j)
                GL.glVertex3f(i+1,0.0,j)
          
            GL.glEnd()
        GL.glEndList()        

    def drawQuad(self):
        #GL.glTranslatef(0,0,2)
        GL.glBegin(GL.GL_QUAD_STRIP)
        GL.glColor4f(1.0, 0.0, 0.0, 1.5)
        GL.glVertex3f(-1,-1,-5)        
        GL.glVertex3f(-1, 1,-5) 
        GL.glVertex3f( 1,-1,-5) 
        GL.glVertex3f( 1, 1,-5) 

        GL.glColor4f(0.0, 1.0, 0.0, 0.5)
        GL.glVertex3f( 2, -1,-5)        
        GL.glVertex3f( 2,  1,-5) 
        
      #  GL.glColor3f(0.0, 0.0, 1.0)        
 
       # GL.glVertex3f( 1, 2,-5) 
        #GL.glVertex3f(-1, 2,-5)
        
        GL.glEnd()

    def drawTriangle2(self):
      #  
        GL.glBegin(GL.GL_TRIANGLES)
       # GL.glNormal3f(0,0,1)
        GL.glVertex3f(0,0,0)
       # GL.glNormal3f(0,0,1)
        GL.glVertex3f(1,0,0)
       # GL.glNormal3f(0,0,1)
        GL.glVertex3f(0,1,0)
        GL.glEnd()       


        GL.glBegin(GL.GL_LINES) 
        GL.glVertex3f(0,0,1)
        GL.glVertex3f(0,0,0)         
        GL.glVertex3f(0,0,1)
        GL.glVertex3f(1,0,0)
        GL.glVertex3f(0,0,1)  
        GL.glVertex3f(0,1,0)               
        GL.glEnd()

        GL.glBegin(GL.GL_LINES) 
        GL.glVertex3f(0,0,-1)
        GL.glVertex3f(0,0,0)         
        GL.glVertex3f(0,0,-1)
        GL.glVertex3f(-1,0,0)
        GL.glVertex3f(0,0,1)  
        GL.glVertex3f(0,-1,0)               
        GL.glEnd()



    def drawTriangle(self):
  
        n = self.normalised(self.calculateVertexNormal([-0.5, -0.5, -1], [0.5, -0.5, -1], [0.0,  0.5, -1]))
        m = self.normalised(self.calculateVertexNormal([0.5, -0.5, -1], [-0.5, -0.5, -1], [0.0,  0.5, -1]))
        k = self.normalised(self.calculateVertexNormal([0.0,  0.5, -1], [0.5, -0.5, -1], [-0.5, -0.5, -1]))
        
    
        k[2] = 1
        #k[1] = 0.5
       # k[0] = 0.0
        m[2] = 1
       # m[1] = -0.5
      #  m[0] = 0.5
        n[2] = 1
       # n[0] = -0.5
       # n[1] = -0.5
        
        plist = [[-0.5, -0.5, -1], [0.5, -0.5, -1], [0.0,  0.5, -1]]
        GL.glBegin(GL.GL_TRIANGLES)
 
        
        GL.glNormal3fv(n)
        #n[2] = -7
        #GL.glNormal3fv(n)
        GL.glVertex3f(-0.5, -0.5, -1)

        GL.glNormal3fv(m)
        #m[2] = -7
        #GL.glNormal3fv(m)
        GL.glVertex3f(0.5, -0.5, -1)        

        GL.glNormal3fv(k)
        #k[2] = -7
        #GL.glNormal3fv(k)
        GL.glVertex3f(0.0,  0.5, -1)        
        GL.glEnd()
    
        GL.glBegin(GL.GL_LINES) 
        GL.glColor3f(1,0,0)
        GL.glVertex3fv(k)
        GL.glVertex3f(0.0,  0.5, -1)         
        GL.glVertex3f(-0.5, -0.5, -1)
        GL.glVertex3fv(n)
        GL.glVertex3f(0.5, -0.5, -1)  
        GL.glVertex3fv(m)               
        GL.glEnd()


        k[2] = -3
        m[2] = -3
        n[2] = -3
        print "dsf" ,k
        GL.glBegin(GL.GL_LINES) 
        GL.glColor3f(0,1,0)
        GL.glVertex3fv(k)
        GL.glVertex3f(0.0,  0.5, -1)         
        GL.glVertex3f(-0.5, -0.5, -1)
        GL.glVertex3fv(n)
        GL.glVertex3f(0.5, -0.5, -1)  
        GL.glVertex3fv(m)               
        GL.glEnd()

    
    def drawTestObject(self):

        plist1 = [[0.0, 0.0, 0.0], [0.030153689607045786, 0.0, 0.02844221322094448], 
                 [0.116977778440511, 0.0, 0.04945887299475936], [0.24999999999999994, 0.0, 0.059412421875], 
                 [0.4131759111665348, 0.0, 0.05751322692417564], [0.5868240888334652, 0.0, 0.046701524680852695], 
                 [0.7499999999999999, 0.0, 0.0316030623052], [0.883022221559489, 0.0, 0.01657043903018468], 
                 [0.9698463103929542, 0.0, 0.005413502659613883], [1.0, 0.0, 0.0]] 
        plist2 = [[0.0, 0.25, 0.0], [0.030153689607045786, 0.25, 0.02844221322094448], 
                  [0.116977778440511, 0.25, 0.04945887299475936], [0.24999999999999994, 0.25, 0.059412421875], 
                  [0.4131759111665348, 0.25, 0.05751322692417564], [0.5868240888334652, 0.25, 0.046701524680852695], 
                  [0.7499999999999999, 0.25, 0.0316030623052], [0.883022221559489, 0.25, 0.01657043903018468], 
                  [0.9698463103929542, 0.25, 0.005413502659613883], [1.0, 0.25, 0.0]]
        
        GL.glBegin(GL.GL_QUADS)
        GL.glNormal3d(1, 0, 0)
        for i in range(len(plist1)-1) :
            GL.glVertex3f(plist1[i+1][0], plist1[i+1][1], plist1[i+1][2])
            GL.glVertex3f(plist1[i][0]  , plist1[i][1]  , plist1[i][2])
            GL.glVertex3f(plist2[i][0]  , plist2[i][1]  , plist2[i][2])
            GL.glVertex3f(plist2[i+1][0], plist2[i+1][1] , plist2[i+1][2])
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
    
    def initializeGL(self):
        self.renderer.init()
    
    def resizeGL(self, w, h):
        self.renderer.resize(w, h)
 
    def paintGL(self):
        self.renderer.display()

    def mousePressEvent(self, event):  
        self.lastPos_x = event.pos().x()
        self.lastPos_y = event.pos().y()
                
    def mouseMoveEvent(self, event):
        dx = (event.x() - self.lastPos_x ) 
        dy = (event.y() - self.lastPos_y ) 
        
        self.lastPos_x += dx
        self.lastPos_y += dy

        oglXunit = 2.0 * self.renderer.aspect * self.renderer.scale
        oglYunit = oglXunit
        
        oglXTrans = oglXunit * 1.0 / self.renderer.viewwidth
        oglYTrans = oglYunit * 1.0 / self.renderer.viewheight
        
        self.renderer.xTrans += (dx * oglXTrans) 
        self.renderer.yTrans += (dy * oglYTrans)

        self.updateGL()

    def keyPressEvent(self, event):
        redraw = False
        offset_rot   = 2.0
        offset_scale = 0.2
        # Right arrow - increase rotation by 5 degree
        if event.key() == QtCore.Qt.Key_Right :
            self.renderer.yRot += offset_rot
            redraw = True
        # Left arrow - decrease rotation by 5 degree
        elif event.key() == QtCore.Qt.Key_Left :
            self.renderer.yRot -= offset_rot
            redraw = True
        elif event.key() == QtCore.Qt.Key_Up :
            self.renderer.xRot += offset_rot
            redraw = True
        elif event.key() == QtCore.Qt.Key_Down :
            self.renderer.xRot -= offset_rot
            redraw = True
        elif event.key() == QtCore.Qt.Key_Plus :
            self.renderer.scale += offset_scale
            redraw = True
        elif event.key() == QtCore.Qt.Key_Minus :
            self.renderer.scale -= offset_scale
            redraw = True

        # Request display update
        if redraw :
            self.updateGL()
    
if __name__ == '__main__':
    app = QtGui.QApplication(["PyQt OpenGL"])
    widget = Widget()
    widget.show()
    app.exec_()    