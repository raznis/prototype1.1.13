from tree import xmlTree
from Node import node
import time



#provide a tree xml file      
def test1():
    start = time.time()
    tree = xmlTree("event1.xml")
    root = tree.getRoot()

    root.treeToXml("testE11.xml")  
    print("test 1.1: success!")
 
    node.debugMode = False
    for i in range(100):
        root.runPlan(0)    
    root.treeToXml("testE12.xml") 
 
    elapsed = (time.time() - start)
    print elapsed
    print "phase 2"
    node.debugMode = True
    for i in range(100):
        root.runPlan(0)    
    root.treeToXml("testE13.xml") 
    elapsed = (time.time() - start)
    print elapsed
    
#
#def test2():
#    start = time.time()
#    tree = xmlTree("event2.xml")
#    root = tree.getRoot()
#
#    root.treeToXml("testE21.xml")  
#    print("test 2.1: success!")
# 
#    node.debugMode = False
#    for i in range(100):
#        root.runPlan(0)    
#    root.treeToXml("testE22.xml") 
# 
#    elapsed = (time.time() - start)
#    print elapsed
#    print "phase 2"
#    node.debugMode = True
#    for i in range(100):
#        root.runPlan(0)    
#    root.treeToXml("testE23.xml") 
#    elapsed = (time.time() - start)
#    print elapsed
#    
#    
#    
#def test3():
#    start = time.time()
#    tree = xmlTree("event3.xml")
#    root = tree.getRoot()
#
#    root.treeToXml("testE31.xml")  
#    print("test 3.1: success!")
# 
#    node.debugMode = False
#    for i in range(100):
#        root.runPlan(0)    
#    root.treeToXml("testE32.xml") 
# 
#    elapsed = (time.time() - start)
#    print elapsed
#    print "phase 2"
#    node.debugMode = True
#    for i in range(100):
#        root.runPlan(0)    
#    root.treeToXml("testE33.xml") 
#    elapsed = (time.time() - start)
#    print elapsed
#        

if __name__ == "__main__":
    #run the 10 tests
    test1()
#    test2()
#    test3()
