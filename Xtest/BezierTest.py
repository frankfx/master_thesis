# Parameter 0 <= t <= 1 #include <stdio.h>




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
        ABC = AB*s + CD*t
        BCD = BC*s + CD*t
        return ABC*s + BCD*t

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
            t += 0.5
    
        return 1

if __name__ == '__main__':
    bez = Bezier()
    bez.test()  

