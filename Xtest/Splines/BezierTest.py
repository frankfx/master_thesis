import math
class Bezier():

    # Start value
    # First control value
    # Second control value
    # Ending value
    def bezier(self,A,B,C,D,t) :   
        s = 1 - t
        AB = A*s + B*t
        BC = B*s + C*t
        CD = C*s + D*t
       # ABC = AB*s + CD*t
        ABC = BC*s + CD*t;
        BCD = BC*s + CD*t
        return ABC*s + BCD*t


    def bezier2(self, P_0, P_1, P_2, P_3, t) :   
        return (math.pow((1-t), 3) * P_0) + \
                (3 * math.pow((1-t),2) * t * P_1) + \
                (3 * (1-t) * t * t * P_2) + \
                (math.pow(t,3) * P_3)

    def test(self):
        a = 10.0
        b = 20.0
        c = 40.0
        d = 5.0
        t = 0.0
        print("Start. A=%d, B=%f, C=%f, D=%f, t=%f\n" % (a,b,c,d,t))
    
        while True :
            if (t>1.0) :
                break
            print("Bezier pt= %f\n" % self.bezier(a,b,c,d,t))
            t += 0.001
    
        return 1

if __name__ == '__main__':
    bez = Bezier()
    bez.test()  















