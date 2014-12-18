import numpy as np
from OpenGL.GL import *
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtOpenGL import *
from OpenGL.GLUT import *
from math import *

vert_source = """
    uniform float scale;
    attribute vec2 position;
    attribute vec4 color;
    varying vec4 v_color;
    uniform mat4 projection;
    uniform mat4 modelview;
    
    void main()
    {
        gl_Position = projection*modelview*vec4(position*scale, 0.0, 1.0);
        v_color = color;
    }
"""


frag_source = """
    varying vec4 v_color;
    
    void main()
    {
        gl_FragColor = v_color;
    }
"""


class HelloWidget(QGLWidget):

    def __init__(self):
        QGLWidget.__init__(self)
       # self.width = 800
       # self.height = 800
        #self.resize(self.width ,self.height)
        self.data = np.zeros(3, dtype = [ ("position", np.float32, 2), ("color", np.float32, 4)] )
        self.projection = np.zeros(16) # projection matrix
        self.modelview = np.zeros(16)  # modelview matrix
        self.t = 1

    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)

        self.setupShaders()

        # setting data
        #self.data["color"]    = [ (1,0,0,1), (0,1,0,1), (0,0,1,1), (1,1,0,1) ]
        #self.data["position"] = [ (-1,-1),   (-1,+1),   (+1,-1),   (+1,+1)   ]
        self.data["color"]    = [ (1,0,0,1), (0,1,0,1), (0,0,1,1) ]
        self.data["position"] = [ (-1,-1),   (0,+1),   (+1,-1)  ]


        # Request a buffer slot from GPU
        bufID = glGenBuffers(1)

        # Make this buffer the default one
        glBindBuffer(GL_ARRAY_BUFFER, bufID)

        # Upload data
        glBufferData(GL_ARRAY_BUFFER, self.data.nbytes, self.data, GL_DYNAMIC_DRAW)

        # Binding the buffer to the program
        # We need to tell the GPU how to read the buffer and bind each value to the relevant attribute. To do this, GPU needs to kow what is the stride between 2 consecutive element and what is the offset to read one attribute
        stride = self.data.strides[0]

        offset = ctypes.c_void_p(0)
        loc = glGetAttribLocation(self.progID, "position")
        glEnableVertexAttribArray(loc)
        glBindBuffer(GL_ARRAY_BUFFER, bufID)
        glVertexAttribPointer(loc, 3, GL_FLOAT, False, stride, offset)

        offset = ctypes.c_void_p(self.data.dtype["position"].itemsize)
        loc = glGetAttribLocation(self.progID, "color")
        glEnableVertexAttribArray(loc)
        glBindBuffer(GL_ARRAY_BUFFER, bufID)
        glVertexAttribPointer(loc, 4, GL_FLOAT, False, stride, offset)

        # Binding the uniform
        # We request the location of the uniform and we upload the value using the dedicated function to upload one float only
        self.loc = glGetUniformLocation(self.progID, "scale")
        
        self.projectionLoc = glGetUniformLocation(self.progID, "projection");
        self.modelviewLoc = glGetUniformLocation(self.progID, "modelview");
        # load the current projection and modelview matrix into the
        # corresponding UNIFORM variables of the shader


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
        glViewport(0, 0, w, h)    
        # this function replaces gluPerspective
        self.mat4Perspective(self.projection, 45.0, 1.0*w/h, 0.5, 4.0)
        # mat4Print(projection);
        

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # camera orbits in the y=2 plane
        # and looks at the origin
        # mat4LookAt replaces gluLookAt
        rad = pi / 180.0 * self.t;
        self.mat4LookAt(self.modelview,
               2.0*cos(rad), 2.0, 2.0*sin(rad), # eye
               0.0, 0.0, 0.0, # look at
               0.1, 1.0, 0.0) # up        
        
        glUseProgram(self.progID)
        
        glUniform1f(self.loc, 0.9)
        glUniformMatrix4fv(self.projectionLoc, 1, False, (ctypes.c_float * 16)(*self.projection))
        glUniformMatrix4fv(self.modelviewLoc, 1, False, (ctypes.c_float * 16)(*self.modelview)) 
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 5)
        
    def mat4Perspective(self, a, fov, aspect, zNear, zFar) : 
        f = 1.0 / (tan (fov/2.0 * (pi / 180.0)))
        self.mat4Identity(a)
        a[0] = f / aspect
        a[1 * 4 + 1] = f
        a[2 * 4 + 2] = (zFar + zNear)  / (zNear - zFar)
        a[3 * 4 + 2] = (2.0 * zFar * zNear) / (zNear - zFar)
        a[2 * 4 + 3] = -1.0
        a[3 * 4 + 3] = 0.0
        
        
    def mat4Identity(self, a) : 
        for i in range(0, 16) : a[i] = 0.0
        for j in range(0, 4) : a[j + j * 4] = 1.0

        
    def mat4LookAt(self, viewMatrix, eyeX, eyeY, eyeZ, centerX, centerY, centerZ, upX, upY, upZ) :
        dir = np.zeros(3)
        right = np.zeros(3)
        up = np.zeros(3)
        eye = np.zeros(3)
        
        up[0] = upX ; up[1]=upY ; up[2]=upZ
        eye[0]=eyeX ; eye[1]=eyeY ; eye[2]=eyeZ

        dir[0]=centerX-eyeX; dir[1]=centerY-eyeY; dir[2]=centerZ-eyeZ
        self.vec3Normalize(dir)
        right = np.cross(dir, up)
        self.vec3Normalize(right)
        up = np.cross(right, dir)
        self.vec3Normalize(up)
        
        # first row
        viewMatrix[0]  = right[0]
        viewMatrix[4]  = right[1]
        viewMatrix[8]  = right[2]
        viewMatrix[12] = -np.dot(right, eye)
        # second row
        viewMatrix[1]  = up[0]
        viewMatrix[5]  = up[1]
        viewMatrix[9]  = up[2]
        viewMatrix[13] = -np.dot(up, eye)
        # third row
        viewMatrix[2]  = -dir[0]
        viewMatrix[6]  = -dir[1]
        viewMatrix[10] = -dir[2]
        viewMatrix[14] =  np.dot(dir, eye)
        # forth row
        viewMatrix[3]  = 0.0
        viewMatrix[7]  = 0.0
        viewMatrix[11] = 0.0
        viewMatrix[15] = 1.0
    
    def vec3Normalize(self, a) :
        mag = sqrt(a[0] * a[0]  +  a[1] * a[1]  +  a[2] * a[2])
        a[0] /= mag; a[1] /= mag; a[2] /= mag
        
    def vec3Cross(self, a, b, res) :
        res[0] = a[1] * b[2]  -  b[1] * a[2];
        res[1] = a[2] * b[0]  -  b[2] * a[0];
        res[2] = a[0] * b[1]  -  b[0] * a[1];
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = HelloWidget()
    w.show()
    app.exec_()