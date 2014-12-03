'''
Created on Dec 3, 2014

@author: fran_re
'''
    
    def initLight(self):
        # mat_ambient   = [0.4, 0.4, 0.4, 1.0] 
        mat_ambient    = [0.6, 0.6, 0.6, 1.0]
        mat_diffuse    = [0.4, 0.8, 0.4, 1.0] 
        mat_specular   = [1.0, 1.0, 1.0, 1.0]
        
        light_position = [0.0, 0.0, 0.0, 1.0]        

        # GL_LIGHT_MODEL_AMBIENT, GL_LIGHT_MODEL_LOCAL_VIEWER,' GL_LIGHT_MODEL_TWO_SIDE und GL_LIGHT_MODEL_COLOR_CONTROL
        GL.glLightModelfv(GL.GL_LIGHT_MODEL_AMBIENT, mat_ambient)
        # Diffuse (non-shiny) light component
        # GL.glLightfv(GL.GL_LIGHT0, GL.GL_DIFFUSE, mat_diffuse)
        # Specular (shiny) light component
        #GL.glLightfv(GL.GL_LIGHT0, GL.GL_SPECULAR, mat_specular)
        
        GL.glLightfv(GL.GL_LIGHT0, GL.GL_POSITION, light_position)
        GL.glLightf(GL.GL_LIGHT0, GL.GL_CONSTANT_ATTENUATION, 1.0)
        GL.glLightf(GL.GL_LIGHT0, GL.GL_LINEAR_ATTENUATION, 0.001)
        GL.glLightf(GL.GL_LIGHT0, GL.GL_QUADRATIC_ATTENUATION, 0.004)
        
        # The color of the sphere
        mat_materialColor = [0.2, 0.2, 1.0, 1.0]
        # The specular (shiny) component of the material
        mat_materialSpecular = [1.0, 1.0, 1.0, 1.0]
        # The color emitted by the material
        mat_materialEmission = [0, 0, 0, 1.0]
        #The shininess parameter
        mat_shininess  = 0.4 

        mat_ambient    = [0.24725,  0.1995, 0.0745, 1.0]
        mat_diffuse    = [0.75164, 0.60648, 0.22648, 1.0] 
        mat_specular   = [0.628281, 0.555802, 0.366065, 1.0]

        GL.glMaterialfv(GL.GL_FRONT_AND_BACK, GL.GL_AMBIENT, mat_ambient)
       # GL.glMaterialfv(GL.GL_FRONT_AND_BACK, GL.GL_DIFFUSE, mat_diffuse)
        GL.glMaterialfv(GL.GL_FRONT_AND_BACK, GL.GL_SPECULAR, mat_specular)
        # GL.glMaterialfv(GL.GL_FRONT, GL.GL_EMISSION, mat_materialEmission)
        GL.glMaterialf(GL.GL_FRONT_AND_BACK, GL.GL_SHININESS, mat_shininess * 128)
        
        
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


    def calculateSurfaceNormal(self, polynom):
        normal = [0.0, 0.0, 0.0]
        for i in range (len(polynom)) :
            cur = polynom[i]
            nxt = polynom[(i+1) % len(polynom)]
            
            normal[0] = normal[0] + ( (cur[1] - nxt[1]) * (cur[2] + nxt[2])) 
            normal[1] = normal[1] + ( (cur[2] - nxt[2]) * (cur[0] + nxt[0])) 
            normal[2] = normal[2] + ( (cur[0] - nxt[0]) * (cur[1] + nxt[1])) 
            
        return normal
    
    # normal in p1
    def calculateVertexNormal(self, p1, p2, p3):
        vec1 = [p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2]]
        vec2 = [p3[0] - p1[0], p3[1] - p1[1], p3[2] - p1[2]]
        v = [0.0, 0.0, 0.0]
        v[0] = vec1[1] * vec2[2] - vec1[2] * vec2[1] 
        v[1] = vec1[2] * vec2[0] - vec1[0] * vec2[2]
        v[2] = vec1[0] * vec2[1] - vec1[1] * vec2[0]
        
        return v
    
    
    def lenVector(self, v):
        import math
        return math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2])
    
    def normalised(self, v):
        l = self.lenVector(v)
        if l == 0.0 :
            return [0.0, 0.0, 0.0]
        else :
            return [v[0] / l, v[1] / l, v[2] / l]
        