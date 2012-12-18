# -*- coding: utf-8 -*-
"""

@author: polak
"""

from distribution import Distribution

class Uniform(Distribution):
    #constractur
    def __init__(self, parmA,parmB):
        Distribution.__init__(self)
        self.parmA = parmA
        self.parmB = parmB
        
        
    def calcProb(self):
        raise NotImplementedError("calcProb- uniform") 
    
    #for debaug     
    def whoAmI(self):
        return "Uniform"