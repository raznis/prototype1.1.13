# -*- coding: utf-8 -*-
"""

@author: polak
"""

from Node import node

class TskNode (node):
    def __init__(self,treeInst,mytree,parent):
        node.__init__(self,treeInst,mytree,"tsk",parent)
        #self.getDistFromAttrib()
        #print ("tsk node has been created!")
                
        # not working yet..
        self.createDistTable("distributionSuccess")
    
    def run (self, index):
        a = [True, 0]
        a[0]= self.getRandomProb(index)
        a[1] = self.getTime()
        # this information should be calculated as part of the tree
#        if a[0]:
#            a[2] = self.getProbAtIndex(index)
#        else:
#            a[2] = self.getProbAtIndex(index)
        print a
        return a
        
    #override the node func- tsk dosn't have children   
    def getChild(self,index):
         return None
         
    #override the node func- tsk dosn't have children      
    def getChildren (self):
        return None
        
        
     #override the node func   
    def DEBUGnode(self,sSUCC=None,sTime=None):
        node.DEBUGnode(None,None)
    
#######################-----Adi changes(17/12/2012)-----####################

    def getDistSuccByIndex(self,index):
        if len(self.distTableSucc) > index:
            return self.distTableSucc[index]
        return None
        
     ################################need update!!!! ################

    def getDistFailByIndex(self,index):
        if len(self.distTableFail) > index:
            return self.distTableFail[index]
        return None
     ################################need update!!!! ################            
            
    
    #table is the name of the table needed- attribute
    def createDistTable(self,table):
        string = self.getAttrib(str(table))
        #print(string)
        
        table =[]        
        if string != None:
            
            table = self._parseString(string)
         #   print (table[0])
        newDistTable =[]
        
        
        #loop over the table- range (0,table len-1)- specifying the step value as 2
        for index in range(0,len(table)-1,2):
            #computed dist   
            if (table[index] == 'C'):
                pass
            #normal dist
            if(table[index] =='N'):
                s = str(table[index+1])
                arr = s.split(',')
                print (arr[0])
                print(arr[1])
                newDistTable.append(self._createNormalDist(arr[0],arr[1]))
            #discrete dist
            if(table[index] == 'D'):
                pass
            #iniform dist- create new instance and 
            if(table[index] == 'U'):
                s = str(table[index+1])
                arr = s.split(',')
                newDistTable.append(self._createUniformDist(arr[0],arr[1]))
                
        return newDistTable
            
        
    def _createComputedDist(self,string):
        pass
    
    def _createNormalDist(self,parmM,parmG):
        from normal import Normal
        return Normal(float(parmM),float(parmG))
        
    def _createUniformDist(self,parmA,parmB):
        from uniform import Uniform
        return Uniform(float(parmA),float(parmB))
    
    def _createDiscreteDist(self,string):
        pass
     

        
            