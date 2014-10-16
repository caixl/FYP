'''
Created on 15 Oct, 2014

@author: Caixl
'''
import json
from charm.schemes.abenc.abenc_bsw07 import CPabe_BSW07
from charm.toolbox.pairinggroup import PairingGroup,ZR, GT
from charm.adapters.abenc_adapt_hybrid import HybridABEnc


from SymbolDiGraph import SymbolDiGraph
from SymbolMatrix import SymbolMatrix

class CPABESymbolDiGraph:
    
    # the symbol graph
    _symbol_graph = {}
    # operating group
    _group = {}
    # Cipertext-Policy Attribute-Based Encryption object
    _cpabe = {}
    # hybrid
    _hyb_abe = {}
    
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
                msg = self._symbol_graph.get_edge_index(i,j)
                cipher = self._hyb_abe.encrypt(self._master_public_key, 
                                             str(msg), 
                                             '(%s AND %s)'%(self._symbol_graph.name(i)+'r',
                                                            self._symbol_graph.name(j)+'c')
                                             )
                self._enc_symbol_matix.set_matrix(cipher, i, j)
                
        return True
    
    @classmethod
    def decrypt(self, master_public_key, sk, cipher_matrix):
        '''
        Decryption requires master_public_key, user secret key, and cipher
        '''
        group = PairingGroup('SS512')
        cpabe = CPabe_BSW07(group)
        hyb_abe = HybridABEnc(cpabe, group)
        
        row = None; col = None
        for label in sk['S']:
            if label[-1:] == 'r':
                row = label[:-1]
            elif label[-1:] == 'c':
                col = label[:-1]
        if not row or not col:
            return None
        
        cipher = cipher_matrix.get_cell_by_symbol(row, col)
        
        msg =  hyb_abe.decrypt(master_public_key, sk, cipher)
        
        return msg
    
    def gen_secret_key(self, attributes):
        '''
        Generate individual's secret key using the given attributes
        '''
        assert (self._master_public_key and self._master_key), "Please do setup first."
        
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
    sg = SymbolDiGraph(['a','b','c','d'])
    abe_graph = CPABESymbolDiGraph()
    abe_graph.setup(sg)
    sk_bob = abe_graph.gen_secret_key(['ar','bc'])
    abe_graph.encrypt()
    abe_graph.print_result()
    
    #''' Current decryption crashes
    result = CPABESymbolDiGraph.decrypt(abe_graph._master_public_key, 
                                        sk_bob, 
                                        abe_graph._enc_symbol_matix)
    print result
    #'''
    