# -*- coding: utf-8 -*-
"""

@author: polak
"""
from distribution import Distribution

class Normal(Distribution):
    #constractur
    def __init__(self, parmM,parmG):
        Distribution.__init__(self)
        self.parmM = parmM
        self.parmG = parmG
        
        
    def calcProb(self):
        raise NotImplementedError("calcProb- Normal") 
    
    #for debaug     
    def whoAmI(self):
        return "Normal"