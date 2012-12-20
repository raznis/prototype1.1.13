# -*- coding: utf-8 -*-
"""

@author: polak
"""

from Node import node

class ParallelNode (node):
    def __init__(self,treeInst,mytree,parent):
        node.__init__(self,treeInst,mytree,"parallel",parent)
    
    def run(self, index):
        tmpIndex = index
        
        b = node.run(self, index)
        if (b!=None):
            self.setProbTableAtIndex(tmpIndex, b[0]) 
            return b           
            
        a = [False, 0]       
        for i in self.getChildren():
            b = i.run(index)
            if (a[0]):
                if b[0]:
                    a[1] = (min(b[1], a[1]))
            else:
                if b[0]:
                    a[1] = (b[1])
                else:
                    a[1] = (max(b[1], a[1]))
            a[0] = b[0] or a[0]
        self.setSucc(a[0])
        self.setTime(a[1])
        
        if (self.getNot()):
            a[0] = not(a[0])
        
        self.setProbTableAtIndex(tmpIndex, a[0]) 
        return a