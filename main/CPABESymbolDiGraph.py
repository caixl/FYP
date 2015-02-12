'''
Created on 15 Oct, 2014
Modified on 2 Feb 2015

@author: Xinlei Cai
'''
from charm.schemes.abenc.abenc_bsw07 import CPabe_BSW07
from charm.toolbox.pairinggroup import PairingGroup
from charm.adapters.abenc_adapt_hybrid import HybridABEnc as HybridABEnc

import time

from SymbolDiGraph import SymbolDiGraphMat
from SymbolMatrix import SymbolMatrix
from TotalSize import total_size 

  
class CPABESymbolDiGraph:
    
    # the symbol graph
    _symbol_graph = None
    # operating group
    _group = None
    # Cipertext-Policy Attribute-Based Encryption object
    _cpabe = None
    # hybrid
    _hyb_abe = None
    
    _master_public_key = 0
    _master_key = 0
    _attributes = []
    _secret_key = 0
    
    # Encrypted matrix
    _enc_symbol_matix = {}
    
    def __init__(self, symbol_graph):
        '''
        Constructor
        '''
        # initialize CPABE object
        self._group = PairingGroup('SS512')
        self._cpabe = CPabe_BSW07(self._group)
        self._hyb_abe = HybridABEnc(self._cpabe, self._group)
        #access_policy = '(ar and bc)'
        #message = "hello world this is an important message."
        #(pk, mk) = self._hyb_abe.setup()
        #sk = self._hyb_abe.keygen(pk, mk, ['AR', 'BC'])
        #ct = self._hyb_abe.encrypt(pk, message, access_policy)
        #try:
        #    result = self._hyb_abe.decrypt(pk, sk, ct)
        #    print result
        #except Exception:
        #    pass
        
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
        
        
    def encrypt(self):
        '''
        Encrypt whole graph with each cell in the matrix using corresponding symbols
        '''
        assert self._master_public_key, "Please do setup first."
            
        size = self._symbol_graph.get_V();
        
        self._enc_symbol_matix = SymbolMatrix(size, self._symbol_graph.get_st())
        for i in range(0, size):
            for j in range(0, size):
                msg = str(self._symbol_graph.get_edge_by_index(i,j))
                cell_access_policy = '(%s AND %s)'%((self._symbol_graph.name(i)+'r'),
                                                    (self._symbol_graph.name(j)+'c'))
                cipher = self._hyb_abe.encrypt(self._master_public_key, 
                                               msg, 
                                               cell_access_policy)
                self._enc_symbol_matix.set_matrix(cipher, i, j)

        return True
    
    @classmethod
    def decrypt(self, master_public_key, sk, cipher_matrix, queries):
        '''
        Decryption requires master_public_key, user secret key, and cipher
        '''
        group = PairingGroup('SS512')
        cpabe = CPabe_BSW07(group)
        hyb_abe = HybridABEnc(cpabe, group)
        
        msg = ''
        for query in queries:
            #convert to lower case
            s1 = query[0].lower()
            s2 = query[1].lower()
            
            cipher = cipher_matrix.get_cell_by_symbol(s1, s2)
            msg += hyb_abe.decrypt(master_public_key, sk, cipher) + " "
        
        return msg
    
    def gen_secret_key(self, attributes):
        '''
        Generate individual's secret key using the given attributes
        '''
        assert (self._master_public_key and self._master_key), "Please do setup first."
        
        # convert strings in attributes to uppercase
        for elem in attributes:
            elem = elem.upper()
        
        return self._hyb_abe.keygen(self._master_public_key, 
                                  self._master_key,
                                  attributes)
        
    def print_result(self):
        print self._enc_symbol_matix
    
    def out_to_file(self, filename):
        pass
    
    def read_from_file(self, filename):
        
        pass
      
  
if __name__ == '__main__':
    '''Owner side'''
    sg = SymbolDiGraphMat(['a','b','c','d'])
    print sg
    
    #encrypt graph
    abe_graph = CPABESymbolDiGraph(sg)
    
    t0 = time.clock()
    abe_graph.setup()
    
    t1 = time.clock()
    
    abe_graph.encrypt()
    t2 = time.clock()
    #abe_graph.print_result()
    
    #bob needs to query graph
    #grant bob access to (a,a)
    sk_bob_aa = abe_graph.gen_secret_key(['AR','BR','AC','BC'])
    
    t3 = time.clock()
    #grant bob access to (b,b)
    #sk_bob_bb = abe_graph.gen_secret_key(['BR','BC'])
    
    #sk_bob_cc = abe_graph.gen_secret_key(['CR'])
    
    
    #print total_size(abe_graph.gen_secret_key(abe_graph._attributes))
    #print total_size(sk_bob_aa)
    #print total_size(sk_bob_bb)
    #print total_size(sk_bob_cc)
    
    '''User/Untrusted Server side'''
    
    query = [['a','b'], ['b','a']]
    
    result1 = CPABESymbolDiGraph.decrypt(abe_graph._master_public_key, 
                                        sk_bob_aa, 
                                        abe_graph._enc_symbol_matix, 
                                        query)
    
    t4 = time.clock()
    print '%s : %s'%(query,result1)
    print '\nCP-ABE Time Spent\n-----\nSetup:%fs\nEncryption:%fs\nKeyGen:%fs\nDecryption:%fs\n-----\nTotal:%fs'%(t1-t0, t2-t1, t3-t2, t4-t3, t4-t0)
    
    
    'Decryption using wrong key crashes Python'
    
    '''
    query = [['a','a'], ['a','b']]
    
    result2 = CPABESymbolDiGraph.decrypt(abe_graph._master_public_key, 
                                        sk_bob_aa, 
                                        abe_graph._enc_symbol_matix, 
                                        query)
    print '%s : %s'%(query,result2)
    '''
    
    
    #sk_bob_aa.extend(query_bb)
    '''
    print sk_bob_aa
    print sk_bob_bb
    sk_bob_ab = sk_bob_aa
    sk_bob_ab['Djp']['BR'] = sk_bob_bb['Djp']['BR']
    sk_bob_ab['Djp']['BC'] = sk_bob_bb['Djp']['BC']
    sk_bob_ab['S'].extend(sk_bob_bb['S'])
    sk_bob_ab['Dj']['BR'] = sk_bob_bb['Dj']['BR']
    sk_bob_ab['Dj']['BC'] = sk_bob_bb['Dj']['BC']
    '''
    #print sk_bob_ab
    
    #result3 = CPABESymbolDiGraph.decrypt(abe_graph._master_public_key, 
    #                                    sk_bob_aa, 
    #                                    abe_graph._enc_symbol_matix, 
    #                                    query_ab)
    #print '(%s,%s): %s'%(query_ab[0],query_ab[1],result3)
    
    
    