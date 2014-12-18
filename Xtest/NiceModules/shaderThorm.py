import numpy as np
from OpenGL.GL import *
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtOpenGL import *


vert_source = """
    vec3 inputPosition;
    vec4 inputColor;
    vec3 forFragColor;
    
    void main(){
        forFragColor = inputColor.rgb;
        gl_Position =  vec4(inputPosition, 1.0);
    }
"""

frag_source = """
    vec3 forFragColor;
    vec4 outputColor;
    void main() {
        outputColor = vec4(forFragColor, 1.0);
    }
"""

class HelloWidget(QGLWidget):

    def __init__(self):
        QGLWidget.__init__(self)
        self.vertex = np.zeros(1, dtype = [ ("position", np.float32, 3), ("color",    np.float32, 4)] )
        
        self.numVAOs = 0
        self.numVBOs = 0
        self.vaoID   = 0

        self.VAOs = {"Triangle" : self.numVAOs}
        self.VBOs =  {"TriangleAll" : self.numVBOs};

        self.vaoID          = np.zeros(self.numVAOs) 
        self.bufID          = np.zeros(self.numVBOs)
        self.triangleVertNo = 0 
        self.progID         = 0
        self.vertID         = 0
        self.fragID         = 0
        self.vertexLoc      = 0
        self.colorLoc       = 0


    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)
        
        self.setupShaders()
        
        # create a Vertex Array Objects (VAO)
        self.vaoID = glGenVertexArrays(self.numVAOs)

        # generate a Vertex Buffer Object (VBO)
        glGenBuffers(self.numVBOs, self.bufID)

        # binding the Triangle VAO
        glBindVertexArray(self.vaoID[self.VAOs["Triangle"]])
        
        triangleVertexData = [
           0.0, 0.5, 0.0, 1.0, 0.0, 0.0, 1.0,
          -0.5,-0.5, 0.0, 0.0, 1.0, 0.0, 1.0,
           0.5,-0.5, 0.0, 0.0, 0.0, 1.0, 1.0,
        ]

        self.triangleVertNo = 3

        glBindBuffer(GL_ARRAY_BUFFER, self.bufID[self.VAOs["TriangleAll"]])
        glBufferData(GL_ARRAY_BUFFER, self.data.nbytes, triangleVertexData, GL_STATIC_DRAW)

        # We need to tell the GPU how to read the buffer and bind each value to the relevant attribute. To do this, GPU needs to kow what is the stride between 2 consecutive element and what is the offset to read one attribute
        self.stride = self.vertex.strides[0]
        offset = ctypes.c_void_p(0)

        # position
        vertexLoc = 0 # glGetAttribLocation(progID, "position")
        glVertexAttribPointer(vertexLoc, 3, GL_FLOAT, GL_FALSE, self.stride, offset)
        glEnableVertexAttribArray(vertexLoc)


        offset = ctypes.c_void_p(self.vertex.dtype["position"].itemsize)
        # color
        glVertexAttribPointer(self.colorLoc, 4, GL_FLOAT, GL_FALSE, self.stride, offset)
        glEnableVertexAttribArray(self.colorLoc)


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
        progID = glCreateProgram();
        glAttachShader(progID, vertID)
        glAttachShader(progID, fragID)

        # "outColor" is a user-provided OUT variable
        # of the fragment shader.
        # Its output is bound to the first color buffer
        # in the framebuffer
        glBindFragDataLocation(progID, 0, "outputColor")


        # link the program
        glLinkProgram(progID)
        # output error messages
        log = glGetProgramInfoLog(progID)
        if log: print 'Program : ', log        
        
    
        # "inputPosition" and "inputColor" are user-provided
        # IN variables of the vertex shader.
        # Their locations are stored to be used later with
        # glEnableVertexAttribArray()
        self.vertexLoc = glGetAttribLocation(progID,"inputPosition")
        self.colorLoc = glGetAttribLocation(progID, "inputColor")


    def reshape(self,width,height):
        glViewport(0, 0, width, height)    

    def paintGL(self):
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glUseProgram(self.progID)

        # bind Triangle VAO
        glBindVertexArray(self.vaoID[self.VAOs["Triangle"]]);
        # render data
        glDrawArrays(GL_TRIANGLES, 0, self.triangleVertNo)
        
        
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    w = HelloWidget()
    w.show()
    app.exec_()