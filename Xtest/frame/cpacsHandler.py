vert_source = """

    attribute vec3 position;
  //  attribute vec4 color;
  //  varying vec4 v_color;
    varying vec3 N;
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
        v = vec3(gl_ModelViewMatrix * gl_Vertex);       
        N = normalize(gl_NormalMatrix * gl_Normal);
        
        mat4 model = modelview * translation * rotationX * rotationY * rotationZ;
        gl_Position = projection * model * vec4(position*scale, 1.0);

      //  v_color = color;        
          
    }
"""


vert_source2 = """
    varying vec3 vertex_light_position;
    varying vec3 vertex_light_half_vector;
    varying vec3 vertex_normal;
    void main() {            
        // Calculate the normal value for this vertex, in world coordinates (multiply by gl_NormalMatrix)
        vertex_normal = normalize(gl_NormalMatrix * gl_Normal);
        // Calculate the light position for this vertex
        vertex_light_position = normalize(gl_LightSource[0].position.xyz);
    
        // Calculate the light’s half vector
        vertex_light_half_vector = normalize(gl_LightSource[0].halfVector.xyz);
    
        // Set the front color to the color passed through with glColor*f
        gl_FrontColor = gl_Color;
        // Set the position of the current vertex 
        gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
    }
"""


frag_source2 = """
    varying vec3 vertex_light_position;
    varying vec3 vertex_light_half_vector;
    varying vec3 vertex_normal;
    
    void main() {
        // Calculate the ambient term
        vec4 ambient_color = gl_FrontMaterial.ambient * gl_LightSource[0].ambient + gl_LightModel.ambient * gl_FrontMaterial.ambient;;
    
        // Calculate the diffuse term
        vec4 diffuse_color = gl_FrontMaterial.diffuse * gl_LightSource[0].diffuse;
    
        // Calculate the specular value
        vec4 specular_color = gl_FrontMaterial.specular * gl_LightSource[0].specular * pow(max(dot(vertex_normal, vertex_light_half_vector), 0.0), gl_FrontMaterial.shininess);
    
        // Set the diffuse value (darkness). This is done with a dot product between the normal and the light
        // and the maths behind it is explained in the maths section of the site.
        float diffuse_value = max(dot(vertex_normal, vertex_light_position), 0.0);
    
        // Set the output color of our current pixel
        gl_FragColor = ambient_color + diffuse_color * diffuse_value + specular_color;
    }
"""














frag_source = """
   // varying vec4 v_color;
    varying vec3 N;
    varying vec3 v; 
    
    void main()
    {
        vec3 L = normalize(gl_LightSource[0].position.xyz - v);   
        vec3 E = normalize(-v); // we are in Eye Coordinates, so EyePos is (0,0,0)  
        vec3 R = normalize(-reflect(L,N)); 

       //calculate Ambient Term:  
       vec4 Iamb = gl_FrontLightProduct[0].ambient;    
    
       //calculate Diffuse Term:  
       vec4 Idiff = gl_FrontLightProduct[0].diffuse * max(dot(N,L), 0.0);
       Idiff = clamp(Idiff, 0.0, 1.0);     
       
       // calculate Specular Term:
       vec4 Ispec = gl_FrontLightProduct[0].specular 
                    * pow(max(dot(R,E),0.0),0.3*gl_FrontMaterial.shininess);
       Ispec = clamp(Ispec, 0.0, 1.0); 
       // write Total Color:  
       gl_FragColor = gl_FrontLightModelProduct.sceneColor + Iamb + Idiff + Ispec;

    }
"""












'''
Created on Aug 5, 2014

@author: fran_re
'''
import sys
from PySide.QtGui import QTextDocument, QMainWindow, QTextEdit, QApplication
#from cpacsPy.tixi import tixiwrapper
#from cpacsPy.tigl import tiglwrapper
import tiglwrapper
import tixiwrapper
from config import Config
import re

class CPACS_Handler():
    
    def __init__ (self):
        self.tixi = tixiwrapper.Tixi()
        self.tigl = tiglwrapper.Tigl()
        
    def loadFile(self, xmlFilename, cpacs_schema):
        try:
            self.tixi.openDocument(xmlFilename) 
            self.tixi.schemaValidateFromFile(cpacs_schema)
            #print self.tixi._handle.value
            #self.tigl.openCPACSConfiguration(self.tixi._handle.value, "")
            
        except tixiwrapper.TixiException, e:  
            raise e

    def getVectorX(self, prof_uid):
        xpath = self.tixi.uIDGetXPath(prof_uid)
        numX = self.tixi.getVectorSize(xpath + "/pointList/x")
        return self.tixi.getFloatVector(xpath + "/pointList/x",numX)

    def getVectorY(self, prof_uid):
        xpath = self.tixi.uIDGetXPath(prof_uid)
        numY = self.tixi.getVectorSize(xpath + "/pointList/y")
        return self.tixi.getFloatVector(xpath + "/pointList/y",numY)
    
    def getVectorZ(self, prof_uid):
        xpath = self.tixi.uIDGetXPath(prof_uid)
        numZ = self.tixi.getVectorSize(xpath + "/pointList/z")
        return self.tixi.getFloatVector(xpath + "/pointList/z",numZ)    
            
    def updatedictionary(self,path_dict, path_schema):
        dict_file = open(path_dict)
        schema_file = open(path_schema, 'r')
        flag = False
        res = ''
        with open(path_dict, 'a') as mydict :
            for line in schema_file :
                res = re.search("(?<=\<xsd:complexType name=\").*(?=Type\"\>)", line)
                if res != None :
                    for tmp in dict_file : 
                        if tmp == res.group(0) +"\n" :
                            flag = True
                            break
                    if(not flag) :
                        mydict.write(res.group(0)+"\n")
            
        dict_file.close()
        mydict.close()
        schema_file.close()            
        
    def __del__(self):
        self.tixi.close()
        self.tixi.cleanup() 

class EditorWindow(QMainWindow):
    """initialize editor"""
    def __init__(self, cpacs_file, cpacs_schema):
        super(EditorWindow, self).__init__()

        self.editor = QTextEdit()      
        self.temp = CPACS_Handler()  
        self.temp.loadFile(cpacs_file, cpacs_schema)
        text = self.temp.tixi.exportDocumentAsString()
        
        xpath = self.temp.tixi.uIDGetXPath('NACA0009')
        print xpath
        #directory = self.temp.tixi.exportDocumentAsString()
        #version = self.temp.tixi.getTextElement('/cpacs/vehicles/aircraft/model/name')
        #attributeValue = self.temp.tixi.getTextAttribute(config.path_element2, config.attrName2)
        
        vecX = self.temp.tixi.getFloatVector(xpath + "/pointList/x",100)
        vecY = self.temp.tixi.getFloatVector(xpath + "/pointList/y",100)
        vecZ = self.temp.tixi.getFloatVector(xpath + "/pointList/z",100)
        print vecX
        print vecY
        print vecZ
        self.temp.tixi.close()
        
        #print version
        #print attributeValue
        self.editor.setText(text)
        
        self.statusBar()
        self.setWindowTitle('Simple XML editor')
        self.setCentralWidget(self.editor)
        self.resize(800, 800)

    def find(self, word) :
        self.editor.find(self.searchbox.text(), QTextDocument.FindBackward)      

    def search(self, xpath):
        print "test"

def main():
    app = QApplication(sys.argv)
    w = EditorWindow(Config.path_cpacs_A320_Fuse, Config.path_cpacs_21_schema)
    w.show()
    w.temp.updatedictionary(Config.path_code_completion_dict, Config.path_cpacs_21_schema)
    sys.exit(app.exec_())
 
if __name__ == "__main__":
    main()
