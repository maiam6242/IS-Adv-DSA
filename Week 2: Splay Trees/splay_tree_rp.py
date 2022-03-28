'''
This is an implementation of a splay tree as described in the Sleator-Tarjan paper with search, insert and delete operations

More Information: https://rpucella.net/other/is-dsa-sp22/
'''

class Node():
    def __init__(self, key, val):
        ''' 
        This method initializes a node with a value, key, left, right, and parent
        '''
        self.key = key
        self.value = val
        self.right = None
        self.left = None
        self.parent = None
    
    def set_left(self, n):
        '''
        This method sets the left child of a node to a given node, n
        '''
        if self.left:
            self.left.parent = None
        self.left = n
        if n:
            n.detach()
            n.parent = self
    
    def set_right(self, n):
        '''
        This method sets the right child of a node to a given node, n
        '''
        if self.right:
            self.right.parent = None
        self.right = n
        if n:
            n.detach()
            n.parent = self
    
    def is_left_child(self):
        '''
        This method returns true if n is a left child, and false otherwise
        '''
        return self.parent.left == self if self.parent else False

    def is_right_child(self):
        '''
        This method returns true if n is a right child, and false otherwise
        '''
        return self.parent.right == self if self.parent else False

    def set_as_left_child(self, parent):
        '''
        Set as left child of parent
        '''
        parent.left.parent = None
        self.parent = parent
        self.parent.left = self

    def set_as_right_child(self, parent):
        '''
        Set as right child of parent
        '''
        parent.right.parent = None
        self.parent = parent
        self.parent.right = self

    def detach(self):
        '''
        Detach the current node from its parent.
        '''
        if self.is_left_child():
            self.parent.left = None
        elif self.is_right_child():
            self.parent.right = None
        self.parent = None
        

class SplayTree():
    def __init__(self, root=None):
        '''
        This method initializes the Splay Tree to be blank
        '''
        if root:
            # Let's be safe and detach the node if is part of another tree.
            root.detach()
        self.root = root

        
    def get_maximum(self):
        '''
        This method returns the maximum of a tree.
        '''
        n = self.root
        while n.right is not None:
            n = n.right
        return n

    
    def join(self, left, right):
        '''
        This method joins to subtrees from their root nodes to form the current splay tree.
        '''
        if not right.root:
            self.root = left.root
            return
        
        if not left.root:
            self.root = right.root
            return

        # find maximum
        max = left.get_maximum()
        print('max of tree w/o deletion ' + str(max.value))

        # Can always splay - if the max is at the root, it'll do nothing.
        left.splay(max)
        self.root = max
        max.set_right(right.root) 
        max.set_left(left.root.left)

        
    def right_rotate(self, starting_top_node):
        '''
        This method is a right rotation, helping to allow the preservation of the red-black tree structure during an insertion 
        '''
        starting_left_child = starting_top_node.left

        # make the starting left child the of the tree if the starting top node was a child of the root
        if not starting_top_node.parent:
            self.root = starting_left_child

        # take the right subtree of the starting left child and make it the left subtree of the top node
        starting_top_node.set_left(starting_left_child.right) 

        # the parent of the starting top node becomes the parent of the starting left node
        if starting_top_node.is_left_child():
            starting_left_child.set_as_left_child(starting_top_node.parent)
        elif starting_top_node.is_right_child():
            starting_left_child.set_as_right_child(starting_top_node.parent)
 
        starting_left_child.set_right(starting_top_node)


    def left_rotate(self, starting_top_node):
        '''
        This method is a left rotation, helping to allow the preservation of the red-black tree structure during an insertion 
        '''
        starting_right_child = starting_top_node.right
        
        # make the starting left child the of the tree if the starting top node was a child of the root
        if not starting_top_node.parent:
            self.root = starting_right_child

        # take the left subtree of the starting right child and make it the right subtree of the top node
        starting_top_node.set_right(starting_right_child.left)

        # the parent of the starting top node becomes the parent of the starting right node
        if starting_top_node.is_left_child():
            starting_right_child.set_as_left_child(starting_top_node.parent)
        elif starting_top_node.is_right_child():
            starting_right_child.set_as_right_child(starting_top_node.parent)
            
        starting_right_child.set_left(starting_top_node) 


    def splay(self, node_for_top):
        '''
        This method splays the tree to place a node, node_for_top on the top of the tree
        '''
        # while the node is not root
        while node_for_top.parent:
            print("splaying " + str(node_for_top.value))
            # if the child of the root, so only needing one rotation
            if not node_for_top.parent.parent:
                # make either right or left rotation to get the node for top on the top of the tree
                if node_for_top.is_left_child():
                    self.right_rotate(node_for_top.parent)
                else:
                    self.left_rotate(node_for_top.parent) 
            # need two rotations
            else:
                # there are four possible double rotations, if the parent and grandparent are in a line on the left, if they are in a line on the right, or if they are on opposite sides, either with the parent being on right or left of grandparent. All of these warrant different rotations which are the cases below
                if node_for_top.is_left_child() and node_for_top.parent.is_left_child():
                    self.right_rotate(node_for_top.parent.parent)
                    self.right_rotate(node_for_top.parent)
                elif node_for_top.is_right_child() and node_for_top.parent.is_right_child():
                    self.left_rotate(node_for_top.parent.parent)
                    self.left_rotate(node_for_top.parent)
                elif node_for_top.is_right_child() and node_for_top.parent.is_left_child():
                    self.left_rotate(node_for_top.parent)
                    self.right_rotate(node_for_top.parent)
                elif node_for_top.is_left_child() and node_for_top.parent.is_right_child():
                    self.right_rotate(node_for_top.parent)
                    self.left_rotate(node_for_top.parent)
        self.print()
        

    def search(self, k):
        '''
        This method returns the value stored in the node at key k, or None if no such key is found
        '''
        n = self.search_return_node(k)
        if not n:
            return None
        else:
            self.splay(n)
            return n.value 

        
    def search_return_node(self,k):
        '''
        This method returns the node where key k is located, or None if no such key is found 
        '''
        current_node = self.root

        while current_node:
            if current_node.key == k:
                return current_node
            if k < current_node.key:
                current_node = current_node.left
            else:
                current_node = current_node.right
        return None
    

    def insert(self, k, v):
        '''
        This method inserts the value v in the tree at key k, overwriting any existing value at the same key
        '''
        found = self.search_return_node(k)
        if found:
            found.value = v
            self.splay(found)
            return
        
        y = None
        x = self.root

        # traverse through the tree until finding the spot where the new node should be located
        while x:
            y = x
            if k < x.key:
                x = x.left
            else:
                x = x.right

        node_to_insert = Node(k, v) 
        node_to_insert.parent = y

        # check if the tree is empty, if it is, insert the new node as the root
        if not y:
            self.root = node_to_insert
            return

        # if not, place it in the tree where it should be (according to binary search tree rules)
        if k < y.key:
            y.left = node_to_insert

        else:
            y.right = node_to_insert

        # splay the tree to place newly inserted node on top
        self.splay(node_to_insert)

        
    def delete(self, k):
        '''
        This method deletes the node at key k if it exists
        '''
        # find the node to be deleted
        node_to_delete = self.search_return_node(k)
        # if key isn't in tree, return 
        if node_to_delete:
            # splay the tree, deletion of the root node gives us two subtrees
            self.splay(node_to_delete)
            right_subtree = self.detach_right(self.root)
            left_subtree = self.detach_left(self.root)
            # join the two subtrees 
            self.join(left_subtree, right_subtree)

            
    def detach_left(self, n):
        if n:
            return SplayTree(root=n.left)

        
    def detach_right(self, n):
        if n:
            return SplayTree(root=n.right)

        
    def print(self):
        
        def prtree(node, indent, last):
            if node:
                print(indent, end='')
                if last:
                    print("R----", end='')
                    indent += "     "
                else:
                    print("L----", end='')
                    indent += "|    "

                ##print(str(node.value), '(parent= ', str(node.parent.value if node.parent else ''), ')')
                print(str(node.value))
                prtree(node.left, indent, False)
                prtree(node.right, indent, True)
                
        prtree(self.root, "", True)

        
def test():
    tree1 = SplayTree()
    # fill a tree with integers
    for x in range(1,7):
       tree1.insert(x, x*20)
    print("Initial tree:")
    tree1.print()
    print("\n-----------------------------------\nSearch 2")
    print(tree1.search(2))
    print("\n-----------------------------------\nSearch 3")
    print(tree1.search(3))
    print("\n-----------------------------------\nSearch 6")
    print(tree1.search(6))
    # print(tree1.search(25))
    print("\n-----------------------------------\nDelete 4")
    tree1.delete(4)
    tree1.print()
    print("\n-----------------------------------\nDelete 2")
    tree1.delete(2)
    tree1.print()
    

if __name__ == "__main__":
    test()
