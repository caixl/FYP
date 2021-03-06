'''
Modified on 15 Apr 2015

@author: Xinlei Cai
'''
from charm.schemes.abenc.abenc_lsw08 import KPabe
from charm.toolbox.pairinggroup import PairingGroup
from charm.adapters.kpabenc_adapt_hybrid import HybridABEnc as HybridKPABEnc
import time

from SymbolDiGraph import SymbolDiGraphMat
from AdjMatrixDiGraph import AdjMatrixDiGraph
from SymbolMatrix import SymbolMatrix

class KPABESymbolDiGraph:
    
    # the symbol graph
    _symbol_graph = None
    # operating group
    _group = None
    # Key-Policy Attribute-Based Encryption object
    _kpabe = None
    # hybrid
    _hyb_abe = None
    
    _master_public_key = 0
    _master_key = 0
    _attributes = []
    _secret_key = 0
    
    # Encrypted matrix
    #_enc_symbol_matix = {}
    
    def __init__(self, symbol_graph):
        '''
        Constructor
        '''
        # initialize CPABEnc object
        self._group = PairingGroup('SS512')
        self._kpabe = KPabe(self._group)
        self._hyb_abe = HybridKPABEnc(self._kpabe, self._group)
        
        
        # attributes should be vertices
        # since its diDraph, the query of two vertices sequence matters
        # row and col symbol is interpreted differently
        self._symbol_graph = symbol_graph
        symbols = self._symbol_graph.get_keys()
        for i in symbols:
            # r means row attributes
            self._attributes.append(symbols[i]+'r')
            # c means column attributes
            self._attributes.append(symbols[i]+'c')
        
        
    def setup(self):
        # ABE setup phase
        (self._master_public_key, self._master_key) = self._hyb_abe.setup()
        return self._master_public_key, self._master_key
        
        
    def encrypt(self):
        '''
        Encrypt whole graph with each cell in the matrix using corresponding symbols
        '''
        assert self._master_public_key, "Please do setup first."
            
        size = self._symbol_graph.get_V();
        
        enc_symbol_matix = SymbolMatrix(size, self._symbol_graph.get_st())
        for i in range(0, size):
            for j in range(0, size):
                msg = str(self._symbol_graph.get_edge_by_index(i,j))
                #cell_access_policy = '(%s AND %s)'%(self._symbol_graph.name(i)+'r',
                #                                    self._symbol_graph.name(j)+'c')
                cipher = self._hyb_abe.encrypt(self._master_public_key, 
                                               msg, 
                                               [(self._symbol_graph.name(i)+'r').upper(), 
                                                (self._symbol_graph.name(j)+'c').upper()])
                enc_symbol_matix.set_matrix(cipher, i, j)

        return enc_symbol_matix
    
    @classmethod
    def decrypt_query(self, sk, cipher_matrix, queries):
        '''
        Decryption requires master_public_key, user secret key, and cipher
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
        
        return msg
    
    @classmethod
    def decrypt(self, sk, cipher_matrix, vertices):
        '''
        Decryption requires master_public_key, user secret key, and cipher
        '''
        group = PairingGroup('SS512')
        kpabe = KPabe(group)
        hyb_abe = HybridKPABEnc(kpabe, group)
        
        N = len(vertices)
        
        resMat = [None]*N;
        for i in range(0,N):
            resMat[i] = [None]*N
            for j in range(0,N):
                #convert to lower case
                s = vertices[i].lower()
                s2 = vertices[j].lower()
            
                cipher = cipher_matrix.get_cell_by_symbol(s, s2)
                resMat[i][j] = hyb_abe.decrypt(cipher, sk)
                if resMat[i][j]==False:
                    return False
        
        result = AdjMatrixDiGraph(mat=resMat)
        return SymbolDiGraphMat(vertices, G=result)
    
    
    
    
    def key_generation(self, policy):
        '''
        Generate individual's secret key using the given policy
        '''
        assert (self._master_public_key and self._master_key), "Please do setup first."
        
        # convert strings in attributes to uppercase
     
        return self._hyb_abe.keygen(self._master_public_key, 
                                  self._master_key,
                                  policy)
        
    @classmethod
    def subgraph(self, cipher_matrix,vertices):
        size = len(vertices)
        enc_symbol_matix = SymbolMatrix(size, vertices=vertices)
        for i in range(0, size):
            for j in range(0, size):
                cipher = cipher_matrix.get_cell_by_symbol(vertices[i],vertices[j])
                enc_symbol_matix.set_matrix(cipher, i, j)
        
        return enc_symbol_matix
        
        
    #def print_result(self):
    #    print self._enc_symbol_matix
    
    def out_to_file(self, filename):
        pass
    
    def read_from_file(self, filename):
        
        pass
      
  
if __name__ == '__main__':
    '''Owner side'''
    nodes = []
    for i in xrange(0,4):
        nodes.append('v%d'%(i+1))
    sg = SymbolDiGraphMat(nodes,rand_E=10)
    print sg
    
    #encrypt graph
    abe_graph = KPABESymbolDiGraph(sg)
    
    t0 = time.clock()
    abe_graph.setup()
    t1 = time.clock()
    
    encMat = abe_graph.encrypt()
    t2 = time.clock()
    print encMat
    
    sk_bob_aa = abe_graph.key_generation('(v2R OR v3R) AND (v2C OR v3C)')
    print "key:"
    print sk_bob_aa
    t3 = time.clock()
    
    '''User/Untrusted Server side'''
    
    subgraphVertices = ['v2','v3']

    subencMat = KPABESymbolDiGraph.subgraph(encMat,subgraphVertices)
    
    
    result1 = KPABESymbolDiGraph.decrypt(sk_bob_aa, 
                                        subencMat, 
                                        subgraphVertices)
    t4 = time.clock()


    print result1
    print '\nKP-ABE Time Spent\n-----\nSetup:%fs\nEncryption:%fs\nKeyGen:%fs\nDecryption:%fs\n-----\nTotal:%fs'%(t1-t0, t2-t1, t3-t2, t4-t3, t4-t0)
    
    ''' decryption with wrong key still crashes python'''
    '''
    query = [['a','b'], ['b','a']]
    result2 = KPABESymbolDiGraph.decrypt(sk_bob_aa, 
                                        abe_graph._enc_symbol_matix, 
                                        query)
    
    print '%s: %s'%(query , result2)
    '''
    