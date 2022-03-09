'''
This is an implementation of a splay tree as described in the Sleator-Tarjan paper with search, insert and delete operations

More Information: https://rpucella.net/other/is-dsa-sp22/
'''

import sys

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
    
    def setLeft(self, n):
        '''
        This method sets the left child of a node to a given node, n
        '''
        self.left = n
        if n:
            n.parent = self
    
    def setRight(self, n):
        '''
        This method sets the right child of a node to a given node, n
        '''
        self.right = n
        if n:
            n.parent = self
    
    def setParent(self, n):
        '''
        This method sets the parent of a node to a given node, n
        '''
        self.parent = n
    
    def isLeftChild(self):
        '''
        This method returns true if n is a left child, and false otherwise
        '''
        return self.parent.left == self

    def isRightChild(self):
        '''
        This method returns true if n is a right child, and false otherwise
        '''
        return self.parent.right == self

class SplayTree():
    def __init__(self):
        '''
        This method initializes the Splay Tree to be blank
        '''
        self.root = None

    def get_maximum(self, n):
        '''
        This method returns the maximum of a tree, given a starting node
        '''
        
        while n.right is not None:
            n = n.right
        return n
    
    def join(self, left, right):
        '''
        This method joins to subtrees from their root nodes
        '''
        # print('left node value at join ' + str(left.value))
        print('right node value at join ' + str(right.value))
        if not right:
            return left
        if not left:
            return right

        # find maximum
        max = left.get_maximum(left.root)
        print('max of tree w/o deletion ' + str(max.value))
       
        if left.root != max:
            left.splay(max)
        # make the max the new root of the tree
        left.print_tree()
        print('splayed in join')
        max.setRight(right) 
        # will this always work?
        max.setLeft(left.root.left)
        return max

    def right_rotate(self, starting_top_node):
        '''
        This method is a right rotation, helping to allow the preservation of the red-black tree structure during an insertion 
        '''
        starting_left_child = starting_top_node.left
       
        # take the right subtree of the starting left child and make it the left subtree of the top node
        starting_top_node.setLeft(starting_left_child.right) 

        if starting_left_child.right:
            starting_left_child.right.parent = starting_top_node

        # the parent of the starting top node becomes the parent of the starting left node
        starting_left_child.setParent(starting_top_node.parent)
 
        # make the starting left child the of the tree if the starting top node was a child of the root
        if starting_top_node.parent == None:
            self.root = starting_left_child

        # retain the binary tree properties, arrange children accordingly(?)
        elif starting_top_node.isRightChild():
            starting_top_node.parent.right = starting_left_child 

        else:
            starting_top_node.parent.left = starting_left_child 

        # carry over the rest of the tree, put the starting top node as the right child of the starting left node (which is now on top!)
        starting_left_child.setRight(starting_top_node) 
        starting_top_node.setParent(starting_left_child)   

    def left_rotate(self, starting_top_node):
        '''
        This method is a left rotation, helping to allow the preservation of the red-black tree structure during an insertion 
        '''
        print(starting_top_node.value)
        starting_right_child = starting_top_node.right
        
        # take the left subtree of the starting right child and make it the right subtree of the top node
        starting_top_node.setRight(starting_right_child.left)

        if starting_right_child.left:
            starting_right_child.left.parent = starting_top_node

        # the parent of the starting top node becomes the parent of the starting right node
        starting_right_child.setParent(starting_top_node.parent)

        # make the starting left child the of the tree if the starting top node was a child of the root
        if starting_top_node.parent == None:
            self.root = starting_right_child

        # retain the binary tree properties, arrange children accordingly(?)
        elif starting_top_node.isLeftChild():
            starting_top_node.parent.left = starting_right_child 

        else:
            starting_top_node.parent.right = starting_right_child 

        # carry over the rest of the tree, put the starting top node as the left child of the starting right node (which is now on top!)
        starting_right_child.setLeft(starting_top_node) 
        starting_top_node.setParent(starting_right_child)    

    def splay(self, node_for_top):
        '''
        This method splays the tree to place a node, node_for_top on the top of the tree
        '''

        # while the node is not root
        while node_for_top.parent:
            print("splaying " + str(node_for_top.value))
            # if the child of the root, so only needing one rotation
            print(type(node_for_top.parent.parent))
            if node_for_top.parent.parent is None:
                # make either right or left rotation to get the node for top on the top of the tree
                if node_for_top.isLeftChild():
                    self.right_rotate(node_for_top.parent)
                else:
                    self.left_rotate(node_for_top.parent) 
            # need two rotations
            else:
                # there are four possible double rotations, if the parent and grandparent are in a line on the left, if they are in a line on the right, or if they are on opposite sides, either with the parent being on right or left of grandparent. All of these warrant different rotations which are the cases below

                if node_for_top.isLeftChild() and node_for_top.parent.isLeftChild():
                    self.right_rotate(node_for_top.parent.parent)
                    self.right_rotate(node_for_top.parent)
                elif node_for_top.isRightChild() and node_for_top.parent.isRightChild():
                    self.left_rotate(node_for_top.parent.parent)
                    self.left_rotate(node_for_top.parent)
                elif node_for_top.isRightChild() and node_for_top.parent.isLeftChild():
                    self.left_rotate(node_for_top.parent)
                    if node_for_top.parent.parent:
                        self.right_rotate(node_for_top.parent.parent)
                elif node_for_top.isLeftChild() and node_for_top.parent.isRightChild():
                    self.right_rotate(node_for_top.parent)
                    if node_for_top.parent.parent:
                        self.left_rotate(node_for_top.parent.parent)
       
        self.print_tree()

    def search(self, k):
        '''
        This method returns the value stored in the node at key k, or None if no such key is found
        '''
        n = self.search_return_node(k)
        if not n:
            return None
        else:
            print(n.value)
            self.splay(n)
            return n.value 
    
    def search_return_node(self,k):
        '''
        This method returns the node where key k is located, or None if no such key is found 
        '''
        current_node = self.root

        while(current_node and current_node.key != k):
            if k < current_node.key:
                current_node = current_node.left
            else:
                current_node = current_node.right
            
        if current_node is None:
            return None 

        if current_node.key == k:
            return current_node 

    def insert(self, k, v):
        '''
        This method inserts the value v in the tree at key k, overwriting any existing value at the same key
        '''
        if self.search(k) is not None:
            # the keyed node already exists in the tree, so simply change the value at node with that key
            self.search_return_node(k).value = v
        else:
            node_to_insert = Node(k, v) 

            y = None
            x = self.root

            # traverse through the tree until finding the spot where the new node should be located
            while x is not None:
                y = x

                if node_to_insert.key < x.key:
                    x = x.left
                else:
                    x = x.right
            
            node_to_insert.parent = y

            # check if the tree is empty, if it is, insert the new node as the root
            if y == None:
                self.root = node_to_insert
                return
           
            # if not, place it in the tree where it should be (according to binary search tree rules)
            elif node_to_insert.key < y.key:
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
        if not node_to_delete:
            return
        else:
            # splay the tree, deletion of the root node gives us two subtrees 
            self.splay(node_to_delete)

            # create the right subtree
            if self.root.right:
                right_subtree = self.root.right 
                right_subtree.setParent(None)
            else:
                right_subtree = None

            # create the left subtree
            
            # right_subtree = self.root.right 

            if self.root.left:
                left_subtree = SplayTree()
                left_subtree.root = self.root.left
                # left_subtree.setParent(None)
            else:
                left_subtree = None

            # join the two subtrees 
            # why doesn't this tree persist??           
            self.root = self.join(left_subtree, right_subtree)
            print("line 295")
            self.print_tree()

    def __print_helper(self, node, indent, last):
        if node:
            sys.stdout.write(indent)
            if last:
                sys.stdout.write("R----")
                indent += "     "
            else:
                sys.stdout.write("L----")
                indent += "|    "

            print(str(node.value))
            self.__print_helper(node.left, indent, False)
            self.__print_helper(node.right, indent, True)
    
    def print_tree(self):
        self.__print_helper(self.root, "", True)

if __name__ == "__main__":
    tree1 = SplayTree()
    # fill a tree with integers
    for x in range(1,7):
       tree1.insert(x, x*20)
    tree1.print_tree()
    print(tree1.search(2))
    print(tree1.search(3))
    print(tree1.search(6))
    # print(tree1.search(25))
    tree1.delete(4)
    tree1.print_tree()
    # # tree1.print_tree()
    tree1.delete(2)
    tree1.print_tree()
    # tree1.delete(20)
    # tree1.print_tree()
    # tree1.delete(27)
    # tree1.print_tree()
    