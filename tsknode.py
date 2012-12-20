# -*- coding: utf-8 -*-
"""

@author: polak
"""

from Node import node

class TskNode (node):
    def __init__(self,treeInst,mytree,parent):
        node.__init__(self,treeInst,mytree,"tsk",parent)
        #self.getDistFromAttrib()                
        # not working yet..
        self.distTableSucc = self.createDistTable("Successdistribution")
        self.distTableFail = self.createDistTable("Failuredistribution")
        self._readDebugFromAttrib()
        
        
        
        
        
    def run (self, index):

        b = node.run(self, index)
        if (b!=None):
            return b  
            
        a = [True, 0]        
        a[0]= self.getRandomProb(index)
        a[1] = self.getTime()
        # this information should be calculated as part of the tree
#        if a[0]:
#            a[2] = self.getProbAtIndex(index)
#        else:
#            a[2] = self.getProbAtIndex(index)
        #print a
        if (self.getNot()):
            a[0] = not(a[0])
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
        #would you like to update success ans time success?
    
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
        
        table =[]        
        if string != None:
            
            table = self._parseString(string)
         #   print (table[0])
        newDistTable =[]
        
        #loop over the table- range (0,table len-1)- specifying the step value as 2
        for index in range(0,len(table)-1,1):

            #computed dist   
            if (table[index][0] == 'C'):
                newDistTable.append(self._createComputedDist(table[index]))
            #normal dist
            if(str(table[index][0]) =='N'):
                newDistTable.append(self._createNormalDist(table[index]))
            #discrete dist
            if(table[index][0] == 'D'):
                pass
            #iniform dist- create new instance and 
            if(table[index][0] == 'U'):
                newDistTable.append(self._createUniformDist(table[index]))
                
        return newDistTable
            
        
    def _createComputedDist(self,Sinput):
        ans =self._getDictOfNumPairFromString(Sinput)
        from distributions.computed import Computed
        return Computed(ans)        
    
    def _createNormalDist(self,Sinput):
      ans = self._getTwoNumFromString(Sinput)
      from distributions.normal import Normal
      return Normal(ans[0],ans[1])
       
       
    def _createUniformDist(self,Sinput):
       ans = self._getTwoNumFromString(Sinput)
       from distributions.uniform import Uniform
       return Uniform(ans[0],ans[1])
    
    def _createDiscreteDist(self,string):
        pass
     

    def _getTwoNumFromString(self,Sinput):
      stringNumA = ""
      stringNumB = ""
      nextNum = False
      
      #loop over the string
      for index in range(0, len(Sinput)):          
          if (Sinput[index].isdigit() or Sinput[index]=='.' ) == True and (nextNum == False):
              stringNumA += str( Sinput[index] )
              continue
          if(str(Sinput[index]) ==','):
              nextNum= True
              continue
          if (Sinput[index].isdigit() or Sinput[index]=='.') == True and (nextNum == True):
              stringNumB+= str(Sinput[index] ) 
              continue
              
      
      return [str(stringNumA),str(stringNumB)]
      
      
      
    # Sinput should look like this - C[123,123],[123,1231],[54,23] 
    #input- the string above, output: disctionary of key and value
    def _getDictOfNumPairFromString(self,Sinput):
        openBracket = False
        stringPair=""
        PairList = {}
        for index in range(0,len(Sinput)):
            if Sinput[index] == '[' and openBracket == False :
                openBracket = True
                continue
            if Sinput[index] == ']' and openBracket == True:
                #call getTwoNumFromString func with stringPair and appand to the PairList
                pair = self._getTwoNumFromString(stringPair)
                PairList[str(pair[0])]= str(pair[1])
                #update open bracket to close                
                openBracket = False
                #init the stringPair
                stringPair = ""
                continue
            if openBracket == True :
                stringPair += Sinput[index]
                continue
            
        return PairList
            
            