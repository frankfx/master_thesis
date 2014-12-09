'''
Created on Dec 9, 2014

@author: fran_re
'''

class profileMainWidget():
    
    def fak(self, val):
        for i in range(-1000, val, 1):
            pass
        return True
    
    def changeVal(self, l):
        l[0] = "Ree"
        return l

if __name__ == '__main__':
    test = profileMainWidget()
    
    if (True == False and test.fak(60000000)) :
        print "yes"
    else : print  "no"
    
    val = ["a", "b"]
    v = test.changeVal(val)
    print val
    print v
    
