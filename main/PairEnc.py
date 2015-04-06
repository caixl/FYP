'''
Modified on 26 Feb 2015

@author: Xinlei Cai
'''

from charm.toolbox.pairinggroup import PairingGroup,pair,G1,G2,GT,ZR
from SymbolDiGraph import SymbolDiGraphLst
from SymbolLinkedlists import SymbolLinkedlists
from AdjListDiGraph import AdjListDiGraph
import time


class PairEncSymbolDiGraph:
    
    # the symbol graph
    _symbol_graph = None
    # operating group
    _group = None
    
    _pk = 0
    _mk = {}
    
    
    # Encrypted adjlist
    _enc_adjlist = {}
    
    def __init__(self, symbol_graph):
        '''
        Constructor
        '''
        self._group = PairingGroup('SS512')
        self._symbol_graph = symbol_graph

        pass
        
    def setup(self):
        '''
        generate public parameters
        '''
        g = self._group.random(G1)
        gp = self._group.random(G2)
        # initialize pre-processing for generators
        g.initPP();
        gp.initPP()
        
        mk_num = self._symbol_graph.get_V()
        #self._mk_s = [None]*mk_num
        #self._mk_t = [None]*mk_num
        self._mk = {'s':{},'t':{}}
        for i in range(mk_num):
            self._mk['s'][self._symbol_graph.get_keys()[i]] = self._group.random(ZR)
            self._mk['t'][self._symbol_graph.get_keys()[i]] = self._group.random(ZR)
        
        self._pk = { 'g':g, 'gp':gp}
        
        #testing
        '''
        a = self._group.random(ZR)
        s = self._group.random(ZR)
        t = self._group.random(ZR)
        gs = g**(s*t)
        gas = gp**(a/s)
        g2at = pair(g,gp)**(a*t)
        print pair(gs,gas)
        print g2at
        '''
        
        
    
    def padding(self, llists):
        '''
        Padding. Being called when encryption is done
        '''
        num = llists.get_size()
        for i in range(num):
            encList = llists.get_encList()
            size = len(encList[i])
            if size < llists.get_longest():
                for _ in range(llists.get_longest()-size):
                    self._enc_adjlist.add_item(self._pk['g']**self._group.random(ZR), i)
                    
        
    def encrypt(self):
        '''
        Encrypt whole graph with each cell in the matrix using corresponding symbols
        '''
        assert self._mk, "Please do setup first."
        
        self._enc_adjlist = SymbolLinkedlists(self._symbol_graph.get_st())
        size = len(self._symbol_graph.get_st())
        for v in range(size):
            for w in self._symbol_graph.adj(v):
                self._enc_adjlist.add_item(self._pk['g']**(self._mk['s'][self._symbol_graph.get_keys()[v]]
                                                           *self._mk['t'][self._symbol_graph.get_keys()[w]])
                                           ,v)
       
        #print self._enc_adjlist
        self.padding(self._enc_adjlist)    
        #print self._enc_adjlist
        
        return self._enc_adjlist
    
    @classmethod
    def decrypt(self, sk, cipher_adjlist, query_attr_list):
        '''
        Decryption requires master_public_key, user secret key, and cipher
        '''
        res_graph = SymbolDiGraphLst(query_attr_list, AdjListDiGraph(len(query_attr_list)))
        
        for attr in query_attr_list:
            cipherlist = cipher_adjlist.get_list(attr)
            for node in cipherlist:
                candi = pair(node,sk['gas'][attr])
                for key in sk['g2at']:
                    if candi == sk['g2at'][key]:
                        res_graph.add_edge(attr,key)
        
        return res_graph
        '''
        group = PairingGroup('SS512')
        kpabe = KPabe(group)
        hyb_abe = HybridKPABEnc(kpabe, group)
        
        #convert to lower case
        msg = ""
        for query in queries:
            s1 = query[0].lower()
            s2 = query[1].lower()
            cipher = cipher_matrix.get_cell_by_symbol(s1, s2)
            msg +=  hyb_abe.decrypt(cipher, sk) + " "
        '''
        return ''
    
    def key_generation(self, attr_list):
        '''
        Generate individual's secret key using the given sub-graph node list
        '''
        assert (self._pk and self._mk), "Please do setup first."
        alpha = self._group.random(ZR)
        sk = {'gas':{},'g2at':{}}
        for attr in attr_list:
            gas = self._pk['gp']**(alpha/self._mk['s'][attr])
            g2at = pair(self._pk['g'],self._pk['gp'])**(alpha*self._mk['t'][attr])
            sk['gas'][attr] = gas
            sk['g2at'][attr] = g2at   
            
        return sk 
                
    """
    def print_result(self):
        print self._enc_symbol_matix
    
    def out_to_file(self, filename):
        pass
    
    def read_from_file(self, filename):
        
        pass
    """
  
if __name__ == '__main__':
    pass
    '''Owner side'''
    
    nodes = []
    for i in xrange(0,4):
        nodes.append('v%d'%(i+1))
        
    sg = SymbolDiGraphLst(nodes,rand_E=10)
    print sg
    
    #encrypt graph
    list_graph = PairEncSymbolDiGraph(sg)
    t0 = time.clock()
    list_graph.setup()
    t1 = time.clock()
    cipher_adjlist = list_graph.encrypt()
    t2 = time.clock()
    
    sk = list_graph.key_generation(['v1','v2'])
    t3 = time.clock()
    print sk
    
    res = PairEncSymbolDiGraph.decrypt(sk, cipher_adjlist, ['v1','v2'])
    t4 = time.clock()
    print res
    print '\nAdjlist Pairing Time Spent\n-----\nSetup:%fs\nEncryption:%fs\nKeyGen:%fs\nDecryption:%fs\n-----\nTotal:%fs'%(t1-t0, t2-t1, t3-t2, t4-t3, t4-t0)
    
    