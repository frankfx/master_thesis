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
        # GL_NEVER, GL_LESS, GL_EQUAL, GL_LEQUAL, GL_GREATER, GL_NOTEQUAL, GL_GEQUAL und GL_ALWAYS. Voreingestellt ist GL_LESS
        GL.glDepthFunc(GL.GL_LESS)
        
        GL.glEnable(GL.GL_LIGHTING)
        GL.glEnable(GL.GL_LIGHT0)
        GL.glEnable(GL.GL_COLOR_MATERIAL)
        GL.glEnable(GL.GL_NORMALIZE)
        GL.glShadeModel(GL.GL_SMOOTH)
        GL.glClearColor (1.0, 1.0, 1.0, 0.0)
        self.initLight()   
        
        
        
    def initLight(self):
        
        mat_ambient    = [0.25, 0.22, 0.06, 1.0]
        mat_diffuse    = [0.35, 0.31, 0.09, 1.0] 
        mat_specular   = [0.80, 0.72, 0.21, 1.0]
        
        light_position = [0.0, 0.0, 0.0, 1.0]        

        GL.glLightModelfv(GL.GL_LIGHT_MODEL_AMBIENT, mat_ambient)
        GL.glLightfv(GL.GL_LIGHT0, GL.GL_DIFFUSE, mat_diffuse)
        GL.glLightfv(GL.GL_LIGHT0, GL.GL_SPECULAR, mat_specular)
        
        GL.glLightfv(GL.GL_LIGHT0, GL.GL_POSITION, light_position)
        
        # GL.glLightf(GL.GL_LIGHT0, GL.GL_CONSTANT_ATTENUATION, 1.0)
        # GL.glLightf(GL.GL_LIGHT0, GL.GL_LINEAR_ATTENUATION, 0.001)
        # GL.glLightf(GL.GL_LIGHT0, GL.GL_QUADRATIC_ATTENUATION, 0.004)
        
        # The color of the sphere
        mat_materialColor = [0.2, 0.2, 1.0, 1.0]

        mat_ambient    = [0.64725,  0.5995, 0.3745, 1.0]
        mat_specular   = [0.628281, 0.555802, 0.366065, 1.0]
        
        mat_shininess  = 111.2 
        
        
        GL.glLightModeli(GL.GL_LIGHT_MODEL_TWO_SIDE, GL.GL_TRUE)
        
        GL.glMaterialfv(GL.GL_FRONT, GL.GL_AMBIENT, mat_ambient)
        # GL.glMaterialfv(GL.GL_FRONT, GL.GL_DIFFUSE, mat_diffuse)
        GL.glMaterialfv(GL.GL_FRONT, GL.GL_SPECULAR, mat_specular)
        # GL.glMaterialfv(GL.GL_FRONT, GL.GL_EMISSION, mat_materialEmission)
        GL.glMaterialf(GL.GL_FRONT, GL.GL_SHININESS, mat_shininess)
    
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

        GL.glTranslatef(self.xTrans,self.yTrans,-6.5)
        GL.glScalef(0.1, 0.1,1.0)
        GL.glRotated(self.xRot, 1.0, 0.0, 0.0)
        GL.glRotated(self.yRot, 0.0, 1.0, 0.0)
        GL.glRotated(self.zRot, 0.0, 0.0, 1.0)

        self.drawQuad()
        #GLUT.glutInit()#
        #GLUT.glutSolidSphere(0.5,40,40)
        GL.glFlush() 


    '''
    get surface noraml
    '''
    def calculateSurfaceNormal(self, polynom):
        normal = [0.0, 0.0, 0.0]
        for i in range (len(polynom)) :
            cur = polynom[i]
            nxt = polynom[(i+1) % len(polynom)]
            
            normal[0] = normal[0] + ( (cur[1] - nxt[1]) * (cur[2] + nxt[2])) 
            normal[1] = normal[1] + ( (cur[2] - nxt[2]) * (cur[0] + nxt[0])) 
            normal[2] = normal[2] + ( (cur[0] - nxt[0]) * (cur[1] + nxt[1])) 
            
        normal[0] = -normal[0]
        normal[1] = -normal[1]
        normal[2] = -normal[2]
        return self.normalised(normal)




        


    def calculateNormal(self, plist):
        n = len(plist)
        m = len(plist[0])
        plist_n = []
        for i in range(n) :
            normal_tmp = []
            for j in range(m):
                n1 = [0.0, 0.0, 0.0] if j<=0   or i<=0   else self.calculateVertexNormal(plist[i][j], plist[i][j-1], plist[i-1][j])
                n2 = [0.0, 0.0, 0.0] if j+1>=m or i<=0   else self.calculateVertexNormal(plist[i][j], plist[i-1][j], plist[i][j+1])
                n3 = [0.0, 0.0, 0.0] if j+1>=m or i+1>=n else self.calculateVertexNormal(plist[i][j], plist[i][j+1], plist[i+1][j])
                n4 = [0.0, 0.0, 0.0] if j<=0   or i+1>=n else self.calculateVertexNormal(plist[i][j], plist[i+1][j], plist[i][j-1])
                
                n1 = self.normalised(n1)
                n2 = self.normalised(n2)
                n3 = self.normalised(n3)
                n4 = self.normalised(n4)
                
                normal = [n1[0] + n2[0] + n3[0] + n4[0] , n1[1] + n2[1] + n3[1] + n4[1] , n1[2] + n2[2] + n3[2] + n4[2]]
                normal_tmp.append(normal)
            plist_n.append(normal_tmp)
        return plist_n

    def crossproduct(self, vec1, vec2):
        x = vec1[1] * vec2[2] - vec1[2] * vec2[1] 
        y = vec1[2] * vec2[0] - vec1[0] * vec2[2] 
        z = vec1[0] * vec2[1] - vec1[1] * vec2[0]
        return [x, y, z] 
    
    # normal in p1
    def calculateVertexNormal(self, p1, p2, p3):
        vec1 = [p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2]]
        vec2 = [p3[0] - p1[0], p3[1] - p1[1], p3[2] - p1[2]]
               
        return self.crossproduct(vec1, vec2)
    
    
    def lenVector(self, v):
        import math
        return math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2])
    
    def normalised(self, v):
        l = self.lenVector(v)
        if l == 0.0 :
            return [0.0, 0.0, 0.0]
        else :
            return [v[0] / l, v[1] / l, v[2] / l]
        

    def drawQuad(self):
        GL.glBegin(GL.GL_QUADS)
        
        # richtig
        GL.glColor3f(0.0,1.0,0.0);    # Color Blue
        GL.glNormal3fv(self.calculateSurfaceNormal( [[1.0, 1.0,-1.0], [-1.0, 1.0,-1.0], [-1.0, 1.0, 1.0], [1.0, 1.0, 1.0]]))
        GL.glVertex3f( 1.0, 1.0,-1.0);    # Top Right Of The Quad (Top)
        GL.glVertex3f(-1.0, 1.0,-1.0);    # Top Left Of The Quad (Top)
        GL.glVertex3f(-1.0, 1.0, 1.0);    # Bottom Left Of The Quad (Top)
        GL.glVertex3f( 1.0, 1.0, 1.0);    # Bottom Right Of The Quad (Top)
        
        # richtig
        GL.glColor3f(0.0,1.0,1.0);    # Color Orange
        GL.glNormal3fv(self.calculateSurfaceNormal( [[1.0, -1.0,1.0], [-1.0, -1.0, 1.0], [-1.0, -1.0, -1.0], [1.0, -1.0, -1.0]]))
        GL.glVertex3f( 1.0,-1.0, 1.0);    # Top Right Of The Quad (Bottom)
        GL.glVertex3f(-1.0,-1.0, 1.0);    # Top Left Of The Quad (Bottom)
        GL.glVertex3f(-1.0,-1.0,-1.0);    # Bottom Left Of The Quad (Bottom)
        GL.glVertex3f( 1.0,-1.0,-1.0);    # Bottom Right Of The Quad (Bottom)

        # richtig
        GL.glColor3f(1.0,0.0,0.0);    # Color Red    
        GL.glNormal3fv(self.calculateSurfaceNormal( [[1.0, 1.0,1.0], [-1.0, 1.0, 1.0], [-1.0, -1.0, 1.0], [1.0, -1.0, 1.0]]))
        GL.glVertex3f( 1.0, 1.0, 1.0);    # Top Right Of The Quad (Front)
        GL.glVertex3f(-1.0, 1.0, 1.0);    # Top Left Of The Quad (Front)
        GL.glVertex3f(-1.0,-1.0, 1.0);    # Bottom Left Of The Quad (Front)
        GL.glVertex3f( 1.0,-1.0, 1.0);    # Bottom Right Of The Quad (Front)


        # richtig
        GL.glColor3f(1.0,1.0,0.0);    # Color Yellow
        GL.glNormal3f( 0.0, 0.0, 1.0);
        GL.glVertex3f( 1.0,-1.0,-1.0);    # Top Right Of The Quad (Back)
        GL.glVertex3f(-1.0,-1.0,-1.0);    # Top Left Of The Quad (Back)
        GL.glVertex3f(-1.0, 1.0,-1.0);    # Bottom Left Of The Quad (Back)
        GL.glVertex3f( 1.0, 1.0,-1.0);    # Bottom Right Of The Quad (Back)

        # fehler
        GL.glColor3f(1.0,0.0,1.0);    # Color Blue
        GL.glNormal3f( 1.0, 0.0, 0.0)
        GL.glVertex3f(-1.0, 1.0, 1.0);    # Top Right Of The Quad (Left)
        GL.glVertex3f(-1.0, 1.0,-1.0);    # Top Left Of The Quad (Left)
        GL.glVertex3f(-1.0,-1.0,-1.0);    # Bottom Left Of The Quad (Left)
        GL.glVertex3f(-1.0,-1.0, 1.0);    # Bottom Right Of The Quad (Left)


        # richtig
        GL.glColor3f(1.0,0.0,1.0);    # Color Violet
        GL.glNormal3f(-1.0, 0.0, 0.0)
        GL.glVertex3f( 1.0, 1.0,-1.0);    # Top Right Of The Quad (Right)
        GL.glVertex3f( 1.0, 1.0, 1.0);    # Top Left Of The Quad (Right)
        GL.glVertex3f( 1.0,-1.0, 1.0);    # Bottom Left Of The Quad (Right)
        GL.glVertex3f( 1.0,-1.0,-1.0);    # Bottom Right Of The Quad (Right)
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