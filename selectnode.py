# -*- coding: utf-8 -*-
"""

@author: polak
"""

from Node import node

class SelectNode (node):
    def __init__(self,treeInst,mytree,parent):
        node.__init__(self,treeInst,mytree,"select",parent)
    
    def run (self, index):
        a = [False, 0]
#        if (self.getChildren() == []):
#            a[1]= self.getRandomProb(index)
#            a[0] = self.getTime()
#        else:
        for i in self.getChildren():                        
            b = i.run(index)           
            a[0] = a[0] or b[0]
            self.setSucc(a[0])
            a[1] = a[1] + b[1]
            self.setTime(a[1])
            if b[0]:	  
                break
        	#i.printChildren()
        return a    