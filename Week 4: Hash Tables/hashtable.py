'''
This is an implementation of a Hash Table with search and insert operations and the ability to grow dynamically

More Information: https://rpucella.net/other/is-dsa-sp22/
'''

class HashTable():
    def __init__(self, size = 1):
        self.table = [[]]*size
        
    def hash_key(self, k):
        '''
        Hashes keys
        '''
        return hash(k) % len(self.table)

    def get_size(self):
        '''
        Returns the size of the hashtable
        '''
        return len(self.table)

    def get_num_used_slots(self):
        '''
        Returns the number of slots/indices in the hashtable that are used
        '''
        return len(list(filter(lambda elem: len(elem) > 0, self.table)))

    def need_to_resize(self):
        '''
        Returns true if needed to resize and false otherwise
        '''
        size = self.get_size()
        slots_used = self.get_num_used_slots()

        if slots_used / size > .75:
            return True
        else:
            return False

    def resize(self):
        '''
        This method doubles the old size of the array and rehashes all of the existing elements accordingly
        '''
        old_table = [num for sublist in self.table for num in sublist]
        self.table = [[]] * (2 * self.get_size())

        for elem in old_table:
            self.insert(elem[0], elem[1])
        

    def insert(self, k, v):
        '''
        This method inserts the key value pair k, v at the hashtable index, and if key k already exists in the table, replaces the existing value with v
        '''
        if self.need_to_resize():
            self.resize()

        hashed_key = self.hash_key(k)       
        content_length = len(self.table[hashed_key])
        
        if content_length == 0:
            self.table[hashed_key] = [(k,v)]
        
        else:
        
            match, index = self.binary_search(self.table[hashed_key], 0, (content_length - 1), k)

            if match:
                self.table[hashed_key][index] = (k,v)
            else:
                self.table[hashed_key].insert(index, (k,v))
        
           
    def binary_search(self, content, start, end, key):
        '''
        This method contains a standard binary search
        '''
       
        if start == end:
          
            if content[start][0] > key:
                return False, start
            elif content[start][0] == key:
                return True, start
            else:
                return False, start + 1
            
        
        if start > end:
            return False, start
        
        mid = (start + end) // 2
        
        if content[mid][0] < key:
            return self.binary_search(content, mid + 1, end, key)
        elif content[mid][0] > key:
            return self.binary_search(content, start, mid - 1, key)
        else:
            return True, mid

    def search(self, k):
        '''
        This method searches the array for a given key and returns the value from that key
        '''

        hashed_key = self.hash_key(k)
        if len(self.table[hashed_key]) == 0:
            return None
        print(type(self.table[hashed_key]))
        print(type(len(self.table[hashed_key]) - 1))
        match, index = self.binary_search(self.table[hashed_key], 0, len(self.table[hashed_key]) - 1, k)

        if match:
            return self.table[hashed_key][index][1]
        else:
            return None

        
    def print_table(self):
        '''
        This method prints the hash table
        '''
        for item in self.table:
            print(item)

if __name__ == "__main__":
    table1 = HashTable(5)
    table1.insert(7, "hello")
    table1.insert(7, "goodbye")
    table1.insert(2, "check")
    table1.insert(89, "see")
    table1.insert(8, "jokes")
    table1.insert(12, "maia")
    table1.insert(12, "work?")
    table1.insert(20, "exciting!")
    table1.insert(31, "yay!!")
    print(table1.search(2))
    print(table1.search(12))
    print(table1.search(4))
    print(table1.search(32))
    table1.insert(87, "test6")
    table1.insert(9, "test5")
    table1.insert(5, "test4")
    table1.insert(24, "test3")
    table1.insert(17, "test2")
    table1.insert(31, "test1")
    table1.print_table()
    