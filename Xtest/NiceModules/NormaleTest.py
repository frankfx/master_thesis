'''
Created on Dec 14, 2014

@author: rene
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
        return normal #self.normalised(normal)

    '''
    get vertex normal in p1
    '''
def calculateVertexNormal(self, p1, p2, p3, face_value):
    vec1 = [p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2]]
    vec2 = [p3[0] - p1[0], p3[1] - p1[1], p3[2] - p1[2]]
               
    return self.__crossproduct(vec1, vec2, face_value)  #self.normalised(self.__crossproduct(vec1, vec2))
    
def __crossproduct(self, vec1, vec2, face_value):
   x = face_value * (vec1[1] * vec2[2] - vec1[2] * vec2[1]) 
   y = face_value * (vec1[2] * vec2[0] - vec1[0] * vec2[2]) 
   z = face_value * (vec1[0] * vec2[1] - vec1[1] * vec2[0])
        
   return [x, y, z]         
