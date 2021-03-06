import numpy as np
from OpenGL.GL import *
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtOpenGL import *
from OpenGL.GLUT import *
from math import *
import time
from OpenGL.GL.exceptional import glVertex

vert_source = """

    uniform float scale;
    uniform float xrot;
    uniform float yrot;
    uniform float zrot;
    uniform float tx;
    uniform float ty;
    uniform float tz;

    attribute vec3 inputPosition;
    attribute vec3 inputNormal;
    
    uniform mat4 projection, modelview, normalMat;
        
    varying vec3 normalInterp;
    varying vec3 vertPos;
       
    mat4 rotationX = mat4(
        vec4(1.0,       0.0,        0.0, 0.0),
        vec4(0.0, cos(xrot), -sin(xrot), 0.0),
        vec4(0.0, sin(xrot),  cos(xrot), 0.0),
        vec4(0.0,       0.0,        0.0, 1.0)
    );
    
    mat4 rotationY = mat4(
        vec4( cos(yrot), 0.0, sin(yrot), 0.0),
        vec4(       0.0, 1.0, 0.0      , 0.0),
        vec4(-sin(yrot), 0.0, cos(yrot), 0.0),
        vec4(       0.0, 0.0,       0.0, 1.0)
    );
    
    mat4 rotationZ = mat4(
        vec4(cos(zrot), -sin(zrot), 0.0, 0.0),
        vec4(sin(zrot),  cos(zrot), 0.0, 0.0),
        vec4(0.0      ,        0.0, 1.0, 0.0),
        vec4(0.0      ,        0.0, 0.0, 1.0)
    );
    
    mat4 translation = mat4(
        vec4(1.0, 0.0, 0.0, 0.0),
        vec4(0.0, 1.0, 0.0, 0.0),
        vec4(0.0, 0.0, 1.0, 0.0),
        vec4(tx, ty, tz, 1.0)
    );
       
       
        
    void main(){
        mat4 model = modelview * translation * rotationX * rotationY * rotationZ;
        gl_Position = projection * model * 
                  vec4(inputPosition*scale, 1.0);    
    
        vec4 vertPos4 = model * 
                  vec4(inputPosition*scale, 1.0);
        vertPos = vec3(vertPos4) / vertPos4.w;
        normalInterp = vec3(normalMat *  vec4(inputNormal, 0.0));
    }
"""


frag_source = """
    varying vec3 normalInterp;
    varying vec3 vertPos;
    
    uniform int mode;

    const vec3 lightPos = vec3(1.0, 1.0, 1.0);
    //const vec3 ambientColor = vec3(0.3, 0.0, 0.0);
    //const vec3 diffuseColor = vec3(0.5, 0.0, 0.0);
    //const vec3 specColor = vec3(1.0, 1.0, 1.0);
    const vec3 ambientColor = vec3(0.24725, 0.1995, 0.0745);
    const vec3 diffuseColor = vec3(0.75164, 0.60648, 0.22648);
    const vec3 specColor = vec3(0.628281, 0.555802, 0.366065);
    
    
    void main() {
        vec3 normal = normalize(normalInterp);
        vec3 lightDir = normalize(lightPos - vertPos);
        vec3 reflectDir = reflect(-lightDir, normal);
        vec3 viewDir = normalize(-vertPos);

        float lambertian = max(dot(lightDir, normal), 0.0);
        float specular = 0.0;
        
        if(lambertian > 0.0) {
            float specAngle = max(dot(reflectDir, viewDir), 0.0);
            specular = pow(specAngle, 4.0);
        }

        gl_FragColor = vec4(ambientColor + 
                    lambertian*diffuseColor +
                    specular*specColor, 1.0);
        
        //only ambient
        if(mode == 2) gl_FragColor = vec4(ambientColor, 1.0);
        //only diffuse
        if(mode == 2) gl_FragColor = vec4(lambertian*diffuseColor, 1.0);
        //only specular
        if(mode == 2) gl_FragColor = vec4(specular*specColor, 1.0);
    }
"""




class HelloWidget(QGLWidget):

    def __init__(self):
        QGLWidget.__init__(self)
        self.width = 800
        self.height = 800
        self.resize(self.width ,self.height)
       
        self.projection = np.zeros(16) # projection matrix
        self.modelview = np.zeros(16)  # modelview matrix
        #self.normalMat = np.zeros(16)  # normal matrix
        
        self.xrot=0.0
        self.yrot=0.0
        self.zrot=0.0
        
        self.tx=0.0
        self.ty=0.0
        self.tz=0.0
        
        self.scale = 1.0
        self.mode = 1

    def initializeGL(self):
        print glGetString(GL_SHADING_LANGUAGE_VERSION)
        glEnable(GL_DEPTH_TEST)
        #glEnable(GL_COLOR_MATERIAL)
        #glEnable(GL_LIGHTING)
        #glEnable(GL_LIGHT0)
        self.setupShaders()
        
        data = np.zeros(6, dtype = [ ("position", np.float32, 3), ("normals", np.float32, 3)] )
        data["position"] = [ (-1.0, -1.0 , 0.0),   (-1.0 , 1.0 ,0.0),  (1.0, -1.0, 0.0), (1.0,1.0,0.0), (1.5, -1.2, -0.5) ,(1.5, 0.8, -0.5) ]
        data["normals"]  = [ (0.0, 0.0, 1.0), (0.0, 0.0, 1.0), (0.70710678118654746, 0.0, 1.7071067811865475), (0.70710678118654746, 0.0, 1.7071067811865475), (0.70710678118654746, 0.0, 0.70710678118654746), 
                                  (0.70710678118654746, 0.0, 0.70710678118654746)]

        data2 = np.zeros(12, dtype = [ ("position", np.float32, 3), ("normals", np.float32, 3)] )
        data2["position"] = [ (-1.0, -1.0 , 0.0), (0.0, 0.0, 1.0),
                              (-1.0 , 1.0 ,0.0), (0.0, 0.0, 1.0),
                              (1.0, -1.0, 0.0), (0.0, 0.0, 1.0), 
                              (1.0,1.0,0.0), (0.70710678118654746, 0.0, 1.7071067811865475),
                              (1.5, -1.2, -0.5) , (0.70710678118654746, 0.0, 1.7071067811865475),
                              (1.5, 0.8, -0.5), (0.70710678118654746, 0.0, 0.70710678118654746) ]





        # Request a buffer slot from GPU
        self.bufID, self.bufID1 = glGenBuffers(2)
        self.createBufferShape(self.bufID, data)
        self.createBufferShape(self.bufID1, data2)

        # setting data
        #self.data["color"]    = [ (1,0,0,1), (0,1,0,1), (0,0,1,1), (1,1,0,1) ]
        #self.data["position"] = [ (-1,-1),   (-1,+1),   (+1,-1),   (+1,+1)   ]
         #[(-1.0, 1.0, 1.0), (-1.0, -1.0, 1.0), (1.0,1.0,1.0), 
         #(1.0,-1.0,1.0), (1.5, 1.2, -1.5), 
         #(1.5, -0.8, -1.5)]

        data["position"] = [ (-1.0, 1.0 , 0.0),   (-1.0 , -1.0 ,0.0),  (1.0, 1.0, 0.0), (1.0,-1.0,0.0), (1.5, 1.2, -0.5) ,(1.5, -0.8, -0.5) ]
        #self.data["position"] = [ (0.0, 0.0, 0.0), (0.24999999999999994, 0.0, 0.059412421875), (0.24999999999999994, 1.0, 0.059412421875), (0.0, 1.0, 0.0), 
        #                         (0.24999999999999994, 0.0, 0.059412421875), (0.7499999999999999, 0.0, 0.0316030623052), (0.7499999999999999, 1.0, 0.0316030623052), (0.24999999999999994, 1.0, 0.059412421875), 
         #                        (0.7499999999999999, 0.0, 0.0316030623052), (1.0, 0.0, 0.0), (1.0, 1.0, 0.0), (0.7499999999999999, 1.0, 0.0316030623052), 
         #                        (0.0, 1.0, 0.0), (0.24999999999999994, 1.0, 0.059412421875), (0.625, 2.0, 0.029706210937499998), (0.5, 2.0, 0.0), 
         #                        (0.24999999999999994, 1.0, 0.059412421875), (0.7499999999999999, 1.0, 0.0316030623052), (0.875, 2.0, 0.0158015311526), (0.625, 2.0, 0.029706210937499998), 
         #                        (0.7499999999999999, 1.0, 0.0316030623052), (1.0, 1.0, 0.0), (1.0, 2.0, 0.0), (0.875, 2.0, 0.0158015311526),
         #                        
         #                        (0.0, 0.0, 0.0), (0.24999999999999994, 0.0, -0.059412421875), (0.24999999999999994, 1.0, -0.059412421875), (0.0, 1.0, 0.0), 
         #                       (0.24999999999999994, 0.0, -0.059412421875), (0.7499999999999999, 0.0, -0.031603062305200005), (0.7499999999999999, 1.0, -0.031603062305200005), (0.24999999999999994, 1.0, -0.059412421875), 
         #                       (0.7499999999999999, 0.0, -0.031603062305200005), (1.0, 0.0, 0.0), (1.0, 1.0, 0.0), (0.7499999999999999, 1.0, -0.031603062305200005), 
         #                       (0.0, 1.0, 0.0), (0.24999999999999994, 1.0, -0.059412421875), (0.625, 2.0, -0.029706210937499998), (0.5, 2.0, 0.0), 
          #                      (0.24999999999999994, 1.0, -0.059412421875), (0.7499999999999999, 1.0, -0.031603062305200005), (0.875, 2.0, -0.015801531152600003), (0.625, 2.0, -0.029706210937499998), 
          #                      (0.7499999999999999, 1.0, -0.031603062305200005), (1.0, 1.0, 0.0), (1.0, 2.0, 0.0), (0.875, 2.0, -0.015801531152600003)
           #                      ]

        self.normalWingUp = [(0.0, 0.0, -1.0), (0.0, 0.0, -1.0),(0.0, 0.0, -1.0),(-0, -0, -1.0)]

        

    def createBufferShape(self, bufID, data):
        self.mat4Identity(self.modelview)

        # Make this buffer the default one
        glBindBuffer(GL_ARRAY_BUFFER, bufID)
        
        # Upload data
        glBufferData(GL_ARRAY_BUFFER, data.nbytes, data, GL_DYNAMIC_DRAW)

        # Binding the buffer to the program
        # We need to tell the GPU how to read the buffer and bind each value to the relevant attribute. To do this, GPU needs to kow what is the stride between 2 consecutive element and what is the offset to read one attribute
        stride = data.strides[0]

        offset = ctypes.c_void_p(0)
        loc = glGetAttribLocation(self.progID, "inputPosition")
        glEnableVertexAttribArray(loc)
        glVertexAttribPointer(loc, 3, GL_FLOAT, False, stride, offset)

        offset = ctypes.c_void_p(data.dtype["position"].itemsize)
        loc = glGetAttribLocation(self.progID, "inputNormal")
        glEnableVertexAttribArray(loc)
        glVertexAttribPointer(loc, 4, GL_FLOAT, False, stride, offset)

        # Binding the uniform
        # We request the location of the uniform and we upload the value using the dedicated function to upload one float only
        self.loc = glGetUniformLocation(self.progID, "scale")
        
        self.projectionLoc = glGetUniformLocation(self.progID, "projection");
        self.modelviewLoc = glGetUniformLocation(self.progID, "modelview");
        self.normalMatrixLoc = glGetUniformLocation(self.progID, "normalMat");
        self.rotLocX = glGetUniformLocation(self.progID, "xrot");
        self.rotLocY = glGetUniformLocation(self.progID, "yrot");
        self.rotLocZ = glGetUniformLocation(self.progID, "zrot");

        self.transLocX = glGetUniformLocation(self.progID, "tx");
        self.transLocY = glGetUniformLocation(self.progID, "ty");
        self.transLocZ = glGetUniformLocation(self.progID, "tz");
        self.modeLoc   = glGetUniformLocation(self.progID, "mode")
        
        self.normalLoc = glGetAttribLocation(self.progID, "inputNormal");

    def drawShape1(self, glMode):
        modelviewInv = np.zeros(16)  # normal matrix = np.zeros(16)  # normal matrix
        normalmatrix = np.zeros(16)
        
        self.mat4Invert(self.modelview, modelviewInv)
        self.mat4Transpose(modelviewInv, normalmatrix)

        glUseProgram(self.progID)
        glUniform1f(self.loc, self.scale)
        glUniformMatrix4fv(self.projectionLoc, 1, False, (ctypes.c_float * 16)(*self.projection))
        glUniformMatrix4fv(self.modelviewLoc, 1, False, (ctypes.c_float * 16)(*self.modelview)) 
        glUniformMatrix4fv(self.normalMatrixLoc, 1, False, (ctypes.c_float * 16)(*normalmatrix)) 
        glUniform1f(self.rotLocX, self.xrot)
        glUniform1f(self.rotLocY, self.yrot)
        glUniform1f(self.rotLocZ, self.zrot)

        glUniform1f(self.transLocX, self.tx)
        glUniform1f(self.transLocY, self.ty)
        glUniform1f(self.transLocZ, self.tz)

        glUniform1i(self.modeLoc, self.mode)

        glDrawArrays(glMode, 0, 6)

    def setupShaders(self):
        # create shader
        vertID   = glCreateShader(GL_VERTEX_SHADER)
        fragID = glCreateShader(GL_FRAGMENT_SHADER)  

        # assign shader code
        glShaderSource(vertID, vert_source)
        glShaderSource(fragID, frag_source)
        
        # compile vertex and fragment shader
        glCompileShader(vertID)
        glCompileShader(fragID)

        # check for errors
        log = glGetShaderInfoLog(vertID)
        if log: print 'Vertex Shader: ', log
        
        log = glGetShaderInfoLog(fragID)
        if log: print 'Fragment Shader: ', log

        # create program and attach shaders
        self.progID = glCreateProgram();
        glAttachShader(self.progID, vertID)
        glAttachShader(self.progID, fragID)

        # link the program
        glLinkProgram(self.progID)
        # output error messages
        log = glGetProgramInfoLog(self.progID)
        if log: print 'Program : ', log        
        
        # We can not get rid of shaders, they won't be used again:
        glDetachShader(self.progID, vertID)
        glDetachShader(self.progID, fragID)        
        
        #glUseProgram(self.progID)
        
    def resizeGL(self,w,h):
        side = min(w, h)
        self.viewwidth = side
        self.viewheight = side

        glViewport((w - side) / 2, (h - side) / 2, self.viewwidth, self.viewheight)
             
        self.__setProjection()       

    def __setProjection(self):
        self.mat4Identity(self.projection)
        self.mat4Ortho(self.projection,-1.0 , 1.0, 1.0, -1.0, -100.0, 100.0)

    def paintGL(self):
        self.__setProjection()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        #self.drawShape1(GL_QUAD_STRIP)
        self.drawShape1(GL_LINES)
        #self.createBufferShape2(self.bufID1)
        #glDrawArrays(GL_LINES, 0, 6)

    def mat4Identity(self, a) : 
        for i in range(0, 16) : a[i] = 0.0
        for j in range(0,  4) : a[j + j * 4] = 1.0

    def mat4Transpose(self, a, transposed) :
        t = 0
        for i in range(0, 4) :
            for j in range(0, 4) :
                transposed[t] = a[j * 4 + i]
                t+=1

    def mat4Ortho(self, mat, left, right, bottom, top, near, far):
        self.mat4Identity(mat)
        mat[0] = 2.0/(right-left)
        mat[3] = - ((right + left) / (right - left))
        mat[5] = 2.0/(top-bottom)
        mat[7] = - ((top + bottom) / (top-bottom))
        mat[10] = -2.0 / (far - near)
        mat[11] = - ((far + near)/(far - near))
        mat[15] = 1.0

    def mat4Invert(self, m, inverse) :
        inv = np.zeros(16)
        inv[0] = m[5]*m[10]*m[15]-m[5]*m[11]*m[14]-m[9]*m[6]*m[15]+\
                 m[9]*m[7]*m[14]+m[13]*m[6]*m[11]-m[13]*m[7]*m[10]
        inv[4] = -m[4]*m[10]*m[15]+m[4]*m[11]*m[14]+m[8]*m[6]*m[15]-\
                 m[8]*m[7]*m[14]-m[12]*m[6]*m[11]+m[12]*m[7]*m[10]
        inv[8] = m[4]*m[9]*m[15]-m[4]*m[11]*m[13]-m[8]*m[5]*m[15]+\
                 m[8]*m[7]*m[13]+m[12]*m[5]*m[11]-m[12]*m[7]*m[9]
        inv[12]= -m[4]*m[9]*m[14]+m[4]*m[10]*m[13]+m[8]*m[5]*m[14]-\
                 m[8]*m[6]*m[13]-m[12]*m[5]*m[10]+m[12]*m[6]*m[9]
        inv[1] = -m[1]*m[10]*m[15]+m[1]*m[11]*m[14]+m[9]*m[2]*m[15]-\
                 m[9]*m[3]*m[14]-m[13]*m[2]*m[11]+m[13]*m[3]*m[10]
        inv[5] = m[0]*m[10]*m[15]-m[0]*m[11]*m[14]-m[8]*m[2]*m[15]+\
                 m[8]*m[3]*m[14]+m[12]*m[2]*m[11]-m[12]*m[3]*m[10]
        inv[9] = -m[0]*m[9]*m[15]+m[0]*m[11]*m[13]+m[8]*m[1]*m[15]-\
                 m[8]*m[3]*m[13]-m[12]*m[1]*m[11]+m[12]*m[3]*m[9]
        inv[13]= m[0]*m[9]*m[14]-m[0]*m[10]*m[13]-m[8]*m[1]*m[14]+\
                 m[8]*m[2]*m[13]+m[12]*m[1]*m[10]-m[12]*m[2]*m[9]
        inv[2] = m[1]*m[6]*m[15]-m[1]*m[7]*m[14]-m[5]*m[2]*m[15]+\
                 m[5]*m[3]*m[14]+m[13]*m[2]*m[7]-m[13]*m[3]*m[6]
        inv[6] = -m[0]*m[6]*m[15]+m[0]*m[7]*m[14]+m[4]*m[2]*m[15]-\
                 m[4]*m[3]*m[14]-m[12]*m[2]*m[7]+m[12]*m[3]*m[6]
        inv[10]= m[0]*m[5]*m[15]-m[0]*m[7]*m[13]-m[4]*m[1]*m[15]+\
                 m[4]*m[3]*m[13]+m[12]*m[1]*m[7]-m[12]*m[3]*m[5]
        inv[14]= -m[0]*m[5]*m[14]+m[0]*m[6]*m[13]+m[4]*m[1]*m[14]-\
                 m[4]*m[2]*m[13]-m[12]*m[1]*m[6]+m[12]*m[2]*m[5]
        inv[3] = -m[1]*m[6]*m[11]+m[1]*m[7]*m[10]+m[5]*m[2]*m[11]-\
                 m[5]*m[3]*m[10]-m[9]*m[2]*m[7]+m[9]*m[3]*m[6]
        inv[7] = m[0]*m[6]*m[11]-m[0]*m[7]*m[10]-m[4]*m[2]*m[11]+\
                 m[4]*m[3]*m[10]+m[8]*m[2]*m[7]-m[8]*m[3]*m[6];
        inv[11]= -m[0]*m[5]*m[11]+m[0]*m[7]*m[9]+m[4]*m[1]*m[11]-\
                 m[4]*m[3]*m[9]-m[8]*m[1]*m[7]+m[8]*m[3]*m[5];
        inv[15]= m[0]*m[5]*m[10]-m[0]*m[6]*m[9]-m[4]*m[1]*m[10]+\
                 m[4]*m[2]*m[9]+m[8]*m[1]*m[6]-m[8]*m[2]*m[5]
    
        det = m[0]*inv[0]+m[1]*inv[4]+m[2]*inv[8]+m[3]*inv[12]
        if (det == 0) : return False
        det = 1.0 / det
        for i in range(0, 16) : inverse[i] = inv[i] * det
        return True
    


    def keyPressEvent(self, event):
        redraw = False
        offset = 0.05

        if event.key() == Qt.Key_X:
            self.xrot += offset
            redraw = True
        elif event.key() == Qt.Key_Y:
            self.yrot += offset
            redraw = True
        elif event.key() == Qt.Key_Z:
            self.zrot += offset
            redraw = True                         
        elif event.key() == Qt.Key_Plus:
            self.scale += offset
            redraw = True   
        elif event.key() == Qt.Key_Minus:
            self.scale -= offset
            redraw = True   
        elif event.key() == Qt.Key_2:
            self.mode = 2
            redraw = True   
        elif event.key() == Qt.Key_3:
            self.mode = 3
            redraw = True  
        elif event.key() == Qt.Key_4:
            self.mode = 4
            redraw = True              

        
        if redraw :
            self.updateGL()

    def mousePressEvent(self, event):  
        self.lastPos_x = event.pos().x()
        self.lastPos_y = event.pos().y()
                
    def mouseMoveEvent(self, event):
        dx = (event.x() - self.lastPos_x ) 
        dy = (event.y() - self.lastPos_y ) 
        
        self.lastPos_x += dx
        self.lastPos_y += dy

        #Betrachtsfeld = -aspect bis aspect
        
        oglXunit = 2.0
        oglYunit = oglXunit
        
        # pixel real world to Pixel ogl world 
        oglXTrans = oglXunit * 1.0 / self.viewwidth
        oglYTrans = oglYunit * 1.0 / self.viewheight
        
        self.tx += (dx * oglXTrans) 
        self.ty += (dy * oglYTrans)

        self.updateGL()
        
    def mat4Print(self, mat):
        print "Matrix :"
        for i in range(0, len(mat), 4) :
            print "|" , mat[i] , mat[i+1] , mat[i+2] , mat[i+3] , "|"
        print "\n"
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = HelloWidget()
    w.show()
    app.exec_()