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
        
        debug = node.run(self, index)
        if (debug!=None):
            return debug           
            
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
            
        if (self.getNot()):
            a[0] = not(a[0])
        if a[0]:
            self.setDistTableSuccAtIndex(tmpIndex, a[1])
        else:
            self.setDistTableFailAtIndex(tmpIndex, a[1])          
        self.setProbTableAtIndex(tmpIndex, a[0])
        return a