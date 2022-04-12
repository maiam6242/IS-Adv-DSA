'''
This is an implementation of a B tree with search, insert and delete operations

More Information: https://rpucella.net/other/is-dsa-sp22/
'''

import copy

# TODO: Comment this!!

class Node():
    def __init__(self, leaf = False):
        ''' 
        This method initializes a node with keys, children, current keys and whether or not it is a leaf
        '''
        self.keys = []
        self.key_val_dict = {}
        self.child = []
        self.leaf = leaf

    def isLeaf(self):
        '''
        This method returns true if n is a leaf, and false otherwise
        '''
        return self.leaf
    
    def get_num_keys(self):
        '''
        This method returns the number of keys associated with a given node
        '''
        return len(self.keys)

    def get_num_children(self):
        '''
        This method returns the number of children associated with a given node
        '''

        return len(self.child)

    def isFull(self, t):
        '''
        This method returns true if a node is full and false otherwise
        '''

        return self.get_num_keys() == 2 * t - 1

    # def __str__(self):
    #     if self.leaf:
    #         return "Leaf BTreeNode with {0} keys\n\tK:{1}\n\tC:{2}\n".format(len(self.keys), self.keys, self.child)
    #     else:
    #         return "Internal BTreeNode with {0} keys, {1} children\n\tK:{2}\n\n".format(len(self.keys), len(self.child), self.keys, self.child)

class BTree():
    def __init__(self, t):
        self.root = Node(True)
        self.t = t
        
    def indexFound(self, node, index, key):
        return (index < node.get_num_keys() and node.keys[index] == key)

    # def search(self, k):
    #     '''
    #     This method returns the value stored in the tree at key k, or None if no such key is found
    #     '''
    #     i = 0
    #     while i < self.get_num_keys() and k > self.keys[i]:
    #         i += 1
        
    #     if i < self.get_num_keys() and k == self.keys[i]:
    #         return self, i
        
    #     if self.leaf:
    #         return None

    #     return self.child[i].search(k)

    def split_child(self, parent_node, index):
        '''
        Splits the children of node around an index
        '''
        t = self.t
        y = parent_node.child[index]
        z = Node(y.leaf)
        y_key_val_dict = copy.copy(y.key_val_dict)
        parent_key_val_dict = copy.copy(parent_node.key_val_dict)       
        
        parent_node.child.insert(index + 1, z)
        parent_node.keys.insert(index, y.keys[t-1])
        z.keys = y.keys[t : 2 * t - 1]
        y.keys = y.keys[0 : t - 1]

        parent_node.key_val_dict.clear()
        for key in parent_node.keys:
            if y_key_val_dict.get(key):
                parent_node.key_val_dict[key] = y_key_val_dict[key]
            elif parent_key_val_dict.get(key):
                parent_node.key_val_dict[key] = parent_key_val_dict[key]

        for key in z.keys:
            z.key_val_dict[key] = y_key_val_dict[key]
               
        y.key_val_dict.clear()
        
        for key in y.keys:
            y.key_val_dict[key] = y_key_val_dict[key]

        if not y.leaf:
            z.child = y.child[t : 2 * t]
            y.child = y.child[0 : t - 1]

    def insert(self, k, v):
        '''
        This method inserts value v in the tree at key k, overwriting any existing value at the same key
        '''
       
        root = self.root

        if root.get_num_keys():
            result = self.search_return_node(k)
            if result: 
                result.key_val_dict[k] = v
                return
        
        if root.isFull(self.t):
            temp = Node()
            self.root = temp
            temp.child.insert(0, root)
            self.split_child(temp, 0)
            self.insert_nonfull(temp, k, v)

        else:
            self.insert_nonfull(root, k, v)

    def insert_nonfull(self, x, k, v):
        '''
        if a node is not full, insert key and value in that node in correct location, rearranging the tree accordingly
        '''
        i = len(x.keys) - 1
        if x.leaf:
            x.keys.append(0)
            while i >= 0 and k < x.keys[i]:
                x.keys[i+1] = x.keys[i]
                i -= 1
            x.keys[i + 1] = k
            x.key_val_dict[k] = v
            self.print_tree(self.root)
        else:
            while i >= 0 and k < x.keys[i]:
                i -= 1
            i += 1
            if x.child[i].isFull(self.t):
                self.split_child(x, i)

                if k > x.keys[i]:
                    i += 1
            self.insert_nonfull(x.child[i], k, v)

    def delete(self, k):
        '''
        This method deletes the key k if it exists
        '''

        node_to_delete = self.search_return_node(k)
        if not node_to_delete:
            return None
        else:
            i = 0
            while i < node_to_delete.get_num_keys() and k > node_to_delete.keys[i]:
                i += 1
            if node_to_delete.leaf:
                if self.indexFound(node_to_delete, i, k):
                    node_to_delete.key_val_dict.pop(node_to_delete.keys[i])
                    node_to_delete.keys.pop(i)
                    return
                return
            if self.indexFound(node_to_delete, i, k):
                return self.delete_internal_node(node_to_delete, k, i)
            elif node_to_delete.child.get_num_keys() >= self.t:
                self.delete(node_to_delete.child[i], k)
            else:
                if i != 0 and i + 2 < node_to_delete.get_num_children():
                    if node_to_delete.child[i - 1].get_num_keys() >= self.t:
                        self.delete_sibling(node_to_delete, i, i - 1)
                    elif node_to_delete.child[i + 1].get_num_keys() >= self.t:
                        self.delete_sibling(node_to_delete, i, i + 1)
                    else:
                        self.delete_merge(node_to_delete, i, i + 1)
                elif i == 0:
                    if node_to_delete.child[i + 1].get_num_keys() >= self.t:
                        self.delete_sibling(node_to_delete, i, i + 1)
                    else:
                        self.delete_merge(node_to_delete, i, i + 1)
                elif i + 1 == node_to_delete.get_num_children():
                    if node_to_delete.child[i - 1].get_num_keys() >= self.t:
                        self.delete_sibling(node_to_delete, i, i - 1)
                    else:
                        self.delete_merge(node_to_delete, i, i - 1)
                self.delete(node_to_delete.child[i], k)
          
    def delete_internal_node(self, node, k, i):
        '''
        
        '''
        t = self.t

        if node.leaf:
                if node.keys[i] == k:
                    print(i)
                    print(node.keys[i])
                    print('line 208')
                    # print(node.key_val_dict)
                    # print(node.key_val_dict.get(node.keys[i]))
                    # node.key_val_dict.pop(node.keys[i])
                    node.keys.pop(i)
                    return
                return
        
        print(type(i))
        print(node.child[i].get_num_keys())
        if node.child[i].get_num_keys() >= t:
            node.keys[i] = self.delete_predecessor(node.child[i])
            return
        elif node.child[i + 1].get_num_keys() >= t:
            node.keys[i] = self.delete_successor(node.child[i + 1])
            return
        else:
            self.delete_merge(node, i, i + 1)
            self.delete_internal_node(node.child[i], k, self.t - 1)

    def delete_predecessor(self, node):
        '''

        '''
        if node.leaf:
            # TODO: Does this delete the node straight off the tree? Do any key val dicts need to be adjusted?
            return node.pop()
        
        n = node.get_num_keys() - 1
        if node.child[n].get_num_keys() >= self.t:
            self.delete_sibling(node, n + 1, n)
        else:
            self.delete_merge(node, n, n + 1)
        self.delete_predecessor(node.child[n])

    def delete_successor(self, node):
        '''
        '''
        if node.leaf:
            # TODO: Does this delete the node straight off the tree? Do any key val dicts need to be adjusted?
            return node.keys.pop(0)
            # need to also pop out of key val dict

        if node.child[1].get_num_keys() >= self.t:
            self.delete_sibling(node, 0, 1)
        else:
            self.delete_merge(node, 0, 1)
        self.delete_successor(node.child[0])

    def delete_merge(self, node, index_first_child, index_second_child):
        '''

        '''
        child_node = node.child[index_first_child]

        if index_second_child > index_first_child:
            rsnode = node.child[index_second_child]
            child_node.keys.append(node.keys[index_first_child])

            for k in range(len(rsnode.keys)):
                child_node.keys.append(rsnode.keys[k])
                if len(rsnode.child) > 0:
                    child_node.child.append(rsnode.child[k])
            if len(rsnode.child) > 0:
                child_node.child.append(rsnode.child.pop())
            
            new = child_node
            node.keys.pop(index_first_child)
            node.child.pop(index_second_child)

        else:
            lsnode = node.child[index_second_child]
            lsnode.keys.append(node.keys[index_second_child])

            for i in range(child_node.get_num_keys()):
                lsnode.keys.append(child_node.keys[i])
                if len(lsnode.child) > 0:
                    lsnode.child.append(child_node.child[i])
            if len(lsnode.child) > 0:
                lsnode.child.append(child_node.child.pop())

            new = child_node
            node.keys.pop(index_first_child)
            node.child.pop(index_second_child)

        if node == self.root and len(node.keys) == 0:
            self.root = new

    def delete_sibling(self, node, index_first_child, index_second_child):
        '''

        '''
        child_node = node.child[index_first_child]
        if index_first_child < index_second_child:
            rsnode = node.child[index_second_child]
            child_node.keys.append(node.keys[index_first_child])
            node.keys[index_first_child] = rsnode.keys[0]
            if len(rsnode.child) > 0:
                child_node.child.append(rsnode.child[0])
                rsnode.child.pop(0)
            rsnode.keys.pop(0)
        else:
            lsnode = node.child[index_second_child]
            child_node.keys.insert(0, node.keys[index_first_child - 1])
            node.keys[index_first_child - 1] = lsnode.keys.pop()
            if len(lsnode.child) > 0:
                child_node.child.insert(0, lsnode.child.pop())

    def search(self, k):
        '''
        This method returns the value stored in the tree at key k, or None if no such key is found
        '''

        result = self.search_return_node(k)
        if result:
            return result.key_val_dict[k]

    def search_return_node(self, k):
        '''
        This method returns the Node stored in the tree associated with key k, or None if no such key is found
        '''

        i = 0
        x = self.root
        while i < x.get_num_keys() and k >= x.keys[i]:
            
            if k == x.keys[i]:
                return x

            i += 1
           
            if i >= x.get_num_keys() or k < x.keys[i-1]:
                if x.child:
                    x = x.child[i]
                    i = 0
                else:
                    return None

        return None

    def print_tree(self, x, l = 0):
        '''
        Prints Btree, found online
        '''
        print("Level ", l, " ", len(x.keys), end = ":")
        for i in x.keys:
            print(i, x.key_val_dict, end=" ")
        print()
        l += 1
        if len(x.child) > 0:
            for i in x.child:
                self.print_tree(i, l)

    # def __str__(self):
    #     r = self.root
    #     return r.__str__() + '\n'.join([child.__str__() for child in r.child])  


if __name__ == "__main__":
    tree1 = BTree(2)
    # fill a tree with integers
    # for x in range(1,10):
    #    tree1.insert(x, 2*x)
    tree1.insert(8, 'a')
    tree1.insert(9, 'b')
    tree1.insert(10, 'c')
    tree1.insert(11, 'd')
    tree1.insert(15, 'e')
    tree1.insert(20, 'f')
    tree1.insert(17, 'g')
    tree1.insert(15, 'eg')
      
    print(tree1.search(3))
    print(tree1.search(17))

    tree1.delete(20)
    tree1.print_tree(tree1.root)
    tree1.delete(9)
    
    tree1.print_tree(tree1.root)
    
    