# -*- coding: utf-8 -*-
"""

@author: polak
"""
from distribution import Distribution

class Computed(Distribution):
    #constractur
    def __init__(self,Map = {}):
        Distribution.__init__(self)
         #map is a python dictionary{[time,count]..}    
        self.map = Map
        
       
    def calcProb(self):
        raise NotImplementedError("calcProb- computed")
     
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