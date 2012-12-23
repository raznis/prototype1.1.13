# -*- coding: utf-8 -*-
"""

@author: polak
"""

from Node import node

class LoopNode (node):
    def __init__(self,treeInst,mytree,parent):
        node.__init__(self,treeInst,mytree,"loop",parent)
    
    def run (self, index):
        tmpIndex = index

        if (node.debugMode):
            if not(self.isChildDebug()):
                return self.runAsBaseCase(index)    
            else:
                if not(self.reset):
                    self.clear()        
        
        
        debug = node.run(self, index)
        if (debug!=None):
            return debug 
            
        a = [True, 0]
        #c=0        
        child = self.getChildren()
        while a[0]: #and c <=10:
            b = child[0].run(index)
            a[0] = a[0] and b[0]
            #self.setSucc(a[0])
            a[1] = a[1] + b[1]
            #self.setTime(a[1])
#            c = c+1
#            print c
            if not b[0]:	  
                break
            
        if (self.getNot()):
            a[0] = not(a[0])
        if (self.monitor):
            if a[0]:
                self.setDistTableSuccAtIndex(tmpIndex, a[1])
            else:
                self.setDistTableFailAtIndex(tmpIndex, a[1])    
            self.setProbTableAtIndex(tmpIndex, a[0]) 
        
        return a    