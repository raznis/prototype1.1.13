from tree import xmlTree
from Node import node
import time



#provide a tree xml file      
def test2():
    start = time.time()
    tree = xmlTree("event1.xml")
    root = tree.getRoot()

    root.treeToXml("testE21.xml")  
    print("test 2.1: success!")
 
    node.debugMode = False
    for i in range(100):
        root.runPlan(0)    
    root.treeToXml("testE22.xml") 
 
    elapsed = (time.time() - start)
    print elapsed
    print "phase 2"
    node.debugMode = True
    for i in range(100):
        root.runPlan(0)    
    root.treeToXml("testE23.xml") 
    elapsed = (time.time() - start)
    print elapsed
    

#changed by RAZ -- we can now import from dist.* files, since the directory has an empty __init__.py file, and python recognizes it as a module.#thanks
def _createComputedDist(string = None):
    from distributions.computed import Computed
    return Computed()
    
#changed by RAZ -- we can now import from dist.* files, since the directory has an empty __init__.py file, and python recognizes it as a module.
def _createNormalDist(parmM,parmG):
   from distributions.normal import Normal
   return Normal(float(parmM),float(parmG))

#changed by RAZ -- we can now import from dist.* files, since the directory has an empty __init__.py file, and python recognizes it as a module.        
def _createUniformDist(parmA,parmB):
   from distributions.uniform import Uniform
   return Uniform(float(parmA),float(parmB))

if __name__ == "__main__":
    #run the 10 tests
    #test1()
    test2()
    #test3()
    #test4()
    #test5()
    #test6()
    #test7()
    #test8()
    #test9()
    #test10()
    #test11()
#   test12()
    #test13()
