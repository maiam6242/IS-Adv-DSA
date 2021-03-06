'''
This is an implementation of a red black tree with search, insert and delete operations

More Information: https://rpucella.net/other/is-dsa-sp22/
'''

import inspect
import sys

def nprint(*args, **kwargs):
    line = inspect.currentframe().f_back.f_lineno
    print("%i:" % line, *args, **kwargs)

SENTINEL = -99

class Node():
    def __init__(self, val):
        """ 
        This method initializes a node with a value, name, color, left, right, and parent
        """
        self.value = val
        # TODO: Ask Riccardo about name/key implementation
        self.key = None
        self.black = True
        self.left = None
        self.right = None
        self.parent = None

class RedBlackTree:
    def __init__(self, key = None):
        """ 
        This method initializes the Red Black Tree to be blank, and sorted by an optional function called key
        """
    
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

    def search_return_node(self,k):
        """ 
        This method returns the node where key k is located, or None if no such key is found 
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
            return current_node

    def minimum(self, n):
        """ This method finds the minimum node in the tree """
        while n.left is not None and n.left is not self.SENTINEL:
            n = n.left
        return n

    def insert(self, v):
        """
        This method inserts value v in the tree using the key computed from v as the key, overwriting any existing value at the same key
        """
        # TODO: ASK RICCARDO -- DOES THE NAME THEN BECOME THE VALUE??
        # TODO: Should this search for key instead?

        # if self.search(v):
                #   TODO: Ask Riccardo, should is this what it looks like for node to insert to have same key???
        #     node_to_insert = self.search_return_node(v)
        # else:

        # create a new node in the tree with value v
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

        # check if the tree is empty, if it is, insert the new node as the root and make it black
        if y == None:
            node_to_insert.black = True
            self.root = node_to_insert
            return

        # if not, place it in the tree where it should be (according to binary search tree rules)
        elif node_to_insert.value < y.value:
            y.left = node_to_insert

        else:
            y.right = node_to_insert

        if node_to_insert.parent.parent == None:
            node_to_insert.black = False
            return     
            
        # if node_to_insert != self.root and node_to_insert.parent.parent != None:

        # fix the tree coloring to ensure red/black coloring rules still hold
        self.insert_fixup(node_to_insert)

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

    def insert_fixup(self, node_to_insert):
        """ 
        This method fixes a tree's red-black coloring on the insertion of a new node
        """

        # while the parent of the node to insert is red and exists
        while node_to_insert.parent and node_to_insert.parent.black == False:
            # if the node to insert's parent is the left child of their parent (node_to_insert's grandparent)
            if node_to_insert.parent == node_to_insert.parent.parent.left:
                # set y to be node_to_insert's parent's sibling
                y = node_to_insert.parent.parent.right
                # if node_to_insert's parent's sibling is red, change coloring of node_to_insert's parent's sibling, node_to_insert's parent, and node to insert's grandparent. Then make node to insert's grandparent take place of node_to_insert
                if y.black == False:
                    node_to_insert.parent.black = True
                    y.black = True
                    node_to_insert.parent.parent.black = False
                    node_to_insert = node_to_insert.parent.parent
                # if node_to_insert's parent's sibling is black, check if node_to_insert is their parent's right child. If so, make node_to_insert equal to node_to_insert's original parent and do a left rotation. Then (even if node_to_insert was not their parent's right child), change tree colors and do a right rotation on node_to_insert's grandparent (which may be their original grandparent, and may be their parent's grandparent, depending on the if statement outcome)
                else:
                    if node_to_insert == node_to_insert.parent.right:
                        node_to_insert = node_to_insert.parent
                        self.left_rotation(node_to_insert)
                    node_to_insert.parent.black = True
                    node_to_insert.parent.parent.black = False
                    self.right_rotation(node_to_insert.parent.parent)
            #  otherwise if the node to insert's parent is the right child of their parent (node_to_insert's grandparent), set y to be node_to_insert's parent's sibling, and do the whole process outlined above in the opposite direction (essentially swapping right for left at every turn)
            else:
                y = node_to_insert.parent.parent.left
                if y.black == False:
                    node_to_insert.parent.black = True
                    y.black = True
                    node_to_insert.parent.parent.black = False
                    node_to_insert = node_to_insert.parent.parent
                else:
                    if node_to_insert == node_to_insert.parent.left:
                        node_to_insert = node_to_insert.parent
                        self.right_rotation(node_to_insert)
                    node_to_insert.parent.black = True
                    node_to_insert.parent.parent.black = False
                    self.left_rotation(node_to_insert.parent.parent)

        self.root.black = True
                
    def transplant(self, to_be_replaced, subtree_root):
        """ 
        This method takes a subtree and transfers it to another place in the tree at 'to_be_replaced'
        """       
        # if to_be_replaced is root, make subtree root
        if to_be_replaced.parent == self.SENTINEL:
            self.root = subtree_root
        # if to_be_replaced is left child
        elif to_be_replaced == to_be_replaced.parent.left:
            to_be_replaced.parent.left = subtree_root
        # to_be_replaced is right child
        else:
            to_be_replaced.parent.right = subtree_root
       
        subtree_root.parent = to_be_replaced.parent

    def delete_fixup(self, x):
        """ 
        This method maintains the red-black properties of the tree after deletion
        """
       
        # while x isn't the root and is black
        while x != self.root and x.black == True and x.value != SENTINEL:
            
            # if x is the left child, make w its sibling
            if x == x.parent.left:
                w = x.parent.right
                # if it's sibling is red, change its color to black, and the parent of x to red. Then rotate the tree to move the black sibling above the red parent and make w the right child of x
                if w.black == False:
                    w.black == True
                    x.parent.black = False
                    self.left_rotation(x.parent)
                    w = x.parent.right

                # if both w's children are black, set it to be red, and make the parent of x equal x
                if w.left.black == True and w.right.black == True:
                    w.black = False
                    x = x.parent

                # if the right child of w is black, set the color of the left child of w to black and the color of w to red, then right rotate so two reds are not in a parent-child relationship and assign the right child of x's parent to w 
                else:
                    if w.right.black == True:
                        w.left.black = True
                        w.black = False
                        self.right_rotation(w)
                        w = x.parent.right
                # TODO: Comment more here
                w.black = x.parent.black
                x.parent.black = True
                w.right.black = True
                self.left_rotation(x.parent)
                x = self.root

            else:
                w = x.parent.left
                if w.black == False:
                    w.black == True
                    x.parent.black = False
                    self.left_rotation(x.parent)
                    w = x.parent.left

                if w.left.black == True and w.left.black == True:
                    w.black = False
                    x = x.parent

                else:
                    if w.left.black == True:
                        w.right.black = True
                        w.black = False
                        self.right_rotation(w)
                        w = x.parent.left
                
                    w.black = x.parent.black
                    x.parent.black = True
                    w.left.black = True
                    self.left_rotation(x.parent)
                    x = self.root
                
        x.black = True 

    def delete(self, k):
        """
        This method deletes the node with key k if it exists
        """
    
        # find node and make sure that it exists before trying to delete it
        k_node = self.search_return_node(k)

        if k_node is None:
            return

        y = k_node
        y_original_color = y.black

        # if the node's (k_node) left child is empty, move k_node's right child to where k_node was
        if k_node.left == self.SENTINEL:
            x = k_node.right          
            self.transplant(k_node, k_node.right)
        # if the node's (k_node) right child is empty, move k_node's left child to where k_node was
        elif k_node.right == self.SENTINEL:
            x = k_node.left
            self.transplant(k_node,k_node.left)

        else:
            # if k_node has two children, find the minimum of k_node's subtree and store that node and it's right child (which should be a sentinel)
            y = self.minimum(k_node.right)

            y_original_color = y.black
            x = y.right
            # if k_node is the parent of the minimum of its subtree, make the parent of the minimum's child in the subtree a sentinel node (essentially just taking a leaf off the end)
            if y.parent == k_node:
                x.parent = y
           
            # CHECK THIS: If k_node isn't the parent of the minimum of its subtree, shift the right subtree of the minimum where y was, and make the right child of the node to be deleted the right child of the minimum. Then make sure that the binary tree holds
            else:
                self.transplant(y, y.right)
                y.right = k_node.right
                y.right.parent = y
                
            # Replace y with node to be deleted and set the coloring and nodes accordingly
            self.transplant(k_node, y)
            y.left = k_node.left
            y.left.parent = y
            y.black = k_node.black
        
        # if the original color is black, fix tree coloring with delete_fixup
        if y_original_color == True:
            self.delete_fixup(x)

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

    def __print_helper(self, node, indent, last):
        """
        Print tree function that I found online and slightly modified to color in the terminal for easy visualization of the tree
        """
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
    tree1 = RedBlackTree(key=lambda obj: obj.name)
    # fill a tree with integers
    for x in range(1,30):
       tree1.insert(x)
    tree1.insert(1)
    tree1.print_tree()
    nprint(tree1.search(25))
    tree1.delete(10)
    tree1.print_tree()
    # tree1.print_tree()
    tree1.delete(4)
    tree1.print_tree()
    tree1.delete(20)
    tree1.print_tree()
    tree1.delete(27)
    tree1.print_tree()
    
    
    