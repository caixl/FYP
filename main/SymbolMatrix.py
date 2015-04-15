'''
Created on 16 Oct, 2014

@author: Xinlei Cai
'''

class SymbolMatrix():
    '''
    classdocs
    '''
    _encMatix = []
    
    #string to index
    _st = {}
    #index to string
    _keys = {}
    

    def __init__(self, N, symbols=None, vertices=None):
        '''
        Constructor
        '''
     
        self._encMatix = []
        self._st = {}
        self._keys = {}
        
        if symbols==None and vertices!=None:
            symbols = {}
            for i in range(0,len(vertices)):
                symbols[vertices[i]] = i
                
                
        self._encMatix = [None]*N
        for i in range(0, N):
            self._encMatix[i] = [None]*N
            
        self._st = symbols
            
        for label in self._st.keys():
            self._keys[self._st[label]] = label
        
    
    def set_matrix(self, value, i, j):
        self._encMatix[i][j] = value
        
    
    def get_cell_by_index(self, i, j):
        return self._encMatix[i][j]
    
    def get_cell_by_symbol(self, s1, s2):
        return self._encMatix[self._st[s1]][self._st[s2]]
    
    
    def __str__(self):
        return str(self._encMatix)