# -*- coding: utf-8 -*-
"""

@author: polak
"""

from Node import node
from distributions.computed import Computed
from distributions.normal import Normal
from distributions.uniform import Uniform


class TskNode (node):
    def __init__(self,treeInst,mytree,parent):
        node.__init__(self,treeInst,mytree,"tsk",parent)
        #self.getDistFromAttrib()                
        # not working yet..
        self.distTableSucc = self.createDistTable("Successdistribution")
        self.distTableFail = self.createDistTable("Failuredistribution")
        #self._readDebugFromAttrib()
        
        
        
        
        
    def run (self, index):

        debug = node.run(self, index)
        if (debug!=None):
            return debug  
            
        a = [True, 0]        
        a[0]= self.getRandomProb(index)
#        if (self.getNot()):
#            a[0] = not(a[0])        
        if a[0]:
            a[1] = round(self.getDistSuccByIndex(index).calcProb())
        else:
            a[1] = round(self.getDistFailByIndex(index).calcProb())   
        #print "Task:[%r %f]" %(a[0] ,a[1])    
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
    
#######################-----Adi changes(23/12/2012)-----####################

    #table is the name of the table needed- attribute
    def createDistTable(self,table):
        string = self.getAttrib(str(table))
        
        table =[]        
        if string != None:
            table = self._parseString(string)
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
            
    #create computed distribution
    def _createComputedDist(self,Sinput):
        ans =self._getDictOfNumPairFromString(Sinput)
        return Computed(ans)        
    #create normal distribution
    def _createNormalDist(self,Sinput):
      ans = self._getTwoNumFromString(Sinput)
      return Normal(ans[0],ans[1])
       
    #create uniform distribution  
    def _createUniformDist(self,Sinput):
       ans = self._getTwoNumFromString(Sinput)
       return Uniform(ans[0],ans[1])
    
    def _createDiscreteDist(self,string):
        pass
     

    #input- string "num,num" output: tauple [num,num]
    # we use this func to divide two numbers for distribution parmeters value
    #can only work for two numbers in the string
    def _getTwoNumFromString(self,Sinput):
      stringNumA = ""
      stringNumB = ""
      nextNum = False
      
      #loop over the string
      for index in range(0, len(Sinput)):  
          #check if the Sinput[index] is a number or "." - for float num.
          if (Sinput[index].isdigit() or Sinput[index]=='.' ) == True and (nextNum == False):
              stringNumA += str( Sinput[index] )
              continue
          if(str(Sinput[index]) ==','):
              nextNum= True
              continue
          if (Sinput[index].isdigit() or Sinput[index]=='.') == True and (nextNum == True):
              stringNumB+= str(Sinput[index] ) 
              continue
              
      #return a tauple of two str that represent float number
      return [str(stringNumA),str(stringNumB)]
      
      
      
    # Sinput should look like this - C[123,123],[123,1231],[54,23] 
    #input- the string above, output: disctionary of key and value
    #we use this func to create the map/dictionary for computed distribution
    def _getDictOfNumPairFromString(self,Sinput):
        openBracket = False
        stringPair=""
        #start pairList as empty dictionary
        PairList = {}
        #iter from index=0 to strint- Sinput size
        for index in range(0,len(Sinput)):
            if Sinput[index] == '[' and openBracket == False :
                openBracket = True
                continue
            if Sinput[index] == ']' and openBracket == True:
                #call getTwoNumFromString func with stringPair and appand to the PairList- to get a tauple[num,num]
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
        #return distionry  
        return PairList
            
            