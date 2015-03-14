'''
Created on 16 Jan, 2015

@author: Xinlei Cai
'''
from random import randint
from collections import deque
#from Bag import Bag

class AdjListDiGraph(object):
    '''
    Graph implemented using adjacency matrix
    '''
    
    #adjacency list
    _adj_l = []
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
        self._adj_l = [None] * V
        for i in range (V):
            self._adj_l[i] = deque()
        
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
            while v==w:
                v = randint(0,V-1)
                w = randint(0,V-1)
            self.add_edge(v, w)
        
    def get_E(self):
        return self._E
    
    def get_V(self):
        return self._V
    
    def validateVertex(self, v):
        if v<0 or v>=self._V:
            raise RuntimeError("vertex %s is not between 0 and %s"%(v,self.V-1))
            
          
        
    def add_edge(self, v, w):
        '''
        add directed edge v->w
        '''
        self.validateVertex(v)
        self.validateVertex(w)
        for elem in self.adj(v):
            if elem==w or w==v:
                return
        self._adj_l[v].append(w)
        self._E += 1
    
    def adj(self, v):
        self.validateVertex(v)
        return self._adj_l[v]
    
    def outdegree(self,v):
        self.validateVertex(v)
        return self._adj_l[v].size()
    
    def reverse(self):
        R = AdjListDiGraph()
        for v in range(self._V):
            for w in self.adj(v):
                R.addEdge(w,v)
        return R
    
    def __str__(self):
        s = "V:%i E:%i \n"%(self._V, self._E)
        for v in range(0, self._V):
            s += "%i: "%v
            for w in self.adj(v):
                s += "%i "%w
            s += "\n"
        return s
        
if __name__=="__main__":
    G = AdjListDiGraph(10)
    G.gen_random(10)
    print G
    
    