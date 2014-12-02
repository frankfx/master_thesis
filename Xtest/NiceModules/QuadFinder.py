'''
Created on Dec 2, 2014

@author: fran_re
'''

# formula http://martin-thoma.com/how-to-check-if-a-point-is-inside-a-rectangle/
def isPinRectangle(r, P):
    """ 
        r: A list of four points, each has a x- and a y- coordinate
        P: A point
    """

    areaRectangle = 0.5*abs(
                        # p1.y     p3.y     p4.x     p2.x          
                        (r[0][1]-r[2][1])*(r[3][0]-r[1][0]) 
                        # p2.y     p4.y     p1.x     p3.x
                      + (r[1][1]-r[3][1])*(r[0][0]-r[2][0])
                    )

    ABP = 0.5*abs(
             r[0][0]*(r[1][1]-P[1])
            +r[1][0]*(P[1]-r[0][1])
            +P[0]*(r[0][1]-r[1][1])
          )
    BCP = 0.5*abs(
             r[1][0]*(r[2][1]-P[1])
            +r[2][0]*(P[1]-r[1][1])
            +P[0]*(r[1][1]-r[2][1])
          )
    CDP = 0.5*abs(
             r[2][0]*(r[3][1]-P[1])
            +r[3][0]*(P[1]-r[2][1])
            +P[0]*(r[2][1]-r[3][1])
          )
    DAP = 0.5*abs(
             r[3][0]*(r[0][1]-P[1])
            +r[0][0]*(P[1]-r[3][1])
            +P[0]*(r[3][1]-r[0][1])
          )
    
    return areaRectangle == ABP+BCP+CDP+DAP


if __name__ == '__main__':
    p  = [0, 0]      # in
    p2 = [1, -1]     # in
    p3 = [0, -1.1]   # out
    p4 = [1.1, 0]    # out
    p5 = [-1.1, 1.1] # out
    rec = [[-1,1],[1,1],[1,-1],[-1,-1]]

    print isPinRectangle(rec, p)
    print isPinRectangle(rec, p2)
    print isPinRectangle(rec, p3)
    print isPinRectangle(rec, p4)
    print isPinRectangle(rec, p5)