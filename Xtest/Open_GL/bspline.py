'''
Created on Oct 22, 2014

@author: fran_re
'''
import numpy as np
from matplotlib import pyplot as plt

class BSpline():
    def __init__(self, control_points, knots, degree):
        '''
        Args:
            knots (numpy array of float): knot vector for which t[i] <= t[i+1]
            control_points (2D numpy array): control points, 
                                array([[x1, x2, x3, ...],
                                       [y1, y2, y3, ...],
                                       [z1, z2, z3, ...]])
                                with control_points.shape[0] = number of arrays
                                with control_points.shape[1] = number of points
            degree (int): degree of the b-spline
            
        '''
        assert(control_points.shape[1] + degree + 1 == np.size(knots))        
        
        self.cp = control_points
        self.knots = knots
        self.degree = degree
        
    def eval(self, t):
        '''
        Evaluates the B-Spline at positions t
        
        Args:
            t (1d numpy array): parameters at which to evaluate the b-spline
        '''
        return b_spline_eval(self.knots, self.cp, self.degree, t)
        # uncomment, to test the slow (unvectorized) version
        #return deboor_array_py(self.knots, self.cp, self.degree, t)


def b_spline_basis_i(i, d, t, x):
    '''
    Computes the i-th b-spline basis function of degree d
    
    Args:
        i (int): The basis' functions index with 0 <= i < size(t) - d - 1
        d (int): Degree of the b-spline
        t (float array): Knot vector with t[i] <= t[i+1]
        x (1d numy array): Paramters, at which the spline is to be evaluated
        
    '''    
    
    assert(0 <= i < t.shape[0] - d - 1)
    res =  b_basis_rec(i,d,t,x)
    
    res[x < t[0]] = 0
    res[x > t[-1]] = 0
    return res

# compute basis function of b_spline
def b_basis_rec(i,d,t,x):
    '''
    Recursive implementation of basis function computation. Fully vectorized and thus faster as deboor.
    
    Can't be used for extrapolation currently.
    
    Args:
        i (int): The basis' functions index with 0 <= i < size(t) - d - 1
        d (int): Degree of the b-spline
        t (float array): Knot vector with t[i] <= t[i+1]
        x (1d numy array): Paramters, at which the spline is to be evaluated
        
    '''   
    
    res = 0. * x
    if d > 0:
        if (t[i+d] - t[i]) != 0.:
            res = res + (x - t[i])/(t[i+d] - t[i]) * b_basis_rec(i, d-1, t, x)
            
        if (t[i+1+d] - t[i+1]) != 0.:
            res = res + (t[i+1+d] - x)/(t[i+1+d] - t[i+1])*b_basis_rec(i+1, d-1, t,x)
    
    # special treatment for endpoint         
    elif t[i+1] < t[-1]:
        res[(t[i] <= x) & (x < t[i+1])] = 1
    else:
        res[t[i] <= x] = 1;
        
    return res


def b_spline_eval(t, cp, d, x):
    '''
    This is an implementation for b-spline evaluation. In contrast to the deboor
    algorithm, it computes the superposition of the b-spline basis functions.
    
    This implementation is faster then the cythonized deboor algorithm since
    it's completely vectorized
    
    Args:
        t (numpy array of float): knot vector for which t[i] <= t[i+1]
        cp (2D numpy array): control points, with cp.shape[1] = number of points
        d (int): degree of the b-spline
        x (float value of numpy array): parameter ar which the function is evaluated
        
    Returns:
        numpy array: The b-spline koordinates for each x parameter
    '''
    assert(cp.shape[1] + d + 1 == np.size(t))

    # res = [[0,0,0,...] , [0,0,0,...] , [0,0,0,...]]  
    res = np.zeros([cp.shape[0], np.size(x)])
    for i in range(cp.shape[1]):
        # cp[:,[i]] ---> on all arrays take elem at pos i and put it in an separate array
        res = res + cp[:,[i]] * b_spline_basis_i(i, d, t, x)
        
    return res