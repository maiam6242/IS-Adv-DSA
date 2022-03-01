'''
This is an implementation of an AVL tree with search, insert and delete operations

More Information: https://rpucella.net/other/is-dsa-sp22/
'''

# TODO: Give it an extra hour to flesh out, if doing walk up fixes stuff, great if not, don't spend too much time

import inspect
import sys


def nprint(*args, **kwargs):
    line = inspect.currentframe().f_back.f_lineno
    print("%i:" % line, *args, **kwargs)


SENTINEL = -99

class Node():
    def __init__(self, val):
        """ This method initializes a node with a value, name, left, right, and parent"""
        self.value = val
        self.left = None
        self.right = None
        self.parent = None
        # self.height = 1
        # self.balance_factor = 0

class AVLTree:
    def __init__(self, key = None):
        """ This method initializes the Red Black Tree to be blank, and sorted by an optional function called key """
    
        self.SENTINEL = Node(val = SENTINEL)
        # self.SENTINEL.left = None
        # self.SENTINEL.right = None
        self.root = self.SENTINEL

        # if there is a key given, order/sort the tree by that key, else sort by value (as is default in a red black tree)
        if key == None:
            self.SENTINEL.key = lambda obj: obj.value
        else:
            self.SENTINEL.key = key
    
    def delete(self, k):
        """
        This method deletes the node with key k if it exists
        """

    def insert(self, v):
        """
        This method inserts value v in the tree using the key computed from v as the key, overwriting any existing value at the same key
        """

        node_to_insert = Node(v)
        node_to_insert.value = v
        node_to_insert.left = self.SENTINEL
        node_to_insert.right = self.SENTINEL
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

        # insert according to binary tree rules
        # check if the tree is empty, if it is, insert the new node as the root 
        if y == None:
            self.root = node_to_insert
            return

        elif node_to_insert.value < y.value:
            y.left = node_to_insert

        else:
            y.right = node_to_insert

        # update the height value of the node that was placed 
        nprint("heights in insert statement")
        # nprint(node_to_insert.height)
        # nprint(node_to_insert.right.height)
        # nprint(node_to_insert.left.height)
        nprint(type(self.get_height(node_to_insert.left)))
        nprint(self.get_height(self.root))
        nprint("test")

        # node_to_insert_height = 1 + max(self.get_height(node_to_insert.left), self.get_height(node_to_insert.right))

        nprint(max(self.get_height(node_to_insert.left), self.get_height(node_to_insert.right)))
        nprint("heights after moving stuff")
        nprint(node_to_insert.value)
        # nprint(node_to_insert.height)

        node_balance_factor = self.get_balance_factor(self.root)

        # TODO: there is an update to height I missed
        # if not at root, walk up a parent and fix as going up

        nprint("balance_factor")
        nprint(node_balance_factor)
        nprint(self.get_height(node_to_insert))
        # nprint(node_to_insert_height)
        nprint(node_to_insert.value)

        # There are 4 ways that the tree can be out of balance. The tree can be left heavy and the nodes can be in a line, meaning there is node with a left child and that left child has a left child that is heavier than the right. The tree can be right heavy and the nodes can be in a line, which is the same situation on the other side. The tree can also be left heavy, but the top node can have a left child and then that node can have a right child that is heavier than the left, or vice versa if the tree is right heavy.

        # This means that the tree is left heavy and that the left childs right subtree is heavier than it's left
        if node_balance_factor >= 2 and self.get_balance_factor(node_to_insert.left) < 0:
            node_to_insert.left = self.left_rotation(node_to_insert.left)
            self.right_rotation(node_to_insert)

        # This means that the tree is left heavy and that the left childs left subtree is heavier than it's right (in a line)
        if node_balance_factor >= 2 and self.get_balance_factor(node_to_insert.left) > 0:
            self.right_rotation(node_to_insert)

        # This means that the tree is right heavy and that the right childs left subtree is heavier than it's right
        if node_balance_factor <= -2 and self.get_balance_factor(node_to_insert.right) > 0:
            node_to_insert.right = self.right_rotation(node_to_insert.right)
            self.left_rotation(node_to_insert)
        
        # This means that the tree is right heavy and that the right childs right subtree is heavier than it's left (in a line)
        if node_balance_factor <= -2 and self.get_balance_factor(node_to_insert.right) < 0:
            self.left_rotation(node_to_insert)


    def left_rotation(self, node):
        """
        This method is a left rotation, helping to allow the preservation of the AVL tree structure during an insertion
        """
        # assign the right child of the top node to node_starting_right
        node_starting_right = node.right
        # assign the left child below it to middle_node_starting_left
        middle_node_starting_left = node_starting_right.left
        # assign the original node to be the left grandchild of where it started
        node_starting_right.left = node
        # assign the orignal left grandchild to be one level up from it started on the right
        node.right = middle_node_starting_left

        # reassign the heights
        # nprint(node.height)
        # nprint(self.get_height(node.right))
        node.height = 1 + max(self.get_height(node.right), self.get_height(node.left))
        # nprint(node.height)
        # node_starting_right.height = 1 + max(self.get_height(node_starting_right.right), self.get_height(node_starting_right.left))

        return node_starting_right
        
    def right_rotation(self,node):
        """
        This method is a right rotation, helping to allow the preservation of the AVL tree structure during an insertion
        """
        # assign the left child of the top node to node_starting_left
        node_starting_left = node.left
        # assign the right child below it to middle_node_starting_right
        middle_node_starting_right = node_starting_left.right
        # assign the original node to be the right grandchild of where it started
        node_starting_left.right = node
        # assign the orignal right grandchild to be one level up from it started on the left
        node.left = middle_node_starting_right

        # reassign the heights
        nprint(node.height)
        node.height = 1 + max(self.get_height(node.right), self.get_height(node.left))
        nprint(node.height)
        node_starting_left.height = 1 + max(self.get_height(node_starting_left.right), self.get_height(node_starting_left.left))

        return node_starting_left

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

    def search_return_node(self,k):
        """ This method returns the node where key k is located, or None if no such key is found """ 

        current_node = self.root

        while(current_node and current_node.value != k):
            if k < current_node.value:
                current_node = current_node.left
            else:
                current_node = current_node.right
            
        if current_node is None:
            return None 

        if current_node.value == k:
            return current_node

    def get_balance_factor(self, node):
        """
        This method calculates the balance factor of a given node in the AVL tree
        """
        # nprint("here")
        # if node.left is None or node.right is None:
        if node is None:
            nprint(node)
            return 0
        # nprint(node.height)
        # nprint(self.get_height(node.right))
        print("in balance factor method")
        nprint(self.get_height(node.left))
        nprint(self.get_height(node.right))
        nprint(self.get_height(node.left) - self.get_height(node.right))
        return self.get_height(node.left) - self.get_height(node.right)

    def get_height(self, node):
        """
        This method returns the height associated with a given node. Importantly, it handles the case when the node is None and returns 0
        """
        # if at bottom of the tree, return 0
        if node is None:
            return 0
        
        # if not, calculate the max of the heights of node left and right, so that only the taller height prevails
        # nprint("height and right height")
        # nprint(self.get_height(node.right))
        # nprint(max(self.get_height(node.left),self.get_height(node.right)))

        return 1 + max(self.get_height(node.left),self.get_height(node.right)) 
        # return node.height

    def __print_helper(self, node, indent, last):
        if node != self.SENTINEL:
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
    tree1 = AVLTree()
    # fill a tree with integers
    # root = Node(val = 10)

    for x in range(1,5):
       tree1.insert(x)
    # tree1.insert(1)
    tree1.print_tree()
    # nprint(tree1.search(25))
    # tree1.delete(68)
    # nprint(tree1.search(39))
    # tree1.print_tree()