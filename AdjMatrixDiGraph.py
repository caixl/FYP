'''
Created on 8 Oct, 2014

@author: Cai Xinlei
'''
from random import randint

class AdjMatrixDiGraph(object):
    '''
    Graph implemented using adjacency matrix
    '''
    
    #adjacency matrix, represented by a 2D array
    _adj_m = []
    #number of vertices and edges
    _V = 0
    _E = 0
    
    def __init__(self, V):
        '''
        Constructor
        Empty graph with _V vertices
        '''
        if V < 0:
            raise RuntimeError("Number of vertices must be nonnegative")
        self._V = V
        self._E = 0
        for i in range (0, V):
            self._adj_m.append([False] * V)
        
    def gen_random(self, E):
        '''
        random graph with _V vertices and _E edges
        '''
        V = self._V
        if E < 0:
            raise RuntimeError("Number of edges must be nonnegative")
        if E > V*V:
            raise RuntimeError("Too many edges")
        
        while self._E != E:
            v = randint(0,V-1)
            w = randint(0,V-1)
            self.add_edge(v, w)
        
    def get_E(self):
        return self._E
    
    def get_V(self):
        return self._V
    
    def add_edge(self, v, w):
        '''
        add directed edge v->w
        '''
        if not self._adj_m[v][w]: 
            self._E += 1
        self._adj_m[v][w] = True
        
     
    class AdjIterator():
        _v = 0
        _w = 0
        _G = None
        
        def __init__(self, v, G):
            self._v = v
            self._G = G
            
        def __iter__(self):
            '''
            return the iterator itself
            '''
            return self
        
        def has_next(self):
            while self._w < self._G._V:
                if self._G._adj_m[self._v][self._w]:
                    return True
                self._w += 1
            return False
        
        def next(self):
            if self.has_next():
                self._w += 1
                return self._w-1
            else:
                raise StopIteration()
    
    def adj(self, v):
        return self.AdjIterator(v, self)
    
    def __str__(self):
        s = "V:%i E:%i \n"%(self._V, self._E)
        for v in range(0, self._V):
            s += "%i: "%v
            for w in self.adj(v):
                s += "%i "%w
            s += "\n"
        return s
        
if __name__=="__main__":
    G = AdjMatrixDiGraph(10)
    G.gen_random(3)
    print G
    
    