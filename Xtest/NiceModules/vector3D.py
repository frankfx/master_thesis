'''
Created on Jul 29, 2014

@author: fran_re
'''

#vector3d.py











import math

class Vector3d:

    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, rhs):
        return Vector3d(rhs.x + self.x, rhs.y + self.y, rhs.z + self.z)

    def __sub__(self, rhs):
        return Vector3d(self.x - rhs.x, self.y - rhs.y, self.z - rhs.z)
    
    def __neg__(self):
        return Vector3d(-self.x, -self.y, -self.z)
    
    def __pos__(self):
        return Vector3d(self.x, self.y, self.z)
    
    def __str__(self):
        return "(% .2f, % .2f, % .2f)" % (self.x, self.y, self.z)
    
    def __repr__(self):
        return "Vector3d(%f, %f, %f)" % (self.x, self.y, self.z)

    def set(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def copy(self):
        return Vector3d(self.x, self.y, self.z)

    def length_sq(self):
        return self.x*self.x + self.y*self.y + self.z*self.z

    def length(self):
        return math.sqrt(self.x*self.x + self.y*self.y + self.z*self.z)

    def scale(self, scale):
        self.x *= scale
        self.y *= scale
        self.z *= scale

    def normalize(self):
        self.scale(1.0 / self.length())

    def scaled_vec(self, scale):
        v = self.copy()
        v.scale(scale)
        return v

    def normal_vec(self):
        return self.scaled_vec(1.0 / self.length())

def dot(a, b):
    return a.x*b.x + a.y*b.y + a.z*b.z


def CrossProductVec(a, b):
    return Vector3d(a.y*b.z - a.z*b.y,
                    a.z*b.x - a.x*b.z,
                    a.x*b.y - a.y*b.x)


def pos_distance(p1, p2):
    return math.sqrt(pos_distance_sq(p2, p1))


def pos_distance_sq(p1, p2):
    x = p1.x - p2.x
    y = p1.y - p2.y
    z = p1.z - p2.z
    return x*x + y*y + z*z;

