# -*- coding: utf-8 -*-
"""

@author: polak
"""
import random
import math
import re
from lxml import etree
from copy import deepcopy
#DISTRIBUTIONS
from distributions.computed import Computed
from distributions.normal import Normal
from distributions.uniform import Uniform

class node:
    
    #global variable - represents the amount of different parmeters of the world.
    #it is a class attribute and can accessed via class node.parameterInTheWorld
    #can be set from everywhere that import node
    parmetersInTheWorld = 1
    debugMode = False
    
    #constractur- treeInstance-node in the etree, the etree itself, and prep-type(seq,plan etc.)
    def __init__(self,treeInstance = None,mytree = None,prep="plan",parent=None):

            
        # you can't have multiple __init__ functions in Python so we use mytree = None
        if mytree == None :
	  #create a new tree instance with plan node as root
            self.treeInst =  etree.Element("plan")
            from tree import xmlTree
            #tree instance new with plan as root
            self.myTree = xmlTree(None,self.treeInst)
        else:
            self.myTree = mytree
            self.treeInst = treeInstance

        self.parent = parent 
        #node monitor property
        self.monitor = True
        #node child list
        self.childList = []
        #node probebility table
        self.probTable = []
        # node distribution table for success and failure
        self.distTableSucc = self.createDistTable("Successdistribution")
        self.distTableFail = self.createDistTable("Failuredistribution")
        #update probability table
        probString = self.getAttrib("probability")
        if probString !=None:
            self.probTable= self._parseString(probString)
        else:
            self.probTable= None
        
        #node debuge child property

        self.DEBUGchild= False   
        self._updateChildDebug()
        
        self.DEBUG = self._setDebugFromXmlFile()
	
	#flag that indicates if this node was updated after debug
        self.reset = False
            
        
        
        
    #parseString by whiteSpace
    def _parseString(self, string):
        words = re.split('\s+',string)
	#return a list of words seperate by whiteSpace
        return words
        
    
	
	
    #return parent. if it's the root- return None   
    def getParent(self):
        return self.parent

    
    #get branch-factor        
    def getBF(self):
        return (len(self.treeInst))
    
    
    #create a new node. append it as a child to the self.treeInst and return a node 
    def createNode(self,tag):
         node = self._createChildByTag(etree.SubElement(self.treeInst,tag))
         return node
         
    #input:string-tagtype, create a new node with tag-type and add it to the node direct children
    #append the new child to the node children list
    #output - return the newNode
    def addNode(self,tag):
        node = self.createNode(tag)
        self.childList.append(node)        
        return node
    
            
    #input: parmeter and his value, add parm and set value or just set value  
    def setAttrib(self,parm,value):
        self.treeInst.attrib[parm] = str(value)
        
    #input: paramter name. output: return the value as a string or None   
    def getAttrib(self,parm):
        return self.treeInst.get(parm)
        
    #input: node, output: boolean if this node is monitore        
    def isMonitored (self):
       # return (self.treeInst.tag == "monitor")
       return (self.monitor == True)
    
    #input- tag, output if this node is this tag type- return True, else- False
    def boolWhoAmI (self, tag):
        return (self.treeInst.tag == tag)

    #return list of the node children
    def getChildren (self):
        #call _createChildList which create a wrap for the etree node chilren - 
        return self._createChildList()
                
        
    #create the wrap for child list and return a list    
    def _createChildList(self):
        if len(self.childList) !=0:
            return self.childList
        for element in list(self.treeInst):
            self.childList.append(self._createChildByTag(element))
        return self.childList
    
    
    #input: child num in the list , output: a new child node- not a deepcopy    
    def getChild(self,index):
        if index >= len(self.childList):
            return None
        else:
            if len(self.childList) > 0:
                return self.childList[index]
            else:
                self._createChildList()
                return self.childList[index]

    #input xml tree elem, create the node wrap    
    def _createChildByTag(self,elem):
        if elem == None:
            return None
        #create the new node according to type
        if elem.tag == "seq":
            from seqnode import SeqNode
            return SeqNode(elem,self.myTree,self)
        if elem.tag == "tsk":
            from tsknode import TskNode
            return TskNode(elem,self.myTree,self)
        #decorstor - L is for loop according to cogniteam code        
        if elem.tag == "dec":
            #createDecNodeFromName will append the right child to self
            return self._CreatDecoratorNodesFromName(elem)
        if elem.tag == "loop":
            from loopnode import LoopNode
            return LoopNode(elem,self.myTree,self)
            #need to continue implementing the rest..
        if elem.tag == "not":
           from notnode import NotNode
           return NotNode(elem,self.myTree,self)
        #parallel        
        if elem.tag =="par": 
            from parallelnode import ParallelNode 
            return ParallelNode(elem,self.myTree,self)
        #selector
        if elem.tag =="sel": 
            from selectnode import SelectNode 
            return SelectNode(elem,self.myTree,self)
                
                        
            
    def treeToXml(self,fileName):
       root =self.myTree.getRoot()
       self._updateEtreeToPrintXmlFile(root)
       self.myTree.treeToXml(fileName)
         
         
    def setMonitor(self,boolSet):
        self.monitor = boolSet
    
    #this func compare the node by there instance ID given by python func id.
    def comparTo(self,nodeToCompare):
        return id(self)==id(nodeToCompare)
    
    #this func remove the elem from the original xml tree. r
    def _removeSubElement(self,elem):
        #remove method compares elements based on identity, not on tag value or contents.
        self.treeInst.remove(elem)
        
    def __getitem__(self):
        return self

    
    #input - EtreeInst- element which it's tag is dec - decorator
    #output new node- loop/not with childen- example- for dec "!L!" crete not - loop - not      
    def _CreatDecoratorNodesFromName(self, element):
        name = element.get("name")
        #update Indentation
        ident = element.text
        identTail = element.tail
        newChild = None
        newEtreeInst = deepcopy(element)
        parent = element.getparent()
        lastChild = None
        #itertating over name char and creating node child as necessary
        for char in name:        
                #new child is the first child that replace decorator
                if newChild == None:
                        #if char is "L"- create loop node
                        if char == "L" :
                            #addNode func- create the node by tag and appand it to self.childList
                            newChild = self.createNode("loop")
                            
                        #if char is "!" - create not node
                        else:
                            if char == "!":
                                    newChild = self.createNode("not")
                        if newChild!= None:
                            newChild.treeInst.text = ident
                            newChild.treeInst.tail = identTail
                #after we create newChild we'll appand it all the other- by newChild.addNode func.
                else:                    
                    if lastChild == None:
                            if char == "L" :
                                lastChild = newChild.addNode("loop")
                                
                            if char == "!":
                                lastChild = newChild.addNode("not")
                                
                            if lastChild!= None:
                                lastChild.treeInst.text = ident
                                lastChild.treeInst.tail = identTail
                    else:
                            if char == "L" :
                                lastChild = lastChild.addNode("loop")
                                
                            if char == "!":
                                lastChild = lastChild.addNode("not")  
                                
                            lastChild.treeInst.text = ident
                            lastChild.treeInst.tail = identTail
                #update Indentation
                ident += "\t"
               
        #if we succeded to create newChild and hid children we will give the last node all decorator attributes by deepcopy dec-treeInst                
        if lastChild !=None :
            lastChildParent =  lastChild.treeInst.getparent()
            #assigning the new tag for dec attributes not/loop.
            if lastChild.treeInst.tag == "not":
                newEtreeInst.tag="not"
            if lastChild.treeInst.tag == "loop":
                newEtreeInst.tag="loop"
            #maintain the pointers with the etree and node tree to point the updated nodes.
           
            lastChildParent.remove(lastChild.treeInst)
            lastChild.treeInst = newEtreeInst
            lastChildParent.append(lastChild.treeInst)
            
        #if we didn't create newChild any other children- exmple- <dec name ="L /dec>
        #we create only new child as loop- we'll git it decorator attributes.
        else:
            if newChild != None:
                if newChild.treeInst.tag == "not":
                    newEtreeInst.tag="not"
                if newChild.treeInst.tag == "loop":
                    newEtreeInst.tag="loop"
                (parent).remove(newChild.treeInst)
                newChild.treeInst = newEtreeInst
                (parent).append(newChild.treeInst)
            
       #after reading it name and creating nodes as necessary we want to replace this subElement with the updated tree and update the xml tree(used to be decorator)
       #replace(self, old_element, new_element)
        parent.replace(element, newChild.treeInst)
        self._updateChildForDec(newChild , len(name))
        return newChild
       
    def _updateChildForDec(self,newChild,num):      
      childToCheck = newChild
      for i in range(num):
        	if childToCheck != None:
                  childToCheck._updateChildDebug()
                  childToCheck.distTableSucc = self.createDistTable("Successdistribution")
                  childToCheck.distTableFail = self.createDistTable("Failuredistribution")
                  childToCheck = childToCheck.getChild(0)
             
      
	
    def _updateEtreeToPrintXmlFile(self,updateNode):
            if updateNode == None :
                return None
            if updateNode.distTableSucc != [] :
                updateNode.setAttrib("Successdistribution",updateNode._distTableToString(updateNode.distTableSucc))
            if updateNode.distTableFail != [] :  
                updateNode.setAttrib("Failuredistribution",updateNode._distTableToString(updateNode.distTableFail))
            #get child list
            childList = updateNode.getChildren()
            #iterate over child list with recursive call (list of lists)  
            if childList != None :
                for child in childList :
                    self._updateEtreeToPrintXmlFile(child)                    
            #update Debug attributes in the xml file.        
            updateNode._updateDebugAttribToXmlFile()
     
               
   #this func update the attribute in the xml file for debug 
    def _updateDebugAttribToXmlFile(self):
            if self.DEBUG != None:
                updateString =""
                
                if self.DEBUG[0]== True or self.DEBUG[0]=="True":
                    updateString+="True"+" "
                else :
                    updateString+="False"+" "
                updateString+= str(self.DEBUG[1])
                self.setAttrib("DEBUG",updateString) 
                
    
    # this func read attribute "DEBUG" from xml. and parse it by whiteSpace
    def _setDebugFromXmlFile(self):
        #get string from xml - "True 0.1" for example.	
          debug = self.getAttrib("DEBUG")
          if debug !=None :
	      #return debug
              self.DEBUG =[]
              #parse the string by whiteSpace and returns a list
              debug = self._parseString(debug)
              #first element in the list should be boolen- success
              if debug[0]!=None and debug[0] == "True":
                  debug[0] = True
              else:
                 debug[0] = False   
             # second element in the list should be time - float number
              if debug[1]!=None:
                  debug[1]=float(debug[1])
              else :
                  debug = None
                  
              return debug  


    def getSuccDistAtIndex(self,index):
        if self.distTableSucc != None and len(self.distTableSucc) > index :
            return self.distTableSucc[index]
            
    def getFailDistAtIndex(self,index):
        if self.distTableFail != None and len(self.distTableFail) > index :
            return self.distTableFail[index]
        
    def _updateChildDebug(self):
        for element in self.treeInst.iter(tag=etree.Element):
	    
            if element.get("DEBUG") != None:
                self.DEBUGchild = True
                break
   
    #return true/false if the node has a debug child         
    def hasDebugChild(self):
        return self.DEBUGchild
        
    def addDistToSuccTable(self, dist):
        self.distTableSucc.append(dist)

    def addDistToFailTable(self, dist):
        self.distTableFail.append(dist)
        
        
    #debug getter
    def getDebug(self):
        return self.DEBUG
        
        
    #get a table-distributions list and translate it back to string that we know how to read from xml file       
    def _distTableToString(self,table):
        if table == None:
            return None
        string =""
        #iterate all over the table len
        for index in range(0,len(table)) :
            #each dist has toString func- that we appand to string
            string += ((table[index]).toString())
            #we don't want whitSpace at the end of the string so we appand it only if we didn't reach the last index in the table            
            if index < (len(table)-1):
                string+=" "
        #return the table as string- for empty table we return empty string.
        return (string)        
        

    def getRandomProb(self, index):
        x = random.random()
        p = float(self.getProbAtIndex(index))
        if p==None:
            return None
        return (x <= p)
   

    def setProbTable(self, probtable):
        self.probTable = probtable
        self.setAttrib("probability",probtable)
        
        
    def setDistTableSucc(self, distTable):
        self.distTableSucc = distTable
        self.setAttrib("Successdistribution",self._distTableToString(self.distTableSucc))
           
    def setDistTableFail(self, distTable):
        self.distTableFail = distTable
        self.setAttrib("Failuredistribution",self._distTableToString(self.distTableFail))    
      
        
    def updateProbTableAtIndex(self, index, val):
        if (self.probTable==None or len(self.probTable)==0 ):
            a = []
            for i in range(int(math.pow(2,node.parmetersInTheWorld))):
                a.append([0,0])
            self.setProbTable(a)
        if val:
            self.probTable[index][0] = self.probTable[index][0]+1
            self.probTable[index][1] = self.probTable[index][1]+1
            self._updateProbTableToXmlFile()            
        else:
            self.probTable[index][1] = self.probTable[index][1]+1
            self._updateProbTableToXmlFile() 
            
            
    def _updateProbTableToXmlFile(self):
        if (self.probTable==None or len(self.probTable)==0 ):
            return
        probTableString = ""
        for index in self.probTable :
             if len(index) == 2 :
                 if float(index[1]) != 0 :
                     probTableString += str(float(index[0])/float(index[1]))
                 else:
                     probTableString += '0'                                                  
             else :
                probTableString += str(index)                
             probTableString +=' '
        self.setAttrib("probability",probTableString)
            
                
        
    def setDistTableSuccAtIndex(self, index, time):
        if (self.distTableSucc==[]):
            a = []
            for i in range(int(math.pow(2,node.parmetersInTheWorld))):
                dist = Computed({})
                a.append(dist)
            self.setDistTableSucc(a)
        self.distTableSucc[index].setValueToTime(time, self.distTableSucc[index].getCountByTime(time)+1)
        self.setAttrib("Successdistribution",self._distTableToString(self.distTableSucc))
            
    
    def setDistTableFailAtIndex(self, index, time):
        if (self.distTableFail==[]):
            a = []          
            for i in range(int(math.pow(2,node.parmetersInTheWorld))):
                dist = Computed({})
                a.append(dist)
            self.setDistTableFail(a)   
        self.distTableFail[index].setValueToTime(time, self.distTableFail[index].getCountByTime(time)+1)
        self.setAttrib("Failuredistribution",self._distTableToString(self.distTableFail))
        
   

    #getter for probIndex
    def getProbAtIndex(self,index):
        if self.probTable!=None and len(self.probTable) > index:
            if (isinstance(self.probTable[index],float) or isinstance(self.probTable[index],int) or 
                (isinstance(self.probTable[index],str))):  
                return float(self.probTable[index])
            else:
                if float(self.probTable[index][1]) !=0 :           
                    return (float(self.probTable[index][0])/float(self.probTable[index][1]))
                return 0
        return None
     
    def run(self, index):
        a = None
        if (node.debugMode):
            tmpIndex  = index
            a = self.DEBUG
            if (a!=None):
                if not(self.boolWhoAmI("tsk")): 
                    if (self.monitor):
                        if a[0]:
                            self.setDistTableSuccAtIndex(tmpIndex, a[1])
                        else:
                            self.setDistTableFailAtIndex(tmpIndex, a[1])          
                        self.updateProbTableAtIndex(tmpIndex, a[0])               
        return a
    

   
    def setDebug(self, succtime):
        self.DEBUG = self._parseString(succtime)    
        self.DEBUG[1] = float(self.DEBUG[1])
        #self.setAttrib("DEBUG", self.DEBUG )
        self._updateDebugAttribToXmlFile()
        
    
    def runAsBaseCase (self, index):
        debug = node.run(self, index)
        if (debug!=None):
            return debug  
        a = [True, 0]
        randP = self.getRandomProb(index)   
        if randP==None:
            return None
        a[0]= randP             
        if a[0]:
            a[1] = self.getDistSuccByIndex(index).calcProb()
        else:          
            a[1] = self.getDistFailByIndex(index).calcProb()

        return a
        
        
    def getDistSuccByIndex(self,index):
        if len(self.distTableSucc) > index:
            return self.distTableSucc[index]
        return None
        


    def getDistFailByIndex(self,index):
        if len(self.distTableFail) > index:
            return self.distTableFail[index]
        return None 
        
        
    def clear (self):
       self.probTable = []
       self.distTableSucc = []
       self.distTableFail = [] 
       self.setAttrib("Successdistribution",[])
       self.setAttrib("probability",[])
       self.setAttrib("Failuredistribution",[])  
       self.reset = True
       
       
    def runPlan(self, index):
      children = self.getChildren()
      children[0].run(index) 

    def getAverageSuccTime(self, index):
        return self.getDistSuccByIndex(index).calcAverageTime()
        


 #table is the name of the table needed- attribute
    def createDistTable(self,table):
        string = self.getAttrib(str(table))
        
        table =[]        
        if string != None:
            table = self._parseString(string)

        newDistTable =[]
        #loop over the table- range (0,table len-1)- specifying the step value as 2
        if table != None:        
            for index in range(len(table)):
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
                    x=self._createUniformDist(table[index])
    #                x.printMe()
                    newDistTable.append(x)

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
    
    def setDEBUGnode(self,sSucc=None,sTime=None):
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
              
      #return a list of two str that represent float numbers
      return [str(stringNumA),str(stringNumB)]
      
      
      
    # Sinput should look like this - C[123,123],[123,1231],[54,23] 
    #input- the string above, output: dictionary of key and value
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
            