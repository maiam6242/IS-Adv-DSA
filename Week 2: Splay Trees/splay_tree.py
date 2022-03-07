'''
This is an implementation of a splay tree as described in the Sleator-Tarjan paper with search, insert and delete operations

More Information: https://rpucella.net/other/is-dsa-sp22/
'''

import sys


SENTINEL = -99

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

class SplayTree():
    def __init__(self):
        '''
        This method initializes the Splay Tree to be blank
        '''
        self.SENTINEL = Node(SENTINEL, SENTINEL)
        self.root = self.SENTINEL

    def right_rotate(self, starting_top_node):
        '''
        This method is a right rotation, helping to allow the preservation of the red-black tree structure during an insertion 
        '''
        starting_left_child = starting_top_node.left
       
        # take the right subtree of the starting left child and make it the left subtree of the top node
        starting_top_node.left = starting_left_child.right

        if starting_left_child.right and starting_left_child.right != self.SENTINEL:
            starting_left_child.right.parent = starting_top_node

        # the parent of the starting top node becomes the parent of the starting left node
        starting_left_child.parent = starting_top_node.parent
 
        # make the starting left child the of the tree if the starting top node was a child of the root
        if starting_top_node.parent == None:
            self.root = starting_left_child

        # retain the binary tree properties, arrange children accordingly(?)
        elif starting_top_node == starting_top_node.parent.right:
            starting_top_node.parent.right = starting_left_child 

        else:
            starting_top_node.parent.left = starting_left_child 

        # carry over the rest of the tree, put the starting top node as the right child of the starting left node (which is now on top!)
        starting_left_child.right = starting_top_node 
        starting_top_node.parent = starting_left_child   

    def left_rotate(self, starting_top_node):
        '''
        This method is a left rotation, helping to allow the preservation of the red-black tree structure during an insertion 
        '''
        print(starting_top_node.value)
        
        starting_right_child = starting_top_node.right
        
        print(starting_right_child.value)

        # take the left subtree of the starting right child and make it the right subtree of the top node
        starting_top_node.right = starting_right_child.left

        if starting_right_child.left != None:
         
            starting_right_child.left.parent = starting_top_node

        # the parent of the starting top node becomes the parent of the starting right node
        starting_right_child.parent = starting_top_node.parent

        # make the starting left child the of the tree if the starting top node was a child of the root
        if starting_top_node.parent == None:
            self.root = starting_right_child

        # retain the binary tree properties, arrange children accordingly(?)
        elif starting_top_node == starting_top_node.parent.left:
            starting_top_node.parent.left = starting_right_child 

        else:
            starting_top_node.parent.right = starting_right_child 

        # carry over the rest of the tree, put the starting top node as the left child of the starting right node (which is now on top!)
        starting_right_child.left = starting_top_node 
        starting_top_node.parent = starting_right_child   
        print("left rotation")
        self.print_tree()  

    def splay(self, node_for_top):
        '''
        '''
        # while the node is not root
        while node_for_top.parent and node_for_top.parent.value is not SENTINEL:
            print("splaying " + str(node_for_top.value))
            # if the child of the root, so only needing one rotation
            if node_for_top.parent.parent is None or node_for_top.parent.parent.value is SENTINEL:
                # make either right or left rotation to get the node for top on the top of the tree
                if node_for_top == node_for_top.parent.left:
                    print("hellloooo")
                    self.right_rotate(node_for_top.parent)
                else:
                    print("heyyy")
                    self.left_rotate(node_for_top.parent) 
            # need two rotations
            # TODO: Finish commenting
            else:
                n_parent = node_for_top.parent
                n_gparent = n_parent.parent

                # if node_for_top.parent.left == node_for_top and node_for_top.parent.parent.left == node_for_top.parent:
                if node_for_top.parent.left == node_for_top and n_parent.parent.left == n_parent:
                    print("this")
                    self.right_rotate(n_gparent)
                    self.right_rotate(n_parent)
                elif node_for_top.parent.right == node_for_top and n_parent.parent.right == n_parent:
                    print("that")
                    self.left_rotate(n_gparent)
                    self.left_rotate(n_parent)
                elif node_for_top.parent.right == node_for_top and n_parent.parent.left == n_parent:
                    print("zig")
                    print(node_for_top)
                    print(node_for_top.parent.parent.value)
                    self.left_rotate(n_parent)
                    print(node_for_top)
                    print(node_for_top.parent.parent.value)
                    self.right_rotate(n_gparent)
                elif node_for_top.parent.left == node_for_top and n_parent.parent.right == n_parent:
                    print("zag")
                    print(node_for_top)
                    print(node_for_top.parent.value)
                    self.right_rotate(n_parent)
                    self.left_rotate(n_gparent)

            self.print_tree()

    def search(self, k):
        '''
        This method returns the value stored in the node at key k, or None if no such key is found
        '''
        current_node = self.root

        while(current_node and current_node.key != SENTINEL and current_node.key != k):
            if k < current_node.key:
                current_node = current_node.left
            else:
                current_node = current_node.right
            
        if current_node is None:
            return None 

        if current_node.key == k:
            self.splay(current_node)
            return current_node.value 
    
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

            # check if the tree is empty, if it is, insert the new node as the root and make it black
            if y == self.SENTINEL:
                self.root = node_to_insert
                print('get here')
                print(y.value)
                return
           
            # if not, place it in the tree where it should be (according to binary search tree rules)
            elif node_to_insert.key < y.key:
                print("should be here?")
                y.left = node_to_insert

            else:
                print("or here?")
                y.right = node_to_insert
            
        # print(self.print_tree())
        self.splay(node_to_insert)

    def delete(self, k):
        '''
        This method deletes the node at key k if it exists
        '''

    def __print_helper(self, node, indent, last):
        if node and node != self.SENTINEL:
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
    print(tree1.search(3))
    # # nprint(tree1.search(25))
    # tree1.delete(10)
    # tree1.print_tree()
    # # tree1.print_tree()
    # tree1.delete(4)
    # tree1.print_tree()
    # tree1.delete(20)
    # tree1.print_tree()
    # tree1.delete(27)
    # tree1.print_tree()
    