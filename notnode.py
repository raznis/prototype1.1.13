# -*- coding: utf-8 -*-
"""
Created on Thu Dec 13 15:44:32 2012

@author: polak
"""


from Node import node

class NotNode (node):
    def __init__(self,treeInst,mytree,parent):
        node.__init__(self,treeInst,mytree,"not",parent)
    
    def run (self, index):
        print ("please implemnt run func in notNode")