'''
Modified on 6 Apr 2015

@author: Xinlei Cai
'''

from SymbolDiGraph import SymbolDiGraphLst
from SymbolDiGraph import SymbolDiGraphMat
from CPABEnc import CPABESymbolDiGraph
from KPABEnc import KPABESymbolDiGraph
from PairEnc import PairEncSymbolDiGraph
import time
  

def testCPABE_ct(nodes, E):
    sg = SymbolDiGraphMat(nodes, rand_E=E)
    abe_graph = CPABESymbolDiGraph(sg)
    abe_graph.setup()
    encMat = abe_graph.encrypt()
    return len(str(encMat))
    
    
def testKPABE_ct(nodes, E):
    sg = SymbolDiGraphMat(nodes, rand_E=E)
    abe_graph = KPABESymbolDiGraph(sg)
    abe_graph.setup()
    encMat = abe_graph.encrypt()
    return len(str(encMat))
    
 
def testPairEnc_ct(nodes,E):
    sg = SymbolDiGraphLst(nodes,rand_E=E)
    list_graph = PairEncSymbolDiGraph(sg)
    list_graph.setup()
    encLists = list_graph.encrypt()
    #print sg
    return len(str(encLists))


def testCPABE_mk(nodes, E):
    sg = SymbolDiGraphMat(nodes, rand_E=E)
    abe_graph = CPABESymbolDiGraph(sg)
    pk_t, mk_t = abe_graph.setup()
    return len(str(mk_t))
    
    
def testKPABE_mk(nodes, E):
    sg = SymbolDiGraphMat(nodes, rand_E=E)
    print len(nodes)
    abe_graph = KPABESymbolDiGraph(sg)
    pk_t, mk_t = abe_graph.setup()
    return len(str(mk_t))
    
 
def testPairEnc_mk(nodes,E):
    sg = SymbolDiGraphLst(nodes,rand_E=E)
    list_graph = PairEncSymbolDiGraph(sg)
    list_graph.setup()
    return len(str(list_graph._mk))


def testCPABE_pp(nodes, E):
    sg = SymbolDiGraphMat(nodes, rand_E=E)
    abe_graph = CPABESymbolDiGraph(sg)
    pk_t, mk_t = abe_graph.setup()
    return len(str(pk_t))
    
    
def testKPABE_pp(nodes, E):
    sg = SymbolDiGraphMat(nodes, rand_E=E)
    print len(nodes)
    abe_graph = KPABESymbolDiGraph(sg)
    pk_t, mk_t = abe_graph.setup()
    return len(str(pk_t))
    
 
def testPairEnc_pp(nodes,E):
    sg = SymbolDiGraphLst(nodes,rand_E=E)
    list_graph = PairEncSymbolDiGraph(sg)
    list_graph.setup()
    return len(str(list_graph._pk))


def testCPABE_dk(nodes, E, A):
    sg = SymbolDiGraphMat(nodes, rand_E=E)
    abe_graph = CPABESymbolDiGraph(sg)
    abe_graph.setup()
    dk = abe_graph.key_generation(A)
    return len(str(dk))
    
    
def testKPABE_dk(nodes, E, P):
    sg = SymbolDiGraphMat(nodes, rand_E=E)
    #print nodes
    abe_graph = KPABESymbolDiGraph(sg)
    abe_graph.setup()
    dk = abe_graph.key_generation(P)
    return len(str(dk))
    
 
def testPairEnc_dk(nodes,E, A):
    sg = SymbolDiGraphLst(nodes,rand_E=E)
    list_graph = PairEncSymbolDiGraph(sg)
    list_graph.setup()
    dk = list_graph.key_generation(A)
    return len(str(dk))


def compare_pp(N, E): 
    nodes = []
    for i in xrange(0,N):
        nodes.append('v%d'%(i+1))    
        
    
    print "KPABE with %d vertices and %d edges: %s"%(N, E, testKPABE_pp(nodes,E))
    print "CPABE with %d vertices and %d edges: %s"%(N, E, testCPABE_pp(nodes,E))
    print "PAIRE with %d vertices and %d edges: %s"%(N, E, testPairEnc_pp(nodes,E))
    print ""

def compare_mk(N, E): 
    nodes = []
    for i in xrange(0,N):
        nodes.append('v%d'%(i+1))
    
    print "KPABE with %d vertices and %d edges: %s"%(N, E, testKPABE_mk(nodes,E))
    print "CPABE with %d vertices and %d edges: %s"%(N, E, testCPABE_mk(nodes,E))
    print "PAIRE with %d vertices and %d edges: %s"%(N, E, testPairEnc_mk(nodes,E))
    print ""
    
    
def compare_ct(N, E): 
    nodes = []
    for i in xrange(0,N):
        nodes.append('v%d'%(i+1))
        
    #print "KPABE with %d vertices and %d edges: %s"%(N, E, testKPABE_ct(nodes,E))
    print "CPABE with %d vertices and %d edges: %s"%(N, E, testCPABE_ct(nodes,E))
    #print "PAIRE with %d vertices and %d edges: %s"%(N, E, testPairEnc_ct(nodes,E))
    #print ""
    
def compare_dk(N, E, Q): 
    nodes = []
    for i in xrange(0,N):
        nodes.append('v%d'%(i+1))
        
    subnodes = []
    attributes = []
    policy = "("
    for i in xrange(0, Q):
        if i!=0:
            policy+=" OR "
        policy+="v%dr"%(i+1)
        
        subnodes.append('v%d'%(i+1)) 
        
        attributes.append('v%dr'%(i+1))  
        attributes.append('v%dc'%(i+1))  
    
    policy+=") AND ("
    
    for i in xrange(0, Q):
        if i!=0:
            policy+=" OR "
        policy+="v%dc"%(i+1)
    
    policy+=")"
    #print policy
    
    print "KPABE with %d vertices and %d edges: %s with policy"%(N, E, testKPABE_dk(nodes,E, policy))
    print "CPABE with %d vertices and %d edges: %s with attributes len: %s"%(N, E, testCPABE_dk(nodes,E, attributes), len(attributes))
    print "PAIRE with %d vertices and %d edges: %s with subnodes len: %s"%(N, E, testPairEnc_dk(nodes,E, subnodes), len(subnodes))
    #print ""
    
    
        
def run_test_ct():
    
        compare_ct(10,10)
        compare_ct(20,20)
        compare_ct(30,30)
        compare_ct(40,40)
        compare_ct(50,50)
        
        compare_ct(10,10**2)
        compare_ct(20,20**2)
        compare_ct(30,30**2)
        compare_ct(40,40**2)
        compare_ct(50,50**2)
    
    

def run_test_dk():
    
    compare_dk(100,100*100,20)
    compare_dk(100,100*100,40)
    compare_dk(100,100*100,60)
    compare_dk(100,100*100,80)
    compare_dk(100,100*100,100)
    
    
    
def testCPABE_dec(pk, dk, encMat, subnodes):
    t0 = time.clock()
    CPABESymbolDiGraph.decrypt(pk,dk,encMat,subnodes)
    t1 = time.clock()
    return t1-t0
    
    
def testKPABE_dec(dk, encMat, subnodes):
    t0 = time.clock()
    KPABESymbolDiGraph.decrypt(dk,  encMat, subnodes)
    t1 = time.clock()
    return t1-t0
    
 
def testPairEnc_dec(dk, cipher_adjlist, subnodes):
    t0 = time.clock()
    PairEncSymbolDiGraph.decrypt(dk, cipher_adjlist, subnodes)
    t1 = time.clock()
    return t1-t0    
    
    
def compare_dec_rt(N, E, K):
    nodes = []
    for i in xrange(0,N):
        nodes.append('v%d'%(i+1))
        
    attributes = []
    vertices = []
    policy = "("
    for i in xrange(0, K):
        if i!=0:
            policy+=" OR "
        policy+="v%dr"%(i+1)
        attributes.append('V%dR'%(i+1))  
        attributes.append('V%dC'%(i+1))  
        vertices.append('v%d'%(i+1))
    
    policy+=") AND ("
    
    for i in xrange(0, K):
        if i!=0:
            policy+=" OR "
        policy+="v%dc"%(i+1)
    
    policy+=")"
    
    sg = SymbolDiGraphMat(nodes, rand_E=E)
    
    cpabe_graph = CPABESymbolDiGraph(sg)
    cpabe_graph.setup()
    cpabeEncMat = cpabe_graph.encrypt()
    
    kpabe_graph = KPABESymbolDiGraph(sg)
    kpabe_graph.setup()
    kpabeEncMat = kpabe_graph.encrypt()
    
    sg = SymbolDiGraphLst(nodes,rand_E=E)
    list_graph = PairEncSymbolDiGraph(sg)
    list_graph.setup()
    pairEncList = list_graph.encrypt()
    
    
    cpabe_dk = cpabe_graph.key_generation(attributes)
    kpabe_dk = kpabe_graph.key_generation(policy)
    plist_dk = list_graph.key_generation(vertices)
    
    Q = 2
    subnodes = []
    for i in xrange(0, Q):
        subnodes.append('v%d'%(i+1)) 
    
    print "CPABE with %d vertices and %d edges and %d queried subnodes %s s"%(N, E, Q, testCPABE_dec(cpabe_graph._master_public_key, cpabe_dk, cpabeEncMat, subnodes))
    print "KPABE with %d vertices and %d edges and %d queried subnodes %s s"%(N, E, Q, testKPABE_dec(kpabe_dk, kpabeEncMat, subnodes))
    print "PAIRE with %d vertices and %d edges and %d queried subnodes %s s"%(N, E, Q, testPairEnc_dec( plist_dk, pairEncList, subnodes ))
    print ""
    
    Q = 4
    subnodes = []
    for i in xrange(0, Q):
        subnodes.append('v%d'%(i+1)) 
    
    print "CPABE with %d vertices and %d edges and %d queried subnodes %s s"%(N, E, Q, testCPABE_dec(cpabe_graph._master_public_key, cpabe_dk, cpabeEncMat, subnodes))
    print "KPABE with %d vertices and %d edges and %d queried subnodes %s s"%(N, E, Q, testKPABE_dec(kpabe_dk, kpabeEncMat, subnodes))
    print "PAIRE with %d vertices and %d edges and %d queried subnodes %s s"%(N, E, Q, testPairEnc_dec( plist_dk, pairEncList, subnodes ))
    print ""
    
    
    Q = 6
    subnodes = []
    for i in xrange(0, Q):
        subnodes.append('v%d'%(i+1)) 
    
    print "CPABE with %d vertices and %d edges and %d queried subnodes %s s"%(N, E, Q, testCPABE_dec(cpabe_graph._master_public_key,cpabe_dk, cpabeEncMat, subnodes))
    print "KPABE with %d vertices and %d edges and %d queried subnodes %s s"%(N, E, Q, testKPABE_dec(kpabe_dk, kpabeEncMat, subnodes))
    print "PAIRE with %d vertices and %d edges and %d queried subnodes %s s"%(N, E, Q, testPairEnc_dec( plist_dk, pairEncList, subnodes ))
    print ""
    
    
    Q = 8
    subnodes = []
    for i in xrange(0, Q):
        subnodes.append('v%d'%(i+1)) 
    
    print "CPABE with %d vertices and %d edges and %d queried subnodes %s s"%(N, E, Q, testCPABE_dec(cpabe_graph._master_public_key,cpabe_dk, cpabeEncMat, subnodes))
    print "KPABE with %d vertices and %d edges and %d queried subnodes %s s"%(N, E, Q, testKPABE_dec(kpabe_dk, kpabeEncMat, subnodes))
    print "PAIRE with %d vertices and %d edges and %d queried subnodes %s s"%(N, E, Q, testPairEnc_dec( plist_dk, pairEncList, subnodes ))
    print ""
    
    
    Q = 10
    subnodes = []
    for i in xrange(0, Q):
        subnodes.append('v%d'%(i+1)) 
    
    print "CPABE with %d vertices and %d edges and %d queried subnodes %s s"%(N, E, Q, testCPABE_dec(cpabe_graph._master_public_key,cpabe_dk, cpabeEncMat, subnodes))
    print "KPABE with %d vertices and %d edges and %d queried subnodes %s s"%(N, E, Q, testKPABE_dec(kpabe_dk, kpabeEncMat, subnodes))
    print "PAIRE with %d vertices and %d edges and %d queried subnodes %s s"%(N, E, Q, testPairEnc_dec( plist_dk, pairEncList, subnodes ))
    print ""
    
    

def testCPABE_enc(nodes, E):
    sg = SymbolDiGraphMat(nodes, rand_E=E)
    abe_graph = CPABESymbolDiGraph(sg)
    abe_graph.setup()
    t0 = time.clock()
    abe_graph.encrypt()
    t1 = time.clock()
    return t1-t0
    
    
def testKPABE_enc(nodes, E):
    sg = SymbolDiGraphMat(nodes, rand_E=E)
    abe_graph = KPABESymbolDiGraph(sg)
    abe_graph.setup()
    t0 = time.clock()
    abe_graph.encrypt()
    t1 = time.clock()
    return t1-t0
    
 
def testPairEnc_enc(nodes,E):
    sg = SymbolDiGraphLst(nodes,rand_E=E)
    list_graph = PairEncSymbolDiGraph(sg)
    list_graph.setup()
    t0 = time.clock()
    list_graph.encrypt()
    #print list_graph._enc_adjlist
    t1 = time.clock()
    return t1-t0

def testCPABE_keygen(nodes, E, attributes):
    sg = SymbolDiGraphMat(nodes, rand_E=E)
    abe_graph = CPABESymbolDiGraph(sg)
    abe_graph.setup()
    t0 = time.clock()
    abe_graph.key_generation(attributes)
    t1 = time.clock()
    return t1-t0
    
    
def testKPABE_keygen(nodes, E, policy):
    sg = SymbolDiGraphMat(nodes, rand_E=E)
    abe_graph = KPABESymbolDiGraph(sg)
    abe_graph.setup()
    t0 = time.clock()
    abe_graph.key_generation(policy)
    t1 = time.clock()
    return t1-t0
    
 
def testPairEnc_keygen(nodes,E,attr_list):
    sg = SymbolDiGraphLst(nodes,rand_E=E)
    list_graph = PairEncSymbolDiGraph(sg)
    list_graph.setup()
    t0 = time.clock()
    list_graph.key_generation(attr_list)
    t1 = time.clock()
    return t1-t0

def compare_keygen(N, E, K): 
    nodes = []
    for i in xrange(0,N):
        nodes.append('v%d'%(i+1))
        
    vertices = []
    attributes = []
    policy = "("
    for i in xrange(0, K):
        if i!=0:
            policy+=" OR "
        policy+="v%dr"%(i+1)
        
        vertices.append('v%d'%(i+1)) 
        
        attributes.append('v%dr'%(i+1))  
        attributes.append('v%dc'%(i+1))  
    
    policy+=") AND ("
    
    for i in xrange(0, K):
        if i!=0:
            policy+=" OR "
        policy+="v%dc"%(i+1)
    
    policy+=")"
    #print policy
    
    print "CPABE with %d vertices and %d edges: %s s with attributes len: %s"%(N, E, testCPABE_keygen(nodes,E, attributes), len(attributes))
    print "KPABE with %d vertices and %d edges: %s s with policy"%(N, E, testKPABE_keygen(nodes,E, policy))
    print "PAIRE with %d vertices and %d edges: %s s with subnodes len: %s"%(N, E, testPairEnc_keygen(nodes,E, vertices), len(vertices))
    print ""

def compare_enc_rt(N, E):
    nodes = []
    for i in xrange(0,N):
        nodes.append('v%d'%(i+1))    
    
    print "CPABE with %d vertices and %d edges: %s s"%(N, E, testCPABE_enc(nodes,E))
    print "KPABE with %d vertices and %d edges: %s s"%(N, E, testKPABE_enc(nodes,E))
    print "PAIRE with %d vertices and %d edges: %s s"%(N, E, testPairEnc_enc(nodes,E))
    print ""

def run_test_enc_rt():
    
    #for i in range(0, len(V10E)):
    '''
    compare_enc_rt(10,10)
    compare_enc_rt(20,20)
    compare_enc_rt(30,30)
    compare_enc_rt(40,40)
    compare_enc_rt(50,50)
    '''
    
    compare_enc_rt(10,10**2)
    compare_enc_rt(20,20**2)
    compare_enc_rt(30,30**2)
    compare_enc_rt(40,40**2)
    compare_enc_rt(50,50**2)
    
def run_test_keygen():
    
    #for i in range(0, len(V10E)):
    compare_keygen(100,100*100,20)
    compare_keygen(100,100*100,40)
    compare_keygen(100,100*100,60)
    compare_keygen(100,100*100,80)
    compare_keygen(100,100*100,100)
    
if __name__ == '__main__':
    
    """Storage"""
    #public parameters
    #run_test_pp()
    
    #master key
    #run_test_mk()
    
    #ciphertext
    #run_test_ct()
    
    #decryption key  
    #run_test_dk()
    
    
    """Runningtime"""
    
    
    #encrypt
    #run_test_enc_rt()
    
    
    #key generation
    #run_test_keygen()
    
    
    #decrypt
    #compare_dec_rt(20,20,10)
    #compare_dec_rt(20,400,10)
    
    