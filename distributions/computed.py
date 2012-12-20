# -*- coding: utf-8 -*-
"""

@author: polak
"""
import random
from distribution import Distribution

class Computed(Distribution):
    #constractur
    def __init__(self,Map = {}):
        Distribution.__init__(self)
         #map is a python dictionary{[time,count]..}    
        self.map = Map
        
       
    def calcProb(self):
        x = random.random()
        return self.distNormalize(x)
    
    
    def distNormalize(self, x):
        s = 0.0
        a = 0
        for i in self.map.values():
            s=s+i
        for i in self.map:
            a = a + self.map.get(i)/s
            if (a >= x):
                return i
            
    #search for the time key in the dictionary- return 0  or count.- value
    def getCountByTime(self,time):
        ans = self.map.get(str(time))        
        if (ans != None):
            return ans
        return 0
    #search for the time key in the dictionary- and update it. or create it with value.   
    #Changed by RAZ - removed casting value to str    
    def setValueToTime(self,time,value):
        if (self.map.get(str(time)) != None):
            self.map[str(time)]=value
            
        else:
            self.map.setdefault(str(time) , value)
     
       
    def stringToDictionary(self,string):
        pass
    
   #for debaug     
    def whoAmI(self):
        return "Computed"
        
    def printMe (self):
        for i in self.map:
            print i, self.map.get(i)
        