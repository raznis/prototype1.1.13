# -*- coding: utf-8 -*-
"""

@author: polak
"""
import random
import math
import re
from lxml import etree
from distributions.computed import Computed
from copy import deepcopy

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
            self.treeInst =  etree.Element("plan")
            from tree import xmlTree
            self.myTree = xmlTree(None,self.treeInst)
        else:
            self.myTree = mytree
            self.treeInst = treeInstance
#        self.succ = False
#        self.time = 0
        self.isNot = False
        self.parent = parent 
        #node monitor property
        self.monitor = True
        #node child list
        self.childList = []
        #node probebility table
        self.probTable = []
        # node distribution table for success and failure
        self.distTableSucc = []
        self.distTableFail = []
        #update probability table
        probString = self.getAttrib("probability")
        if probString !=None:
            self.probTable= self._parseString(probString)
        else:
            self.probTable= None
        
        #node debuge child property
        self.DEBUGchild= False   
        self._updateChildDebug()
        self.DEBUG = None
     
        #node not property
        #self._updateNot()
        self.reset = False
            
        
        
        
    #parseString by whiteSpace
    def _parseString(self, string):
        words = re.split('\s+',string)
        return words
        
    
	
	
    #return parent. if it's the root- return None   
    def getParent(self):
        return self.parent
    

    
    #getter for probIndex
#    def getProbAtIndex(self,index):
#        if self.probTable!=None and len(self.probTable) > index:
#            return self.probTable[index]
      
        return None

    #return childs-list
    #def getChildList(self):
    #    return list(self.treeInst)
    
    #get branch-factor        
    def getBF(self):
        return (len(self.treeInst))
    
    

    #input:string-tagtype, create a new node with tag-type and add it to the node direct children
    #output - return the newNode
    def addNode(self,tag):
        node =self._createChildByTag(etree.SubElement(self.treeInst,tag))
        self.childList.append(node)
        return node
    #    while True :
    #        print("would you like to add attri0.1" resubutes to the new node?(Y/N)")
    #        ans = sys.stdin.read(1)
    #        if ans == 'N':getProbString(self):
    #            break
    #        
    #        parm = raw_input("Enter parm Name")
    #        value =  raw_input("Enter parma
    #        
    #        child.attrib[parm]=value
            
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
    
    #output: distribution as a string, or None
    #def _getDisttribuationType(self):
    #    return self.getAttrib("distribution")
    
    #output: return prob string or None
    # def getProbString(self):
    #     prob = self.getAttrib("probability")
    #     if prob == None :
    #         print ("can't get probability for")
    #         print (self.treeInst.tag)
    #         print (self.getAttrib("name"))
    #         print("please check if there is a probString")
    #    return prob
    
    #input: child num in the list , output: a new child node- not a deepcopy    
    def getChild(self,index):
            if index >= len(self.childList):
                print ("there is no such a child index")
                return None
            else:
                if len(self.childList) > 0:
                    return self.childList[index]
                else:
                    self._createChildList()
                    return self.childList[index]
             #run the node. each subclass should imple
        
    #def run(self, index):
    #    print "liat"
        #raise NotImplementedError("Subclasses should implement this!")    

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
      #  if elem.tag == "monitor":
      #      from monitornode import monitorNode
      #      return monitorNode(elem,self.myTree,self)
      
        #decorstor - L is for loop according to cogniteam code        
        if elem.tag == "dec":
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
        
#    def __getitem__(self):
#        return self
#######################-----Adi changes(23/12/2012)-----####################  

    #input - EtreeInst- element which it's tag is dec - decorator
    #output new node- loop/not with childen- example- for dec "!L!" crete not - loop - not      
    def _CreatDecoratorNodesFromName(self, element):
        name = element.get("name")
        newChild = None
        newEtreeInst = deepcopy(element)
        parent = element.getparent()
        lastChild = None
        #print (etree.tostring( newEtreeInst))
        #itertating over name char and creating node child as necessary
        for char in name:        
                #new child is the first child that replace decorator
                if newChild == None:
                        #if char is "L"- create loop node
                        if char == "L" :
                            #addNode func- create the node by tag and appand it to self.childList
                            newChild = self.addNode("loop") 
                        #if char is "!" - create not node
                        else:
                            if char == "!":
                                    newChild = self.addNode("not")
                #after we create newChild we'll appand it all the other- by newChild.addNode func.
                else:
                    if char == "L" :
                        lastChild = newChild.addNode("loop")
                    if char == "!":
                        lastChild = newChild.addNode("not")
                        
                        
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
                newChild.treeInst = newEtreeInst
            
       #after reading it name and creating nodes as necessary we want to replace this subElement with the updated tree and update the xml tree(used to be decorator)
       #replace(self, old_element, new_element)
        parent.replace(element, newChild.treeInst)
        
        return newChild
       
        
    def _updateEtreeToPrintXmlFile(self,updateNode):
            if updateNode == None :
                return None
            if updateNode.distTableSucc != [] :
                self.setAttrib("Successdistribution",self._distTableToString(self.distTableSucc))
            if updateNode.distTableFail != [] :  
                self.setAttrib("Failuredistribution",self._distTableToString(self.distTableFail))
                
            #get child list
            childList = updateNode.getChildren()
            #iterate over child list with recursive call (list of lists)  
            if childList != None :
                for child in childList :
                    self._updateEtreeToPrintXmlFile(child)
            
            
            
#######################-----Adi changes(17/12/2012)-----####################

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
        
    #dont know when we use this func        
    def DEBUGnode(self,sSucc=None,sTime=None):
        self.DEBUG = True
        
        
    def getDistSuccFromAttrib(self):
        pass
    
    def getDistFailFromAttrib(self):
         pass

    def addDistToSuccTable(self, dist):
        self.distTableSucc.append(dist)

    def addDistToFailTable(self, dist):
        self.distTableFail.append(dist)
        
    #try to read attribute from the xml file and update not node. if no attribute, update to False    
   # def _updateNot(self):
    #    ans = self.getAttrib("not")
    #    if ans!= None:
    #        if str(ans) == "T":
    #            self.isNot = True
    #        else:
    #            self.isNot = False
                
    #return true or false is this node is not
    #def getNot(self):
    #    return self.isNot
        
    #debug getter
    def getDebug(self):
        return self.DEBUG
        
        
    #check debug attribute - [True/False , time]   
    def _readDebugFromAttrib(self):
        ans = self.getAttrib("DEBUG")       
        if ans!=None :
            #debug is a list. hold two parms- DEBUG[0]- True/False , DEBUG[1]- time
            self.DEBUG = self._parseString(ans)            
        else:
            #debug set to None if can't read attributes from xml file
            self.DEBUG = None
            
            
    #get a table-distributions list and translate it back to string that we know how to read from xml file       
    def _distTableToString(self,table):
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
        
#######################-----Liat changes-----###############################



    def getRandomProb(self, index):
        x = random.random()
        #print x, self.getProbAtIndex(index)
        return (x <= float(self.getProbAtIndex(index)))
        
    def getTimeByDist(self, index):
        pass
   

    def setProbTable(self, probtable):
        self.probTable = probtable
        self.setAttrib("probability",probtable)
        
        
    def setDistTableSucc(self, distTable):
        self.distTableSucc = distTable
        self.setAttrib("Successdistribution",self._distTableToString(self.distTableSucc))
           
    def setDistTableFail(self, distTable):
        self.distTableFail = distTable
        self.setAttrib("Failuredistribution",self._distTableToString(self.distTableFail))    
      
#    #getter-time
#    def getTime(self):
#        if (self.getSucc()):
#            #self.setTime(random.random())
#            self.setTime(1)
#        else:
#            self.setTime(2)             
#        return self.time
#    
#    #setter time
#    def setTime(self,time):
#        self.time = time
#        self.setAttrib("time",time)   
#        
#        
#    def getSucc(self):
#        return (self.succ == True)
#        
#    def setSucc(self, setbool):
#        if setbool == True:
#             self.succ = True
#        else :
#             self.succ = False
#        self.setAttrib("succ",self.succ)
        
        
    def updateProbTableAtIndex(self, index, val):
        if (self.probTable==None or len(self.probTable)==0 ):
#            print "liat"
            a = []
            for i in range(int(math.pow(2,node.parmetersInTheWorld))):
                a.append([0,0])
            self.setProbTable(a)
        if val:
            self.probTable[index][0] = self.probTable[index][0]+1
            self.probTable[index][1] = self.probTable[index][1]+1
            self.setAttrib("probability",self.probTable)
        else:
            self.probTable[index][1] = self.probTable[index][1]+1
            self.setAttrib("probability",self.probTable)
            
            
            
            
            
    def setDistTableSuccAtIndex(self, index, time):
        if (self.distTableSucc==[]):
            a = []
            for i in range(int(math.pow(2,node.parmetersInTheWorld))):
                dist = Computed({})
                a.append(dist)
            self.setDistTableSucc(a)
        self.distTableSucc[index].setValueToTime(time, self.distTableSucc[index].getCountByTime(time)+1)
        self.setAttrib("Successdistribution",self._distTableToString(self.distTableSucc))
        #self.distTableSucc[index].printMe()
            
    
    def setDistTableFailAtIndex(self, index, time):
        if (self.distTableFail==[]):
            a = []          
            for i in range(int(math.pow(2,node.parmetersInTheWorld))):
                dist = Computed({})
                a.append(dist)
            self.setDistTableFail(a)   
        self.distTableFail[index].setValueToTime(time, self.distTableFail[index].getCountByTime(time)+1)
        self.setAttrib("Failuredistribution",self._distTableToString(self.distTableFail))
        #self.distTableFail[index].printMe()
        
   

    #getter for probIndex
    def getProbAtIndex(self,index):
        if self.probTable!=None and len(self.probTable) > index:
            if self.boolWhoAmI("tsk"):
                return self.probTable[index]
            else:                
                return self.probTable[index][0]/self.probTable[index][1]                
        return None
     
    def run(self, index):
        a = None
        if (node.debugMode):
            tmpIndex  = index
            a = self.getDebug()
            if (a!=None):
                if (self.getNot()):
                    a[0] = not(a[0])
                if not(self.boolWhoAmI("tsk")): 
                    if (self.monitor):
                        if a[0]:
                            self.setDistTableSuccAtIndex(tmpIndex, a[1])
                        else:
                            self.setDistTableFailAtIndex(tmpIndex, a[1])          
                        self.setProbTableAtIndex(tmpIndex, a[0])
        return a
    

   
    def setDebug(self, succ, time):
        self.DEBUG = [succ, time]     
        self.setAttrib("DEBUG", self.DEBUG )
        
    
    def runAsBaseCase (self, index):
        debug = node.run(self, index)
        if (debug!=None):
            return debug  
            
        a = [True, 0]        
        a[0]= self.getRandomProb(index)
        if (self.getNot()):
            a[0] = not(a[0])        
        if a[0]:
            a[1] = self.getDistSuccByIndex(index).calcProb()
        else:
            a[1] = self.getDistFailByIndex(index).calcProb()
        #print "Task:[%r %f]" %(a[0] ,a[1])    
        return a
        
###copy from task
        
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
