# -*- coding: utf-8 -*-
"""

@author: polak
"""

from Node import node

class LoopNode (node):
    def __init__(self,treeInst,mytree,parent):
        node.__init__(self,treeInst,mytree,"loop",parent)
    
    def run (self, index):
        a = [True, 0]
        c=0
#        if (self.getChildren() == []):
#            a[1]= self.getRandomProb(index)
#            a[0] = self.getTime()
#        else:
        child = self.getChildren()
        while a[0] and c <=10:
            b = child[0].run(index)
            a[0] = a[0] and b[0]
            self.setSucc(a[0])
            a[1] = a[1] + b[1]
            self.setTime(a[1])
            c = c+1
            print c
            if not b[0]:	  
                break
        	#i.printChildren()
        return a    