"""
This class is a heap implementation that has been
modified to optimize Djikstra's Algorithm. It is
taken in its entirety from the code cited below.

CSCI-603: Heaps
Authors:  (11/16/2016) Adam Purtee @ RIT CS
                       -- added separation of keys and items
                          keys can now be decreased
          (Original Version) Sean Strout @ RIT CS
"""
__author__ = 'Amit Maller', 'Kyle McGlynn'

class Heap(object):
    '''
    Heap that orders by a given comparison function, default to less-than.
    '''
    __slots__ = ('data','size','lessfn','keys', 'itemIndex')

    def __init__(self,lessfn=lambda x,y:x<y):
        '''
        Constructor takes a comparison function.
        :param lessfn: Function that takes in two keys and returns a boolean
        if the first arg goes higher in the heap than the second
        '''
        self.data = []        # the array
        self.size = 0         # the number of things in the heap
        self.lessfn = lessfn  # the comparison function
        self.itemIndex = {}   # hashmap from items to slots
        self.keys = []        # parallel array for keys in data

    def __parent(self,loc):
        '''
        Helper function to compute the parent location of an index
        :param loc: Index in the heap
        :return: Index of parent
        '''
        return (loc-1)//2

    def __bubbleUp(self,loc):
        '''
        Starts from the given location and moves the item at that spot
        as far up the heap as necessary
        :param loc: Place to start bubbling from
        '''
        while loc > 0 and \
                self.lessfn(self.keys[loc],self.keys[self.__parent(loc)]):
            self.__swap(loc, self.__parent(loc))
            loc = self.__parent(loc)

    def __swap(self, i, j):
        """
        Swap the items at position i and j, and their keys, and update itemIndex
        """
        self.data[i], self.data[j] = self.data[j], self.data[i]
        self.keys[i], self.keys[j] = self.keys[j], self.keys[i]
        self.itemIndex[self.data[i]] = i
        self.itemIndex[self.data[j]] = j


    def __bubbleDown(self,loc):
        '''
        Starts from the given location and moves the item at that spot
        as far down the heap as necessary
        :param loc: Place to start bubbling from
        '''
        swapLoc = self.__smallest(loc)
        while swapLoc != loc:
            self.__swap(loc, swapLoc)
            loc = swapLoc
            swapLoc = self.__smallest(loc)

    def __smallest(self,loc):
        '''
        Finds the "smallest" value of loc and loc's two children.
        Correctly handles end-of-heap issues.
        :param loc: Index
        :return: index of smallest value
        '''
        ch1 = loc*2 + 1
        ch2 = loc*2 + 2
        if ch1 >= self.size:
            return loc
        if ch2 >= self.size:
            if self.lessfn(self.keys[loc],self.keys[ch1]):
                return loc
            else:
                return ch1
        # now consider all 3
        if self.lessfn(self.keys[ch1],self.keys[ch2]):
            if self.lessfn(self.keys[loc],self.keys[ch1]):
                return loc
            else:
                return ch1
        else:
            if self.lessfn(self.keys[loc],self.keys[ch2]):
                return loc
            else:
                return ch2

    def decreaseKey(self, item, newkey):
        """
        Assumes item in heap!  Will break if not!
        Note that this assumes that the newKey will cause the
        item to bubble UP not down.
        :param item:  item in heap to have it's key decreased
        :param newKey:  the new value of the key.
        """
        idx = self.itemIndex[item]
        self.keys[idx] = newkey
        self.__bubbleUp(idx)

    def insert(self,item, key=None):
        '''
        Inserts an item into the heap.
        :param item: Item to be inserted
        :param key:  The key for the item.  Defaults to the item if not given.
        '''
        if key is None:
            key = item

        if self.size < len(self.data):
            self.data[self.size] = item
            self.keys[self.size] = key
        else:
            self.data.append(item)
            self.keys.append(key)
        self.size += 1
        self.itemIndex[item] = self.size-1
        self.__bubbleUp(self.size-1)

    def pop(self):
        '''
        Removes and returns top of the heap
        :return: Item on top of the heap
        '''
        retjob = self.data[0]
        self.size -= 1
        # if we are popping the only element, assignment will fail,
        # but bubbling is unnecessary, so:
        if self.size > 0:
            self.data[0] = self.data.pop(self.size)   # PYTHON LIST POP NOT HEAP POP
            self.keys[0] = self.keys.pop(self.size)
            self.__bubbleDown(0)
        return retjob

    def __len__(self):
        '''
        Defining the "length" of a data structure also allows it to be
        used as a boolean value!
        :return: size of heap
        '''
        return self.size

    def __str__(self):
        ret = ""
        for item in range(self.size):
            ret += str(self.data[item]) + " "
        return ret

def namecmp(n1, n2):
    '''
    Simple comparison function as an example.
    Assumes each name is (first, last) tuple
    :param n1: Name
    :param n2: Other name
    :return: True if n1 comes before n2
    '''
    return n1[1] < n2[1]

def main():
    # here's a min heap (comparison is less than)
    print("Numerical min heap");
    minh = Heap(lambda x,y: x<y)
    print("Array contents:",minh.data)
    print("Insert 5, 3, 7, 2.")
    for num in (5,3,7,2):
        minh.insert(num)
    print("Heap is now: " + str(minh))
    print("Array contents:",minh.data)
    print("Pop.")
    print(minh.pop())
    print("Array contents:",minh.data)
    print("Insert 1, 8.")
    minh.insert(1)
    minh.insert(8)
    print("Heap is now: " + str(minh))
    print("Array contents:",minh.data)
    print("Emptying heap.")
    while minh:
        print(minh.pop())
    print("Array contents:",minh.data)

    # here's a max heap
    print("\nNumerical max heap");
    maxh = Heap(lambda x,y: x > y)
    print("Insert 4, 6, 10, 2, -1, 3.")
    for num in (4,6,10,2,-1,3):
        maxh.insert(num)
    print("Emptying max heap.")
    while maxh:
        print(maxh.pop())
    print("Insert 5, 7, 11, 3, -2, 4.")
    for num in 5,7,11,3,-2,4:
        maxh.insert(num)
    print("Emptying max heap.")
    while maxh:
        print(maxh.pop())

    print("\nString min heap");
    nameheap = Heap(namecmp)
    for name in ('Sean','Strout'), ('Zack','Butler'), \
                ('James','Heliotis'), ('Alan','Turing'):
        print("Insert",name)
        nameheap.insert(name)
    print("Pop.")
    print(nameheap.pop())
    print("Pop.")
    print(nameheap.pop())
    print("Pop.")
    print(nameheap.pop())
    for name in ('Ada','Lovelace'), ('Grace','Hopper'):
        print("Insert",name)
        nameheap.insert(name)
    print("Emptying string heap.")
    while nameheap:
        print(nameheap.pop())

    print("New heap to test decreaseKey")
    h = Heap()
    for item, key in [("a", 10), ("b", 5), ("c", 200)]:
        print("insert " +str((item, key)))
        h.insert(item, key)
    print("decrease key for c to 2")
    h.decreaseKey("c", 2)
    while h:
        print("popped " + str(h.pop()))

if __name__ == '__main__':
    main()
