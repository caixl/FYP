'''
Created on 9 Oct, 2014

@author: Xinlei Cai
'''

from AdjMatrixDiGraph import AdjMatrixDiGraph

class SymbolDiGraph(object):
    
    #string to index
    _st = {}
    #index to string
    _keys = {}
    #DiGraph
    _G = None
    
    def __init__(self, symbols, G=None):
        '''
        Randomly generate a graph if digraph G is not set
        '''
        if G==None:
            self._G = AdjMatrixDiGraph(len(symbols))
            self._G.gen_random(6)
            G = self._G
        
        V = len(symbols)
        if V != G.get_V():
            raise RuntimeError("Number of symbols does not match number of vertices")
        if V > len(set(symbols)):
            raise RuntimeError("Symbols are not unique, please check")
        
        for symbol in symbols:
            if symbol not in self._st:
                self._st[symbol] = len(self._st)
            
        for label in self._st.keys():
            self._keys[self._st[label]] = label

    def add_edge(self, s1, s2):
        '''
        Add an edge to the graph
        '''
        v = self._st[s1]
        w = self._st[s2]
        self._G.add_edge(v, w)
    
    def contains(self, s):
        '''
        Does the digraph contain the vertex named s
        '''
        return (s in self._st)
    
        
    def index(self, s):
        '''
        Returns the integer associated with the vertex named s
        '''
        return self._st[s]
    
    
    def name(self, v):
        '''
        Returns the name of the vertex associated with the integer v
        '''
        return self._keys[v]
    
    def get_V(self):
        '''
        Returns the size of the vertices
        '''
        return self._G.get_V()
    
    def get_G(self):
        '''
        Returns the digraph assoicated with the symbol graph.
        '''
        return self._G
    
    def get_edge_index(self, i, j):
        '''
        Get the number of edges by indices
        '''
        return self._G._adj_m[i][j]
    
    def get_edge_symbol(self, s1, s2):
        '''
        Get the number of edges by symbols
        '''
        return self._G._adj_m[self._st[s1]][self._st[s2]]
    
    def get_keys(self):
        return self._keys
    
    def get_st(self):
        return self._st
    
    def __str__(self):
        s = "  "
        for v in range(0, self._G._V):
            s += "%s "%self._keys[v]
        
        s += "\n"   
        for v in range(0, self._G._V):
            s += "%s "%self._keys[v]
            for w in range(0, self._G._V):
                s += "%i "%self._G._adj_m[v][w]
            s += "\n"
        return s
 
if __name__=="__main__":
    vertices = ['a','b','c','d']
    sg = SymbolDiGraph(vertices)
    
    print sg
    
