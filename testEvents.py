from tree import xmlTree
from Node import node
import time



#provide a tree xml file      
def test1():
    
    start = time.time()
    tree = xmlTree("event1.xml")
    root = tree.getRoot()
    node.parmetersInTheWorld = 1
    root.treeToXml("testE11.xml")  
    print("test 1.1: success!, testE11.xml")
 
    node.debugMode = False
    for i in range(100):
        root.runPlan(0)    
    root.treeToXml("testE12.xml") 
    print("test 1.2: success!, testE12.xml")
    print "Success probability befor debug mode: %f" %root.getChild(0).getProbAtIndex(0)
    print "Average success time: %f" %root.getChild(0).getAverageSuccTime(0)
    elapsed = (time.time() - start)
    print "Time: %f" %elapsed
    print "-------Debug mode-------"
    node.debugMode = True
    for i in range(100):
        root.runPlan(0)    
    root.treeToXml("testE13.xml") 
    print("test 1.3: success!, testE13.xml")
    print "Success probability after debug mode: %f" %root.getChild(0).getProbAtIndex(0)
    print "Average success time: %f" %root.getChild(0).getAverageSuccTime(0)
    elapsed = (time.time() - start)
    print "Time: %f" %elapsed
    
    
def test2():
    start = time.time()
    tree = xmlTree("event2.xml")
    root = tree.getRoot()
    node.parmetersInTheWorld = 1

    root.treeToXml("testE21.xml")  
    print("test 2.1: success!")
 
    node.debugMode = False
    for i in range(100):
        root.runPlan(0)    
    root.treeToXml("testE22.xml") 
    print("test 2.2: success!")
    print "Success probability befor debug mode: %f" %root.getChild(0).getProbAtIndex(0)
    print "Average success time: %f" %root.getChild(0).getAverageSuccTime(0)
    elapsed = (time.time() - start)
    print "Time: %f" %elapsed
    print "-------Debug mode-------"
    node.debugMode = True
    for i in range(100):
        root.runPlan(0)    
    root.treeToXml("testE23.xml") 
    print("test 2.3: success!")
    print "Success probability after debug mode: %f" %root.getChild(0).getProbAtIndex(0)
    print "Average success time: %f" %root.getChild(0).getAverageSuccTime(0)
    elapsed = (time.time() - start)
    print "Time: %f" %elapsed
    
    
def test3():
    start = time.time()
    tree = xmlTree("event3.xml")
    root = tree.getRoot()
    node.parmetersInTheWorld = 1

    root.treeToXml("testE31.xml")  
    print("test 3.1: success!")
 
    node.debugMode = False
    for i in range(100):
        root.runPlan(0)    
    root.treeToXml("testE32.xml") 
    print("test 3.2: success!")
    print "Success probability befor debug mode: %f" %root.getChild(0).getProbAtIndex(0)
    print "Average success time: %f" %root.getChild(0).getAverageSuccTime(0)
    elapsed = (time.time() - start)
    print "Time: %f" %elapsed
    print "-------Debug mode-------"
    node.debugMode = True
    for i in range(100):
        root.runPlan(0)    
    root.treeToXml("testE33.xml") 
    print("test 3.3: success!")
    print "Success probability after debug mode: %f" %root.getChild(0).getProbAtIndex(0)
    print "Average success time: %f" %root.getChild(0).getAverageSuccTime(0)
    elapsed = (time.time() - start)
    print "Time: %f" %elapsed

def test4():
    print "-------TEST 4-------"
    start = time.time()
    tree = xmlTree("small_test.xml")
    root = tree.getRoot()
    node.parmetersInTheWorld = 1

    root.treeToXml("small_test_before_run.xml")  
    print("test 4.1: success!")
 
    node.debugMode = False
    for i in range(100):
        root.runPlan(0)    
    for i in range(100):
        root.runPlan(1)
    root.treeToXml("small_test_no_debug.xml") 
    print("test 4.2: success!")
    print "Success probability in offline mode: Clear sky = %f, Cloudy = %f" %(root.getChild(0).getProbAtIndex(0),root.getChild(0).getProbAtIndex(1))
    print "Average success time with clear sky = %f" %(root.getChild(0).getAverageSuccTime(0))
    print "Average success time when Cloudy = %f" %(root.getChild(0).getAverageSuccTime(1))
    elapsed = (time.time() - start)
    print "Time: %f" %elapsed
    print "-------Debug mode-------"
    node.debugMode = True
    for i in range(100):
        root.runPlan(0)    
    for i in range(100):
        root.runPlan(1)   
    root.treeToXml("small_test_debug_mode.xml") 
    print("test 4.3: success!")
    print "Success probability in debug mode: Clear sky = %f, Cloudy = %f" %(root.getChild(0).getProbAtIndex(0),root.getChild(0).getProbAtIndex(1))
    print "Average success time in debug mode with clear sky = %f" %(root.getChild(0).getAverageSuccTime(0))
    print "Average success time in debug mode when Cloudy = %f" %(root.getChild(0).getAverageSuccTime(1))
    elapsed = (time.time() - start)
    print "Time: %f" %elapsed
    print "-----------------------"
    
if __name__ == "__main__":
    #run the 10 tests
    test1()
    test2()
    test3()
    test4()
