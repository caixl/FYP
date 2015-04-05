'''
Created on 16 Jan, 2015

@author: Xinlei Cai
'''

class Node:
    item = None
    next = None
    value = None
        
        
class Bag:
    '''
    classdocs
    '''
    #number of elements in bag 
    _N = 0
    #beginning of bag
    _first = None

    def __init__(self):
        '''
        Constructor
        '''
        return
    
    def isEmpty(self):
        '''
        Is this bag empty?
        @return true if this bag is empty;
        '''
        return self._first == None
    
    def size(self):
        return self._N
    
    def add(self, item):
        oldfirst = self._first
        self._first = Node()
        self._first.item = item
        #self._first.value = True
        self._first.next = oldfirst
        self._N += 1
        
    
    def __str__(self):
        iterBag = self.ListIterator(self)
        strList = ""
        for itr in iterBag:
            strList += "%s -> "%itr
        strList+="NULL"
        return strList
        
        
    class ListIterator:
        _current = Node()
        
        def __init__(self, bag):
            self._current = bag._first
            
        def has_next(self):
            return self._current!=None
            
        def next(self):
            if not self.has_next():
                raise StopIteration()
            item = self._current.item
            self._current = self._current.next
            return item
            
        def __iter__(self):
            '''
            return the iterator
            '''
            return self
        
        


if __name__=="__main__":
    bag = Bag()
    bag.add('#')
    bag.add(2)
    bag.add('M')
    print bag