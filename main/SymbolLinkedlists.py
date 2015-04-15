'''
Created on 11 Feb, 2015

@author: Xinlei Cai
'''
from collections import deque
from charm.toolbox.pairinggroup import PairingGroup,pair,G1,G2,ZR

class SymbolLinkedlists():
    '''
    classdocs
    '''
    _encList = []
    #string to index
    _st = {}
    #index to string
    _keys = {}
    
    #tracking the longest length
    _longest = 0
    

    def __init__(self, symbols=None, vertices=None):
        '''
        Constructor
        '''
        self._encList = []
        self._st = {}
        self._keys = {}
        self._longest = 0
        
        if symbols==None and vertices!=None:
            symbols = {}
            for i in range(0,len(vertices)):
                symbols[vertices[i]] = i
            
            
        N = len(symbols)
        self._encList = [None]*N
        for i in range(N):
            self._encList[i] = deque()
            
        self._st = symbols
            
        for label in self._st.keys():
            self._keys[self._st[label]] = label
            
    
    def add_item(self, value, index):
        if index >= 0 and index<=len(self._st):
            self._encList[index].append(value)
            
            curlen = len(self._encList[index])
            if curlen > self._longest:
                self._longest = curlen
            return index
        
        return -1
    
    def get_list(self, nodename):
        return self._encList[self._st[nodename]]
    
    def get_size(self):
        return len(self._st)
    
    def get_encList(self):
        return self._encList
    
    def get_longest(self):
        return self._longest
    
    def __str__(self):
        """
        s = ""
        for v in range(len(self._st)):
            s += "%s: "%self._keys[v]
            for w in self._encList[v]:
                s += "->%s"%w
            s += "\n"
        """
        return str(self._encList) 