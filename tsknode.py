# -*- coding: utf-8 -*-
"""

@author: polak
"""

from Node import node



class TskNode (node):
    def __init__(self,treeInst,mytree,parent):
        node.__init__(self,treeInst,mytree,"tsk",parent)

        self.distTableSucc = self.createDistTable("Successdistribution")
        self.distTableFail = self.createDistTable("Failuredistribution")
           
        
        
        
        
    def run (self, index):
        debug = node.run(self, index)
        if (debug!=None):
            return debug             
        a = [True, 0]        
        a[0]= self.getRandomProb(index)	
        if a[0]:
            a[1] = round(self.getDistSuccByIndex(index).calcProb())
        else:
            a[1] = round(self.getDistFailByIndex(index).calcProb())      
        return a
        
    #override the node func- tsk dosn't have children   
    def getChild(self,index):
         return None
         
    #override the node func- tsk dosn't have children      
    def getChildren (self):
        return None
        
        
     #override the node func   
    def setDEBUGnode(self,sSucc=None,sTime=None):
        node.DEBUGnode(None,None)
        self.DEBUG = [sSucc,sTime]
     
    


   
            