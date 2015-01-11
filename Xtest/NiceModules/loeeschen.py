'''
Created on Jan 2, 2015

@author: rene
'''

    attribute vec3 position;
    attribute vec4 color;
    varying vec4 v_color;
    varying vec4 N;
    varying vec3 v; 
    
    uniform mat4 projection;
    uniform mat4 modelview;
    uniform float scale;
    uniform float xrot;
    uniform float yrot;
    uniform float zrot;
    uniform float tx;
    uniform float ty;
    uniform float tz;
    
    
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
    
    
    void main()
    {   
        mat4 model = modelview * translation * rotationX * rotationY * rotationZ;
        gl_Position = projection * model * vec4(position*scale, 1.0);
        
        v_color = color;  
    }
"""







frag_source = """
    varying vec4 v_color;
    varying vec4 N;
    varying vec3 v; 
    
    
    void main()
    {
        gl_FragColor = v_color;
    }
"""
