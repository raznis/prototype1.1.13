# -*- coding: utf-8 -*-
"""

@author: polak
"""

from Node import node

class ParallelNode (node):
    def __init__(self,treeInst,mytree,parent):
        node.__init__(self,treeInst,mytree,"parallel",parent)
    
    def run (self, index):
        node.run()
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
        return a