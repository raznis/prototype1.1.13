
import random
import sys



class Node:
  
  def __init__(self, prob, timef, times, n):
    self.prob = prob
    self.times = times
    self.timef = timef
    self.child = n
    self.status = False
    self.time = 0
    
  def getTimef(self):
    return self.timef
    
  def getTimes(self):
    return self.times  
    
  def getProb(self):
    return self.prob
    
  def getChildren(self):
    return self.child
    
    
  def getTheTime(self):
    return self.time
    
  def getStatus(self):
    return self.status 
    
    
  def setTheTime(self, t):
    self.time =t 
    
    
  def setStatus(self , s):
    self.status = s   
    
  def __iter__(self):
        return iter(self.time)  
    
  def randomProb(self):
    x = random.random()
    self.status = (x<= self.getProb())
    return (self.status)
    
  def getTime(self):
    if self.randomProb():
      self.time = self.getTimes()
      return self.getTimes()
    else:
      self.time = self.getTimef()
      return self.getTimef()
      
      
  def printChildren2(self):
    t= self.getChildren()
    count =1
    for i in t:
      print "child %d: %f prob, %f times, %f timef, %f time, %r status" %(count, i.getProb(), i.getTimes(), i.getTimef(), i.getTheTime(), i.getStatus())
      count = count +1
   
   
  def printChildren(self):
    global c
    c = 1
    if (self.getChildren() == []):
      print "child %d: %f prob, %f times, %f timef, %f time, %r status" %(c, self.getProb(), self.getTimes(), self.getTimef(),self.getTheTime(), self.getStatus())
    else:  
      for i in self.getChildren():      
	c = c + 1
	i.printChildren()
      c = c + 1
      print "parent %d: %f prob, %f times, %f timef, %f time, %r status" %(c, self.getProb(), self.getTimes(), self.getTimef(), self.getTheTime(), self.getStatus())
      
    
    
#task, seq   
  def run(self):
    global a
    a = True
    c = 0
    if (self.getChildren() == []):
     c = self.getTime() 
     a = a and (self.getStatus())
    else:
      for i in self.getChildren():	
	if not a:	  
	  break	
	c = c + i.run() 
	self.setStatus(a)
	i.printChildren()
    return c
      

  def runBool(self):
    a = True
    if (self.getChildren() == []):
      c = self.getTime()
      a = self.getStatus()
    else:
      for i in self.getChildren():
	if not a:	  
	  break	
	a = a and i.runBool()
	self.setStatus(a)
	self.setTheTime(self.getTheTime()+ i.getTheTime())  	
	#i.printChildren()
    return a    

 
 
  def runBoolList(self):
    a = [True, 0]
    if (self.getChildren() == []):
      a[1]= self.getTime()
      a[0] = self.getStatus()
    else:
      for i in self.getChildren():
	if not a[0]:	  
	  break	
	b = i.runBoolList()  
	a[0] = a[0] and b[0]
	self.setStatus(a[0])
	a[1] = a[1] + b[1]
	self.setTheTime(a[1])  	
	#i.printChildren()
    return a    
 
 
#task, sel   
  def runSel(self):
    global a
    a = False
    c = 0
    if (self.getChildren() == []):
     c = self.getTime() 
     a = a or (self.getStatus())
    else:
      for i in self.getChildren():	
	if a:	  
	  break	
	c = c + i.runSel() 
	self.setStatus(a)
	i.printChildren()
    return c  
 
  def runSelBool(self):
    a = False
    if (self.getChildren() == []):
      c = self.getTime()
      a = self.getStatus()
    else:
      for i in self.getChildren():
	if a:	  
	  break	
	a = a or i.runSelBool()
	self.setStatus(a)
	self.setTheTime(self.getTheTime()+ i.getTheTime())  	
	#i.printChildren()
    return a  
    
    


#task, prl 
  #def runPrl(self):
    #global a
    #a = False
    #c = 0
    #if (self.getChildren() == []):
      #print "befor a: %r, c: %f" %(a,c)
      #if (self.getStatus() and a):
	#c = min(c, self.getTime())
	#print "1"
      #elif (self.getStatus() and not(a)):
	#c = self.getTime()
	#print "2"
      #elif (not (self.getStatus()) and not(a)):   
	#c = max(c, self.getTime()) 
	#print "3"
      #a = a or self.getStatus()
      #print "after a: %r, c: %f" %(a,c)
    #else:
      #for i in self.getChildren():	
	#c = i.runPrl() 
	#self.setStatus(a)
	#i.printChildren()
    #return c  


##task, prl 
  #def runPrl(self):
    #a = False
    #c=0
    #if (self.getChildren() == []):
      #c = self.getTime()
      #a = self.getStatus()
    #else:
      #for i in self.getChildren():
	#a = a or i.runPrl()
	#self.setStatus(a)
	#i.printChildren()
	#t=[]
	#if (self.getStatus()):
	  ##self.setTheTime(min(filter(self.getStatus(), self.getChildren())))	
	  #for i in self.getChildren(): 
	    #if i.getStatus():
	      #t.append(i.getTheTime())
	  #self.setTheTime(min(t))
	#else:
	  #for i in self.getChildren(): 
	    #if not(i.getStatus()):
	      #t.append(i.getTheTime())
	  #self.setTheTime(max(t))	    
    #return a  
     

     ##task, sel without break
  #def runPrl(self):
    #a = False
    #if (self.getChildren() == []):
      #c = self.getTime()
      #a = self.getStatus()
    #else:
      #for i in self.getChildren():
	#a = a or i.runPrl()
	#self.setTheTime(self.getTheTime()+ i.getTheTime()) 
	#self.setStatus(a)	 	
	##i.printChildren()
    #return a 

    
  #def runPrl(self):
    ##global a
    #a = False
    #if (self.getChildren() == []):
      #c = self.getTime()
      #a = self.getStatus()
    #else:
      #for i in self.getChildren():
	#a = i.runPrl() or a 
	#self.setStatus(a)
	#self.setTheTime(self.getTheTime()+ i.getTheTime())	
    #return a
    
    
#self t, a t - take min
#self t, a f - take self
#self f, a t - take a
#self f, a f - take max   
    
  def runPrl(self):
    #global a
    a = False
    if (self.getChildren() == []):
      c = self.getTime()
      a = self.getStatus()
    else:
      for i in self.getChildren():
	#a = i.runPrl() or a 
	a = i.runPrl()
	if (self.getStatus()):
	  if a:
	    self.setTheTime(min(self.getTheTime(), i.getTheTime()))
	else:
	  if a:
	    self.setTheTime(i.getTheTime())
	  else:
	    self.setTheTime(max(self.getTheTime(), i.getTheTime()))
	a = self.getStatus() or a    
	self.setStatus(a)
    return a
    
    
    
    
	