# -*- coding: utf-8 -*-
"""

@author: polak
"""
import random
import re
from lxml import etree


class node:
    
    #global variable - represents the amount of different parmeters of the world.
    #it is a class attribute and can accessed via class node.parameterInTheWorld
    #can be set from everywhere that import node
    parmetersInTheWorld = 0
    
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
        self.succ = False
        self.time = 0
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
            self.probTable = self._parseString(probString)
        else:
            self.probTable= None
        
        #node debuge child property
        self.DEBUGchild= False   
        self._updateChildDebug()
        self.DEBUG = False
        #node not property
        self._updateNot()
            
        
        
        
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
        return self._createChildList()
                
        
    #create the childs list    
    def _createChildList(self):
        if len(self.childList) !=0:
            return self.childList
        for element in list(self.treeInst):
            self.childList.append(self._createChildByTag(element))
        return self.childList
    
    #output: disType as a string, or None
    def _getDisttribuationType(self):
        return self.getAttrib("distribution")
    
    #output: return prob string or None
    # def getProbString(self):
    #     prob = self.getAttrib("probability")
    #     if prob == None :
    #         print ("can't get probability for")
    #         print (self.treeInst.tag)
    #         print (self.getAttrib("name"))
    #         print("please check if there is a probString")
    #    return prob
    
    #input: child num in the list , output: a new child now- not a deepcopy    
    def getChild(self,index):
            if index >= self.getBF():
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
        #create the new node accordint to the type
        if elem.tag == "seq":
            from seqnode import SeqNode
            return SeqNode(elem,self.myTree,self)
        if elem.tag == "tsk":
            from tsknode import TskNode
            return TskNode(elem,self.myTree,self)
      #  if elem.tag == "monitor":
      #      from monitornode import monitorNode
      #      return monitorNode(elem,self.myTree,self)
        if elem.tag == "loop":
            from loopnode import LoopNode
            return LoopNode(elem,self.myTree,self)
            #need to continue implementing the rest..
      # if elem.tag == "not":
      #     from notnode import NotNode
      #     return NotNode(elem,self.myTree,self)
        if elem.tag =="parallel":
            from parallelnode import ParallelNode 
            return ParallelNode(elem,self.myTree,self)
        if elem.tag =="select":
            from selectnode import SelectNode 
            return SelectNode(elem,self.myTree,self)
                
            
            
            
    def treeToXml(self,fileName):
       self.myTree.treeToXml(fileName)
         
         
    def setMonitor(self,boolSet):
        self.monitor = boolSet
        
    def comparTo(self,nodeToCompare):
        return id(self)==id(nodeToCompare)
        
    def __getitem__(self):
        return self
        
      
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
            
    def isChildDebug(self):
        return self.DEBUGchild
        
            
    def DEBUGnode(self,sSUCC=None,sTime=None):
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
    def _updateNot(self):
        ans = self.getAttrib("not")
        if ans!= None:
            if str(ans) == "T":
                self.isNot = True
            else:
                self.isNot = False
                
    #return true or false is this node is not
    def isNot(self):
        return self.isNot
        
    def isDEBUG(self):
        return self.DEBUG
        
#######################-----Liat changes-----###############################



    def getRandomProb(self, index):
        succprob = []
        x = random.random()
        #print x, self.getProbAtIndex(index)
        if (x <= self.getProbAtIndex(index)):
            self.setSucc(True)
            succprop = [True,self.getProbAtIndex(index)]
        else:
            self.setSucc(False)
            succprop = [False, (1-self.getProbAtIndex(index))]        
        return self.getSucc()
        
        
    def getTimeByDist(self, index):
        pass
   

    def setProbTable(self, probtable):
        self.probTable = probtable
        self.setAttrib("probability",probtable)
      
    #getter-time
    def getTime(self):
        if (self.getSucc()):
            #self.setTime(random.random())
            self.setTime(1)
        else:
            self.setTime(2)             
        return self.time
    
    #setter time
    def setTime(self,time):
        self.time = time
        self.setAttrib("time",time)   
        
        
    def getSucc(self):
        return (self.succ == True)
        
    def setSucc(self, setbool):
        if setbool == True:
             self.succ = True
        else :
             self.succ = False
        self.setAttrib("succ",self.succ)
        
        
    def setProbTableAtIndex(self, index, val):
        if (self.probTable==None):
            a = []
            #rang have to be the num of 2^param - need from Adi 
            for i in range(2):
                a.append([0,0])
            self.setProbTable(a)
        if val:
            self.probTable[index][0] = self.probTable[index][0]+1
            self.probTable[index][1] = self.probTable[index][1]+1
            self.setAttrib("probability",self.probTable)
        else:
            self.probTable[index][1] = self.probTable[index][1]+1
            self.setAttrib("probability",self.probTable)
   

    #getter for probIndex
    def getProbAtIndex(self,index):
        if self.probTable!=None and len(self.probTable) > index:
            if self.boolWhoAmI("tsk"):
                return self.probTable[index]
            else:                
                return self.probTable[index][0]/self.probTable[index][1]                
        return None
     
    def run(self, index):
        print "liat"
        if (self.DEBUGnode()):
            return [True, 1]
        #raise NotImplementedError("Subclasses should implement this!")   