from tree import xmlTree
from Node import node
import sys
sys.path.append("/home/polak/Desktop/lxmlEtreeWiteDist/dist")


#create a tree from scratch
def test1():
    
    tree = node()
    root = tree
    #first child
    newChild = root.addNode("parallel")
    #notice that the childlist start from zero.
    child = root.getChild(0)
    #compare by instance id:
    if newChild.comparTo(child) == True :
        print("test 1: success!")
    else:
        print("test 1: failed :-(")

#provide a tree xml file      
def test2():
    tree = xmlTree("test2.xml")
    root = tree.getRoot()
    # root is always a plan    
    newNode = root.getChild(0)
    ChildList = newNode.getChildren()
    #iterate over first node children:
    count = 0
    for childNode in ChildList:
        count += 1
    if count == 5:
        print("test 2: success!")
    else:
        print("test 2: failed :-(")
    
    
#this test check the node-type contratur and thir oo
def test3():
    tree = node()
    root = tree
    #first child
    firstChild = root.addNode("seq")
    if firstChild == None:
        print ("error creating seq node")
        print("test 3: failed :-(")
        return None
        
    tempN = firstChild.addNode("seq")
    if tempN == None:
        print ("error creating seq node")
    else:
        tempN.setAttrib("probability","0.1 0.5")
        
    tempN = firstChild.addNode("not")
    if tempN == None:
        print ("error creating not node")
    else:
        tempN.setAttrib("probability","0.1 0.5")
        
    tempN = firstChild.addNode("loop")
    if tempN == None:
        print ("error creating loop node")
    else:
        tempN.setAttrib("probability","0.1 0.5")
        
    tempN = firstChild.addNode("parallel")
    if tempN == None:
         print ("error creating parallel node")
    else:
        tempN.setAttrib("probability","0.1 0.5")
        
    tempN = firstChild.addNode("tsk")
    if tempN == None:
        print ("error creating tsk node")
    else:
        tempN.setAttrib("probability","0.1 0.5")
        
    tempN = firstChild.addNode("select")
    if tempN == None:
        print ("error creating selector node")
    else:
        tempN.setAttrib("probability","0.1 0.5")
    
    #iterate over firstChild children:
    firstChildList = firstChild.getChildren()
    count = 0
    for childNode in firstChildList:
        count += 1
    if count == 6:
        print("test 3: success! please check the file test3.xml - every tag need to have the same attrib.")
    else:
        print("test 3: failed :-(")
    
    #print the tree we built from scratch to xml file.
    #please check the file- every tag need to have the same attrib.
    root.treeToXml("test3.xml")
    

#please run test 3 before test 4:    
def test4():
    tree = xmlTree("test3.xml")
    #remember- root is alwayes type/tag- plan
    root = tree.getRoot()
    ans = []
    ans.append(root.boolWhoAmI("plan"))
    firstChild = root.getChild(0)
    ans.append(firstChild.boolWhoAmI("seq"))
    ans.append((firstChild.getChild(0)).boolWhoAmI("seq"))
    ans.append((firstChild.getChild(1)).boolWhoAmI("not"))
    ans.append((firstChild.getChild(2)).boolWhoAmI("loop"))
    ans.append((firstChild.getChild(3)).boolWhoAmI("parallel"))
    ans.append((firstChild.getChild(4)).boolWhoAmI("tsk"))
    ans.append((firstChild.getChild(5)).boolWhoAmI("select"))
    
    for index in range(0,7):
        if ans[index] == False:
            print("test 4: failed :-(")
            
    print("test 4: success!")
 
           
#please run test 3 before test 5: - check attrib func/method    
def test5():
    tree = xmlTree("test3.xml")
    #remember- root is alwayes type/tag- plan
    root = tree.getRoot()
    ans = []
    ans.append(root.getAttrib("probability"))
    firstChild = root.getChild(0)
    ans.append(firstChild.getAttrib("probability"))
    ans.append((firstChild.getChild(0)).getAttrib("probability"))
    ans.append((firstChild.getChild(1)).getAttrib("probability"))
    ans.append((firstChild.getChild(2)).getAttrib("probability"))
    ans.append((firstChild.getChild(3)).getAttrib("probability"))
    ans.append((firstChild.getChild(4)).getAttrib("probability"))
    ans.append((firstChild.getChild(5)).getAttrib("probability"))
    
    #ans 1+2 dosn't have attribut- None
    if ans[0] !=None or ans[1] != None :
        print("test 5: failed :-(")
        
    for index in range(2,7):
        if ans[index] != "0.1 0.5":
            print("test 5: failed :-(")
            print (index)
            
    print("test 5: success!")

    
 #check the monitor set/get func/method   
def test6():
    tree = xmlTree("test2.xml")
    root = tree.getRoot()
    firstChild = root.getChild(0)
    childList = firstChild.getChildren()
    for childNode in childList:
        childNode.setMonitor(False)
        
    for childNode in childList:
        boolVal = childNode.isMonitored()
        if boolVal != False :
            print("test 6: failed :-(")
            return None
    
    print("test 6: success!")
     
 #empty test - will be implemented- feeling creative? :-)    
def test7():
  
    tree = node()
    root = tree
    #first child
    firstChild = root.addNode("parallel")
    if firstChild == None:
        print ("error creating seq node")
        print("test 3: failed :-(")
        return None
    
    
    for j in range(3): 
      tempN = firstChild.addNode("seq")
      if tempN == None:
	  print ("error creating seq node")
	  
      for i in range(5):
          if ((j==1) and (i==2)):
              tempN1 = tempN.addNode("seq")
              if tempN1 == None:
                  print ("error creating seq node")
              else:
                  for i in range(4):
                      tempN2 = tempN1.addNode("tsk")
                      if tempN2 == None:
                          print ("error creating seq node")
                      else:
                          tempN2.setAttrib("time","1")
                          tempN2.setAttrib("succ","T")
                          tempN2.setTime(0)
                          tempN2.setSucc(False)
                          tempN2.setProbTable([0.8, 0.5])
          else:
              tempN1 = tempN.addNode("tsk")
              if tempN1 == None:
                  print ("error creating seq node")
              else:
                  tempN1.setAttrib("time","1")
                  tempN1.setAttrib("succ","T")
                  tempN1.setTime(0)
                  tempN1.setSucc(False)
                  tempN1.setProbTable([0.7, 0.5])
             
	    
        

    
    #iterate over firstChild children: 
    firstChildList = firstChild.getChildren()
    firstChild.run(0)
    count = 0
    for childNode in firstChildList:
        count += 1
    if count == 3:
        print("test 3: success! please check the file test4.xml - every tag need to have the same attrib.")
    else:
        print("test 3: failed :-(")
    
    #print the tree we built from scratch to xml file.
    #please check the file- every tag need to have the same attrib.
    root.treeToXml("test4.xml")
    
    
def test8():
   tree = xmlTree("test3.xml")
   root = tree.getRoot()
   
   #this child is type- tsk
   child = root.getChild(0)
   
   ### create a new dist - and 
   dist = _createNormalDist(5,2)
   #add to succ table
   child.addDistToSuccTable(dist)
   #add to fail table/
   child.addDistToFailTable(dist)
   #get distribute from the node by it's index (p1,p2,p3..)
   distGet = child.getSuccDistAtIndex(0)
   #check that it has the same parms 
   if (distGet!=None and distGet.parmM == float(5)):
       print ("test 8.1: success!")

   else:
        ("test 8.1: failed :-(")
        
    # try to create computed dist.
   dist = _createComputedDist()
   dist.setValueToTime(0.1,1)
   
   if (dist.getCountByTime(0.1) == 1):
       print ("test 8.2: success!")

   else:
        ("test 8.2: failed :-( - check computed dist")
        
   print ("1,2,3,4,5")
   
def test9():
    pass
def test10():
    pass
def _createComputedDist(string = None):
    from computed import Computed
    return Computed()
    
#just for the test.
def _createNormalDist(parmM,parmG):
   from normal import Normal
   return Normal(float(parmM),float(parmG))
        
def _createUniformDist(parmA,parmB):
   from uniform import Uniform
   return Uniform(float(parmA),float(parmB))

if __name__ == "__main__":
    #run the 10 tests
#    test1()
#    test2()
#    test3()
#    test4()
#    test5()
#    test6()
#    test7()
     test8()
#    test9()
#    test10()
    