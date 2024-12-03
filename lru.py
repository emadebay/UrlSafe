
class LRUNode:
    def __init__(self, key : int = 0, value :int = 0, prev = None, next = None):

        self.key = key
        self.value = value
        self.prev = prev
        self.next = next


class LRUCache:

    def __init__(self, capacity: int):
        #set left and right dummy nodes
        self.left = LRUNode()
        self.right = LRUNode()

        #set the pointers of let and right
        self.left.next = self.right
        self.right.prev = self.left
        #set capacity
        self.capacity = capacity
        #set cache map
        self.cache = {}

    def remove(self, node):
        #get the left and right pointers of the node
        left = node.prev
        right = node.next

        #break the link in between the nodes and update the pointer
        left.next = right
        right.prev = left

    def insert(self, node):

        #insertion can only happen from the right
        #get the rightmost node which is node before dummy right
        left = self.right.prev

        #update the pointers
        left.next = node
        node.prev = left
        #update the pointers
        node.next = self.right
        self.right.prev = node


    def get(self, key: int) -> int:

        #check if item is in list
        if key in self.cache:

            #if key is present, this is current the mostly recently used
            #remove it and insert it back at the right

            mru = self.cache[key]
            self.remove(mru)
            self.insert(mru)

            return mru.value
        return -1


    def put(self, key: int, value: int) -> None:

        if key in self.cache:
            mru = self.cache[key]
            self.remove(mru)
            new_node = LRUNode(key, value, None, None)
            self.cache[key] = new_node
            self.insert(new_node)
        else:
            #key does not exist
            new_node = LRUNode(key, value, None, None)
            self.cache[key] = new_node
            self.insert(new_node)



        #now make sure we haven't exceeded capacity
        if len(self.cache) > self.capacity:

            #remove the least recently used
            lru = self.left.next
            self.remove(lru)

            #delete it in the cache map as well
            del self.cache[lru.key]



