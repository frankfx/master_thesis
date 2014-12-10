'''
Created on Nov 11, 2014

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
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0
        self.xTrans = 0
        self.yTrans = 0  
        self.scale   = 5.0 
        self.aspect  = 0.25  
        self.viewwidth  = 0.0
        self.viewheight = 0.0
        self.plist = [
                 [[0.0, 0.0, 0.0], [0.1464466094067262, 0.0, -0.05308323560069057], [0.1464466094067262, 1.0, -0.05308323560069057], [0.0, 1.0, 0.0],
                  [0.1464466094067262, 0.0, -0.05308323560069057], [0.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.1464466094067262, 1.0, -0.05308323560069057]],
                 [[1.0, -1.0,1.0], [-1.0, -1.0, 1.0], [-1.0, -1.0, -1.0], [1.0, -1.0, -1.0]],
                 [[1.0, 1.0,1.0], [-1.0, 1.0, 1.0], [-1.0, -1.0, 1.0], [1.0, -1.0, 1.0]],
                 [[1.0, -1.0,-1.0], [-1.0, -1.0, -1.0], [-1.0, 1.0, -1.0], [1.0, 1.0, -1.0]],
                 [[-1.0, 1.0, 1.0], [-1.0, 1.0, -1.0], [-1.0, -1.0, -1.0], [-1.0, -1.0, 1.0]],
                 [[1.0, 1.0, -1.0], [1.0, 1.0, 1.0], [1.0, -1.0, 1.0], [1.0, -1.0, -1.0]]
                 ]
        self.plist2 = [[[[0.0, 0.0, 0.0], [0.1464466094067262, 0.0, -0.05308323560069057], [0.1464466094067262, 1.0, -0.05308323560069057], [0.0, 1.0, 0.0],[0.1464466094067262, 0.0, -0.05308323560069057], [0.49999999999999994, 0.0, -0.05294025200059999], [0.49999999999999994, 1.0, -0.05294025200059999], [0.1464466094067262, 1.0, -0.05308323560069057], [0.49999999999999994, 0.0, -0.05294025200059999], [0.8535533905932737, 0.0, -0.02010727196643753], [0.8535533905932737, 1.0, -0.02010727196643753], [0.49999999999999994, 1.0, -0.05294025200059999], [0.8535533905932737, 0.0, -0.02010727196643753], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0], [0.8535533905932737, 1.0, -0.02010727196643753]], [[0.0, 1.0, 0.0], [0.1464466094067262, 1.0, -0.05308323560069057], [0.5732233047033631, 2.0, -0.026541617800345287], [0.5, 2.0, 0.0], [0.1464466094067262, 1.0, -0.05308323560069057], [0.49999999999999994, 1.0, -0.05294025200059999], [0.75, 2.0, -0.026470126000299996], [0.5732233047033631, 2.0, -0.026541617800345287], [0.49999999999999994, 1.0, -0.05294025200059999], [0.8535533905932737, 1.0, -0.02010727196643753], [0.9267766952966369, 2.0, -0.010053635983218765], [0.75, 2.0, -0.026470126000299996], [0.8535533905932737, 1.0, -0.02010727196643753], [1.0, 1.0, 0.0], [1.0, 2.0, 0.0], [0.9267766952966369, 2.0, -0.010053635983218765]]]]

    
        
        
        
        #[1.0, 1.0,-1.0], [-1.0, 1.0,-1.0], [-1.0, 1.0, 1.0], [1.0, 1.0, 1.0]
        
        #
        
        
        
    def init(self):
        GL.glEnable(GL.GL_DEPTH_TEST)
        # GL_NEVER, GL_LESS, GL_EQUAL, GL_LEQUAL, GL_GREATER, GL_NOTEQUAL, GL_GEQUAL und GL_ALWAYS. Voreingestellt ist GL_LESS
      #  GL.glDepthFunc(GL.GL_LESS)
        
        GL.glEnable(GL.GL_LIGHTING)
        GL.glEnable(GL.GL_LIGHT0)
        GL.glEnable(GL.GL_COLOR_MATERIAL)
       # GL.glEnable(GL.GL_NORMALIZE)
        GL.glShadeModel(GL.GL_SMOOTH)
        #GL.glEnable(GL.GL_CULL_FACE)
        GL.glClearColor (1.0, 1.0, 1.0, 0.0)
        self.initLight()   
        
        
        
    def initLight(self):
        
        mat_ambient    = [0.75164, 0.60648, 0.22648, 1.0]  #[0.24725, 0.1995, 0.0745, 1.0]
        mat_diffuse    =  [0.75164, 0.40648, 0.22648, 1.0] 
        mat_specular   = [0.01, 0.99, 0.0, 1.0]
        
        light_position = [0.0, 0.0, 0.0, 1.0]        

        GL.glLightModelfv(GL.GL_LIGHT_MODEL_AMBIENT, mat_ambient)
        GL.glLightfv(GL.GL_LIGHT0, GL.GL_DIFFUSE, mat_diffuse)
        GL.glLightfv(GL.GL_LIGHT0, GL.GL_SPECULAR, mat_specular)
        
        GL.glLightfv(GL.GL_LIGHT0, GL.GL_POSITION, light_position)
        
        # GL.glLightf(GL.GL_LIGHT0, GL.GL_CONSTANT_ATTENUATION, 1.0)
        # GL.glLightf(GL.GL_LIGHT0, GL.GL_LINEAR_ATTENUATION, 0.001)
        # GL.glLightf(GL.GL_LIGHT0, GL.GL_QUADRATIC_ATTENUATION, 0.004)
        
        # The color of the sphere
        #mat_materialColor = [0.2, 0.2, 1.0, 1.0]

        mat_ambient  = [0.24725, 0.1995, 0.0745, 1.0]
        mat_diffuse  = [0.75164, 0.60648, 0.22648, 1.0]
        mat_specular = [0.628281, 0.555802, 0.366065, 1.0]
        
        mat_shininess  = 0.4 
        
        #GL.glLightModeli(GL.GL_LIGHT_MODEL_TWO_SIDE, GL.GL_TRUE)
        GL.glColorMaterial(GL.GL_FRONT_AND_BACK,GL.GL_AMBIENT_AND_DIFFUSE)
        GL.glMaterialfv(GL.GL_FRONT_AND_BACK, GL.GL_AMBIENT, mat_ambient)
        GL.glMaterialfv(GL.GL_FRONT_AND_BACK, GL.GL_DIFFUSE, mat_diffuse)
        GL.glMaterialfv(GL.GL_FRONT_AND_BACK, GL.GL_SPECULAR, mat_specular)
        GL.glMaterialf(GL.GL_FRONT_AND_BACK, GL.GL_SHININESS, mat_shininess * 128)
    
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

        #GL.glCullFace(GL.GL_FRONT)
        self.initLight()

        GL.glTranslatef(self.xTrans,self.yTrans,-6.5)
        GL.glScalef(0.1, 0.1,1.0)
        GL.glRotated(self.xRot, 1.0, 0.0, 0.0)
        GL.glRotated(self.yRot, 0.0, 1.0, 0.0)
        GL.glRotated(self.zRot, 0.0, 0.0, 1.0)

        
        #self.drawQuad()
      #  self.drawTriangle()
        
        self.createOglShape()
        
        #self.initLight()
        
        #GLUT.glutInit()#
        #GLUT.glutSolidSphere(0.5,40,40)
        GL.glFlush() 


    '''
    get surface normal
    '''
    def calculateSurfaceNormal(self, polynom):
        normal = [0.0, 0.0, 0.0]
        for i in range (len(polynom)) :
            cur = polynom[i]
            nxt = polynom[(i+1) % len(polynom)]
            
            normal[0] = normal[0] + ( (cur[1] - nxt[1]) * (cur[2] + nxt[2])) 
            normal[1] = normal[1] + ( (cur[2] - nxt[2]) * (cur[0] + nxt[0])) 
            normal[2] = normal[2] + ( (cur[0] - nxt[0]) * (cur[1] + nxt[1])) 
            
        #normal[0] = -normal[0]
        #normal[1] = -normal[1]
       # normal[2] = -normal[2]
        return self.normalised(normal)

    '''
    get vertex normal in p1
    '''
    def calculateVertexNormal(self, p1, p2, p3):
        vec1 = [p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2]]
        vec2 = [p3[0] - p1[0], p3[1] - p1[1], p3[2] - p1[2]]
               
        return (self.__crossproduct(vec1, vec2))  #self.normalised(self.__crossproduct(vec1, vec2))

    
    def __crossproduct(self, vec1, vec2):
        x = vec1[1] * vec2[2] - vec1[2] * vec2[1] 
        y = vec1[2] * vec2[0] - vec1[0] * vec2[2] 
        z = vec1[0] * vec2[1] - vec1[1] * vec2[0]
        
        return [x, -y, -z]         


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


    
    def lenVector(self, v):
        import math
        return math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2])
    
    def normalised(self, v):
        l = self.lenVector(v)
        if l == 0.0 :
            return [0.0, 0.0, 0.0]
        else :
            return [v[0] / l, v[1] / l, v[2] / l]
        

    def drawQuad4(self):
        GL.glBegin(GL.GL_QUADS)
      #  GL.glColor3f(1.0,0.0,0.0)    # Color Blue

        for quad in self.plist :
            GL.glNormal3fv(self.calculateSurfaceNormal(quad))
            GL.glVertex3fv(quad[0])    # Top Right Of The Quad (Top)
            GL.glVertex3fv(quad[1])    # Top Left Of The Quad (Top)
            GL.glVertex3fv(quad[2])    # Bottom Left Of The Quad (Top)
            GL.glVertex3fv(quad[3])    # Bottom Right Of The Quad (Top)
        GL.glEnd()
        
        GL.glPointSize(8)
        for quad in self.plist :
            GL.glBegin(GL.GL_POINTS)
            GL.glVertex3fv(self.calculateSurfaceNormal(quad))
            GL.glEnd()
        

    def drawQuad(self):
        GL.glBegin(GL.GL_QUADS)
        #GL.glColor3f(0.0,1.0,0.0)    # Color Blue

        for quad in self.plist :
            GL.glNormal3fv(self.calculateVertexNormal(quad[0], quad[3], quad[1]))
            GL.glVertex3fv(quad[0])    # Top Right Of The Quad (Top)
            GL.glNormal3fv(self.calculateVertexNormal(quad[1], quad[2], quad[0]))
            GL.glVertex3fv(quad[1])    # Top Left Of The Quad (Top)
            GL.glNormal3fv(self.calculateVertexNormal(quad[2], quad[3], quad[1]))
            GL.glVertex3fv(quad[2])    # Bottom Left Of The Quad (Top)
            GL.glNormal3fv(self.calculateVertexNormal(quad[3], quad[2], quad[0]))
            GL.glVertex3fv(quad[3])    # Bottom Right Of The Quad (Top)
            #break
        GL.glEnd()

        GL.glBegin(GL.GL_LINES)
        GL.glColor3f(0.0,1.0,0.0)
        for quad in self.plist :
            for i in range(0, len(quad), 1) :
                t = self.calculateVertexNormal(quad[i], quad[len(quad)-1 if (i-1) < 0 else i-1], quad[0 if i+1 >= len(quad) else i+1])
                GL.glVertex3fv(quad[i])
                GL.glVertex3fv(t)
          #  break
        GL.glEnd()



    def createOglShape(self):
        i = 0
        GL.glBegin(GL.GL_QUADS)
        for shape in self.plist2 :
            for seg in shape :
                for pIdx in range(0, len(seg), 1) :
                    
                    snd = pIdx-1 if i%4>0 else pIdx+3
                    thd = pIdx+1 if i%4 < 3 else pIdx-3
                    
                    t = self.calculateVertexNormal(seg[pIdx], seg[snd], seg[thd])   
                    
                    #t = self.calculateSurfaceNormal([seg[0],seg[1],seg[2],seg[3]])
    
                    GL.glNormal3fv(t)
                    GL.glVertex3fv(seg[pIdx])
                    i += 1
                    if i == 4: break
               # break
           # break
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