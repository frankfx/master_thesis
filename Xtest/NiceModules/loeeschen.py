import pylab as pl
from Xtest import utility
import math


def __createSuperEllipse(a=1.0, b=1.0, m = 2.0, n=2.0, cnt=100, isTopSide=True):
    x_List = []
    y_List = []
    n = 2.0
    m = n
    print m , n
    x = -a
    # run on x-axis from -a to a in "dist" steps
    dist = (2.0 * a) / cnt
    
    while x < a or utility.equalFloats2(x, a) :
        
        fst = utility.absolut(x / a)
        snd = utility.absolut(1.0 - math.pow(fst, m ))
        
        y = math.pow(snd , 1/n ) / b
        # y = b * math.pow( utility.absolut( 1 - math.pow( utility.absolut(x / a), 2/n) ), n/2 )
        
        y_List.append(y)
        x_List.append(x)
            
        x += dist 




        
    return x_List, y_List





x1 , y1 = __createSuperEllipse() 
print x1
print y1

pl.plot(x1, y1)
pl.show()