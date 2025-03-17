#username - talsofer1
#id1      - 323869842
#name1    - Tal Sofer
#id2      - 323916395
#name2    - Jonathan Klier

"""A class represnting a node in an AVL tree"""

class AVLNode(object):
    """Constructor, you are allowed to add more fields. 
    
    @type key: int or None
    @param key: key of your node
    @type value: string
    @param value: data of your node
    """
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.height = -1
        self.size = 1

    """returns whether self is not a virtual node 

    @rtype: bool
    @returns: False if self is a virtual node, True otherwise.
    """
    def is_real_node(self):
        return self.key != None

"""
A class implementing an AVL tree.
"""

class AVLTree(object):

    """
    Constructor, you are allowed to add more fields.  

    """
    def __init__(self):
        self.root = None

    """searches for a node in the dictionary corresponding to the key

    @type key: int
    @param key: a key to be searched
    @rtype: AVLNode
    @returns: node corresponding to key
    """
    def search(self, key):
        node = self.root
        while node != None:
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else: return node
        return None

    """inserts a new node into the dictionary with corresponding key and value

    @type key: int
    @pre: key currently does not appear in the dictionary
    @param key: key of item that is to be inserted to self
    @type val: string
    @param val: the value of the item
    @rtype: int
    @returns: the number of rebalancing operation due to AVL rebalancing
    """
    def insert(self,key,val):
        if self.root == None:
            self.root = AVLNode(key,val)
            return 0
        
        node = self.root
        while node != None:
            node_parent = node
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                node.value = val
                return 0
            
        new_node = AVLNode(key,val)
        new_node.parent = node_parent
        if key < node_parent.key:        
            node_parent.left = new_node
        if key > node_parent.key:
            node_parent.right = new_node
        new_node.height = 0

        
        return self.maintenance(node_parent,1)

    def maintenance(self,node_parent,ins_or_del):
        rotations = 0
        while node_parent != None:
            node_parent.size += ins_or_del
            prev_height = node_parent.height
            node_parent.height = self.get_height(node_parent)
            bf = self.get_bf(node_parent)
            if bf == 2:
                node_son = node_parent.left
                son_bf = self.get_bf(node_son)
                if son_bf != 1:
                    rotations += 1
                    self.rotate_left(node_son)
                rotations += 1
                self.rotate_right(node_parent)
                node_parent = node_parent.parent
            elif bf == -2:
                node_son = node_parent.right
                son_bf = self.get_bf(node_son)
                if son_bf != -1:
                    rotations += 1
                    self.rotate_right(node_son)
                rotations += 1
                self.rotate_left(node_parent)
                node_parent = node_parent.parent
            else:
                if prev_height == node_parent.height:
                    node_parent = node_parent.parent
                    while node_parent != None:
                        node_parent.size += ins_or_del
                        node_parent = node_parent.parent
                    return rotations
            node_parent = node_parent.parent

        return rotations


    def rotate_left(self,node):
        r_node = node.right
        node.right = None
        if r_node.left != None:
            node.right = r_node.left
            node.right.parent = node
        if node == self.root:
            r_node.parent = None
            self.root = r_node
        else:
            r_node.parent = node.parent
            if r_node.parent.key > r_node.key:
                r_node.parent.left = r_node
            else:
                r_node.parent.right = r_node
        r_node.left = node
        node.parent = r_node
        node.height = self.get_height(node)
        r_node.height = self.get_height(r_node)
        node.size = 1
        if node.left != None:
            node.size += node.left.size
        if node.right != None:
            node.size += node.right.size
        r_node.size  = node.size + 1
        if r_node.right !=None:
            r_node.size += r_node.right.size

        
    def rotate_right(self,node):
        l_node = node.left
        node.left = None
        if l_node.right != None:
            node.left = l_node.right
            node.left.parent = node
        if node == self.root:
            l_node.parent = None
            self.root = l_node
        else:
            l_node.parent = node.parent
            if l_node.parent.key > l_node.key:
                l_node.parent.left = l_node
            else:
                l_node.parent.right = l_node
        l_node.right = node
        node.parent = l_node
        node.height = self.get_height(node)
        l_node.height = self.get_height(l_node)
        node.size = 1
        if node.left != None:
            node.size += node.left.size
        if node.right != None:
            node.size += node.right.size
        l_node.size  = node.size + 1
        if l_node.left !=None:
            l_node.size += l_node.left.size
            

    def get_bf(self,node):
        if node.left == None:
            l_height = -1
        else:
            l_height = node.left.height
        if node.right == None:
            r_height = -1
        else:
            r_height = node.right.height
        return l_height - r_height

    def get_height(self,node):
        if node.left == None:
            l_height = -1
        else:
            l_height = node.left.height
        if node.right == None:
            r_height = -1
        else:
            r_height = node.right.height
        return 1 + max(l_height,r_height)
        
    """deletes node from the dictionary

    @type node: AVLNode
    @pre: node is a real pointer to a node in self
    @rtype: int
    @returns: the number of rebalancing operation due to AVL rebalancing
    """
    def delete(self, node):
        
        if self.size() == 1:
            self.root = None
            return 0
    
        if node.right == None:        
            if node == self.root:
                node.left.parent = None
                self.root = node.left
                return 0

            node_parent = node.parent
            
            if node_parent.left == node:
                node_parent.left = node.left
                if node.left != None:
                    node_parent.left.parent = node_parent
            else:
                node_parent.right = node.left
                if node.left != None:
                    node_parent.right.parent = node_parent

            del node
            return self.maintenance(node_parent,-1)

        else:
            succ = self.successor(node)
            if succ != None:
                succ_parent = succ.parent
            else:
                node_parent = node.parent
                node_parent.right = node.left
                if node.left != None:
                    node_parent.right.parent = node_parent
                return self.maintenance(node_parent,-1)           


            if succ_parent == node:
                
                succ.left = node.left
                if succ.left != None:
                    succ.left.parent = succ
                if node == self.root:
                    succ.size = node.size
                    self.root = succ
                    return self.maintenance(self.root,-1)
                succ.parent = node.parent
                if node.parent.key > node.key:
                    succ.parent.left = succ
                else:
                    succ.parent.right = succ
                succ.size = node.size
                node = succ
                return self.maintenance(node,-1)
            
                
            succ_parent.left = succ.right
            if succ_parent.left != None:
                succ_parent.left.parent = succ_parent

            succ.left = node.left
            if succ.left != None:
                succ.left.parent = succ
            succ.right = node.right
            if succ.right != None:
                succ.right.parent = succ
            succ.size = node.size
            if node == self.root:
                succ.parent = None
                self.root = succ
            else:
                succ.parent = node.parent
                if succ.parent.key > succ.key:
                    succ.parent.left = succ
                else:
                    succ.parent.right = succ
            return self.maintenance(succ_parent,-1)

    """returns an array representing dictionary 

    @rtype: list
    @returns: a sorted list according to key of touples (key, value) representing the data structure
    """
    def avl_to_array(self):
        SortedTree = []
        node = self.minimum(self.root)
        # goes through the whole tree using the successor() function,
        # and for each node it adds its key and value to the array
        for i in range(1, self.root.size+1):
            SortedTree.append((node.key, node.value))
            node = self.successor(node)
        return SortedTree

    """returns the number of items in dictionary 

    @rtype: int
    @returns: the number of items in dictionary 
    """
    def size(self):
        if self.root != None:
            return self.root.size
        return 0


    """compute the rank of node in the dictionary

    @type node: AVLNode
    @pre: node is in self
    @param node: a node in the dictionary to compute the rank for
    @rtype: int
    @returns: the rank of node in self
    """
    def rank(self, node):
        # initializing the parameters
        count = 0
        curr = node
        minimum = self.minimum(self.root)

        # the rank calculation algorithm
        while curr.parent != None and curr.key != minimum.key:
            if curr.parent.key < curr.key:
                if curr.left != None:
                    count += curr.left.size + 1 
                else:
                    count += 1
                if curr.key < curr.parent.key and curr.parent.key != self.root.key:
                    curr = self.predecessor(curr)
                else:
                    curr = curr.parent
            else:
                if curr.key < curr.parent.key and curr.parent.key == self.root.key:
                    break
                count += 1
                if curr.key < curr.parent.key:
                    curr = self.predecessor(curr)
                else:
                    curr = curr.parent

        # we reached the last node according to our limitations, now we return the rank
        if curr.left == None:
            return count + 1
        else:
            return count + curr.left.size + 1

    def predecessor(self, node):
        if node == self.minimum(self.root):
            return None
        if node.left == None: # case 1: if there's no left node
            while node.parent.key > node.key:
                node = node.parent
            node = node.parent
        else:                 # case 2: if there's a left node
            node = node.left
            while node.right != None:
                node = node.right
        return node

    def successor(self, node):
        # if the given node is the maximum, return None
        if node == self.maximum(self.root):
            return None
        if node.right == None: # case 1: if there's no right node
            while node.parent.key < node.key:
                node = node.parent
            node = node.parent
        else:                  # case 2: if there's a right node
            node = node.right
            while node.left != None:
                node = node.left
        return node

    def minimum(self, node):
        tmp = node
        while tmp.left != None:
            tmp = tmp.left
        return tmp
    
    def maximum(self, node):
        tmp = node
        while tmp.right != None:
            tmp = tmp.right
        return tmp

    """finds the i'th smallest item (according to keys) in the dictionary

    @type i: int
    @pre: 1 <= i <= self.size()
    @param i: the rank to be selected in self
    @rtype: AVLNode
    @returns: the node of rank i in self
    """
    def select(self, i):
        node = self.root
        rnk = self.rank(node)
        while rnk != i:
            rnk = self.rank(node)
            if rnk > i:
                node = node.left
            if rnk < i:
                node = node.right        
        return node


    """finds the node with the largest value in a specified range of keys

    @type a: int
    @param a: the lower end of the range
    @type b: int
    @param b: the upper end of the range
    @pre: a<b
    @rtype: AVLNode
    @returns: the node with maximal (lexicographically) value having a<=key<=b, or None if no such keys exist
    """
    def max_range(self, a, b):
        # Initializing a sorted array of all the keys and values in the tree
        sortedTree = self.avl_to_array()

        # Searching for the smallest key which is >= a
        for i in range(0, self.root.size+1):
            if a <= sortedTree[i][0]:
                break

        # if the interval is inbetween two adjacent nodes, return None
        if b < sortedTree[i][0]:
            return None
        
        # Comparing all the values of keys in interval [a,b]
        maxNode = self.select(i+1)
        for j in range(i, self.root.size+1):
            if b < sortedTree[j][0]:    
                break
            if str.lower(maxNode.value) < str.lower(sortedTree[j][1]):
                maxNode = self.select(j+1)
    
        return maxNode


    """returns the root of the tree representing the dictionary

    @rtype: AVLNode
    @returns: the root, None if the dictionary is empty
    """
    def get_root(self):
        if self.root != None: 
            return self.root
        return None
