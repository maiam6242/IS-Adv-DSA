'''
This is an implementation of a red black tree with search, insert and delete operations

More Information: https://rpucella.net/other/is-dsa-sp22/
'''

import inspect
import sys

def nprint(*args):
    line = inspect.currentframe().f_back.f_lineno
    print("%i:" % line, *args)


SENTINEL = -99

class Node():
    def __init__(self, val):
        """ This method initializes a node with a value, name, color, left, right, and parent"""
        self.value = val
        self.black = True
        self.left = None
        self.right = None
        self.parent = None

class RedBlackTree:
    def __init__(self, key = None):
        """ This method initializes the Red Black Tree to be blank, and sorted by an optional function called key """
    
        self.SENTINEL = Node(val = SENTINEL)
        self.SENTINEL.black = True
        # self.SENTINEL.left = None
        # self.SENTINEL.right = None
        self.root = self.SENTINEL

        # if there is a key given, order/sort the tree by that key, else sort by value (as is default in a red black tree)
        if key == None:
            self.SENTINEL.key = lambda obj: obj.value
        else:
            self.SENTINEL.key = key

    def search(self, k):
        """
        This method returns the value stored in the node at key k, or None if no such key is found
        """
        current_node = self.root

        while(current_node and current_node.value != k):
            if k < current_node.value:
                current_node = current_node.left
            else:
                current_node = current_node.right
            
        if current_node is None:
            return None 
        if current_node.value == k:
            return current_node.value
      
        
        

    def insert(self, v):
        """
        This method inserts value v in the tree using the key computed from v as the key, overwriting any existing value at the same key
        """
        node_to_insert = Node(v)
        node_to_insert.value = v
        node_to_insert.left = self.SENTINEL
        node_to_insert.right = self.SENTINEL
        node_to_insert.black = False
        node_to_insert.parent = None
        
        y = None
        x = self.root

        # traverse through the tree until finding the spot where the new node should be located
        while x != self.SENTINEL:
            y = x
            if node_to_insert.value < x.value:
                x = x.left
            else:
                x = x.right
        
        node_to_insert.parent = y
        # nprint("node to insert value")
        # nprint(node_to_insert.value)
        # nprint("node to insert parent value")
        # if node_to_insert.parent != None:
        #     nprint(node_to_insert.parent.value)
        # nprint("node to insert right")
        # nprint(node_to_insert.right.value)
        # nprint("node to insert parent right value")
        # if node_to_insert.parent != None:
        #     nprint(node_to_insert.parent.right.value)

        # check if the tree is empty, if it is, insert the new node as the root and make it black
        if y == None:
            node_to_insert.black = True
            self.root = node_to_insert
            return

        elif node_to_insert.value < y.value:
            y.left = node_to_insert

        else:
            y.right = node_to_insert

        if y != None:
            nprint("y value")
            nprint(y.value)
            nprint("y right value")
            nprint(y.right.value)
            nprint("y left value")
            nprint(y.left.value)
   

        # if node_to_insert.parent == None:
        #     node_to_insert.black = True
        #     return

        if node_to_insert.parent.parent == None:
            node_to_insert.black = False
            return     
            
        # if node_to_insert != self.root and node_to_insert.parent.parent != None:
        self.rb_insert_fixup(node_to_insert)

    def left_rotation(self, starting_top_node):
        """
        This method is a left rotation, helping to allow the preservation of the red-black tree structure during an insertion 
        """
  
        starting_right_child = starting_top_node.right

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

    def right_rotation(self, starting_top_node):
        """ 
        This method is a right rotation, helping to allow the preservation of the red-black tree structure during an insertion 
        """
      
        starting_left_child = starting_top_node.left
       
        # take the right subtree of the starting left child and make it the left subtree of the top node
        starting_top_node.left = starting_left_child.right

        if starting_left_child.right != self.SENTINEL:
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

    def rb_insert_fixup(self, node_to_insert):
        """ """
        # while the parent of the node to insert is red
        while node_to_insert.parent and node_to_insert.parent.black == False:
            if node_to_insert.parent == node_to_insert.parent.parent.left:
                y = node_to_insert.parent.parent.right
                if y.black == False:
                    node_to_insert.parent.black = True
                    y.black = True
                    node_to_insert.parent.parent.black = False
                    node_to_insert = node_to_insert.parent.parent

                else:
                    if node_to_insert == node_to_insert.parent.right:
                        node_to_insert = node_to_insert.parent
                        self.left_rotation(node_to_insert)
                    node_to_insert.parent.black = True
                    node_to_insert.parent.parent.black = False
                    self.right_rotation(node_to_insert.parent.parent)
                
            else:
                y = node_to_insert.parent.parent.left
                if y.black == False:
                    node_to_insert.parent.black = True
                    y.black = True
                    node_to_insert.parent.parent.black = False
                    self.print_tree()
                    nprint(node_to_insert.parent.parent.value)
                    nprint(node_to_insert.parent.parent.black)
                    node_to_insert = node_to_insert.parent.parent
                else:
                    if node_to_insert == node_to_insert.parent.left:
                        node_to_insert = node_to_insert.parent
                        self.right_rotation(node_to_insert)
                    node_to_insert.parent.black = True
                    node_to_insert.parent.parent.black = False
                    self.left_rotation(node_to_insert.parent.parent)

        self.root.black = True
                

    def delete(self, k):
        """
        This method deletes the node with key k if it exists
        """

    def tree_nprint(self):
        """
        This method prints the tree in a way that is readable
        """
        # TODO: Test this!!
        thislevel = [self.root]
        a = '                                    '
        while thislevel:
            nextlevel = list()
            out = ''
            a = a[:len(a)//2]
            for n in thislevel:

                if n.black == False:
                    # if red, print in red
                    out += '\033[31m' + a + str(n.value) + '\033[0m'
                else:
                    # if black, print in white
                    out += str(out) + a + str(n.value)
            nprint(out)
            if n.left: 
                nextlevel.append(n.left)
            if n.right: 
                nextlevel.append(n.right)
            thislevel = nextlevel
     
# Printing the tree
    def __print_helper(self, node, indent, last):
        if node != self.SENTINEL:
            sys.stdout.write(indent)
            if last:
                sys.stdout.write("R----")
                indent += "     "
            else:
                sys.stdout.write("L----")
                indent += "|    "

            if node.black == False:
                print('\033[31m' + str(node.value) + '\033[0m')
            else:
                print(str(node.value))
            self.__print_helper(node.left, indent, False)
            self.__print_helper(node.right, indent, True)


    def print_tree(self):
        self.__print_helper(self.root, "", True)

if __name__ == "__main__":
    tree1 = RedBlackTree()
    # fill a tree with integers
    root = Node(val = 10)
    for x in range(1,60):
       tree1.insert(x)
    tree1.print_tree()
    print(tree1.search(25))
    
    
    