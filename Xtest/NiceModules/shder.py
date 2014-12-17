import numpy as np
from OpenGL.GL import *
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtOpenGL import *

_vertexShaderSource = (
    'uniform float scale;'
    'attribute vec2 position;'
    'attribute vec4 color;' 
    'varying vec4 v_color;'
    'void main()'
    '{'
    '    gl_Position = vec4(position*, scale, 0.0, 1.0);'
    '    v_color = color;'
    '}'
)

_vertexShader = (
    'attribute vec2 a_position;'
    'attribute vec3 a_color;'
    'varying vec3 v_color;'
    ''
    'void main()'
    '{'
    '   gl_Position = vec4(a_position, 0.0, 1.0);'
    '   v_color = a_color;'
    '}'
)

_fragShader = (
    'void main()'
    '{'
        'gl_FragColor = vec4(0.0,0.0,0.0,1.0);'
    '}'
)



_fragmentShaderSource = (
    'varying vec4 v_color;'
    ''
    'void main()'
    '{'
    '    gl_FragColor = v_color;'
    '}'
)


class HelloWidget(QGLWidget):

    def __init__(self):
        QGLWidget.__init__(self)

    def initializeGL(self):
        self.data = np.zeros(4, dtype = [ ("position", np.float32, 3),
                                ("color",    np.float32, 4)] )
        
        # request program and shader slots from GPU
        program  = glCreateProgram()
        vertex   = glCreateShader(GL_VERTEX_SHADER)
        fragment = glCreateShader(GL_FRAGMENT_SHADER)        
        
        # compile shaders into GPU objects
        # Set shaders source
#        glShaderSource(vertex, _vertexShaderSource)
#        glShaderSource(fragment, _fragmentShaderSource)
        glShaderSource(vertex, _vertexShaderSource)
        glShaderSource(fragment, _fragmentShaderSource)
        
        # Compile shaders
        glCompileShader(vertex)
        glCompileShader(fragment)
        
        # build and link the program:

        glAttachShader(program, vertex)
        glAttachShader(program, fragment)
        glLinkProgram(program)

        # We can not get rid of shaders, they won't be used again:
        glDetachShader(program, vertex)
        glDetachShader(program, fragment)

        # make program the default program to be ran. 
        # We can do it now because we'll use a single in this example:
        glUseProgram(program)
        
        # Request a buffer slot from GPU
        buffere = glGenBuffers(1)

        # Make this buffer the default one
        glBindBuffer(GL_ARRAY_BUFFER, buffere)

        # Upload data
        glBufferData(GL_ARRAY_BUFFER, self.data.nbytes, self.data, GL_DYNAMIC_DRAW)
        
        # Binding the buffer to the program
        # We need to tell the GPU how to read the buffer and bind each value to the relevant attribute. To do this, GPU needs to kow what is the stride between 2 consecutive element and what is the offset to read one attribute
        stride = self.data.strides[0]
        
        offset = ctypes.c_void_p(0)
        loc = glGetAttribLocation(program, "position")
        glEnableVertexAttribArray(loc)
        glBindBuffer(GL_ARRAY_BUFFER, buffere)
        glVertexAttribPointer(loc, 3, GL_FLOAT, False, stride, offset)
        
        offset = ctypes.c_void_p(self.data.dtype["position"].itemsize)
        loc = glGetAttribLocation(program, "color")
        glEnableVertexAttribArray(loc)
        glBindBuffer(GL_ARRAY_BUFFER, buffere)
        glVertexAttribPointer(loc, 4, GL_FLOAT, False, stride, offset)        
        
        # Binding the uniform
        #We request the location of the uniform and we upload the value using the dedicated function to upload one float only
        loc = glGetUniformLocation(program, "scale")
        glUniform1f(loc, 1.0)
        
        
        
        # setting data
        self.data['color']    = [ (1,0,0,1), (0,1,0,1), (0,0,1,1), (1,1,0,1) ]
        self.data['position'] = [ (-1,-1),   (-1,+1),   (+1,-1),   (+1,+1)   ]

    def reshape(self,width,height):
        glViewport(0, 0, width, height)    

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)
        
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    w = HelloWidget()
    w.show()
    app.exec_()