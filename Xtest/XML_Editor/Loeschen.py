'''
Created on Aug 18, 2014

@author: rene
'''

import re


class Test: 
    def __init__(self): 
        self.str= "Rene hat <eine> nette, aber <auch> dumme Freundin"
        
    def isWellfomed(self):
        stack = re.findall("[<>]", self.str)
        return False if len(stack)%2 != 0 else self.rec_isWellformed(stack)
 
    def rec_isWellformed(self, stack):
        return True if len(stack) == 0 else self.wellFormed(stack.pop(), stack.pop()) and self.rec_isWellformed(stack)
    
    def wellFormed(self, fst, snd):
        return fst == ')' and snd == '(' or \
               fst == '>' and snd == '<' or \
               fst == '}' and snd == '{'
            

a = Test()
print a.isWellfomed()