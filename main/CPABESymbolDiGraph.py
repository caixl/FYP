'''
Created on 15 Oct, 2014

@author: Caixl
'''
from charm.schemes.abenc.abenc_bsw07 import CPabe_BSW07
from charm.toolbox.pairinggroup import PairingGroup,GT
from charm.adapters.abenc_adapt_hybrid import HybridABEnc


from SymbolDiGraph import SymbolDiGraph
from SymbolMatrix import SymbolMatrix

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
    # Random parameters
    _encRand = []
    
    def __init__(self):
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
        
    def setup(self, symbol_graph):
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
        (self._master_public_key, self._master_key) = self._hyb_abe.setup()
        
        
    def encrypt(self):
        '''
        Encrypt each cell in the matrix using corresponding symbols
        '''
        assert self._master_public_key, "Please do setup first."
            
        size = self._symbol_graph.get_V();
        
        self._enc_symbol_matix = SymbolMatrix(size, self._symbol_graph.get_st())
        for i in range(0, size):
            for j in range(0, size):
                msg = str(self._symbol_graph.get_edge_index(i,j))
                cell_access_policy = '(%s AND %s)'%(self._symbol_graph.name(i)+'r',
                                                    self._symbol_graph.name(j)+'c')
                cipher = self._hyb_abe.encrypt(self._master_public_key, 
                                               msg, 
                                               cell_access_policy)
                self._enc_symbol_matix.set_matrix(cipher, i, j)
                
        return True
    
    @classmethod
    def decrypt(self, master_public_key, sk, cipher_matrix, vertex):
        '''
        Decryption requires master_public_key, user secret key, and cipher
        '''
        group = PairingGroup('SS512')
        cpabe = CPabe_BSW07(group)
        hyb_abe = HybridABEnc(cpabe, group)
        
        #convert to lower case
        s1 = vertex[0].lower()
        s2 = vertex[1].lower()
        
        cipher = cipher_matrix.get_cell_by_symbol(s1, s2)
        msg =  hyb_abe.decrypt(master_public_key, sk, cipher)
        
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
    sg = SymbolDiGraph(['a','b','c','d'])
    print sg
    
    #encrypt graph
    abe_graph = CPABESymbolDiGraph()
    abe_graph.setup(sg)
    
    abe_graph.encrypt()
    #abe_graph.print_result()
    
    #bob needs to query graph
    #grant bob access to (a,a)
    sk_bob_aa = abe_graph.gen_secret_key(['AR','AC'])
    #grant bob access to (b,b)
    sk_bob_bb = abe_graph.gen_secret_key(['BR','BC'])
    
    
    '''User/Untrusted Server side'''
    query_aa = ['a','a']
    query_bb = ['b','b']
    
    result1 = CPABESymbolDiGraph.decrypt(abe_graph._master_public_key, 
                                        sk_bob_aa, 
                                        abe_graph._enc_symbol_matix, 
                                        query_aa)
    print '(%s,%s): %s'%(query_aa[0],query_aa[1],result1)
    
    result2 = CPABESymbolDiGraph.decrypt(abe_graph._master_public_key, 
                                        sk_bob_bb, 
                                        abe_graph._enc_symbol_matix, 
                                        query_bb)
    print '(%s,%s): %s'%(query_bb[0],query_bb[1],result2)
    
    
    
    